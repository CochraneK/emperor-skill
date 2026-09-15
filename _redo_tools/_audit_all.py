# -*- coding: utf-8 -*-
"""全仓审计：emperor-skill/skills 下所有朝代的所有 -perspective 包。
合规口径：SKILL.md >1KB 且 references/research/01-06 六份齐全 且 scripts/quality_check.py 存在。
另：定位「宣王」相关目录（用于判定周宣王是否为僵尸任务）。
只读。报告同时写 UTF-8 到 _audit_all.txt。
"""
import re
from pathlib import Path

_BUF = []
_op = print


def print(*a, **k):  # noqa: A001
    _BUF.append(" ".join(str(x) for x in a))
    _op(*a, **k)


ROOT = Path(r"D:/2026/WB项目/emperor-skill/skills")
NEED = ["01-writings.md", "02-conversations.md", "03-expression-dna.md",
        "04-external-views.md", "05-decisions.md", "06-timeline.md"]

pkgs = sorted(p for p in ROOT.rglob("*-perspective") if p.is_dir())
by_dyn = {}
for p in pkgs:
    dyn = p.parent.relative_to(ROOT).as_posix()
    by_dyn.setdefault(dyn, []).append(p)

bad = []
grand = 0
print(f"=== 全仓审计 ===  根目录 {ROOT}")
for dyn in sorted(by_dyn):
    lst = by_dyn[dyn]
    grand += len(lst)
    ok = 0
    for p in lst:
        sk = p / "SKILL.md"
        sk_ok = sk.is_file() and sk.stat().st_size > 1024
        rdir = p / "references" / "research"
        ref_ok = all((rdir / n).is_file() for n in NEED)
        qc_ok = (p / "scripts" / "quality_check.py").is_file()
        if sk_ok and ref_ok and qc_ok:
            ok += 1
        else:
            missing = []
            if not sk_ok:
                missing.append("SKILL")
            if not ref_ok:
                missing.append("refs")
            if not qc_ok:
                missing.append("qc")
            bad.append((dyn, p.name, ",".join(missing)))
    print(f"  {dyn:<28} {len(lst):>3} 包 | 合规 {ok:>3} | 不合规 {len(lst)-ok}")

print(f"\n>>> 全仓 -perspective 包总数 {grand} | 合规 {grand-len(bad)} | 不合规 {len(bad)}")
if bad:
    print("--- 不合规清单 ---")
    for dyn, name, miss in bad:
        print(f"  {dyn}/{name}  缺: {miss}")

print("\n=== 「宣王」相关目录检索 ===")
hits = [p for p in pkgs if "xuanwang" in p.name.lower() or "宣" in p.name]
if hits:
    for p in hits:
        print("  " + p.relative_to(ROOT).as_posix())
else:
    print("  （skills 下无任何名称含 xuanwang / 宣 的 -perspective 目录）")

print("\n=== 周代（zhou）目录逐条 ===")
z = ROOT / "zhou"
if z.is_dir():
    for p in sorted(x for x in z.iterdir() if x.is_dir()):
        sk = p / "SKILL.md"
        print(f"  {p.name:<34} SKILL={'Y' if sk.is_file() else 'N'} ({(sk.stat().st_size if sk.is_file() else 0)}B)")
else:
    print("  无 zhou 目录")

Path(r"D:/2026/WB项目/emperor-skill/_redo_tools/_audit_all.txt").write_text("\n".join(_BUF), encoding="utf-8")
