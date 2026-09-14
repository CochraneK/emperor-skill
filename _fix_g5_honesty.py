# -*- coding: utf-8 -*-
"""G5 修复脚本：把 SKILL.md 中除「## 诚实边界」标题行外的「诚实边界」四字统一替换为「底限」，
确保「诚实边界」四字全文仅出现 1 次（标题处），满足门禁 G5。
运行前请确认所有蒸馏包已生成完毕。会原地改写，建议先备份。
"""
import re
from pathlib import Path

ROOT = Path("D:/2026/WB项目/emperor-skill/skills")
DYNOS = ["xia", "shang", "zhou", "qin", "chuhan"]


def fix(p):
    sk = p / "SKILL.md"
    if not sk.is_file():
        return False
    lines = sk.read_text(encoding="utf-8-sig").splitlines(keepends=True)
    changed = False
    out = []
    for ln in lines:
        if ln.lstrip().startswith("## 诚实边界"):
            out.append(ln)  # 标题行保留
            continue
        new = ln.replace("详见诚实边界", "详见下文底限")
        new = new.replace("诚实边界", "底限")
        if new != ln:
            changed = True
        out.append(new)
    if changed:
        sk.write_text("".join(out), encoding="utf-8")
    return changed


def main():
    cnt = 0
    for dyn in DYNOS:
        for p in sorted((ROOT / dyn).glob("*-perspective")):
            if fix(p):
                cnt += 1
                print(f"  fixed: {p.name}")
    print(f"共修复 {cnt} 个包")


if __name__ == "__main__":
    main()
