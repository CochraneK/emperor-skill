# -*- coding: utf-8 -*-
"""把 _pending/bei3/yuanye-perspective 就位到 skills/nanbeichao/（复制 SKILL.md + quality_check.py），
不删源，待复核通过后再清 _pending。"""
import pathlib, shutil
ES = pathlib.Path(r"D:/2026/WB项目/emperor-skill")
src = ES / "_pending/bei3/yuanye-perspective"
dst = ES / "skills/nanbeichao/yuanye-perspective"
(dst / "references/research").mkdir(parents=True, exist_ok=True)
(dst / "scripts").mkdir(parents=True, exist_ok=True)
shutil.copy2(src / "SKILL.md", dst / "SKILL.md")
_qc = src / "quality_check.py"
if not _qc.exists():  # 残件里 qc 可能在 scripts/ 下，或从参考包取
    _qc = ES / "skills/nanbeichao/yuanziyou-perspective/scripts/quality_check.py"
shutil.copy2(_qc, dst / "scripts/quality_check.py")
print("staged:", dst)
print("SKILL.md bytes:", (dst / "SKILL.md").stat().st_size)
print("qc bytes:", (dst / "scripts/quality_check.py").stat().st_size)
