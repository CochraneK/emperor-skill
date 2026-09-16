# -*- coding: utf-8 -*-
"""独立复核南梁 6 包：不采信 worker 自报，自跑 quality_check.py + 核对结构/声明/诚实边界。"""
import os, re, subprocess

ES = r"D:/2026/WB项目/emperor-skill/skills/nanbeichao"
PY = r"C:/Users/cunyi/.workbuddy/binaries/python/versions/3.13.12/python.exe"
IDS = ["xiaoyan", "xiaozhengde", "xiaogang", "xiaodong", "xiaoyi", "xiaofangzhi"]
CANON = ["01-writings.md", "02-conversations.md", "03-expression-dna.md",
         "04-external-views.md", "05-decisions.md", "06-timeline.md"]
QC = os.path.join(ES, "liuyu-perspective", "scripts", "quality_check.py")
EXCL = "排除声明"

results = []
for sid in IDS:
    base = os.path.join(ES, sid + "-perspective")
    rec = {"id": sid, "ok": True, "issues": []}
    if not os.path.isdir(base):
        rec["ok"] = False; rec["issues"].append("目录缺失"); results.append(rec); continue
    files = []
    for root, dirs, fnames in os.walk(base):
        for f in fnames:
            files.append(os.path.relpath(os.path.join(root, f), base))
    if len(files) != 8:
        rec["ok"] = False; rec["issues"].append(f"文件数={len(files)} (应8)")
    sk = os.path.join(base, "SKILL.md")
    qc = os.path.join(base, "scripts", "quality_check.py")
    rr = os.path.join(base, "references", "research")
    if not os.path.isfile(sk): rec["ok"] = False; rec["issues"].append("无SKILL.md")
    elif os.path.getsize(sk) < 1024: rec["ok"] = False; rec["issues"].append("SKILL.md<1KB")
    if not os.path.isfile(qc): rec["ok"] = False; rec["issues"].append("无quality_check.py")
    rfiles = sorted([f for f in os.listdir(rr)] if os.path.isdir(rr) else [])
    if len(rfiles) != 6:
        rec["ok"] = False; rec["issues"].append(f"底稿数={len(rfiles)} (应6)")
    noncanon = [f for f in rfiles if f not in CANON]
    if noncanon: rec["ok"] = False; rec["issues"].append("非规范文件名:" + ",".join(noncanon))
    for f in rfiles:
        p = os.path.join(rr, f); sz = os.path.getsize(p)
        if sz < 2560: rec["ok"] = False; rec["issues"].append(f"{f} {sz}B<2.5KB")
        t = open(p, encoding="utf-8", errors="replace").read()
        if EXCL not in t or "知乎" not in t or "百度百科" not in t:
            rec["ok"] = False; rec["issues"].append(f"{f} 缺排除声明")
    t = open(sk, encoding="utf-8", errors="replace").read()
    m = re.search(r"^---\r?\n(.*?)\r?\n---", t, re.S | re.M); fm = m.group(1) if m else ""
    mod = re.search(r"^module:[ \t]*([^\r\n]*)", fm, re.M)
    grp = re.search(r"^group:[ \t]*([^\r\n]*)", fm, re.M)
    mod = mod.group(1).strip() if mod else ""; grp = grp.group(1).strip() if grp else ""
    rec["module"] = mod; rec["group"] = grp
    if mod != "nanbeichao-emperors": rec["ok"] = False; rec["issues"].append(f"module={mod}")
    if grp != "nanbeichao-main": rec["ok"] = False; rec["issues"].append(f"group={grp}")
    cnt = len(re.findall("诚实边界", t)); rec["honesty_cnt"] = cnt
    if cnt != 1: rec["ok"] = False; rec["issues"].append(f"诚实边界出现{cnt}次(应1)")
    try:
        out = subprocess.run([PY, QC, sk], capture_output=True, text=True, encoding="utf-8", timeout=120)
        rec["qc_pass"] = ("6/6" in out.stdout) or ("PASS" in out.stdout.upper())
        if not rec["qc_pass"]: rec["ok"] = False; rec["issues"].append("QC非6/6")
    except Exception as e:
        rec["qc_pass"] = False; rec["ok"] = False; rec["issues"].append(f"QC异常:{e}")
    results.append(rec)

out_path = r"D:/2026/WB项目/emperor-skill/_redo_tools/_verify_nanliang.txt"
lines = []; ALL_OK = True
for r in results:
    if not r["ok"]: ALL_OK = False
    lines.append(f"\n=== {r['id']}  ok={r['ok']} ===")
    if "module" in r: lines.append(f"  module={r.get('module')} group={r.get('group')} honesty={r.get('honesty_cnt')} qc_pass={r.get('qc_pass')}")
    if r["issues"]: lines.append("  ISSUES: " + " | ".join(r["issues"]))
lines.append(f"\nALL_OK = {ALL_OK}")
open(out_path, "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines))
