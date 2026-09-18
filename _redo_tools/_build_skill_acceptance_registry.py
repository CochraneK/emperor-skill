#!/usr/bin/env python3
"""Build the model-agnostic Skill acceptance registry.

This generator is intentionally conservative:
- machine/static signals never create ACCEPTED;
- historical 39-package semantic triage remains actionable;
- only an explicit L1-L4 attestation can create ACCEPTED.

Generated outputs:
  data/skill-acceptance-registry.json
  assessment/SKILL_ACCEPTANCE.md
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SKILLS = ROOT / "skills"
ATTEST = DATA / "skill-acceptance-attestations.json"
PROV = DATA / "provenance-repair-registry.json"
L3 = DATA / "l3-semantic-review-queue.json"
GAP = DATA / "corpus-gap.json"
OUT = DATA / "skill-acceptance-registry.json"
REPORT = ROOT / "assessment" / "SKILL_ACCEPTANCE.md"

VALID_L1 = {"PASS", "UNCERTAIN", "FAIL"}
VALID_L2 = {"PASS", "PARTIAL", "FAIL", "LIMITED-EVIDENCE"}
VALID_L3 = {"PASS", "WEAK", "FAIL"}
VALID_L4 = {"PASS", "PARTIAL", "FAIL"}
VALID_TEST = {"PASS", "WEAK", "FAIL"}
VALID_ACTION = {"KEEP", "CLEAN", "PATCH", "REDISTILL", "RESEARCH-GAP", "RERESEARCH", "REBUILD", "REVIEW"}

STATUS_ORDER = ["ACCEPTED", "PATCH", "REDISTILL", "RERESEARCH", "REBUILD", "REVIEW", "UNASSESSED"]


def load(path: Path, default=None):
    if not path.exists():
        if default is not None:
            return default
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def packages():
    for dyn in sorted(p for p in SKILLS.iterdir() if p.is_dir() and not p.name.startswith("_")):
        for pkg in sorted(p for p in dyn.iterdir() if p.is_dir()):
            skill = pkg / "SKILL.md"
            if skill.exists():
                yield dyn.name, pkg.name, pkg


def person_map():
    doc = load(GAP)
    out = {}
    for row in doc.get("person_matches", []):
        pid = row.get("candidate_id") or row.get("person_id")
        for path in row.get("matched_skill_paths", []):
            if path and pid:
                out[str(path)] = str(pid)
    return out


def latest_attestations():
    doc = load(ATTEST, {"attestations": []})
    by_path = {}
    for row in doc.get("attestations", []):
        path = str(row.get("skill_path", "")).rstrip("/")
        if not path:
            raise RuntimeError("acceptance attestation missing skill_path")
        required = ["reviewed_at", "reviewer", "l1", "l2", "l3", "genericity_test",
                    "counter_evidence_test", "l4", "action", "reason"]
        missing = [k for k in required if not row.get(k)]
        if missing:
            raise RuntimeError(f"{path}: attestation missing {missing}")
        if row["l1"] not in VALID_L1 or row["l2"] not in VALID_L2 or row["l3"] not in VALID_L3:
            raise RuntimeError(f"{path}: invalid L1/L2/L3 value")
        if row["l4"] not in VALID_L4:
            raise RuntimeError(f"{path}: invalid L4 value")
        if row["genericity_test"] not in VALID_TEST or row["counter_evidence_test"] not in VALID_TEST:
            raise RuntimeError(f"{path}: invalid semantic test value")
        if row["action"] not in VALID_ACTION:
            raise RuntimeError(f"{path}: invalid action")
        previous = by_path.get(path)
        if previous is None or str(row["reviewed_at"]) >= str(previous["reviewed_at"]):
            by_path[path] = row
    return by_path


def normalize_status(att):
    action = att["action"]
    if action == "KEEP":
        hard_pass = (
            att["l1"] == "PASS"
            and att["l2"] in {"PASS", "LIMITED-EVIDENCE"}
            and att["l3"] == "PASS"
            and att["genericity_test"] == "PASS"
            and att["counter_evidence_test"] == "PASS"
            and att["l4"] == "PASS"
        )
        if not hard_pass:
            raise RuntimeError(
                f"{att['skill_path']}: KEEP cannot yield ACCEPTED without complete L1-L4 PASS"
            )
        return "ACCEPTED"
    if action in {"CLEAN", "PATCH"}:
        return "PATCH"
    if action == "REDISTILL":
        return "REDISTILL"
    if action in {"RESEARCH-GAP", "RERESEARCH"}:
        return "RERESEARCH"
    if action == "REBUILD":
        return "REBUILD"
    return "REVIEW"


def legacy_repairs():
    doc = load(PROV, {"items": []})
    out = {}
    for row in doc.get("items", []):
        path = str(row.get("skill_path", "")).rstrip("/")
        if not path:
            continue
        repair = str(row.get("recommended_repair", "REVIEW"))
        if "REDISTILL" in repair:
            status = "REDISTILL"
        elif "RERESEARCH" in repair or "RESEARCH" in repair:
            status = "RERESEARCH"
        elif "PATCH" in repair or "VERIFY" in repair:
            status = "PATCH"
        else:
            status = "REVIEW"
        out[path] = {
            "status": status,
            "recommended_repair": repair,
            "semantic_triage": row.get("semantic_triage"),
            "execution_tracking": row.get("execution_tracking", {}),
        }
    return out


def l3_flagged_paths():
    doc = load(L3, {"review_queue": []})
    flagged = set()
    for row in doc.get("review_queue", []):
        for key in ("skill_path", "left", "right", "path"):
            value = row.get(key) if isinstance(row, dict) else None
            if isinstance(value, str) and value.startswith("skills/"):
                flagged.add(value.rsplit("/SKILL.md", 1)[0].rstrip("/"))
    return flagged


def research_signal(pkg: Path):
    research = pkg / "references" / "research"
    files = sorted(research.glob("*.md")) if research.exists() else []
    return {
        "research_md_files": len(files),
        "has_local_quality_check": (pkg / "scripts" / "quality_check.py").exists(),
    }


def main():
    pmap = person_map()
    attest = latest_attestations()
    legacy = legacy_repairs()
    flagged = l3_flagged_paths()

    rows = []
    current_paths = set()

    for dynasty, package, pkg in packages():
        path = f"skills/{dynasty}/{package}"
        current_paths.add(path)
        a = attest.get(path)
        legacy_row = legacy.get(path)

        if a:
            status = normalize_status(a)
            basis = "EXPLICIT_L1_L4_ATTESTATION"
            action = a["action"]
            reason = a["reason"]
        elif legacy_row:
            status = legacy_row["status"]
            basis = "HISTORICAL_SEMANTIC_TRIAGE"
            action = legacy_row.get("recommended_repair", status)
            reason = "Frozen provenance cohort was semantically triaged; repair remains un-attested."
        else:
            status = "UNASSESSED"
            basis = "NO_CONTENT_LEVEL_ATTESTATION"
            action = "REVIEW"
            reason = "No explicit L1-L4 acceptance verdict has been recorded."

        rows.append({
            "skill_path": path,
            "person_id": pmap.get(path),
            "dynasty": dynasty,
            "package": package,
            "status": status,
            "queue_action": action,
            "verdict_basis": basis,
            "reason": reason,
            "machine_signals": {
                **research_signal(pkg),
                "l3_similarity_review_flag": path in flagged,
            },
            "attestation": a,
        })

    stale = sorted(set(attest) - current_paths)
    if stale:
        raise RuntimeError(f"acceptance attestations reference missing Skill paths: {stale}")

    counts = Counter(r["status"] for r in rows)
    summary = {
        "current_skills": len(rows),
        "accepted": counts["ACCEPTED"],
        "patch": counts["PATCH"],
        "redistill": counts["REDISTILL"],
        "reresearch": counts["RERESEARCH"],
        "rebuild": counts["REBUILD"],
        "review": counts["REVIEW"],
        "unassessed": counts["UNASSESSED"],
        "explicit_attestations": len(attest),
        "historical_triage_rows_applied": sum(r["verdict_basis"] == "HISTORICAL_SEMANTIC_TRIAGE" for r in rows),
        "machine_l3_flags": sum(r["machine_signals"]["l3_similarity_review_flag"] for r in rows),
    }
    if sum(summary[k] for k in ("accepted", "patch", "redistill", "reresearch", "rebuild", "review", "unassessed")) != len(rows):
        raise RuntimeError("acceptance status partition does not cover current Skills exactly once")

    doc = {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "MODEL_AGNOSTIC_ACCEPTANCE_REGISTRY",
        "policy": "SKILL_ACCEPTANCE_POLICY.md",
        "canonical_audit": "NUWA_AUDIT_V2.md",
        "automatic_acceptance": False,
        "summary": summary,
        "items": rows,
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Skill Acceptance · Canonical Queue",
        "",
        "> Generated from current Skills, explicit L1–L4 attestations, the frozen 39-package semantic triage, and machine signals. **UNASSESSED is not FAIL; machine-green is not ACCEPTED.**",
        "",
        "## Summary",
        "",
        f"- Current Skills: **{len(rows)}**",
        f"- ACCEPTED: **{counts['ACCEPTED']}**",
        f"- PATCH: **{counts['PATCH']}**",
        f"- REDISTILL: **{counts['REDISTILL']}**",
        f"- RERESEARCH: **{counts['RERESEARCH']}**",
        f"- REBUILD: **{counts['REBUILD']}**",
        f"- REVIEW: **{counts['REVIEW']}**",
        f"- UNASSESSED: **{counts['UNASSESSED']}**",
        f"- Explicit content-level attestations: **{len(attest)}**",
        f"- Historical 39-package triage rows applied: **{summary['historical_triage_rows_applied']}**",
        "",
        "## Acceptance rule",
        "",
        "`ACCEPTED` requires an explicit L1–L4 attestation with L1 PASS, L2 PASS/LIMITED-EVIDENCE, L3 PASS, Genericity PASS, Counter-evidence PASS, L4 PASS, and action KEEP.",
        "",
        "Passing local quality_check, CI, file-count checks or lexical similarity checks does not create ACCEPTED.",
        "",
        "## Repair / review queue",
        "",
    ]

    for status in STATUS_ORDER:
        selected = [r for r in rows if r["status"] == status]
        if not selected:
            continue
        lines += [f"### {status} · {len(selected)}", ""]
        limit = 80 if status != "UNASSESSED" else 40
        for r in selected[:limit]:
            pid = r.get("person_id") or "no-person-id"
            lines.append(f"- `{r['skill_path']}` · {pid} · basis={r['verdict_basis']} · action={r['queue_action']}")
        if len(selected) > limit:
            lines.append(f"- … and {len(selected)-limit} more; see `data/skill-acceptance-registry.json`.")
        lines.append("")

    REPORT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
