# -*- coding: utf-8 -*-
"""登记西汉以前 90 位帝王包到主仓 modules.json（people/modules/groups），供外挂站点 build 展示。
只增不删：读取现有 modules.json，追加 xia/shang/zhou/qin/chuhan 五模块与 90 个 people 条目。
"""
import json, re, os
from pathlib import Path

MAIN = Path("D:/2026/WB项目/蒸馏skill/.workbuddy/data/modules.json")
EMP = Path("D:/2026/WB项目/emperor-skill/skills")
PRE = ["xia", "shang", "zhou", "qin", "chuhan"]

# 模块定义（view 沿用帝王 relation-graph；order 接在既有帝王模块之后）
MODULE_DEFS = {
    "xia-emperors":   {"id": "xia-emperors",   "name": "夏朝帝王",     "view": "relation-graph", "order": 10, "desc": "夏朝 17 王（约前2070–前1600）。传说与考古并存的早期王朝，二里头文化为可能对应；继承与世系图谱，节点可点击查看帝王心智模型。"},
    "shang-emperors": {"id": "shang-emperors", "name": "商朝帝王",     "view": "relation-graph", "order": 11, "desc": "商朝 31 王（约前1600–前1046）。早商半信史、晚商甲骨文信史；继承与世系图谱，节点可点击查看帝王心智模型。"},
    "zhou-emperors":  {"id": "zhou-emperors",  "name": "周朝帝王",     "view": "relation-graph", "order": 12, "desc": "周朝 37 王（前1046–前256，西周12·东周25）。分封与礼崩乐坏之世；继承与世系图谱，节点可点击查看帝王心智模型。"},
    "qin-emperors":   {"id": "qin-emperors",   "name": "秦朝帝王",     "view": "relation-graph", "order": 13, "desc": "秦 3 王（前221–前207）。始皇一统、二世而亡；继承与世系图谱，节点可点击查看帝王心智模型。"},
    "chuhan-emperors":{"id": "chuhan-emperors","name": "楚汉帝王",     "view": "relation-graph", "order": 14, "desc": "楚汉 2 王（前206–前202）。项羽（西楚霸王）与义帝（熊心）；秦汉之际的霸业与短祚，节点可点击查看帝王心智模型。"},
}
GROUP_DEFS = [
    {"id": "xia-main",        "module": "xia-emperors",   "name": "夏朝帝王",     "main": True, "order": 1},
    {"id": "shang-main",      "module": "shang-emperors", "name": "商朝帝王",     "main": True, "order": 1},
    {"id": "zhou-west-main",  "module": "zhou-emperors",  "name": "西周帝王",     "main": True, "order": 1},
    {"id": "zhou-east-main",  "module": "zhou-emperors",  "name": "东周帝王",     "main": True, "order": 2},
    {"id": "qin-main",        "module": "qin-emperors",   "name": "秦朝帝王",     "main": True, "order": 1},
    {"id": "chuhan-main",     "module": "chuhan-emperors","name": "楚汉帝王",     "main": True, "order": 1},
]


def parse_front(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    data = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data


def parse_list(s):
    # tags 形如 [a, b, c]
    s = s.strip()
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
    return [s]


def main():
    cfg = json.loads(MAIN.read_text(encoding="utf-8-sig"))
    people = cfg.setdefault("people", {})
    modules = cfg.setdefault("modules", [])
    groups = cfg.setdefault("groups", [])

    added_people = 0
    for dyn in PRE:
        base = EMP / dyn
        if not base.is_dir():
            continue
        for sk in sorted(base.glob("*-perspective")):
            fm = parse_front((sk / "SKILL.md").read_text(encoding="utf-8-sig"))
            sid = fm.get("name")
            if not sid or not sid.endswith("-perspective"):
                continue
            if sid in people:
                continue
            people[sid] = {
                "module": fm.get("module", ""),
                "group": fm.get("group", ""),
                "tags": parse_list(fm.get("tags", "[]")),
            }
            added_people += 1

    added_modules = 0
    existing_mods = {m["id"] for m in modules}
    for mid, mdef in MODULE_DEFS.items():
        if mid not in existing_mods:
            modules.append(mdef)
            added_modules += 1

    added_groups = 0
    existing_grps = {g["id"] for g in groups}
    for gdef in GROUP_DEFS:
        if gdef["id"] not in existing_grps:
            groups.append(gdef)
            added_groups += 1

    MAIN.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"新增 people 条目: {added_people}")
    print(f"新增 modules: {added_modules} -> {[m for m in MODULE_DEFS if m not in existing_mods]}")
    print(f"新增 groups: {added_groups} -> {[g['id'] for g in GROUP_DEFS if g['id'] not in existing_grps]}")
    print(f"people 总条目: {len(people)}")
    print(f"modules 总数: {len(modules)}")
    print(f"groups 总数: {len(groups)}")


if __name__ == "__main__":
    main()
