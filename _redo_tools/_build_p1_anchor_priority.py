#!/usr/bin/env python3
"""Build a neutral P1 anchor research schedule.

This generator deliberately does NOT score or rank rulers. It creates a deterministic,
cross-polity review sequence, attaches source/evidence review annotations, and finalizes
an initial tranche only when enough candidates have completed source review.
"""
from __future__ import annotations

from collections import defaultdict, deque
import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSESSMENT = ROOT / "assessment"
PRIORITY = DATA / "distillation-priority.json"
POLICY = DATA / "p1-anchor-selection-policy.json"
REVIEWS = DATA / "p1-anchor-reviews.json"
PERSON_INDEX = DATA / "rulers-person-index.json"
OUT = DATA / "p1-anchor-priority.json"
REPORT = ASSESSMENT / "P1_ANCHOR_PRIORITY.md"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def pid_number(pid: str) -> int:
    try:
        return int(pid.rsplit("-", 1)[1])
    except (IndexError, ValueError):
        return 10**9


def source_segment(row: dict[str, Any]) -> int:
    values: list[int] = []
    for path in row.get("source_files", []):
        m = re.search(r"rulers-master-h(\d+)", str(path))
        if m:
            values.append(int(m.group(1)))
    return min(values) if values else 999


def build_sequence(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_polity: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    polity_segment: dict[str, int] = {}
    for row in candidates:
        polities = row.get("polities") or ["UNSPECIFIED"]
        seg = source_segment(row)
        for polity in polities:
            by_polity[polity].append(row)
            polity_segment[polity] = min(polity_segment.get(polity, 999), seg)

    for polity, rows in by_polity.items():
        rows.sort(key=lambda r: (pid_number(str(r["person_id"])), str(r.get("canonical_name", ""))))

    polity_order = sorted(by_polity, key=lambda p: (polity_segment.get(p, 999), p))
    queues = {p: deque(by_polity[p]) for p in polity_order}
    seen: set[str] = set()
    sequence: list[dict[str, Any]] = []

    while True:
        progressed = False
        for polity in polity_order:
            q = queues[polity]
            while q and str(q[0]["person_id"]) in seen:
                q.popleft()
            if not q:
                continue
            row = q.popleft()
            pid = str(row["person_id"])
            if pid in seen:
                continue
            seen.add(pid)
            progressed = True
            sequence.append({
                "sequence": len(sequence) + 1,
                "person_id": pid,
                "canonical_name": row.get("canonical_name"),
                "polities": row.get("polities", []),
                "source_files": row.get("source_files", []),
                "source_segment": source_segment(row),
                "status": "NEEDS_SOURCE_REVIEW",
                "sequence_note": "Deterministic cross-polity work queue; sequence is not a rank."
            })
        if not progressed:
            break

    if len(sequence) != len(candidates):
        raise RuntimeError(f"P1 sequence lost candidates: {len(sequence)} != {len(candidates)}")
    return sequence


def validate_reviews(
    review_doc: dict[str, Any],
    candidate_by_id: dict[str, dict[str, Any]],
    person_by_id: dict[str, dict[str, Any]],
    allowed_evidence: set[str],
) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for raw in review_doc.get("reviews", []):
        pid = str(raw.get("person_id", ""))
        if pid in out:
            errors.append(f"duplicate review person_id: {pid}")
            continue
        candidate = candidate_by_id.get(pid)
        if not candidate:
            # Completed candidates leave the active P1 pool once a Skill is added.
            # Keep their source-review rows as durable research metadata instead of
            # turning successful distillation into a workflow failure.
            if pid in person_by_id:
                continue
            errors.append(f"unknown person_id in P1 source-review registry: {pid!r}")
            continue
        canonical = candidate.get("canonical_name")
        supplied = raw.get("canonical_name")
        if supplied and supplied != canonical:
            errors.append(f"{pid}: canonical_name mismatch {supplied!r} != {canonical!r}")
            continue
        complete = raw.get("source_review_complete")
        if not isinstance(complete, bool):
            errors.append(f"{pid}: source_review_complete must be boolean")
            continue
        evidence_state = str(raw.get("evidence_state", "UNKNOWN"))
        if evidence_state not in allowed_evidence:
            errors.append(f"{pid}: invalid evidence_state {evidence_state!r}")
            continue
        pointers = [str(x).strip() for x in (raw.get("evidence_pointers") or []) if str(x).strip()]
        evidence_note = str(raw.get("evidence_note", "")).strip()
        if complete and not pointers and not evidence_note:
            errors.append(f"{pid}: completed source review requires evidence_pointers or evidence_note")
            continue
        out[pid] = {
            "person_id": pid,
            "canonical_name": canonical,
            "source_review_complete": complete,
            "evidence_state": evidence_state,
            "evidence_note": evidence_note,
            "evidence_pointers": pointers,
            "transition_contexts": [str(x) for x in raw.get("transition_contexts", [])],
            "comparison_links": [str(x) for x in raw.get("comparison_links", [])],
            "simulation_contexts": [str(x) for x in raw.get("simulation_contexts", [])],
            "reviewed_by": raw.get("reviewed_by"),
            "reviewed_on": raw.get("reviewed_on"),
        }
    if errors:
        raise RuntimeError("Invalid P1 source review registry:\n- " + "\n- ".join(errors))
    return out


def build() -> dict[str, Any]:
    priority = load(PRIORITY)
    policy = load(POLICY)
    review_doc = load(REVIEWS)
    person_index = load(PERSON_INDEX)
    candidates = priority["p1_high_leverage_anchors"]["candidate_pool"]
    candidate_by_id = {str(r["person_id"]): r for r in candidates}
    person_by_id = {str(r["person_id"]): r for r in person_index.get("persons", [])}
    allowed_evidence = set(policy["descriptive_review_fields"]["evidence_state"]["allowed"])
    reviews = validate_reviews(review_doc, candidate_by_id, person_by_id, allowed_evidence)
    sequence = build_sequence(candidates)

    annotated: list[dict[str, Any]] = []
    for row in sequence:
        review = reviews.get(row["person_id"])
        merged = dict(row)
        if review:
            merged["source_review"] = review
            merged["status"] = "SOURCE_REVIEW_COMPLETE" if review["source_review_complete"] else "SOURCE_REVIEW_PARTIAL"
        annotated.append(merged)

    complete = [r for r in annotated if r["status"] == "SOURCE_REVIEW_COMPLETE"]
    target = int(policy["selection"]["initial_anchor_tranche_target"])
    diversity_floor = int(policy["selection"]["minimum_cross_polity_diversity"])
    tranche_candidate = complete[:target]
    tranche_polities = sorted({p for r in tranche_candidate for p in (r.get("polities") or [])})
    p0_missing = int(priority["summary"]["p0_backbone_missing"])
    tranche_ready = p0_missing == 0 and len(tranche_candidate) >= target and len(tranche_polities) >= diversity_floor

    if p0_missing:
        status = "LOCKED_BY_P0"
    elif tranche_ready:
        status = "INITIAL_TRANCHE_READY"
    else:
        status = "SOURCE_REVIEW_IN_PROGRESS"

    return {
        "schema_version": "1.1",
        "status": status,
        "policy_file": str(POLICY.relative_to(ROOT)).replace("\\", "/"),
        "review_file": str(REVIEWS.relative_to(ROOT)).replace("\\", "/"),
        "source_priority_file": str(PRIORITY.relative_to(ROOT)).replace("\\", "/"),
        "warning": "Sequence positions are deterministic work-queue positions, not rankings or judgments of persons.",
        "summary": {
            "p0_missing": p0_missing,
            "candidate_pool": len(candidates),
            "source_reviews_recorded": len(reviews),
            "source_reviews_archived_or_completed": len(review_doc.get("reviews", [])) - len(reviews),
            "source_reviews_complete": len(complete),
            "needs_or_partial_review": len(candidates) - len(complete),
            "initial_anchor_tranche_target": target,
            "initial_anchor_tranche_selected": len(tranche_candidate) if tranche_ready else 0,
            "minimum_cross_polity_diversity": diversity_floor,
            "selected_polity_diversity": len(tranche_polities) if tranche_ready else 0,
        },
        "initial_anchor_tranche": tranche_candidate if tranche_ready else [],
        "review_sequence": annotated,
    }


def write_report(doc: dict[str, Any], policy: dict[str, Any]) -> None:
    s = doc["summary"]
    slate_size = int(policy["selection"]["initial_review_slate_size"])
    lines = [
        "# P1 Anchor Plan",
        "",
        "> Neutral research scheduling for post-Qin CORE coverage. Sequence positions are **not ranks** and do not express historical worth, legitimacy, morality, or ruler quality.",
        "",
        "## State",
        "",
        f"- Status: **{doc['status']}**",
        f"- P0 missing: **{s['p0_missing']}**",
        f"- P1 candidate pool: **{s['candidate_pool']}**",
        f"- Active source reviews recorded: **{s['source_reviews_recorded']}**",
        f"- Archived/completed source reviews: **{s.get('source_reviews_archived_or_completed', 0)}**",
        f"- Active source reviews complete: **{s['source_reviews_complete']}**",
        f"- Needs or partial review: **{s['needs_or_partial_review']}**",
        f"- Initial tranche target: **{s['initial_anchor_tranche_target']}** across at least **{s['minimum_cross_polity_diversity']}** polities",
        "",
        "## Method",
        "",
        "Candidates are placed into a deterministic polity round-robin sequence using source-segment order, polity name, and stable person ID. This balances corpus work without assigning a person score or winner.",
        "",
        f"## First {slate_size} source-review slots",
        "",
        "| Seq | Person | Polity | Evidence state | Review state |",
        "|---:|---|---|---|---|",
    ]
    for row in doc["review_sequence"][:slate_size]:
        review = row.get("source_review") or {}
        lines.append(
            f"| {row['sequence']} | {row['canonical_name']} | {' / '.join(row.get('polities') or ['—'])} | {review.get('evidence_state', 'UNKNOWN')} | {row['status']} |"
        )
    if doc["initial_anchor_tranche"]:
        lines += ["", "## Initial research/distillation tranche", ""]
        for row in doc["initial_anchor_tranche"]:
            lines.append(f"- **{row['canonical_name']}** · {' / '.join(row.get('polities') or ['—'])} · `{row['person_id']}`")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    policy = load(POLICY)
    doc = build()
    dump(OUT, doc)
    write_report(doc, policy)
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
