#!/usr/bin/env python3
"""Local L4/evidence-structure checks for wangmang-perspective.

This script cannot certify Nuwa L3 semantic quality. It only catches mechanical package
regressions and obvious evidence-structure omissions.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
RESEARCH = ROOT / "references" / "research"
REQUIRED_RESEARCH = [
    "01-writings.md",
    "02-conversations.md",
    "03-expression-dna.md",
    "04-external-views.md",
    "05-decisions.md",
    "06-timeline.md",
]
REQUIRED_FRONTMATTER = [
    "name", "description", "cn", "en", "type", "domain", "era", "module", "group", "tags"
]


def main() -> int:
    failures: list[str] = []
    if not SKILL.exists():
        failures.append("missing SKILL.md")
        text = ""
    else:
        text = SKILL.read_text(encoding="utf-8")

    if text:
        if not text.startswith("---\n"):
            failures.append("frontmatter missing")
        else:
            end = text.find("\n---", 4)
            fm = text[4:end] if end >= 0 else ""
            for key in REQUIRED_FRONTMATTER:
                if not re.search(rf"(?m)^{re.escape(key)}:\s*\S", fm):
                    failures.append(f"frontmatter field missing: {key}")

        models = re.findall(r"(?m)^### 模型\d+[：:]", text)
        if len(models) != 6:
            failures.append(f"expected 6 core models, found {len(models)}")

        for heading in ["## 反模式", "## 时间线", "## 调研来源", "## 诚实边界", "## 表达DNA"]:
            if heading not in text:
                failures.append(f"missing section: {heading}")

        if text.count("## 诚实边界") != 1:
            failures.append("诚实边界 must occur exactly once as H2")

        if "框架推断" not in text:
            failures.append("missing explicit framework-inference boundary")
        if "现代研究" not in text or "传世史料" not in text:
            failures.append("evidence taxonomy not explicit")

    for name in REQUIRED_RESEARCH:
        path = RESEARCH / name
        if not path.exists():
            failures.append(f"missing research file: {name}")
        elif path.stat().st_size == 0:
            failures.append(f"empty research file: {name}")

    if failures:
        print("FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("PASS: mechanical package checks only; semantic L3 still requires Nuwa review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
