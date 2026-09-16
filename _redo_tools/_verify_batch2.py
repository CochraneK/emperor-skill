# -*- coding: utf-8 -*-
import os, re, io, glob, subprocess

ROOT = "D:/2026/WB项目/emperor-skill/skills/sanguo"
PKGS = ["caorui-perspective", "liushan-perspective", "sunliang-perspective"]
PY = "C:/Users/cunyi/.workbuddy/binaries/python/versions/3.13.12/python.exe"

def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

report = []
for pkg in PKGS:
    d = os.path.join(ROOT, pkg)
    if not os.path.isdir(d):
        report.append("## %s: MISSING DIR" % pkg)
        continue
    report.append("## %s: dir_ok" % pkg)
    skill = os.path.join(d, "SKILL.md")
    txt = read(skill)
    if txt is None:
        report.append("   SKILL.md MISSING")
        continue
    mm = re.search(r"^module:\s*(.+)$", txt, re.M)
    gm = re.search(r"^group:\s*(.+)$", txt, re.M)
    module = mm.group(1).strip() if mm else "(none)"
    group = gm.group(1).strip() if gm else "(none)"
    report.append("   module=%s group=%s" % (module, group))
    hc = txt.count("诚实边界")
    report.append("   诚实边界_occurrences=%d  size=%dB" % (hc, len(txt.encode("utf-8"))))
    rdir = os.path.join(d, "references", "research")
    if os.path.isdir(rdir):
        for i in range(1, 7):
            matches = glob.glob(os.path.join(rdir, "0%d-*.md" % i))
            if matches:
                c = read(matches[0])
                sz = len(c.encode("utf-8")) if c else 0
                has_excl = bool(c) and (("排除" in c) or ("未采纳" in c))
                report.append("   0%d: %s %dB excl=%s" % (i, os.path.basename(matches[0]), sz, has_excl))
            else:
                report.append("   0%d: MISSING" % i)
    else:
        report.append("   references/research MISSING")
    allfiles = []
    for dp, _, fns in os.walk(d):
        for fn in fns:
            allfiles.append(os.path.relpath(os.path.join(dp, fn), d))
    report.append("   total_walked_files=%d" % len(allfiles))
    qc = os.path.join(d, "scripts", "quality_check.py")
    if os.path.isfile(qc):
        try:
            r = subprocess.run([PY, qc, skill], capture_output=True, text=True, timeout=120)
            out = (r.stdout + r.stderr).strip()
            report.append("   QC_OUTPUT:\n%s" % out)
        except Exception as e:
            report.append("   QC_ERROR: %s" % e)
    else:
        report.append("   quality_check.py MISSING")

outpath = "D:/2026/WB项目/emperor-skill/_redo_tools/_verify_batch2.txt"
with io.open(outpath, "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("WROTE", outpath, "lines", len(report))
