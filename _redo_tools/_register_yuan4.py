# -*- coding: utf-8 -*-
"""补登记元前四汗（太祖铁木真/太宗窝阔台/定宗贵由/宪宗蒙哥）进主仓 yuan-emperors 模块。
此前已 push emperor-skill 但漏登记，导致站点 yuan-emperors 只有 11 人（应 15）。
"""
import os, re, json, shutil, datetime

ES = r"D:/2026/WB项目/emperor-skill/skills/yuan"
MJ = r"D:/2026/WB项目/蒸馏skill/.workbuddy/data/modules.json"
BK = r"D:/2026/WB项目/蒸馏skill/.workbuddy/backups"

NEW = ["temujin", "ogodei", "guyuk", "mongke"]

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
    sk = os.path.join(ES, p, "SKILL.md")
    if not os.path.isfile(sk):
        print("  !! 缺包:", sk); continue
    t = open(sk, encoding="utf-8", errors="replace").read()
    m = re.search(r"^---\r?\n(.*?)\r?\n---", t, re.S | re.M); fm = m.group(1) if m else ""
    def g(k):
        r = re.search(r"^" + k + r":[ \t]*([^\r\n]*)", fm, re.M)
        return (r.group(1).strip() if r else "")
    mod = g("module") or "yuan-emperors"; grp = g("group") or "yuan-main"
    tags_raw = g("tags")
    tags = [x.strip() for x in tags_raw.strip("[]").split(",") if x.strip()] if tags_raw else []
    people[key] = {"module": mod, "group": grp, "tags": tags}
    added.append(f"yuan/{p}  ({g('cn')})")

data["updated"] = datetime.datetime.now().strftime("%Y-%m-%d")
json.dump(data, open(MJ, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n[people] +{len(added)}  （原 {before} → 现 {len(people)}）")
for x in added:
    print("    " + x)
