#!/usr/bin/env python3
"""Build ruler corpus with an auditable identity-resolution overlay.

The segmented discovery/master files remain untouched. The overlay supports three
semantically different operations before stable person IDs are frozen:

1. canonical_overrides: evidence-backed same-person normalization;
2. source_corrections: choose a defensible canonical label without promoting every
   raw composite token to a true alias;
3. ambiguous_splits: turn a composite discovery label into separate REVIEW people
   when the historical literature does not justify a merge.

This keeps raw provenance inspectable while preventing a cosmetically clean QA score
from being achieved through false identity merges.
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
CORRECTIONS = DOC.get("source_corrections", {})
SPLITS = DOC.get("ambiguous_splits", {})
EXCLUDED = set(DOC.get("excluded_non_person_placeholders", {}))

_original_normalize_identity = base.normalize_identity
_original_emit_person = base.emit_person
_original_build_candidate_index = base.build_candidate_index


def _resolution_for_raw(cleaned: str) -> dict[str, Any] | None:
    return CANONICAL.get(cleaned) or CORRECTIONS.get(cleaned)


def normalize_identity(name: str | None) -> str | None:
    cleaned = base._clean_name(name)
    if not cleaned:
        return None
    override = _resolution_for_raw(cleaned)
    if override:
        return str(override["canonical_name"])
    return _original_normalize_identity(cleaned)


def emit_person(item: Any, parent: dict[str, Any], key: str, source: Path, out: list[dict[str, Any]]) -> None:
    raw_name: str | None = None
    if isinstance(item, str):
        raw_name = item
    elif isinstance(item, dict) and item.get("name"):
        raw_name = str(item["name"])
    cleaned = base._clean_name(raw_name) if raw_name else None

    if cleaned in EXCLUDED:
        return

    split = SPLITS.get(cleaned or "")
    if split:
        for candidate in split.get("candidates", []):
            replacement: dict[str, Any] = {
                "name": candidate["name"],
                "aliases": candidate.get("aliases", []),
                "status": candidate.get("status", "IDENTITY_REVIEW"),
                "reason": split.get("basis"),
            }
            before = len(out)
            _original_emit_person(replacement, parent, key, source, out)
            # Preserve the discovery-layer composite as provenance, not as an alias.
            for rec in out[before:]:
                rec["raw_name"] = raw_name
        return

    _original_emit_person(item, parent, key, source, out)


def _resolution_metadata(record: dict[str, Any], raw: str, default_status: str) -> dict[str, Any]:
    return {
        "status": record.get("resolution_type", default_status),
        "source": "data/corpus-identity-overrides.json",
        "confidence": record.get("confidence"),
        "basis": record.get("basis"),
        "source_raw_labels": [raw],
        "evidence": record.get("evidence", []),
        "reported_aliases_unverified": record.get("reported_aliases_unverified", []),
    }


def build_candidate_index() -> dict[str, Any]:
    candidate = _original_build_candidate_index()

    extras_by_canonical: dict[str, set[str]] = {}
    suppress_by_canonical: dict[str, set[str]] = {}
    metadata_by_canonical: dict[str, dict[str, Any]] = {}

    for section, default_status in (
        (CANONICAL, "EVIDENCE_BACKED_OVERRIDE"),
        (CORRECTIONS, "SOURCE_LABEL_CORRECTION"),
    ):
        for raw, record in section.items():
            canonical = str(record["canonical_name"])
            extras = extras_by_canonical.setdefault(canonical, set())
            extras.update(str(x) for x in record.get("aliases", []) if x)
            if not record.get("suppress_raw_identity_hint", False):
                extras.add(raw)
            else:
                suppress_by_canonical.setdefault(canonical, set()).add(raw)
            metadata_by_canonical[canonical] = _resolution_metadata(record, raw, default_status)

    split_relations: list[dict[str, Any]] = []
    for raw, split in SPLITS.items():
        names = [str(c["name"]) for c in split.get("candidates", [])]
        relation = {
            "source_raw_label": raw,
            "candidates": names,
            "relation": split.get("relation", "POSSIBLE_SAME_PERSON_DISPUTED"),
            "status": "OPEN_REVIEW_RELATION",
            "basis": split.get("basis"),
            "evidence": split.get("evidence", []),
        }
        split_relations.append(relation)
        for part in split.get("candidates", []):
            canonical = str(part["name"])
            extras_by_canonical.setdefault(canonical, set()).update(
                str(x) for x in part.get("aliases", []) if x
            )
            suppress_by_canonical.setdefault(canonical, set()).add(raw)
            metadata_by_canonical[canonical] = {
                "status": "AMBIGUOUS_SPLIT_REVIEW",
                "source": "data/corpus-identity-overrides.json",
                "confidence": split.get("confidence", "DISPUTED"),
                "basis": split.get("basis"),
                "source_raw_labels": [raw],
                "evidence": split.get("evidence", []),
                "related_candidates": [n for n in names if n != canonical],
                "relation": split.get("relation", "POSSIBLE_SAME_PERSON_DISPUTED"),
            }

    for person in candidate.get("persons", []):
        canonical = str(person.get("canonical_name"))
        extras = extras_by_canonical.get(canonical, set())
        suppressed = suppress_by_canonical.get(canonical, set())
        if not extras and not suppressed and canonical not in metadata_by_canonical:
            continue

        aliases = set(person.get("aliases", [])) | extras
        aliases.difference_update(suppressed)
        aliases.discard(canonical)
        person["aliases"] = sorted(aliases)
        person["identity_hints"] = sorted(base.person_alias_hints(canonical, person["aliases"]))
        if canonical in metadata_by_canonical:
            person["identity_resolution"] = metadata_by_canonical[canonical]

    candidate["identity_override_file"] = "data/corpus-identity-overrides.json"
    candidate["identity_review_relations"] = split_relations
    candidate["identity_override_stats"] = {
        "canonical_overrides": len(CANONICAL),
        "source_corrections": len(CORRECTIONS),
        "ambiguous_splits": len(SPLITS),
        "excluded_non_person_placeholders": len(EXCLUDED),
        "open_identity_questions": len(DOC.get("open_identity_questions", {})),
    }
    return candidate


# Monkey-patch the standard builder's runtime globals so all downstream matching,
# reports and manifests use the resolved identity layer without editing raw segments.
base.normalize_identity = normalize_identity
base.emit_person = emit_person
base.build_candidate_index = build_candidate_index


if __name__ == "__main__":
    base.main()
