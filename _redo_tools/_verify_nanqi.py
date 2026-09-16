# -*- coding: utf-8 -*-
"""独立复核南齐 7 包：不采信 worker 自报，自跑 quality_check.py + 核对结构/声明/诚实边界。
落盘目录：D:/2026/WB项目/emperor-skill/skills/nanbeichao/<id>-perspective
"""
import os, re, json, subprocess, sys

ES = r"D:/2026/WB项目/emperor-skill/skills/nanbeichao"
PY = r"C:/Users/cunyi/.workbuddy/binaries/python/versions/3.13.12/python.exe"
IDS = ["xiaodaochang", "xiaozhe", "xiaozhaoye", "xiaozhaowen", "xiaoluan", "xiaobaojuan", "xiaobaorong"]
CANON = ["01-writings.md", "02-conversations.md", "03-expression-dna.md",
         "04-external-views.md", "05-decisions.md", "06-timeline.md"]
QC = os.path.join(ES, "liuyu-perspective", "scripts", "quality_check.py")

EXCL = "排除声明"  # 末段须含此词 + 知乎 + 百度百科
results = []

for sid in IDS:
    base = os.path.join(ES, sid + "-perspective")
    rec = {"id": sid, "ok": True, "issues": []}
    if not os.path.isdir(base):
        rec["ok"] = False; rec["issues"].append("目录缺失"); results.append(rec); continue

    # 1. 文件清单：必须恰好 8 个（不含子目录名自身）
    files = []
    for root, dirs, fnames in os.walk(base):
        for f in fnames:
            files.append(os.path.relpath(os.path.join(root, f), base))
    rec["files"] = sorted(files)
    if len(files) != 8:
        rec["ok"] = False; rec["issues"].append(f"文件数={len(files)} (应8)")

    # 2. 必须项
    sk = os.path.join(base, "SKILL.md")
    qc = os.path.join(base, "scripts", "quality_check.py")
    rr = os.path.join(base, "references", "research")
    if not os.path.isfile(sk): rec["ok"] = False; rec["issues"].append("无SKILL.md")
    elif os.path.getsize(sk) < 1024: rec["ok"] = False; rec["issues"].append("SKILL.md<1KB")
    if not os.path.isfile(qc): rec["ok"] = False; rec["issues"].append("无quality_check.py")

    # 3. 六维底稿：glob references/research/*.md 应恰好 6 份
    rfiles = []
    if os.path.isdir(rr):
        rfiles = sorted([f for f in os.listdir(rr) if f.endswith(".md")])
    rec["research_files"] = rfiles
    if len(rfiles) != 6:
        rec["ok"] = False; rec["issues"].append(f"底稿数={len(rfiles)} (应6)")
    # 命名对照
    noncanon = [f for f in rfiles if f not in CANON]
    if noncanon:
        rec["issues"].append("非规范文件名:" + ",".join(noncanon))
        rec["rename_needed"] = True
    # 每份 ≥2.5KB + 排除声明
    for f in rfiles:
        p = os.path.join(rr, f)
        sz = os.path.getsize(p)
        if sz < 2560:
            rec["ok"] = False; rec["issues"].append(f"{f} {sz}B<2.5KB")
        t = open(p, encoding="utf-8", errors="replace").read()
        if EXCL not in t or "知乎" not in t or "百度百科" not in t:
            rec["ok"] = False; rec["issues"].append(f"{f} 缺排除声明")

    # 4. frontmatter module/group
    t = open(sk, encoding="utf-8", errors="replace").read()
    m = re.search(r"^---\r?\n(.*?)\r?\n---", t, re.S | re.M)
    fm = m.group(1) if m else ""
    mod = re.search(r"^module:[ \t]*([^\r\n]*)", fm, re.M)
    grp = re.search(r"^group:[ \t]*([^\r\n]*)", fm, re.M)
    mod = mod.group(1).strip() if mod else ""
    grp = grp.group(1).strip() if grp else ""
    rec["module"] = mod; rec["group"] = grp
    if mod != "nanbeichao-emperors": rec["ok"] = False; rec["issues"].append(f"module={mod}")
    if grp != "nanbeichao-main": rec["ok"] = False; rec["issues"].append(f"group={grp}")

    # 5. 诚实边界 全文仅 1 次
    cnt = len(re.findall("诚实边界", t))
    rec["honesty_cnt"] = cnt
    if cnt != 1: rec["ok"] = False; rec["issues"].append(f"诚实边界出现{cnt}次(应1)")

    # 6. 自跑 quality_check.py
    try:
        out = subprocess.run([PY, QC, sk], capture_output=True, text=True, encoding="utf-8", timeout=120)
        rec["qc_out"] = out.stdout.strip()[-400:] + out.stderr.strip()[-200:]
        # 判定 6/6：脚本末尾应含 "6/6" 或 "PASS"
        if "6/6" in out.stdout or "6 / 6" in out.stdout or "PASS" in out.stdout.upper():
            rec["qc_pass"] = True
        else:
            rec["qc_pass"] = False; rec["ok"] = False; rec["issues"].append("QC非6/6")
    except Exception as e:
        rec["qc_pass"] = False; rec["ok"] = False; rec["issues"].append(f"QC异常:{e}")

    results.append(rec)

# 输出
out_path = r"D:/2026/WB项目/emperor-skill/_redo_tools/_verify_nanqi.txt"
lines = []
ALL_OK = True
for r in results:
    if not r["ok"]: ALL_OK = False
    lines.append(f"\n=== {r['id']}  ok={r['ok']} ===")
    if "module" in r: lines.append(f"  module={r.get('module')} group={r.get('group')} honesty={r.get('honesty_cnt')} qc_pass={r.get('qc_pass')}")
    if "research_files" in r: lines.append(f"  research={r['research_files']}")
    if r["issues"]: lines.append("  ISSUES: " + " | ".join(r["issues"]))
    if "qc_out" in r and not r.get("qc_pass"): lines.append("  QC: " + r["qc_out"])
lines.append(f"\nALL_OK = {ALL_OK}")
msg = "\n".join(lines)
open(out_path, "w", encoding="utf-8").write(msg)
print(msg)
