# -*- coding: utf-8 -*-
import os, re, io, glob, subprocess

ROOT = "D:/2026/WB项目/emperor-skill/skills/jin"
PKGS = ["simarui-perspective", "simashao-perspective", "simayancheng-perspective",
        "simayue-perspective", "simadan-perspective", "simapi-perspective",
        "simayi-perspective", "simayu-perspective", "simayao-perspective",
        "simadezong-perspective", "simadewen-perspective"]
PY = "C:/Users/cunyi/.workbuddy/binaries/python/versions/3.13.12/python.exe"

def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception:
        return None

report = []
all_ok = True
for pkg in PKGS:
    d = os.path.join(ROOT, pkg)
    report.append("## %s" % pkg)
    skill = os.path.join(d, "SKILL.md")
    txt = read(skill)
    if txt is None:
        report.append("   SKILL.md MISSING"); all_ok = False; continue
    mm = re.search(r"^module:\s*(.+)$", txt, re.M)
    gm = re.search(r"^group:\s*(.+)$", txt, re.M)
    module = (mm.group(1).strip() if mm else "(none)")
    group = (gm.group(1).strip() if gm else "(none)")
    if module != "jin-emperors" or group != "jin-main":
        all_ok = False
    report.append("   module=%s group=%s" % (module, group))
    hc = txt.count("诚实边界")
    if hc != 1:
        all_ok = False
    report.append("   诚实边界_occurrences=%d size=%dB" % (hc, len(txt.encode("utf-8"))))
    rdir = os.path.join(d, "references", "research")
    if not os.path.isdir(rdir):
        report.append("   references/research MISSING"); all_ok = False
    else:
        for i in range(1, 7):
            matches = glob.glob(os.path.join(rdir, "0%d-*.md" % i))
            if matches:
                c = read(matches[0])
                sz = len(c.encode("utf-8")) if c else 0
                has_excl = bool(c) and (("排除" in c) or ("未采纳" in c))
                if sz < 2500 or not has_excl:
                    all_ok = False
                report.append("   0%d: %s %dB excl=%s" % (i, os.path.basename(matches[0]), sz, has_excl))
            else:
                report.append("   0%d: MISSING" % i); all_ok = False
    allfiles = []
    for dp, _, fns in os.walk(d):
        for fn in fns:
            allfiles.append(os.path.relpath(os.path.join(dp, fn), d))
    if len(allfiles) != 8:
        all_ok = False
    report.append("   total_walked_files=%d (expect 8)" % len(allfiles))
    qc = os.path.join(d, "scripts", "quality_check.py")
    if os.path.isfile(qc):
        try:
            r = subprocess.run([PY, qc, skill], capture_output=True, text=True, timeout=120)
            out = (r.stdout + r.stderr).strip()
            if "6/6" not in out:
                all_ok = False
            report.append("   QC: %s" % ("6/6 PASS" if "6/6" in out else "FAIL"))
        except Exception as e:
            report.append("   QC_ERROR: %s" % e); all_ok = False
    else:
        report.append("   quality_check.py MISSING"); all_ok = False

outpath = "D:/2026/WB项目/emperor-skill/_redo_tools/_verify_dongjin.txt"
io.open(outpath, "w", encoding="utf-8").write(("ALL_OK=%s\n" % all_ok) + "\n".join(report))
print("WROTE", outpath, "ALL_OK=", all_ok)
