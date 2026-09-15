# -*- coding: utf-8 -*-
"""覆盖度盘点：
1) emperor-skill/skills 下各朝代包名（看缺哪些帝王）
2) 主仓 data/modules.json 的 people 登记情况（看哪些包有包但没上架）
"""
import os, json, re, collections

ES = r"D:/2026/WB项目/emperor-skill/skills"
MJ = r"D:/2026/WB项目/蒸馏skill/.workbuddy/data/modules.json"
OUT = r"D:/2026/WB项目/emperor-skill/_redo_tools/_coverage.txt"

BUF = []
def w(s=""):
    BUF.append(s)

# ---------- 1) 各朝代包清单 ----------
CN = {}
for dyn in sorted(os.listdir(ES)):
    d = os.path.join(ES, dyn)
    if not os.path.isdir(d):
        continue
    pkgs = sorted(p for p in os.listdir(d) if os.path.isdir(os.path.join(d, p)))
    CN[dyn] = pkgs
    names = []
    for p in pkgs:
        sk = os.path.join(d, p, "SKILL.md")
        cn = ""
        if os.path.exists(sk):
            m = re.search(r"^cn:\s*(.+?)\s*$", open(sk, encoding="utf-8", errors="replace").read(), re.M)
            if m:
                cn = m.group(1).strip()
        names.append(cn or "?")
    w(f"### {dyn}  ({len(pkgs)} 包)")
    w("    " + "、".join(names))
    w()

w("=" * 90)
w("合计 " + str(sum(len(v) for v in CN.values())) + " 包")
w()

# ---------- 2) modules.json 登记情况 ----------
data = json.load(open(MJ, encoding="utf-8"))
people = data.get("people", [])
w(f"modules.json people 类型: {type(people).__name__}, 条目数 {len(people)}")

has = set()
if isinstance(people, dict):
    has = set(people.keys())
    sample = list(people.items())[:2]
else:
    for p in people:
        if isinstance(p, str):
            has.add(p)
        elif isinstance(p, dict):
            sid = p.get("id") or p.get("skill_id") or p.get("name")
            if sid:
                has.add(sid)
    sample = [(x, None) for x in list(has)[:2]]
w(f"--- people 样例 ---")
for k, v in sample:
    w(f"    {k}  ->  {str(v)[:160]}")
w()

# 未登记的帝王包
w()
w("--- 有包但未登记进 people 的包（站点不会显示） ---")
missing = []
for dyn, pkgs in CN.items():
    for p in pkgs:
        key = p.replace("-perspective", "")
        if p not in has and key not in has:
            missing.append(f"{dyn}/{p}")
w(f"  共 {len(missing)} 个")
for m in missing:
    w("    " + m)

open(OUT, "w", encoding="utf-8").write("\n".join(BUF))
print("written", OUT, len(BUF), "lines")
