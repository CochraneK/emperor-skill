# -*- coding: utf-8 -*-
"""把北朝第二批·北魏5帝登记进主仓 data/modules.json 的 nanbeichao-emperors 模块。"""
import os, re, json, shutil, datetime

ES = r"D:/2026/WB项目/emperor-skill/skills"
MJ = r"D:/2026/WB项目/蒸馏skill/.workbuddy/data/modules.json"
BK = r"D:/2026/WB项目/蒸馏skill/.workbuddy/backups"

NEW = ["tuobahong", "yuanhong", "yuanke", "yuanxu", "yuanziyou"]

os.makedirs(BK, exist_ok=True)
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
bak = os.path.join(BK, f"modules.json.bak-{stamp}")
shutil.copy2(MJ, bak)
print("[backup]", bak)

data = json.load(open(MJ, encoding="utf-8"))
people = data["people"]
before = len(people)
added = []
for sid in NEW:
    p = sid + "-perspective"; key = p
    if key in people:
        print("  跳过已存在:", key); continue
    sk = os.path.join(ES, "nanbeichao", p, "SKILL.md")
    if not os.path.isfile(sk):
        print("  !! 缺包:", sk); continue
    t = open(sk, encoding="utf-8", errors="replace").read()
    m = re.search(r"^---\r?\n(.*?)\r?\n---", t, re.S | re.M); fm = m.group(1) if m else ""
    def g(k):
        r = re.search(r"^" + k + r":[ \t]*([^\r\n]*)", fm, re.M)
        return (r.group(1).strip() if r else "")
    mod = g("module") or "nanbeichao-emperors"; grp = g("group") or "nanbeichao-main"
    tags_raw = g("tags")
    tags = [x.strip() for x in tags_raw.strip("[]").split(",") if x.strip()] if tags_raw else []
    people[key] = {"module": mod, "group": grp, "tags": tags}
    added.append(f"nanbeichao/{p}  ({g('cn')})")

data["updated"] = datetime.datetime.now().strftime("%Y-%m-%d")
json.dump(data, open(MJ, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n[people] +{len(added)}  （原 {before} → 现 {len(people)}）")
for x in added:
    print("    " + x)
