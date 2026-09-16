# -*- coding: utf-8 -*-
"""独立复核 北朝第一批：北魏 拓跋珪/嗣/焘/余/濬 五包。
不信任 worker 自报，自跑 quality_check.py + 逐项核对。
"""
import os, re, subprocess, json

ES = r"D:/2026/WB项目/emperor-skill/skills/nanbeichao"
QC = r"D:/2026/WB项目/emperor-skill/_redo_tools/quality_check.py"
PY = r"C:/Users/cunyi/.workbuddy/binaries/python/versions/3.13.12/python.exe"

IDS = ["tuobagui", "tuobasi", "tuobatao", "tuobayu", "tuobajun"]
EXPECT_NAMES = ["SKILL.md",
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
    line = f"\n===== {sid} ====="
    out.append(line)
    ok = True
    # 1) 文件齐全 + 无 stray
    if not os.path.isdir(d):
        out.append("  !! 目录缺失"); ALL_OK = ok = False; continue
    actual = []
    for root, _, files in os.walk(d):
        for f in files:
            actual.append(os.path.relpath(os.path.join(root, f), d).replace("\\", "/"))
    actual_s = set(actual)
    missing = [n for n in EXPECT_NAMES if n not in actual_s]
    stray = [a for a in actual if a not in EXPECT_NAMES]
    if missing:
        out.append(f"  !! 缺文件: {missing}"); ALL_OK = ok = False
    if stray:
        out.append(f"  !! 多余文件(stray): {stray}"); ALL_OK = ok = False
    if len(actual) != 8:
        out.append(f"  !! 文件数={len(actual)} (应8)"); ALL_OK = ok = False
    # 2) 六份底稿 >=2.5KB + 排除声明
    for rn in EXPECT_NAMES[1:7]:
        p = os.path.join(d, rn)
        if os.path.isfile(p):
            sz = os.path.getsize(p)
            t = open(p, encoding="utf-8", errors="replace").read()
            if sz < 2500:
                out.append(f"  !! {rn} 仅 {sz}B (<2.5KB)"); ALL_OK = ok = False
            if EXCL not in t:
                out.append(f"  !! {rn} 缺排除声明"); ALL_OK = ok = False
    # 3) QC 6/6
    r = subprocess.run([PY, QC, os.path.join(d, "SKILL.md")], capture_output=True, text=True, encoding="utf-8")
    qcout = r.stdout
    # 解析 "结果: X/6 通过"
    m = re.search(r"结果:\s*(\d+)/(\d+)", qcout)
    n6 = int(m.group(1)) if m else -1
    out.append(f"  QC: {n6}/6")
    if n6 != 6:
        ALL_OK = ok = False
        out.append("  ---- QC stdout ----")
        out.append(qcout)
    # 4) 诚实边界 仅1次
    sk = open(os.path.join(d, "SKILL.md"), encoding="utf-8", errors="replace").read()
    cnt = sk.count("诚实边界")
    if cnt != 1:
        out.append(f"  !! '诚实边界' 出现 {cnt} 次 (应1)"); ALL_OK = ok = False
    # 5) frontmatter module/group
    fm = re.search(r"^---\r?\n(.*?)\r?\n---", sk, re.S)
    fms = fm.group(1) if fm else ""
    mod = re.search(r"^module:\s*(\S+)", fms, re.M)
    grp = re.search(r"^group:\s*(\S+)", fms, re.M)
    modv = mod.group(1) if mod else "?"
    grpv = grp.group(1) if grp else "?"
    if modv != "nanbeichao-emperors":
        out.append(f"  !! module={modv}"); ALL_OK = ok = False
    if grpv != "nanbeichao-main":
        out.append(f"  !! group={grpv}"); ALL_OK = ok = False
    out.append(f"  module={modv} group={grpv} 诚实边界x{cnt}")
    out.append("  OK" if ok else "  *** FAIL ***")

print("\n".join(out))
print("\n=== ALL_OK:", ALL_OK, "===")

logp = os.path.join(os.path.dirname(__file__), "_verify_bei1.txt")
open(logp, "w", encoding="utf-8").write("\n".join(out) + f"\n=== ALL_OK: {ALL_OK} ===")
