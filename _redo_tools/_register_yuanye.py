# -*- coding: utf-8 -*-
"""把 yuanye-perspective 登记进主仓 modules.json 的 people（插在 yuanziyou 之后，保持北魏时间序）"""
import json, pathlib, collections
MS = pathlib.Path(r"D:/2026/WB项目/蒸馏skill")
p = MS / ".workbuddy/data/modules.json"
d = json.loads(p.read_text(encoding="utf-8"), object_pairs_hook=collections.OrderedDict)
people = d["people"]
assert "yuanye-perspective" not in people, "已登记过 yuanye"
before = len(people)

entry = collections.OrderedDict([
    ("module", "nanbeichao-emperors"),
    ("group", "nanbeichao-main"),
    ("tags", ["北朝", "北魏", "帝王", "长广王", "元晔", "尔朱氏", "傀儡"]),
])

new = collections.OrderedDict()
inserted = False
for k, v in people.items():
    new[k] = v
    if k == "yuanziyou-perspective":
        new["yuanye-perspective"] = entry
        inserted = True
if not inserted:                      # 兜底：找不到锚点就追加
    new["yuanye-perspective"] = entry
d["people"] = new
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# 回填校验
d2 = json.loads(p.read_text(encoding="utf-8"))
after = len(d2["people"])
assert after == before + 1, f"人数异常 {before}->{after}"
assert d2["people"]["yuanye-perspective"]["module"] == "nanbeichao-emperors"
nb = [k for k, v in d2["people"].items() if isinstance(v, dict) and v.get("module") == "nanbeichao-emperors"]
print(f"people {before} -> {after}")
print(f"nanbeichao-emperors 人数: {len(nb)}")
print("北魏末段顺序（尾部 4 个）:", nb[-4:])
