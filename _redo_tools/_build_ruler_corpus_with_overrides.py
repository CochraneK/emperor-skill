#!/usr/bin/env python3
"""Build the ruler corpus with identity resolution and stable person IDs.

The segmented discovery/master files remain untouched. The overlay supports three
semantically different identity operations:

1. canonical_overrides: evidence-backed same-person normalization;
2. source_corrections: choose a defensible canonical label without promoting every
   raw composite token to a true alias;
3. ambiguous_splits: turn a composite discovery label into separate REVIEW people
   when the historical literature does not justify a merge.

After canonical-label QA, the builder assigns append-only stable person IDs from
``data/ruler-person-id-registry.json``. Existing IDs never shift when a newly
discovered ruler sorts earlier alphabetically. REVIEW entities may later be retired
or redirected after scholarship resolves an identity dispute, but their historical
IDs remain in the registry for referential integrity.
"""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import re
import sys
from typing import Any

import _build_ruler_corpus as base

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OVERRIDE_PATH = DATA / "corpus-identity-overrides.json"
REGISTRY_PATH = DATA / "ruler-person-id-registry.json"


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


def _load_id_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {
            "schema_version": "1.0",
            "status": "APPEND_ONLY_STABLE_PERSON_ID_REGISTRY",
            "id_format": "ruler-NNNN",
            "next_sequence": 1,
            "entries": [],
        }
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _id_number(person_id: str) -> int:
    m = re.fullmatch(r"ruler-(\d+)", person_id)
    if not m:
        raise RuntimeError(f"invalid stable person id in registry: {person_id!r}")
    return int(m.group(1))


def _assign_stable_person_ids(candidate: dict[str, Any]) -> None:
    registry = _load_id_registry()
    entries = registry.get("entries", [])
    by_id = {str(e["person_id"]): e for e in entries}

    if len(by_id) != len(entries):
        raise RuntimeError("stable person ID registry contains duplicate person_id values")

    by_canonical: dict[str, list[str]] = {}
    historical_label_to_ids: dict[str, list[str]] = {}
    for pid, entry in by_id.items():
        canonical = str(entry.get("canonical_name", ""))
        if canonical:
            by_canonical.setdefault(canonical, []).append(pid)
        for label in entry.get("known_labels", []):
            if label:
                historical_label_to_ids.setdefault(str(label), []).append(pid)

    next_sequence = int(registry.get("next_sequence") or 1)
    if by_id:
        next_sequence = max(next_sequence, max(_id_number(pid) for pid in by_id) + 1)

    initial_freeze = not by_id
    used_ids: set[str] = set()
    today = date.today().isoformat()

    for person in candidate.get("persons", []):
        canonical = str(person["canonical_name"])
        stable_id: str | None = None

        direct = by_canonical.get(canonical, [])
        if len(direct) > 1:
            raise RuntimeError(f"registry has multiple exact canonical matches for {canonical!r}: {direct}")
        if direct:
            stable_id = direct[0]
        elif canonical in historical_label_to_ids:
            # A canonical rename must be an explicit migration, never an implicit alias
            # merge. This protects homonymous rulers and disputed identities.
            raise RuntimeError(
                f"new canonical label {canonical!r} matches a historical registry label; "
                "add an explicit registry migration instead of auto-reusing an ID"
            )

        if stable_id is None:
            if initial_freeze:
                # Preserve the already-published temporary numbering at the freeze
                # boundary so existing references do not churn needlessly.
                stable_id = str(person["candidate_id"])
                next_sequence = max(next_sequence, _id_number(stable_id) + 1)
            else:
                stable_id = f"ruler-{next_sequence:04d}"
                next_sequence += 1

            if stable_id in by_id:
                raise RuntimeError(f"attempted to reuse existing stable person id {stable_id}")
            entry = {
                "person_id": stable_id,
                "canonical_name": canonical,
                "canonical_history": [canonical],
                "known_labels": [],
                "first_frozen_on": today,
                "first_status": person.get("corpus_status"),
                "active_in_current_build": True,
            }
            entries.append(entry)
            by_id[stable_id] = entry
            by_canonical.setdefault(canonical, []).append(stable_id)
        else:
            entry = by_id[stable_id]

        if stable_id in used_ids:
            raise RuntimeError(f"two current corpus people resolved to the same stable id {stable_id}")
        used_ids.add(stable_id)

        old_canonical = str(entry.get("canonical_name", ""))
        history = [str(x) for x in entry.get("canonical_history", []) if x]
        if old_canonical and old_canonical not in history:
            history.append(old_canonical)
        if canonical not in history:
            history.append(canonical)
        entry["canonical_history"] = history
        entry["canonical_name"] = canonical

        known_labels = set(str(x) for x in entry.get("known_labels", []) if x)
        known_labels.add(canonical)
        known_labels.update(str(x) for x in person.get("aliases", []) if x)
        entry["known_labels"] = sorted(known_labels)
        entry["polities_seen"] = sorted(
            set(str(x) for x in entry.get("polities_seen", []) if x)
            | set(str(x) for x in person.get("polities", []) if x)
        )
        entry["statuses_seen"] = sorted(
            set(str(x) for x in entry.get("statuses_seen", []) if x)
            | {str(person.get("corpus_status"))}
        )
        entry["current_status"] = person.get("corpus_status")
        entry["active_in_current_build"] = True
        entry["last_seen_on"] = today

        person["build_sequence_id"] = person["candidate_id"]
        person["candidate_id"] = stable_id  # backward-compatible field, now stable
        person["person_id"] = stable_id
        person["identity_status"] = "STABLE_PERSON_ID_ASSIGNED"

    for pid, entry in by_id.items():
        if pid not in used_ids:
            entry["active_in_current_build"] = False

    entries.sort(key=lambda e: _id_number(str(e["person_id"])))
    registry.update({
        "schema_version": "1.0",
        "status": "APPEND_ONLY_STABLE_PERSON_ID_REGISTRY",
        "id_format": "ruler-NNNN",
        "freeze_policy": "IDs are never renumbered. Later identity merges retire/redirect IDs instead of reusing them.",
        "initial_freeze_on": registry.get("initial_freeze_on") or today,
        "next_sequence": next_sequence,
        "active_count": len(used_ids),
        "total_ids_ever_issued": len(entries),
        "entries": entries,
    })

    if "--check" not in sys.argv:
        REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    candidate["schema_version"] = "0.6"
    candidate["status"] = "STABLE_PERSON_ID_REGISTRY_ACTIVE"
    candidate["warning"] = (
        "candidate_id is retained for compatibility but now equals stable person_id. "
        "REVIEW identities may later be retired/redirected; IDs are never renumbered."
    )
    candidate["person_id_registry"] = "data/ruler-person-id-registry.json"
    candidate["stable_id_stats"] = {
        "active_ids": len(used_ids),
        "issued_ids": len(entries),
        "next_sequence": next_sequence,
        "initial_freeze": initial_freeze,
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
        if extras or suppressed or canonical in metadata_by_canonical:
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

    _assign_stable_person_ids(candidate)
    return candidate


# Monkey-patch the standard builder's runtime globals so all downstream matching,
# reports and manifests use the resolved identity layer without editing raw segments.
base.normalize_identity = normalize_identity
base.emit_person = emit_person
base.build_candidate_index = build_candidate_index


if __name__ == "__main__":
    base.main()
