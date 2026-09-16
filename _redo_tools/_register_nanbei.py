# -*- coding: utf-8 -*-
"""把南北朝·南朝宋 8 个已合规的包登记进主仓 data/modules.json。
复用 _register_jin.py 的搬运逻辑。南朝宋 8 帝全部 6/6 已落盘并推送。
注：南北朝共享 dir=nanbeichao / module=nanbeichao-emperors / group=nanbeichao-main，
本批只登记南朝宋 8 帝；后续南齐/梁/陈/北朝批次继续往同一 module/group 累加，
统一登记扩展（people 累计 +N），module/group 仅在首次出现时新增。
"""
import os, re, json, shutil, datetime

ES = r"D:/2026/WB项目/emperor-skill/skills"
MJ = r"D:/2026/WB项目/蒸馏skill/.workbuddy/data/modules.json"
BK = r"D:/2026/WB项目/蒸馏skill/.workbuddy/backups"

TARGET = {
    "nanbeichao": {
        "module": "nanbeichao-emperors", "group": "nanbeichao-main",
        "name": "南北朝帝王", "order": 20,
        "desc": "南北朝帝王（420–589，南朝宋齐梁陈 + 北朝魏齐周）。 "
                "门阀与寒人、宗室相残、侯景之乱、南北对峙；"
                "继承与世系图谱，节点可点击查看帝王心智模型。",
    },
}

os.makedirs(BK, exist_ok=True)
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
bak = os.path.join(BK, f"modules.json.bak-{stamp}")
shutil.copy2(MJ, bak)
print("[backup]", bak)

data = json.load(open(MJ, encoding="utf-8"))
people = data["people"]

added_p, added_m, added_g = [], [], []
have_m = {m["id"] for m in data["modules"]}
have_g = {g["id"] for g in data["groups"]}

for dyn, cfg in TARGET.items():
    d = os.path.join(ES, dyn)
    if cfg["module"] not in have_m:
        data["modules"].append({
            "id": cfg["module"], "name": cfg["name"],
            "view": "relation-graph", "order": cfg["order"], "desc": cfg["desc"],
        })
        added_m.append(cfg["module"])
    if cfg["group"] not in have_g:
        data["groups"].append({
            "id": cfg["group"], "module": cfg["module"],
            "name": cfg["name"], "main": True, "order": 1,
        })
        added_g.append(cfg["group"])
    pkgs = sorted([p for p in os.listdir(d)
                   if os.path.exists(os.path.join(d, p, "SKILL.md"))])
    for p in pkgs:
        sk = os.path.join(d, p, "SKILL.md")
        t = open(sk, encoding="utf-8", errors="replace").read()
        m = re.search(r"^---\r?\n(.*?)\r?\n---", t, re.S | re.M)
        if not m:
            print("  !! 无 frontmatter:", p)
            continue
        fm = m.group(1)

        def g(k):
            r = re.search(r"^" + k + r":[ \t]*([^\r\n]*)", fm, re.M)
            return (r.group(1).strip() if r else "")

        mod = g("module") or cfg["module"]
        grp = g("group") or cfg["group"]
        tags_raw = g("tags")
        tags = [x.strip() for x in tags_raw.strip("[]").split(",") if x.strip()] if tags_raw else []
        people[p] = {"module": mod, "group": grp, "tags": tags}
        added_p.append(f"{dyn}/{p}  ({g('cn')})")

data["updated"] = datetime.datetime.now().strftime("%Y-%m-%d")
json.dump(data, open(MJ, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print(f"\n[modules] +{len(added_m)}  {added_m}")
print(f"[groups ] +{len(added_g)}  {added_g}")
print(f"[people ] +{len(added_p)}  （原 {len(people) - len(added_p)} → 现 {len(people)}）")
for x in added_p:
    print("    " + x)
