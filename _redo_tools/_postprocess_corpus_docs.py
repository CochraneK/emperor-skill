#!/usr/bin/env python3
"""Synchronize generated corpus metadata with the production stable-ID layer.

The base corpus builder remains usable on its own, while the production workflow runs
through `_build_ruler_corpus_with_overrides.py`. This postprocessor removes obsolete
"freeze IDs next" language and exposes the registry state in generated manifests.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSESSMENT = ROOT / "assessment"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, doc) -> None:
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
    master = doc.setdefault("master_corpus", {})
    master.update({
        "status": index.get("status"),
        "person_id_registry": "data/ruler-person-id-registry.json",
        "stable_ids_active": idreg.get("active_count"),
        "stable_ids_issued": idreg.get("total_ids_ever_issued"),
        "next_person_id_sequence": idreg.get("next_sequence"),
        "identity_qa_summary": issues.get("summary", {}),
        "note": "Canonical-label P0 QA is clean and stable IDs are active. Remaining REVIEW disputes and polity discovery are modeled explicitly without renumbering existing persons.",
    })
    dump(path, doc)


def main() -> None:
    update_coverage_report()
    update_master_manifest()
    update_corpus_registry()
    print("Synced corpus reports/manifests with stable person-ID registry.")


if __name__ == "__main__":
    main()
