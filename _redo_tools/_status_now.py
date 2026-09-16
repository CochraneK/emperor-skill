# -*- coding: utf-8 -*-
"""只读盘点：emperor-skill 包数 / _pending 暂存 / 主仓 people 数。输出落盘 _status_now.txt"""
import json, pathlib, re

ES = pathlib.Path(r"D:/2026/WB项目/emperor-skill")
MS = pathlib.Path(r"D:/2026/WB项目/蒸馏skill")

out = []
def w(s=""):
    out.append(str(s))

# 1) emperor-skill skills 各朝代目录包数（只数含 SKILL.md 的目录）
skills = ES / "skills"
total = 0
rows = []
for d in sorted([p for p in skills.iterdir() if p.is_dir()]):
    subs = [p for p in d.iterdir() if p.is_dir()]
    n_ok = len([p for p in subs if (p / "SKILL.md").exists()])
    total += n_ok
    rows.append((d.name, len(subs), n_ok))
w("== emperor-skill / skills 各朝代目录 ==")
for name, n, ok in rows:
    w(f"  {name:<14} 目录 {n:>3}  含SKILL.md {ok:>3}")
w(f"  合计含 SKILL.md: {total}")

# 2) _pending 暂存
pend = ES / "_pending"
w("")
w("== _pending 暂存（限流残件） ==")
if pend.exists():
    for key in sorted([p for p in pend.iterdir() if p.is_dir()]):
        for p in sorted([x for x in key.iterdir() if x.is_dir()]):
            files = sorted([f.name for f in p.rglob("*") if f.is_file()])
            w(f"  {key.name}/{p.name}: {len(files)} 文件")
            for f in files:
                w(f"      - {f}")
else:
    w("  (无 _pending)")

# 3) 主仓 people / groups / modules
mj = MS / ".workbuddy/data/modules.json"
if mj.exists():
    data = json.loads(mj.read_text(encoding="utf-8"))
    people = data.get("people", {})
    w("")
    w("== 主仓 modules.json ==")
    w(f"  people: {len(people)}")
    w(f"  modules: {len(data.get('modules', []))}")
    w(f"  groups: {len(data.get('groups', []))}")
    nan = [k for k, v in people.items() if isinstance(v, dict) and v.get("module") == "nanbeichao-emperors"]
    w(f"  nanbeichao-emperors 人数: {len(nan)}")
    bymod = {}
    for k, v in people.items():
        if isinstance(v, dict):
            bymod[v.get("module", "?")] = bymod.get(v.get("module", "?"), 0) + 1
    w("  各 module 人数：")
    for k, v in sorted(bymod.items(), key=lambda x: -x[1]):
        w(f"      {k:<28} {v}")

# 4) 站点 html 人数粗查
docs = MS / "docs"
if docs.exists():
    w("")
    w("== docs 帝王模块页人数 ==")
    for h in sorted(docs.glob("*-emperors.html")):
        t = h.read_text(encoding="utf-8", errors="ignore")
        w(f"  {h.name:<34} {len(re.findall(r'data-person-id=', t)) or t.count('class=\"person\"')}  (size {h.stat().st_size})")

(r"D:/2026/WB项目/emperor-skill/_redo_tools").__str__()
outp = ES / "_redo_tools/_status_now.txt"
outp.write_text("\n".join(out), encoding="utf-8")
print("OK", outp)
