# -*- coding: utf-8 -*-
import subprocess, os
QC = "D:/2026/WB项目/emperor-skill/scripts/quality_check.py"
PY = "C:/Users/cunyi/.workbuddy/binaries/python/versions/3.13.12/python.exe"
for pkg in ["liubang-perspective", "liuying-perspective", "liuheng-xihan-perspective"]:
    p = os.path.join("D:/2026/WB项目/emperor-skill/skills/xihan", pkg)
    print("="*60)
    print(pkg)
    if not os.path.isdir(p):
        print("  MISSING DIR")
        continue
    # research sizes
    ref = os.path.join(p, "references", "research")
    if os.path.isdir(ref):
        for f in sorted(os.listdir(ref)):
            fp = os.path.join(ref, f)
            print("  %s : %d bytes" % (f, os.path.getsize(fp)))
    # quality check if SKILL.md exists
    if os.path.isfile(os.path.join(p, "SKILL.md")):
        try:
            r = subprocess.run([PY, QC, p], capture_output=True, text=True, encoding="utf-8", cwd="D:/2026/WB项目/emperor-skill")
            print("---- quality_check stdout ----")
            print(r.stdout[-2000:])
            if r.stderr:
                print("---- stderr ----")
                print(r.stderr[-800:])
        except Exception as e:
            print("  QC ERROR: %s" % e)
    else:
        print("  SKILL.md MISSING -> cannot run quality_check")
