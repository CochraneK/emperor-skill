#!/usr/bin/env python3
"""Mechanical checks for Liu Yi LIMITED-EVIDENCE package.

Unlike ordinary emperor packages, fewer than six mental models is intentional here.
The checker guards evidence restraint rather than rewarding artificial completeness.
"""
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
    fail = []
    text = SKILL.read_text(encoding="utf-8") if SKILL.exists() else ""
    if not text:
        fail.append("missing SKILL.md")
    else:
        for token in [
            "evidence_level: LIMITED-EVIDENCE",
            "STRUCTURALLY_UNOBSERVABLE",
            "UNKNOWN_NOT_RECORDED",
            "## 诚实边界",
        ]:
            if token not in text:
                fail.append(f"missing evidence-boundary token: {token}")
        models = re.findall(r"(?m)^### 模型\d+[：:]", text)
        if not 1 <= len(models) <= 4:
            fail.append(f"limited-evidence package should use 1-4 justified models, found {len(models)}")
        if "六条人格心智模型" not in text:
            fail.append("missing explicit no-six-model-padding statement")

    for name in FILES:
        p = RESEARCH / name
        if not p.exists() or p.stat().st_size == 0:
            fail.append(f"missing/empty research file: {name}")

    if fail:
        print("FAIL")
        print("\n".join(f"- {x}" for x in fail))
        return 1
    print("PASS: LIMITED-EVIDENCE restraint preserved; this is not an L3 verdict.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
