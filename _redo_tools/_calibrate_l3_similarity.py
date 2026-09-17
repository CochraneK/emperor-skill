#!/usr/bin/env python3
"""Calibrate Nuwa L3 lexical-review thresholds from the current corpus.

Imports the production payload extractor and records the empirical upper tail of pair
similarities. This is diagnostic only; it does not flag or pass any Skill.
"""
from __future__ import annotations

import json
from pathlib import Path
import statistics

import _audit_l3_semantic_similarity as l3

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "l3-similarity-baseline.json"


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    xs = sorted(values)
    pos = (len(xs) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def main() -> None:
    docs = l3.collect()
    filtered = l3.remove_common_shingles(docs)
    rows = []
    for i, left in enumerate(docs):
        for right in docs[i + 1:]:
            j, c, overlap = l3.pair_metrics(filtered[left.path], filtered[right.path])
            if overlap < 30:
                continue
            rows.append({
                "left": left.path,
                "right": right.path,
                "same_dynasty": left.dynasty == right.dynasty,
                "jaccard": round(j, 6),
                "containment": round(c, 6),
                "overlap_shingles": overlap,
            })

    js = [r["jaccard"] for r in rows]
    cs = [r["containment"] for r in rows]
    by_j = sorted(rows, key=lambda r: (r["jaccard"], r["containment"], r["overlap_shingles"]), reverse=True)
    by_c = sorted(rows, key=lambda r: (r["containment"], r["jaccard"], r["overlap_shingles"]), reverse=True)

    doc = {
        "schema_version": "1.0",
        "status": "DIAGNOSTIC_BASELINE_NOT_QUALITY_VERDICT",
        "summary": {
            "packages": len(docs),
            "pairs_with_overlap_at_least_30": len(rows),
            "jaccard_max": max(js) if js else None,
            "jaccard_p95": percentile(js, 0.95),
            "jaccard_p99": percentile(js, 0.99),
            "jaccard_p995": percentile(js, 0.995),
            "containment_max": max(cs) if cs else None,
            "containment_p95": percentile(cs, 0.95),
            "containment_p99": percentile(cs, 0.99),
            "containment_p995": percentile(cs, 0.995),
            "jaccard_median": statistics.median(js) if js else None,
            "containment_median": statistics.median(cs) if cs else None,
        },
        "top_30_by_jaccard": by_j[:30],
        "top_30_by_containment": by_c[:30],
        "note": "Use this distribution to choose conservative REVIEW thresholds. Never translate a percentile directly into PASS/FAIL.",
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
