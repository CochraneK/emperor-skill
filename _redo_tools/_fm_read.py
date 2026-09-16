# -*- coding: utf-8 -*-
"""读东汉/隋 16 个包的 frontmatter 关键字段，供补登记 modules.json 用。"""
import os, re, json

ES = r"D:/2026/WB项目/emperor-skill/skills"
OUT = r"D:/2026/WB项目/emperor-skill/_redo_tools/_fm_dh_sui.txt"

BUF = []
for dyn in ("donghan", "sui"):
    d = os.path.join(ES, dyn)
    BUF.append("===== " + dyn)
    for p in sorted(os.listdir(d)):
        sk = os.path.join(d, p, "SKILL.md")
        if not os.path.exists(sk):
            BUF.append("  无 SKILL.md: " + p)
            continue
        t = open(sk, encoding="utf-8", errors="replace").read()
        m = re.search(r"^---\r?\n(.*?)\r?\n---", t, re.S | re.M)
        fm = m.group(1) if m else ""
        if not fm:
            BUF.append(f"  {p:<28} !! 未匹配到 frontmatter")
            # 打印前 3 行帮助诊断
            BUF.append("     head: " + " | ".join(t.splitlines()[:3])[:150])
            continue

        def g(k):
            r = re.search(r"^" + k + r":[ \t]*([^\r\n]*)", fm, re.M)
            return (r.group(1).strip() if r else "")

        BUF.append(f"  {p:<28} cn={g('cn'):<8} module={g('module'):<18} "
                   f"group={g('group'):<14} era={g('era')[:20]:<22} tags={g('tags')[:70]}")
    BUF.append("")

open(OUT, "w", encoding="utf-8").write("\n".join(BUF))
print(open(OUT, encoding="utf-8").read())
