# -*- coding: utf-8 -*-
"""独立复核 北朝第二批：北魏 拓跋弘/元宏/元恪/元诩/元子攸 五包。不信任 worker 自报。"""
import os, re, subprocess

ES = r"D:/2026/WB项目/emperor-skill/skills/nanbeichao"
QC = r"D:/2026/WB项目/emperor-skill/_redo_tools/quality_check.py"
PY = r"C:/Users/cunyi/.workbuddy/binaries/python/versions/3.13.12/python.exe"

IDS = ["tuobahong", "yuanhong", "yuanke", "yuanxu", "yuanziyou"]
EXPECT = ["SKILL.md",
          "references/research/01-writings.md",
          "references/research/02-conversations.md",
          "references/research/03-expression-dna.md",
          "references/research/04-external-views.md",
          "references/research/05-decisions.md",
          "references/research/06-timeline.md",
          "scripts/quality_check.py"]
EXCL = "未引用知乎"

out = []
ALL_OK = True
for sid in IDS:
    d = os.path.join(ES, sid + "-perspective")
    out.append(f"\n===== {sid} =====")
    ok = True
    if not os.path.isdir(d):
        out.append("  !! 目录缺失"); ALL_OK = ok = False; continue
    actual = []
    for root, _, files in os.walk(d):
        for f in files:
            actual.append(os.path.relpath(os.path.join(root, f), d).replace("\\", "/"))
    a_s = set(actual)
    miss = [n for n in EXPECT if n not in a_s]
    stray = [a for a in actual if a not in EXPECT]
    if miss: out.append(f"  !! 缺:{miss}"); ALL_OK = ok = False
    if stray: out.append(f"  !! stray:{stray}"); ALL_OK = ok = False
    if len(actual) != 8: out.append(f"  !! 文件数={len(actual)}"); ALL_OK = ok = False
    for rn in EXPECT[1:7]:
        p = os.path.join(d, rn)
        if os.path.isfile(p):
            if os.path.getsize(p) < 2500:
                out.append(f"  !! {rn} <2.5KB"); ALL_OK = ok = False
            if EXCL not in open(p, encoding="utf-8", errors="replace").read():
                out.append(f"  !! {rn} 缺排除声明"); ALL_OK = ok = False
    r = subprocess.run([PY, QC, os.path.join(d, "SKILL.md")], capture_output=True, text=True, encoding="utf-8")
    m = re.search(r"结果:\s*(\d+)/(\d+)", r.stdout)
    n6 = int(m.group(1)) if m else -1
    out.append(f"  QC: {n6}/6")
    if n6 != 6: ALL_OK = ok = False; out.append(r.stdout)
    sk = open(os.path.join(d, "SKILL.md"), encoding="utf-8", errors="replace").read()
    c = sk.count("诚实边界")
    if c != 1: out.append(f"  !! 诚实边界x{c}"); ALL_OK = ok = False
    fm = re.search(r"^---\r?\n(.*?)\r?\n---", sk, re.S); fms = fm.group(1) if fm else ""
    mod = re.search(r"^module:\s*(\S+)", fms, re.M); grp = re.search(r"^group:\s*(\S+)", fms, re.M)
    if (mod.group(1) if mod else "?") != "nanbeichao-emperors": out.append("  !! module错"); ALL_OK = ok = False
    if (grp.group(1) if grp else "?") != "nanbeichao-main": out.append("  !! group错"); ALL_OK = ok = False
    out.append(f"  module={(mod.group(1) if mod else '?')} group={(grp.group(1) if grp else '?')} 诚实边界x{c}")
    out.append("  OK" if ok else "  *** FAIL ***")

print("\n".join(out))
print("\n=== ALL_OK:", ALL_OK, "===")
open(os.path.join(os.path.dirname(__file__), "_verify_bei2.txt"), "w", encoding="utf-8").write("\n".join(out) + f"\n=== ALL_OK: {ALL_OK} ===")
