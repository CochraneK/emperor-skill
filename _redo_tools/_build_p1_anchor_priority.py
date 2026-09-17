#!/usr/bin/env python3
"""Build the P1 high-leverage anchor review queue and reviewed ranking.

P1 is a work-scheduling layer, not a judgment of historical worth. Machine signals only
order the review queue. Final anchor scores exist only after all policy dimensions have
explicit evidence-backed reviews in data/p1-anchor-reviews.json.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSESSMENT = ROOT / "assessment"
PRIORITY = DATA / "distillation-priority.json"
POLICY = DATA / "p1-anchor-scoring-policy.json"
REVIEWS = DATA / "p1-anchor-reviews.json"
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


def validate_review(
    row: dict[str, Any],
    candidate_by_id: dict[str, dict[str, Any]],
    dimensions: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    pid = str(row.get("person_id", ""))
    if pid not in candidate_by_id:
        errors.append(f"unknown/non-P1 person_id: {pid!r}")
        return None, errors

    scores = row.get("scores") or {}
    rationales = row.get("rationales") or {}
    weighted = 0.0
    for dim in dimensions:
        did = dim["id"]
        score = scores.get(did)
        if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 3:
            errors.append(f"{pid}: {did} must be integer 0..3")
            continue
        rationale = str(rationales.get(did, "")).strip()
        if not rationale:
            errors.append(f"{pid}: {did} requires rationale")
        weighted += score * float(dim["weight"])

    if errors:
        return None, errors

    candidate = candidate_by_id[pid]
    canonical = candidate.get("canonical_name")
    supplied = row.get("canonical_name")
    if supplied and supplied != canonical:
        errors.append(f"{pid}: canonical_name mismatch {supplied!r} != {canonical!r}")
        return None, errors

    return {
        "person_id": pid,
        "canonical_name": canonical,
        "polities": candidate.get("polities", []),
        "source_files": candidate.get("source_files", []),
        "scores": {dim["id"]: scores[dim["id"]] for dim in dimensions},
        "rationales": {dim["id"]: str(rationales[dim["id"]]).strip() for dim in dimensions},
        "scheduling_score": round(weighted, int(load(POLICY)["ranking"].get("precision", 3))),
        "evidence_notes": row.get("evidence_notes", []),
        "reviewed_by": row.get("reviewed_by"),
        "reviewed_on": row.get("reviewed_on"),
        "status": "REVIEWED",
    }, []


def build_review_queue(
    candidates: list[dict[str, Any]],
    reviewed_ids: set[str],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    polity_counts = Counter(
        polity
        for row in candidates
        for polity in (row.get("polities") or ["UNSPECIFIED"])
    )
    by_polity: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in candidates:
        if row["person_id"] in reviewed_ids:
            continue
        polities = row.get("polities") or ["UNSPECIFIED"]
        for polity in polities:
            by_polity[polity].append(row)

    for polity, rows in by_polity.items():
        rows.sort(key=lambda r: (-len(r.get("polities") or []), pid_number(r["person_id"]), r["canonical_name"]))

    polity_order = sorted(by_polity, key=lambda p: (-polity_counts[p], p))
    queues = {p: deque(by_polity[p]) for p in polity_order}
    seen: set[str] = set()
    out: list[dict[str, Any]] = []

    while True:
        progressed = False
        for polity in polity_order:
            q = queues[polity]
            while q and q[0]["person_id"] in seen:
                q.popleft()
            if not q:
                continue
            row = q.popleft()
            pid = row["person_id"]
            if pid in seen:
                continue
            seen.add(pid)
            progressed = True
            polities = row.get("polities") or []
            counts = {p: polity_counts[p] for p in polities}
            out.append({
                "review_order": len(out) + 1,
                "person_id": pid,
                "canonical_name": row["canonical_name"],
                "polities": polities,
                "source_files": row.get("source_files", []),
                "machine_context": {
                    "p1_missing_candidates_by_person_polity": counts,
                    "polity_membership_count": len(polities),
                    "screening_reason": "Round-robin across uncovered polities; machine context orders review only and is not an anchor score."
                },
                "status": "NEEDS_REVIEW"
            })
        if not progressed:
            break

    return out, dict(sorted(polity_counts.items()))


def build() -> dict[str, Any]:
    priority = load(PRIORITY)
    policy = load(POLICY)
    review_doc = load(REVIEWS)

    p0_missing = priority["summary"]["p0_backbone_missing"]
    if p0_missing != 0:
        raise RuntimeError(f"P1 cannot run while P0 missing={p0_missing}")

    candidates = priority["p1_high_leverage_anchors"]["candidate_pool"]
    candidate_by_id = {str(r["person_id"]): r for r in candidates}
    dimensions = policy["dimensions"]

    valid_reviews: list[dict[str, Any]] = []
    review_errors: list[str] = []
    duplicate_ids: set[str] = set()
    seen_review_ids: set[str] = set()
    for row in review_doc.get("reviews", []):
        pid = str(row.get("person_id", ""))
        if pid in seen_review_ids:
            duplicate_ids.add(pid)
            continue
        seen_review_ids.add(pid)
        normalized, errors = validate_review(row, candidate_by_id, dimensions)
        review_errors.extend(errors)
        if normalized:
            valid_reviews.append(normalized)
    if duplicate_ids:
        review_errors.append("duplicate review person_ids: " + ", ".join(sorted(duplicate_ids)))
    if review_errors:
        raise RuntimeError("Invalid P1 review registry:\n- " + "\n- ".join(review_errors))

    weights = {d["id"]: float(d["weight"]) for d in dimensions}
    rank_dims = [d["id"] for d in dimensions]
    valid_reviews.sort(
        key=lambda r: (
            -r["scheduling_score"],
            -r["scores"].get("structural_coverage_gain", 0),
            -r["scores"].get("transition_leverage", 0),
            -r["scores"].get("evidence_readiness", 0),
            pid_number(r["person_id"]),
        )
    )
    for i, row in enumerate(valid_reviews, 1):
        row["rank"] = i

    reviewed_ids = {r["person_id"] for r in valid_reviews}
    review_queue, polity_counts = build_review_queue(candidates, reviewed_ids)

    tranche_target = int(policy["selection"]["initial_anchor_tranche_target"])
    min_diversity = int(policy["selection"]["minimum_cross_polity_diversity"])
    selected = valid_reviews[:tranche_target]
    selected_polities = sorted({p for r in selected for p in r.get("polities", [])})
    tranche_ready = len(selected) >= tranche_target and len(selected_polities) >= min_diversity

    return {
        "schema_version": "1.0",
        "status": "READY_TO_DISTILL_INITIAL_TRANCHE" if tranche_ready else "REVIEW_IN_PROGRESS",
        "policy_file": str(POLICY.relative_to(ROOT)).replace("\\", "/"),
        "review_file": str(REVIEWS.relative_to(ROOT)).replace("\\", "/"),
        "source_priority_file": str(PRIORITY.relative_to(ROOT)).replace("\\", "/"),
        "warning": "P1 ordering is project scheduling only; never interpret it as historical worth or Nuwa quality.",
        "summary": {
            "p0_missing": p0_missing,
            "candidate_pool": len(candidates),
            "reviewed_complete": len(valid_reviews),
            "needs_review": len(review_queue),
            "initial_anchor_tranche_target": tranche_target,
            "initial_anchor_tranche_selected": len(selected) if tranche_ready else 0,
            "minimum_cross_polity_diversity": min_diversity,
            "selected_polity_diversity": len(selected_polities) if tranche_ready else 0,
            "reviewed_dimensions": rank_dims,
            "weights": weights,
        },
        "polity_candidate_counts": polity_counts,
        "ranked_reviewed_candidates": valid_reviews,
        "initial_anchor_tranche": selected if tranche_ready else [],
        "review_queue": review_queue,
    }


def write_report(doc: dict[str, Any]) -> None:
    s = doc["summary"]
    lines = [
        "# P1 Anchor Priority",
        "",
        "> Scheduling priority for post-Qin CORE research/distillation. This is **not** a ranking of historical worth, legitimacy, morality, ethnicity, or ruler quality.",
        "",
        "## State",
        "",
        f"- Status: **{doc['status']}**",
        f"- P0 missing: **{s['p0_missing']}**",
        f"- P1 candidate pool: **{s['candidate_pool']}**",
        f"- Fully reviewed: **{s['reviewed_complete']}**",
        f"- Needs review: **{s['needs_review']}**",
        f"- Initial anchor target: **{s['initial_anchor_tranche_target']}**",
        "",
        "## Method",
        "",
        "All five policy dimensions require explicit 0–3 review plus rationale. Machine signals only diversify and order the review queue; they never become historical or quality scores.",
        "",
        "## Reviewed ranking",
        "",
        "| Rank | Person | Polity | Scheduling score |",
        "|---:|---|---|---:|",
    ]
    for row in doc["ranked_reviewed_candidates"]:
        lines.append(f"| {row['rank']} | {row['canonical_name']} | {' / '.join(row['polities'])} | {row['scheduling_score']:.3f} |")
    if not doc["ranked_reviewed_candidates"]:
        lines.append("| — | No complete reviews yet | — | — |")

    lines += ["", "## Next review slate", ""]
    for row in doc["review_queue"][:30]:
        polities = " / ".join(row.get("polities") or ["—"])
        lines.append(f"- {row['review_order']}. **{row['canonical_name']}** · {polities} · `{row['person_id']}`")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    doc = build()
    dump(OUT, doc)
    write_report(doc)
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
