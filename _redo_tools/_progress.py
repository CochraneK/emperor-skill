# -*- coding: utf-8 -*-
"""盘点 emperor-skill 下 xia / shang 两个朝代目录的 nuwa 合规包现状。
合规口径：SKILL.md >1KB 且 references/research/01-06 六份齐全 且 scripts/quality_check.py 存在。
只读，不写任何文件。
"""
import sys
from pathlib import Path

ROOT = Path(r"D:/2026/WB项目/emperor-skill/skills")

def audit(d: Path):
    sk = d / "SKILL.md"
    sk_ok = sk.is_file() and sk.stat().st_size > 1024
    refs = list((d / "references" / "research").glob("0*.md")) if (d / "references" / "research").is_dir() else []
    ref_names = sorted(p.name for p in refs)
    need = ["01-writings.md", "02-conversations.md", "03-expression-dna.md",
            "04-external-views.md", "05-decisions.md", "06-timeline.md"]
    ref_ok = all(n in ref_names for n in need)
    qc_ok = (d / "scripts" / "quality_check.py").is_file()
    return sk_ok, len(ref_names), ref_ok, qc_ok, (sk.stat().st_size if sk.is_file() else 0)

for dynasty in ("xia", "shang"):
    base = ROOT / dynasty
    if not base.is_dir():
        print(f"[{dynasty}] 目录不存在：{base}")
        continue
    dirs = sorted([p for p in base.iterdir() if p.is_dir() and p.name.endswith("-perspective")])
    full, partial = [], []
    for d in dirs:
        sk_ok, nref, ref_ok, qc_ok, size = audit(d)
        ok = sk_ok and ref_ok and qc_ok
        (full if ok else partial).append((d.name, sk_ok, nref, ref_ok, qc_ok, size))
    print(f"\n===== {dynasty} =====")
    print(f"目录数 {len(dirs)} | 合规 {len(full)} | 不合规 {len(partial)}")
    if partial:
        print("--- 不合规明细 ---")
        for name, sk_ok, nref, ref_ok, qc_ok, size in partial:
            print(f"  {name}: SKILL={sk_ok}({size}B) refs={nref} refs_ok={ref_ok} qc={qc_ok}")
    print("--- 合规包名 ---")
    for name, *_ in full:
        print(f"  {name}")

allpkgs = []
for dynasty in ("xia", "shang"):
    base = ROOT / dynasty
    if base.is_dir():
        allpkgs += [p.name for p in base.iterdir() if p.is_dir() and p.name.endswith("-perspective")]
print(f"\n>>> xia+shang 合计 {len(allpkgs)} 个 -perspective 目录")
