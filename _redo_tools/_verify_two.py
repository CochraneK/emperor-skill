# -*- coding: utf-8 -*-
import subprocess, os, re
ROOT = "D:/2026/WB项目/emperor-skill"
PY = "C:/Users/cunyi/.workbuddy/binaries/python/versions/3.13.12/python.exe"
QC = "D:/2026/WB项目/emperor-skill/_redo_tools/quality_check.py"

def audit(pkg):
    p = os.path.join(ROOT, "skills", "xihan", pkg)
    print("="*60); print(pkg)
    if not os.path.isdir(p):
        print("  DIR MISSING"); return
    skill = os.path.join(p, "SKILL.md")
    if not os.path.isfile(skill):
        print("  SKILL.md MISSING"); return
    txt = open(skill, encoding="utf-8").read()
    # frontmatter
    fm = txt.split("---")[1] if txt.startswith("---") else ""
    mod = re.search(r"module:\s*(.+?)\s*$", fm, re.M)
    grp = re.search(r"group:\s*(.+?)\s*$", fm, re.M)
    print("  module=%s group=%s" % (mod.group(1).strip() if mod else None, grp.group(1).strip() if grp else None))
    print("  SKILL.md=%d bytes" % os.path.getsize(skill))
    print("  '诚实边界' occurrences=%d" % txt.count("诚实边界"))
    # research
    ref = os.path.join(p, "references", "research")
    if os.path.isdir(ref):
        sizes = {f: os.path.getsize(os.path.join(ref,f)) for f in sorted(os.listdir(ref))}
        print("  research: %s" % sizes)
        # check exclude declaration in each
        for f,sz in sizes.items():
            c = open(os.path.join(ref,f), encoding="utf-8").read()
            has_ex = ("知乎" in c) and ("百度百科" in c)
            print("    %s %d bytes 排除声明=%s" % (f, sz, has_ex))
    # stray temp
    stray = []
    for r,_,fs in os.walk(p):
        for f in fs:
            if f.endswith((".tmp",".txt")) or f.startswith("_out"):
                stray.append(os.path.join(r,f))
    if stray: print("  !! STRAY: %s" % stray)
    # quality check
    r = subprocess.run([PY, QC, skill], capture_output=True, text=True, encoding="utf-8")
    out = r.stdout.strip().splitlines()
    for line in out:
        if "PASS" in line or "结果" in line or "通过" in line:
            print("  QC: " + line.strip())

for pkg in ["liuying-perspective", "liuheng-xihan-perspective"]:
    audit(pkg)
