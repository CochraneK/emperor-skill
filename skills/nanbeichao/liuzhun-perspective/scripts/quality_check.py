#!/usr/bin/env python3
"""Mechanical evidence-restraint checks for liuzhun-perspective."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
RESEARCH = ROOT / "references" / "research"
FILES = [
    "01-writings.md", "02-conversations.md", "03-expression-dna.md",
    "04-external-views.md", "05-decisions.md", "06-timeline.md",
]


def main() -> int:
    failures = []
    text = SKILL.read_text(encoding="utf-8") if SKILL.exists() else ""
    for token in [
        "evidence_level: LIMITED-EVIDENCE",
        "UNVERIFIED_PERSONAL_AUTHORSHIP",
        "STRUCTURALLY_UNOBSERVABLE",
        "## 诚实边界",
    ]:
        if token not in text:
            failures.append(f"missing evidence-restraint token: {token}")
    models = re.findall(r"(?m)^### 模型\d+[：:]", text)
    if not 1 <= len(models) <= 4:
        failures.append(f"expected restrained 1-4 models, found {len(models)}")
    for name in FILES:
        p = RESEARCH / name
        if not p.exists() or p.stat().st_size == 0:
            failures.append(f"missing/empty research file: {name}")
    if failures:
        print("FAIL")
        print("\n".join(f"- {x}" for x in failures))
        return 1
    print("PASS: mechanical LIMITED-EVIDENCE checks only; no semantic L3 verdict.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
