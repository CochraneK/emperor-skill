#!/usr/bin/env python3
"""Build ruler corpus with an auditable identity-normalization overlay.

The segmented discovery/master files remain untouched. Evidence-backed canonical-name
normalizations and explicit non-person placeholders live in
``data/corpus-identity-overrides.json`` and are applied here before the standard corpus
builder runs. This keeps raw provenance inspectable while allowing P0 identity QA to
converge before stable person IDs are frozen.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import _build_ruler_corpus as base

ROOT = Path(__file__).resolve().parents[1]
OVERRIDE_PATH = ROOT / "data" / "corpus-identity-overrides.json"


def _load_overrides() -> dict[str, Any]:
    return json.loads(OVERRIDE_PATH.read_text(encoding="utf-8"))


DOC = _load_overrides()
CANONICAL = DOC.get("canonical_overrides", {})
EXCLUDED = set(DOC.get("excluded_non_person_placeholders", {}))

_original_normalize_identity = base.normalize_identity
_original_emit_person = base.emit_person
_original_build_candidate_index = base.build_candidate_index


def normalize_identity(name: str | None) -> str | None:
    cleaned = base._clean_name(name)
    if not cleaned:
        return None
    override = CANONICAL.get(cleaned)
    if override:
        return str(override["canonical_name"])
    return _original_normalize_identity(cleaned)


def emit_person(item: Any, parent: dict[str, Any], key: str, source: Path, out: list[dict[str, Any]]) -> None:
    raw_name: str | None = None
    if isinstance(item, str):
        raw_name = item
    elif isinstance(item, dict) and item.get("name"):
        raw_name = str(item["name"])
    if raw_name and base._clean_name(raw_name) in EXCLUDED:
        return
    _original_emit_person(item, parent, key, source, out)


def build_candidate_index() -> dict[str, Any]:
    candidate = _original_build_candidate_index()
    extras_by_canonical: dict[str, set[str]] = {}
    for raw, record in CANONICAL.items():
        canonical = str(record["canonical_name"])
        extras = extras_by_canonical.setdefault(canonical, set())
        extras.add(raw)
        extras.update(str(x) for x in record.get("aliases", []) if x)

    for person in candidate.get("persons", []):
        canonical = person.get("canonical_name")
        extras = extras_by_canonical.get(str(canonical), set())
        if not extras:
            continue
        aliases = set(person.get("aliases", [])) | extras
        aliases.discard(str(canonical))
        person["aliases"] = sorted(aliases)
        person["identity_hints"] = sorted(base.person_alias_hints(str(canonical), person["aliases"]))
        person["identity_resolution"] = {
            "status": "EVIDENCE_BACKED_OVERRIDE",
            "source": "data/corpus-identity-overrides.json",
        }

    candidate["identity_override_file"] = "data/corpus-identity-overrides.json"
    candidate["identity_override_stats"] = {
        "canonical_overrides": len(CANONICAL),
        "excluded_non_person_placeholders": len(EXCLUDED),
        "unresolved_review": len(DOC.get("unresolved_review", {})),
    }
    return candidate


# Monkey-patch the standard builder's runtime globals so all downstream matching,
# reports and manifests use the resolved identity layer without editing raw segments.
base.normalize_identity = normalize_identity
base.emit_person = emit_person
base.build_candidate_index = build_candidate_index


if __name__ == "__main__":
    base.main()
