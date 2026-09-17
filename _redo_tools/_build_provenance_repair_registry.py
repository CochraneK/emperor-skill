#!/usr/bin/env python3
"""Build structured tracking for the historical 39-package provenance snapshot.

The 39 packages were selected by a now-invalid mtime heuristic, then semantically
triaged 39/39 in assessment/PROVENANCE_RECOVERY.md. This registry separates three
facts that must not be conflated:

1. historical trigger: package was in the frozen mtime snapshot;
2. semantic triage: research is reusable, with a repair class;
3. execution attestation: whether that repair has explicitly been recorded complete.

No attestation != proof of current defect. It only means completion is not recorded in
this ledger yet.
"""
from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SNAPSHOT = ROOT / "_redo_tools" / "_order_suspects_39.md"
TRIAGE = ROOT / "assessment" / "PROVENANCE_RECOVERY.md"
ATTESTATIONS = DATA / "provenance-repair-attestations.json"
OUT = DATA / "provenance-repair-registry.json"

ACTION_BY_DYNASTY = {
    "jin": "PATCH_TARGETED_VERIFY_REDISTILL",
    "sanguo": "PATCH_REDISTILL",
    "nanbeichao": "PATCH_TARGETED_VERIFY_REDISTILL",
    "shang": "PATCH_TARGETED_VERIFY_REDISTILL",
    "xia": "PATCH_TARGETED_VERIFY_REDISTILL",
    "zhou": "PATCH_TARGETED_VERIFY_REDISTILL",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def skill_person_map() -> dict[str, str]:
    gap = load_json(DATA / "corpus-gap.json")
    out: dict[str, str] = {}
    for person in gap.get("person_matches", []):
        pid = person.get("candidate_id") or person.get("person_id")
        for p in person.get("matched_skill_paths", []):
            if pid and p:
                out[str(p)] = str(pid)
    return out


def parse_snapshot() -> list[dict]:
    rows = []
    pat = re.compile(r"^\|\s*([a-z]+)\s*\|\s*([a-z0-9-]+-perspective)\s*\|\s*(\d+)s\s*\|$")
    for line in SNAPSHOT.read_text(encoding="utf-8").splitlines():
        m = pat.match(line.strip())
        if not m:
            continue
        dynasty, package, delta = m.groups()
        rows.append({"dynasty": dynasty, "package": package, "historical_mtime_delta_seconds": int(delta)})
    return rows


def load_attestations() -> dict[str, dict]:
    if not ATTESTATIONS.exists():
        return {}
    doc = load_json(ATTESTATIONS)
    out = {}
    for row in doc.get("attestations", []):
        path = row.get("skill_path")
        if path:
            out[str(path)] = row
    return out


def main() -> None:
    snapshot = parse_snapshot()
    if len(snapshot) != 39:
        raise RuntimeError(f"expected frozen 39-package snapshot, parsed {len(snapshot)}")

    triage_text = TRIAGE.read_text(encoding="utf-8")
    if "Completed snapshot review · 39/39" not in triage_text:
        raise RuntimeError("semantic triage document no longer attests 39/39 completion")

    pmap = skill_person_map()
    attest = load_attestations()
    items = []
    for row in snapshot:
        path = f"skills/{row['dynasty']}/{row['package']}"
        att = attest.get(path)
        items.append({
            "skill_path": path,
            "person_id": pmap.get(path),
            "dynasty": row["dynasty"],
            "package": row["package"],
            "historical_trigger": "FROZEN_MTIME_ORDER_SNAPSHOT_ONLY",
            "historical_mtime_delta_seconds": row["historical_mtime_delta_seconds"],
            "semantic_triage": "RESEARCH_REUSABLE",
            "recommended_repair": ACTION_BY_DYNASTY[row["dynasty"]],
            "execution_tracking": (
                {"status": "ATTESTED_COMPLETE", **att}
                if att else
                {"status": "NO_EXPLICIT_ATTESTATION"}
            ),
        })

    completed = sum(i["execution_tracking"]["status"] == "ATTESTED_COMPLETE" for i in items)
    linked = sum(bool(i.get("person_id")) for i in items)
    doc = {
        "schema_version": "1.0",
        "status": "TRIAGED_REPAIR_EXECUTION_TRACKING",
        "sources": {
            "historical_snapshot": "_redo_tools/_order_suspects_39.md",
            "semantic_triage": "assessment/PROVENANCE_RECOVERY.md",
            "completion_attestations": "data/provenance-repair-attestations.json",
        },
        "policy": {
            "mtime_is_not_quality_evidence": True,
            "semantic_triage_completed": True,
            "absence_of_attestation_means": "COMPLETION_NOT_RECORDED_NOT_PROOF_OF_DEFECT",
            "allowed_future_actions": ["KEEP", "CLEAN", "PATCH", "TARGETED_VERIFY", "REDISTILL", "RERESEARCH", "REBUILD"],
        },
        "summary": {
            "historical_snapshot_packages": len(items),
            "semantic_triage_completed_packages": len(items),
            "research_reusable_packages": len(items),
            "explicit_completion_attestations": completed,
            "without_explicit_completion_attestation": len(items) - completed,
            "stable_person_id_linked": linked,
        },
        "items": items,
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
