# -*- coding: utf-8 -*-
"""全包年份盘点：统计每个商包内出现的所有绝对年份（前XXXX / 公元前XXXX），
按文件归类，输出行样例，供人工核定替换映射。
"""
import os, re, collections

BASE = r"D:/2026/WB项目/emperor-skill/skills/shang"
OUT = r"D:/2026/WB项目/emperor-skill/_redo_tools/_yearscan.txt"

# 商王世次（与 _era_check.py 一致）
ORDER = [
    "tang-shang-perspective", "taiding-shang-perspective", "waibing-perspective",
    "zhongren-shang-perspective", "taijia-perspective", "woding-perspective",
    "taigeng-perspective", "xiaojia-shang-perspective", "yongji-perspective",
    "taiwu-perspective", "zhongding-perspective", "wairen-perspective",
    "hedanja-perspective", "zuyi-perspective", "zuxin-perspective",
    "wojia-perspective", "zuding-shang-perspective", "nangeng-perspective",
    "yangjia-perspective", "pangeng-perspective", "xiaoxin-shang-perspective",
    "xiaoyi-shang-perspective", "wuding-perspective", "zugeng-perspective",
    "zujia-perspective", "linxin-perspective", "kangding-perspective",
    "wuyi-perspective", "wending-shang-perspective", "diyi-perspective",
    "dixin-perspective",
]

YEAR_RE = re.compile(r"(?:公元前|前)\s?([1-2]\d{3})")
# 世纪式表述
CENT_RE = re.compile(r"前?\s?(\d{1,2})\s?世纪")

BUF = []
def w(s=""):
    BUF.append(s)

for pkg in ORDER:
    d = os.path.join(BASE, pkg)
    if not os.path.isdir(d):
        w(f"!! 缺失目录 {pkg}")
        continue
    files = []
    for root, _, fs in os.walk(d):
        for f in fs:
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, d).replace("\\", "/")
            if rel.startswith("scripts/"):
                continue
            files.append((rel, fp))
    files.sort()
    w("=" * 100)
    w(f"### {pkg}")
    total = collections.Counter()
    for rel, fp in files:
        t = open(fp, encoding="utf-8", errors="replace").read()
        yrs = YEAR_RE.findall(t)
        cens = CENT_RE.findall(t)
        if not yrs and not cens:
            continue
        c = collections.Counter(yrs)
        total.update(c)
        w(f"  --- {rel}  (年份 {len(yrs)} 处 / 世纪式 {len(cens)} 处)")
        w(f"      年份: {dict(sorted(c.items()))}")
        if cens:
            w(f"      世纪: {dict(collections.Counter(cens))}")
        # 行样例（前 4 条含年份的行）
        shown = 0
        for i, line in enumerate(t.splitlines(), 1):
            if YEAR_RE.search(line) or CENT_RE.search(line):
                w(f"        L{i}: {line.strip()[:150]}")
                shown += 1
                if shown >= 4:
                    break
    w(f"  >>> 汇总年份: {dict(sorted(total.items()))}")
    w()

Path = None
open(OUT, "w", encoding="utf-8").write("\n".join(BUF))
print("written", OUT, len(BUF), "lines")
