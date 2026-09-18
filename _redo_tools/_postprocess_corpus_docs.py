#!/usr/bin/env python3
"""Synchronize generated corpus metadata with production stable IDs and live Skill layout."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSESSMENT = ROOT / "assessment"
SKILLS = ROOT / "skills"
LANE_CONFIG = DATA / "skill-lane-display-names.json"

DYNASTY_ORDER = [
    "xia", "shang", "zhou", "qin", "chuhan", "xihan", "xin", "donghan", "sanguo", "jin",
    "nanbeichao", "sui", "tang", "wudai", "song", "yuan", "ming", "qing",
]
DYNASTY_NAMES = {
    "xia": "夏", "shang": "商", "zhou": "周", "qin": "秦", "chuhan": "楚汉",
    "xihan": "西汉", "xin": "新", "donghan": "东汉", "sanguo": "三国", "jin": "晋",
    "nanbeichao": "南北朝", "sui": "隋", "tang": "唐", "wudai": "五代",
    "song": "宋", "yuan": "元", "ming": "明", "qing": "清",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, doc) -> None:
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def live_skill_layout() -> tuple[list[dict[str, object]], list[str], int]:
    order = list(DYNASTY_ORDER)
    names = dict(DYNASTY_NAMES)
    if LANE_CONFIG.exists():
        config = load(LANE_CONFIG)
        order = [str(x) for x in config.get("order", order)]
        names.update({str(k): str(v) for k, v in config.get("names", {}).items()})

    dynasty_counts: dict[str, int] = {}
    non_dynasty: list[str] = []
    for top in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        if top.name.startswith("_"):
            non_dynasty.append(top.name)
            continue
        count = sum(1 for _ in top.glob("*/SKILL.md"))
        if count:
            dynasty_counts[top.name] = count

    ordered = [x for x in order if x in dynasty_counts]
    ordered += sorted(x for x in dynasty_counts if x not in ordered)
    dynasties = [
        {"id": did, "name": names.get(did, did), "count": dynasty_counts[did]}
        for did in ordered
    ]
    return dynasties, non_dynasty, sum(dynasty_counts.values())


def update_coverage_report() -> None:
    path = ASSESSMENT / "CORPUS_COVERAGE.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "These are engineering counts, not final historical totals. Small-polity discovery, REVIEW decisions and cross-polity identity QA remain open. REVIEW is excluded from locked CORE until evidence resolves it.",
        "These are engineering counts, not final historical totals. Small-polity discovery and REVIEW decisions remain open. Canonical-label QA is collision-free; every current entity has an append-only stable person ID. REVIEW remains outside locked CORE until evidence resolves it.",
    )
    text = text.replace(
        "One person may have multiple rule episodes/titles/polities but must ultimately receive one stable person ID. Existing analytically useful Skills that fail the ruler admission rule are kept through explicit scope exceptions rather than deleted or falsely promoted into CORE.",
        "One person may have multiple rule episodes/titles/polities but keeps one stable person ID. Later identity merges retire/redirect old IDs instead of renumbering the corpus. Existing analytically useful Skills that fail the ruler admission rule are kept through explicit scope exceptions rather than deleted or falsely promoted into CORE.",
    )
    text = text.replace(
        "2. Resolve REVIEW candidates and cross-polity aliases, then freeze stable IDs.",
        "2. Resolve REVIEW candidates and cross-polity relations using explicit retire/redirect migrations; never renumber stable IDs.",
    )
    text = text.replace(
        "See `data/corpus-gap.json`, `data/existing-skill-person-map.json`, `data/corpus-scope-exceptions.json`, and `data/rulers-person-index.json`.",
        "See `data/corpus-gap.json`, `data/existing-skill-person-map.json`, `data/corpus-scope-exceptions.json`, `data/rulers-person-index.json`, and `data/ruler-person-id-registry.json`.",
    )
    path.write_text(text, encoding="utf-8")


def update_master_manifest() -> None:
    path = DATA / "rulers-master.json"
    doc = load(path)
    index = load(DATA / "rulers-person-index.json")
    doc["status"] = "STABLE_PERSON_ID_REGISTRY_ACTIVE"
    doc["person_id_registry"] = "data/ruler-person-id-registry.json"
    doc["candidate_stats"] = index.get("stats", doc.get("candidate_stats", {}))
    doc["identity_rule"] = (
        "one person = one stable append-only person ID; reigns/titles/polities are rule episodes; "
        "later merges retire/redirect IDs rather than renumbering"
    )
    doc["warning"] = (
        "CORE canonical labels passed automated collision/composite QA. REVIEW identity relations and remaining polity discovery stay explicit and may append or retire entities, but existing IDs do not shift."
    )
    dump(path, doc)


def update_corpus_registry() -> None:
    path = DATA / "corpus-registry.json"
    doc = load(path)
    index = load(DATA / "rulers-person-index.json")
    idreg = load(DATA / "ruler-person-id-registry.json")
    issues = load(DATA / "corpus-identity-issues.json")
    dynasties, non_dynasty, skill_total = live_skill_layout()

    doc["generated_from"] = "live repository snapshot"
    doc["totals"] = {
        "skills": skill_total,
        "dynasty_directories": len(dynasties),
        "skills_top_level_directories": len(dynasties) + len(non_dynasty),
    }
    doc["non_dynasty_directories"] = non_dynasty
    doc["dynasties"] = dynasties

    master = doc.setdefault("master_corpus", {})
    master.update({
        "status": index.get("status"),
        "person_id_registry": "data/ruler-person-id-registry.json",
        "stable_ids_active": idreg.get("active_count"),
        "stable_ids_issued": idreg.get("total_ids_ever_issued"),
        "next_person_id_sequence": idreg.get("next_sequence"),
        "identity_qa_summary": issues.get("summary", {}),
        "existing_skills": skill_total,
        "note": "Canonical-label QA is clean and stable IDs are active. REVIEW disputes and polity discovery remain explicit without renumbering existing persons.",
    })
    dump(path, doc)


def main() -> None:
    update_coverage_report()
    update_master_manifest()
    update_corpus_registry()
    print("Synced corpus reports/manifests with stable IDs and live Skill layout.")


if __name__ == "__main__":
    main()
