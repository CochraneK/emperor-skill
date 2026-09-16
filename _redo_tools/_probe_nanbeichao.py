# -*- coding: utf-8 -*-
"""探测主仓 modules.json 中 nanbeichao 相关条目的确切结构（只打印，不修改）"""
import json, pathlib
MS = pathlib.Path(r"D:/2026/WB项目/蒸馏skill")
p = MS / ".workbuddy/data/modules.json"
d = json.loads(p.read_text(encoding="utf-8"))
out = []
def w(s=""): out.append(str(s))
w("== people['yuanziyou-perspective'] ==")
w(json.dumps(d["people"].get("yuanziyou-perspective"), ensure_ascii=False, indent=2))
w("")
w("== people 是否已含 yuanye ==")
w(str("yuanye-perspective" in d["people"]))
w("")
w("== modules 中 nanbeichao ==")
for m in d["modules"]:
    if "nanbeichao" in json.dumps(m, ensure_ascii=False):
        w(json.dumps(m, ensure_ascii=False, indent=2))
w("")
w("== groups 中 nanbeichao ==")
for g in d["groups"]:
    if "nanbeichao" in json.dumps(g, ensure_ascii=False):
        w(json.dumps(g, ensure_ascii=False, indent=2))
w("")
w("== people 值字段并集（前 200 个键）==")
keys = set()
for k, v in list(d["people"].items())[:200]:
    if isinstance(v, dict):
        keys |= set(v.keys())
w(str(sorted(keys)))
(MS / ".workbuddy/data/_probe_nanbeichao.txt").write_text("\n".join(out), encoding="utf-8")
print("OK")
