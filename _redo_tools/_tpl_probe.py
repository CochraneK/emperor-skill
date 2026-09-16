# -*- coding: utf-8 -*-
"""列出参考合规包的完整文件树 + 一份底稿的头部，作为补齐模板。输出 _tpl_probe.txt"""
import pathlib
ES = pathlib.Path(r"D:/2026/WB项目/emperor-skill")
out = []
def w(s=""): out.append(str(s))

for sid in ["nanbeichao/yuanziyou-perspective", "nanbeichao/yuanxu-perspective"]:
    p = ES / "skills" / sid
    w(f"== {sid} ==")
    for f in sorted(p.rglob("*")):
        if f.is_file():
            w(f"   {str(f.relative_to(p))}  ({f.stat().st_size}B)")
    w("")

# 打印 01-writings.md 前 40 行 与 06-timeline.md 前 40 行（作为格式样例）
for sid, name in [("nanbeichao/yuanziyou-perspective", "01-writings.md"),
                  ("nanbeichao/yuanziyou-perspective", "03-expression-dna.md"),
                  ("nanbeichao/yuanziyou-perspective", "06-timeline.md")]:
    f = ES / "skills" / sid / "references" / "research" / name
    if f.exists():
        w(f"---- 样例 {sid}/{name} 前 30 行 ----")
        lines = f.read_text(encoding="utf-8").splitlines()[:30]
        for i, l in enumerate(lines, 1):
            w(f"{i:>3}| {l}")
        w("")

(ES / "_redo_tools/_tpl_probe.txt").write_text("\n".join(out), encoding="utf-8")
print("OK")
