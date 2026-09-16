# -*- coding: utf-8 -*-
"""全仓覆盖度汇总：按朝代目录统计帝王包数 + 合规数 + 主仓 people 数。"""
import os, json

ES = r"D:/2026/WB项目/emperor-skill/skills"
MJ = r"D:/2026/WB项目/蒸馏skill/.workbuddy/data/modules.json"
EXPECT = 8  # SKILL.md + 6 research + quality_check.py

CN = {
    "xia": "夏", "shang": "商", "zhou": "西周/东周", "qin": "秦", "chuhan": "楚汉",
    "xihan": "西汉", "donghan": "东汉", "sanguo": "三国", "jin": "两晋",
    "nanbeichao": "南北朝", "sui": "隋", "tang": "唐", "song": "宋",
    "yuan": "元", "ming": "明", "qing": "清",
}

print("== emperor-skill 各朝代目录包数 / 合规 ==")
total = 0
ok_total = 0
rows = []
for d in sorted(os.listdir(ES)):
    dd = os.path.join(ES, d)
    if not os.path.isdir(dd):
        continue
    pkgs = [p for p in os.listdir(dd) if os.path.isdir(os.path.join(dd, p))]
    n = len(pkgs)
    ok = 0
    for p in pkgs:
        pd = os.path.join(dd, p)
        files = sum(len(fs) for _, _, fs in os.walk(pd))
        if files == EXPECT:
            ok += 1
    total += n
    ok_total += ok
    rows.append((d, CN.get(d, d), n, ok))
    print(f"  {d:<12} {CN.get(d,d):<10} {n:>3} 包  (合规 {ok})")
print(f"\n合计: {total} 包，合规 {ok_total}")

d = json.load(open(MJ, encoding="utf-8"))
people = d["people"]
print(f"\n== 主仓 modules.json ==")
print("  people:", len(people))
mods = {}
for k, v in people.items():
    mods[v.get("module", "?")] = mods.get(v.get("module", "?"), 0) + 1
for m in sorted(mods):
    print(f"    {m:<26} {mods[m]}")
