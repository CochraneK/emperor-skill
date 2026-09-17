#!/usr/bin/env python3
"""Mechanical evidence-restraint checks for yuanlang-perspective."""
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
        "evidence_level: PARTIAL-EVIDENCE",
        "ATTRIBUTION_UNCERTAIN",
        "LOW_EVIDENCE",
        "不建立完整个人表达 DNA",
        "## 诚实边界",
        "框架推断",
    ]:
        if token not in text:
            failures.append(f"missing evidence-restraint token: {token}")
    models = re.findall(r"(?m)^### 模型\d+[：:]", text)
    if not 2 <= len(models) <= 5:
        failures.append(f"expected restrained 2-5 models, found {len(models)}")
    if "少称明悟" not in text:
        failures.append("missing preserved historiographical characterization")
    if "高欢" not in text:
        failures.append("missing effective-actor attribution")
    for name in FILES:
        p = RESEARCH / name
        if not p.exists() or p.stat().st_size == 0:
            failures.append(f"missing/empty research file: {name}")
    if failures:
        print("FAIL")
        print("\n".join(f"- {x}" for x in failures))
        return 1
    print("PASS: mechanical PARTIAL-EVIDENCE checks only; no semantic L3 verdict.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
