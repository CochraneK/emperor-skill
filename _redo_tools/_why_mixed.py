# -*- coding: utf-8 -*-
"""回答「为什么同一朝代有的合规有的不合规」：对比 zhou / donghan 每包的
底稿体量、SKILL.md 提交批次时间（用 SKILL.md 的 mtime 近似分组）。
输出 _redo_tools/_why_mixed.txt
"""
import pathlib, re, datetime

ES = pathlib.Path(r"D:/2026/WB项目/emperor-skill")
DIMS = ["01-writings", "02-conversations", "03-expression-dna",
        "04-external-views", "05-decisions", "06-timeline"]

def ts(p):
    return datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime("%m-%d %H:%M")

out = []
for dyn in ["zhou", "donghan", "tang", "xia"]:
    d = ES / "skills" / dyn
    rows = []
    for p in sorted([x for x in d.iterdir() if x.is_dir()]):
        sk = p / "SKILL.md"
        if not sk.exists():
            continue
        sizes = []
        for n in DIMS:
            f = p / "references/research" / (n + ".md")
            sizes.append(f.stat().st_size if f.exists() else 0)
        lo = min(sizes)
        rows.append((p.name, lo, sum(sizes), ts(sk), sk.stat().st_size))
    out.append(f"== {dyn}（{len(rows)} 包）==  表：包 / 最薄底稿 / 六维合计 / SKILL.md 最后修改 / SKILL.md 大小")
    out.append("   —— 按 SKILL.md 修改时间排序，可见明显的时间分组")
    for r in sorted(rows, key=lambda x: x[3]):
        flag = "合规" if r[1] >= 2500 else "★底稿薄"
        out.append(f"  {flag}  {r[0]:<34} 最薄 {r[1]:>5}B  合计 {r[2]:>6}B  {r[3]}  SKILL {r[4]}B")
    out.append("")

(ES / "_redo_tools/_why_mixed.txt").write_text("\n".join(out), encoding="utf-8")
print("OK")
