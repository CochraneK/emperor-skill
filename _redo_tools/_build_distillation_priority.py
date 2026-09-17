#!/usr/bin/env python3
"""Generate the canonical distillation schedule.

Scheduling policy is intentionally separate from corpus admission. A ruler can be CORE
without being early in the work queue. Phase P0 follows the user-selected project
strategy: finish the main Qin-to-Qing dynastic backbone lane-by-lane, then select
high-leverage anchors, then finish other post-Qin CORE, then bulk early/pre-Qin CORE.

The P0 sequence is read from data/distillation-priority-policy.json and the source
master files themselves, so ruler order follows the curated historical sequence rather
than alphabetical person IDs.
"""
from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSESSMENT = ROOT / "assessment"
POLICY_PATH = DATA / "distillation-priority-policy.json"
OUT_PATH = DATA / "distillation-priority.json"

EARLY_FILES = {
    "data/rulers-master-h1-early.json",
    "data/rulers-master-h2-preqin.json",
    "data/ruler-candidates-preqin-other.json",
    "data/legendary-rulers.json",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def item_name(item: Any) -> str | None:
    if isinstance(item, str):
        return item.strip()
    if isinstance(item, dict) and item.get("name"):
        return str(item["name"]).strip()
    return None


def item_labels(item: Any) -> list[str]:
    name = item_name(item)
    labels: list[str] = []
    if name:
        labels.append(name)
        labels.extend(x.strip() for x in re.split(r"[/／]", name) if x.strip())
    if isinstance(item, dict):
        for alias in item.get("aliases", []) or []:
            alias = str(alias).strip()
            if alias:
                labels.append(alias)
                labels.extend(x.strip() for x in re.split(r"[/／]", alias) if x.strip())
    # stable de-dup preserving source preference
    return list(dict.fromkeys(labels))


def find_lane(doc: dict[str, Any], collection: str, polity_id: str) -> dict[str, Any]:
    rows = doc.get(collection, [])
    for row in rows:
        if row.get("id") == polity_id:
            return row
    raise RuntimeError(f"policy lane {polity_id!r} not found in collection {collection!r}")


def build_label_index(persons: list[dict[str, Any]]) -> dict[str, set[str]]:
    lookup: defaultdict[str, set[str]] = defaultdict(set)
    for p in persons:
        pid = str(p["candidate_id"])
        labels = [p.get("canonical_name"), *p.get("aliases", []), *p.get("identity_hints", [])]
        for label in labels:
            if label:
                lookup[str(label)].add(pid)
    return lookup


def resolve_person(item: Any, lane_name: str, persons_by_id: dict[str, dict[str, Any]], label_index: dict[str, set[str]]) -> tuple[str | None, dict[str, Any]]:
    labels = item_labels(item)
    ids: set[str] = set()
    for label in labels:
        ids.update(label_index.get(label, set()))

    candidates = [persons_by_id[i] for i in sorted(ids)]
    core = [p for p in candidates if p.get("corpus_status") == "CORE"]
    lane_core = [p for p in core if lane_name in (p.get("polities") or [])]

    if len(lane_core) == 1:
        return str(lane_core[0]["candidate_id"]), {"resolution": "LABEL_AND_POLITY"}
    if len(core) == 1:
        return str(core[0]["candidate_id"]), {"resolution": "UNIQUE_CORE_LABEL"}
    if len(candidates) == 1:
        return str(candidates[0]["candidate_id"]), {"resolution": "UNIQUE_LABEL_NONCORE", "noncore": True}

    return None, {
        "resolution": "UNRESOLVED_OR_AMBIGUOUS",
        "labels": labels,
        "candidate_ids": [str(p["candidate_id"]) for p in candidates],
        "candidate_names": [p.get("canonical_name") for p in candidates],
    }


def build() -> dict[str, Any]:
    policy = load(POLICY_PATH)
    index = load(DATA / "rulers-person-index.json")
    gap = load(DATA / "corpus-gap.json")

    persons = index["persons"]
    by_id = {str(p["candidate_id"]): p for p in persons}
    label_index = build_label_index(persons)
    missing_ids = {str(p["candidate_id"]) for p in gap.get("missing_core", [])}

    lanes_out: list[dict[str, Any]] = []
    p0_queue: list[dict[str, Any]] = []
    p0_ids: set[str] = set()
    mapping_issues: list[dict[str, Any]] = []

    lanes = sorted(policy["phases"]["P0_DYNASTIC_BACKBONE_FULL_CHAIN"]["lanes"], key=lambda x: x["order"])
    for lane_index, lane_cfg in enumerate(lanes, start=1):
        source = load(ROOT / lane_cfg["file"])
        lane = find_lane(source, lane_cfg["collection"], lane_cfg["polity_id"])
        lane_name = str(lane.get("name") or lane_cfg["label"])
        source_people = lane.get("persons", [])

        resolved_rows: list[dict[str, Any]] = []
        complete = 0
        missing = 0
        noncore = 0

        for succession_index, raw in enumerate(source_people, start=1):
            raw_name = item_name(raw)
            pid, detail = resolve_person(raw, lane_name, by_id, label_index)
            if not pid:
                mapping_issues.append({
                    "phase": "P0_DYNASTIC_BACKBONE_FULL_CHAIN",
                    "lane": lane_cfg["label"],
                    "source_file": lane_cfg["file"],
                    "raw_name": raw_name,
                    **detail,
                })
                resolved_rows.append({
                    "succession_order": succession_index,
                    "raw_name": raw_name,
                    "status": "MAPPING_REVIEW",
                })
                continue

            person = by_id[pid]
            status = person.get("corpus_status")
            if status != "CORE":
                noncore += 1
                resolved_rows.append({
                    "succession_order": succession_index,
                    "person_id": pid,
                    "canonical_name": person.get("canonical_name"),
                    "corpus_status": status,
                    "status": "NON_CORE_DOES_NOT_BLOCK_P0",
                })
                continue

            p0_ids.add(pid)
            has_skill = bool(person.get("existing_skill_paths"))
            is_missing = pid in missing_ids or not has_skill
            state = "MISSING" if is_missing else "COMPLETE"
            if is_missing:
                missing += 1
                p0_queue.append({
                    "phase": "P0_DYNASTIC_BACKBONE_FULL_CHAIN",
                    "backbone_lane_order": lane_cfg["order"],
                    "lane": lane_cfg["label"],
                    "polity_name": lane_name,
                    "succession_order": succession_index,
                    "person_id": pid,
                    "canonical_name": person.get("canonical_name"),
                    "source_files": person.get("source_files", []),
                    "action": "RESEARCH_THEN_DISTILL",
                })
            else:
                complete += 1

            resolved_rows.append({
                "succession_order": succession_index,
                "person_id": pid,
                "canonical_name": person.get("canonical_name"),
                "corpus_status": status,
                "existing_skill_paths": person.get("existing_skill_paths", []),
                "status": state,
            })

        core_total = complete + missing
        lanes_out.append({
            "lane_order": lane_cfg["order"],
            "label": lane_cfg["label"],
            "polity_name": lane_name,
            "source_file": lane_cfg["file"],
            "source_polity_id": lane_cfg["polity_id"],
            "core_sequence_total": core_total,
            "complete": complete,
            "missing": missing,
            "noncore_primary_entries": noncore,
            "completion_ratio": round(complete / core_total, 4) if core_total else 1.0,
            "persons": resolved_rows,
        })

    p0_queue.sort(key=lambda r: (r["backbone_lane_order"], r["succession_order"]))
    first_incomplete = next((lane for lane in lanes_out if lane["missing"] > 0), None)
    active_lane_order = first_incomplete["lane_order"] if first_incomplete else None
    for row in p0_queue:
        row["execution_state"] = (
            "ACTIVE_NOW" if row["backbone_lane_order"] == active_lane_order
            else "WAIT_FOR_PRIOR_BACKBONE_LANES"
        )

    all_missing_core = [by_id[str(r["candidate_id"])] for r in gap.get("missing_core", [])]
    early_missing = [p for p in all_missing_core if set(p.get("source_files", [])) & EARLY_FILES]
    remaining_post_qin = [
        p for p in all_missing_core
        if p["candidate_id"] not in p0_ids and not (set(p.get("source_files", [])) & EARLY_FILES)
    ]

    # P1 is intentionally not auto-ranked yet. It is a selection problem, not a fame
    # list. The whole candidate pool is exposed so a later evidence/leverage scorer can
    # select anchors only after P0 is closed.
    p1_candidate_pool = [
        {
            "person_id": p["candidate_id"],
            "canonical_name": p["canonical_name"],
            "polities": p.get("polities", []),
            "source_files": p.get("source_files", []),
            "status": "ELIGIBLE_AFTER_P0_NOT_YET_ANCHOR_RANKED",
        }
        for p in remaining_post_qin
    ]

    return {
        "schema_version": "1.0",
        "status": "CANONICAL_DISTILLATION_PRIORITY_GENERATED",
        "policy_file": "data/distillation-priority-policy.json",
        "policy_note": "Scheduling priority is not a historical worth/orthodoxy ranking.",
        "summary": {
            "all_missing_core": len(all_missing_core),
            "p0_backbone_core_persons": sum(l["core_sequence_total"] for l in lanes_out),
            "p0_backbone_complete": sum(l["complete"] for l in lanes_out),
            "p0_backbone_missing": len(p0_queue),
            "p0_backbone_completion_ratio": round(
                sum(l["complete"] for l in lanes_out) / max(1, sum(l["core_sequence_total"] for l in lanes_out)), 4
            ),
            "p1_post_qin_anchor_candidate_pool": len(p1_candidate_pool),
            "p2_remaining_post_qin_core_pool": len(remaining_post_qin),
            "p3_early_and_preqin_missing_core": len(early_missing),
            "mapping_issues": len(mapping_issues),
            "current_focus_lane": first_incomplete["label"] if first_incomplete else None,
            "current_focus_missing": first_incomplete["missing"] if first_incomplete else 0,
        },
        "p0_backbone": {
            "rule": policy["phases"]["P0_DYNASTIC_BACKBONE_FULL_CHAIN"]["rule"],
            "current_focus_lane": first_incomplete["label"] if first_incomplete else None,
            "lanes": lanes_out,
            "queue": p0_queue,
        },
        "p1_high_leverage_anchors": {
            "status": "LOCKED_UNTIL_P0_COMPLETE" if p0_queue else "READY_FOR_ANCHOR_SCORING",
            "rule": policy["phases"]["P1_HIGH_LEVERAGE_ANCHORS"]["rule"],
            "candidate_pool": p1_candidate_pool,
        },
        "p2_remaining_post_qin_core": {
            "status": "AFTER_P1",
            "count": len(remaining_post_qin),
        },
        "p3_early_and_preqin_core": {
            "status": "AFTER_POST_QIN",
            "count": len(early_missing),
        },
        "mapping_issues": mapping_issues,
    }


def write_report(doc: dict[str, Any]) -> None:
    s = doc["summary"]
    lines = [
        "# Distillation Priority · Qin → Qing Backbone", "",
        "> Canonical **work scheduling** plan, not a ranking of historical worth, legitimacy, ethnicity, or orthodoxy.", "",
        "## Current state", "",
        f"- All missing locked CORE: **{s['all_missing_core']}**",
        f"- P0 backbone CORE persons: **{s['p0_backbone_core_persons']}**",
        f"- P0 already distilled: **{s['p0_backbone_complete']}**",
        f"- P0 still missing: **{s['p0_backbone_missing']}**",
        f"- P0 completion: **{s['p0_backbone_completion_ratio']:.1%}**",
        f"- Current focus lane: **{s['current_focus_lane'] or 'P0 complete'}**",
        f"- Mapping issues: **{s['mapping_issues']}**", "",
        "## Execution order", "",
        "1. **P0 · Qin→Qing major dynastic backbone** — finish each lane before advancing.",
        "2. **P1 · High-leverage anchors** — select from remaining post-Qin CORE only after P0 closes.",
        "3. **P2 · Remaining post-Qin CORE** — parallel and transition polities systematically.",
        "4. **P3 · Early/pre-Qin CORE** — bulk completion with sparse-evidence discipline.",
        "5. **REVIEW/EXTENDED/LEGENDARY** — resolve scope/evidence first; never bulk-distill to inflate coverage.", "",
        "## P0 lanes", "",
        "| Order | Lane | Complete | Missing | Coverage |",
        "|---:|---|---:|---:|---:|",
    ]
    for lane in doc["p0_backbone"]["lanes"]:
        lines.append(
            f"| {lane['lane_order']} | {lane['label']} | {lane['complete']} | {lane['missing']} | {lane['completion_ratio']:.0%} |"
        )
    lines += ["", "## Next P0 tasks", ""]
    active = [r for r in doc["p0_backbone"]["queue"] if r["execution_state"] == "ACTIVE_NOW"]
    if not active:
        lines.append("P0 backbone is complete; proceed to P1 anchor scoring.")
    else:
        for row in active:
            lines.append(f"- `{row['person_id']}` · **{row['canonical_name']}** · {row['lane']} · succession #{row['succession_order']}")
    lines += ["", "Machine-readable schedule: `data/distillation-priority.json`. Policy: `data/distillation-priority-policy.json`."]
    ASSESSMENT.mkdir(parents=True, exist_ok=True)
    (ASSESSMENT / "DISTILLATION_PRIORITY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    doc = build()
    dump(OUT_PATH, doc)
    write_report(doc)
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
