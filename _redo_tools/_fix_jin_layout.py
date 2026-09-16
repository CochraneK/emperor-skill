# -*- coding: utf-8 -*-
import os, re, io, glob, shutil, subprocess

ROOT = "D:/2026/WB项目/emperor-skill/skills/jin"
PY = "C:/Users/cunyi/.workbuddy/binaries/python/versions/3.13.12/python.exe"
FIX = ["simachi-perspective", "simayan-perspective", "simazhong-perspective"]
NAMES = ["01-writings.md", "02-conversations.md", "03-expression-dna.md",
         "04-external-views.md", "05-decisions.md", "06-timeline.md"]

log = []
for pkg in FIX:
    d = os.path.join(ROOT, pkg)
    rdir = os.path.join(d, "references", "research")
    if not os.path.isdir(rdir):
        os.makedirs(rdir)
    # move each file if it sits in root
    for nm in NAMES:
        src = os.path.join(d, nm)
        dst = os.path.join(rdir, nm)
        if os.path.isfile(src) and not os.path.isfile(dst):
            shutil.move(src, dst)
            log.append("moved %s/%s -> references/research/" % (pkg, nm))
    # update SKILL.md references
    sk = os.path.join(d, "SKILL.md")
    t = open(sk, encoding="utf-8").read()
    new = t
    for nm in NAMES:
        new = new.replace(nm, "references/research/" + nm)
    if new != t:
        open(sk, "w", encoding="utf-8").write(new)
        log.append("updated SKILL.md refs in %s" % pkg)
    # verify tree after
    files = []
    for dp, _, fns in os.walk(d):
        for fn in fns:
            files.append(os.path.relpath(os.path.join(dp, fn), d))
    log.append("%s files=%s" % (pkg, sorted(files)))
    # re-run QC
    qc = os.path.join(d, "scripts", "quality_check.py")
    r = subprocess.run([PY, qc, sk], capture_output=True, text=True, timeout=120)
    log.append("%s QC: %s" % (pkg, "6/6" if "6/6" in (r.stdout+r.stderr) else "FAIL"))

out = "D:/2026/WB项目/emperor-skill/_redo_tools/_fix_jin_layout.txt"
io.open(out, "w", encoding="utf-8").write("\n".join(log))
print("WROTE", out)
for l in log: print(l)
