#!/usr/bin/env python3
"""Mechanical MODERATE-EVIDENCE checks for yuanxiu-perspective."""
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
        "evidence_level: MODERATE-EVIDENCE",
        "DIRECT_SPEECH_SUPPORTED",
        "NOT_SCORED",
        "受限表达 DNA",
        "名义主权",
        "高欢",
        "宇文泰",
        "## 诚实边界",
        "框架推断",
    ]:
        if token not in text:
            failures.append(f"missing evidence-boundary token: {token}")
    models = re.findall(r"(?m)^### 模型\d+[：:]", text)
    if not 4 <= len(models) <= 7:
        failures.append(f"expected evidence-supported 4-7 models, found {len(models)}")
    for quote in ["非卖我耶", "不得不称朕"]:
        if quote not in text:
            failures.append(f"missing direct-speech anchor: {quote}")
    for name in FILES:
        p = RESEARCH / name
        if not p.exists() or p.stat().st_size == 0:
            failures.append(f"missing/empty research file: {name}")
    if failures:
        print("FAIL")
        print("\n".join(f"- {x}" for x in failures))
        return 1
    print("PASS: mechanical MODERATE-EVIDENCE checks only; no semantic L3 verdict.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
