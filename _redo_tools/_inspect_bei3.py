# -*- coding: utf-8 -*-
"""检查北朝第三批（限流中断）5 个疑似残留目录的内容与质检结果。"""
import os, re, subprocess

ES = r"D:/2026/WB项目/emperor-skill/skills/nanbeichao"
QC = r"D:/2026/WB项目/emperor-skill/_redo_tools/quality_check.py"
PY = r"C:/Users/cunyi/.workbuddy/binaries/python/versions/3.13.12/python.exe"

for sid in ["yuanye", "yuanguan", "yuanlang", "yuanxiu", "yuanzhao"]:
    d = os.path.join(ES, sid + "-perspective")
    print("=====", sid, "=====")
    if not os.path.isdir(d):
        print("  目录不存在")
        continue
    n = 0
    for root, _, fs in os.walk(d):
        for f in fs:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, d).replace("\\", "/")
            print("   ", rel, os.path.getsize(p))
            n += 1
    print("  文件总数:", n)
    sk = os.path.join(d, "SKILL.md")
    if os.path.isfile(sk):
        r = subprocess.run([PY, QC, sk], capture_output=True, text=True, encoding="utf-8")
        m = re.search(r"结果:\s*(\d+)/(\d+)", r.stdout)
        print("  QC:", (m.group(1) + "/" + m.group(2)) if m else "N/A")
    else:
        print("  无 SKILL.md")
