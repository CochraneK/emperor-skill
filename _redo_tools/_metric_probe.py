# -*- coding: utf-8 -*-
"""为「2.5KB 是否合理」提供决策数据 + 落实「⑧按⑫执行」。
统计 1：每份底稿「带可信度前缀」的条目数（信息量，而非字数）
统计 2：SKILL.md 的证据回溯标记（据 0X 稿）数 —— ⑧的主判据
统计 3：倒序判定改为只读固化快照（不再实时算 mtime）
模拟：若新增「每份底稿 ≥N 条带出处条目」，通过率如何变化
输出 _redo_tools/_metric_probe.txt
"""
import pathlib, re, statistics

ES = pathlib.Path(r"D:/2026/WB项目/emperor-skill")
DIMS = ["01-writings", "02-conversations", "03-expression-dna",
        "04-external-views", "05-decisions", "06-timeline"]
MARK = re.compile(r"【(?:原话|史料原文|框架推断|史论)[^】]*】")
TRACE = re.compile(r"据\s*0[1-6]\s*稿")

# 读固化快照（倒序 39）
snap = set()
sf = ES / "_redo_tools/_order_suspects_39.md"
if sf.exists():
    for line in sf.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*([a-z]+)\s*\|\s*([a-z0-9\-]+)-perspective\s*\|", line)
        if m:
            snap.add((m.group(1), m.group(2) + "-perspective"))

rows = []
for d in sorted([p for p in (ES / "skills").iterdir() if p.is_dir()]):
    for p in sorted([x for x in d.iterdir() if x.is_dir()]):
        if not (p / "SKILL.md").exists():
            continue
        per, sizes = [], []
        for n in DIMS:
            f = p / "references/research" / (n + ".md")
            if not f.exists():
                per.append(0); sizes.append(0); continue
            t = f.read_text(encoding="utf-8", errors="ignore")
            lines = [l for l in t.splitlines() if MARK.search(l)]
            per.append(len(lines)); sizes.append(f.stat().st_size)
        t = (p / "SKILL.md").read_text(encoding="utf-8", errors="ignore")
        rows.append(dict(dyn=d.name, sid=p.name, items=min(per), itemsum=sum(per),
                         size=min(sizes), trace=len(TRACE.findall(t)),
                         susp=(d.name, p.name) in snap))

out = []
def w(s=""): out.append(str(s))
items_all = [r["items"] for r in rows]
w("== 1. 每包「最薄的那份底稿」里，带可信度前缀的条目数 ==")
w(f"   包数 {len(rows)}，最少 {min(items_all)} 条，中位 {int(statistics.median(items_all))} 条，最多 {max(items_all)} 条")
w("   分布（最薄底稿的条目数 → 包数）：")
hist = {}
for v in items_all:
    hist[v] = hist.get(v, 0) + 1
for k in sorted(hist):
    w(f"     {k:>2} 条 : {hist[k]:>3} 包  {'█'*min(40,hist[k])}")
w("")
w("== 2. 模拟：若新增「每份底稿 ≥N 条带出处条目」，全仓通过率 ==")
for n in [3, 4, 5, 6, 8, 10]:
    ok = sum(1 for r in rows if r["items"] >= n)
    w(f"   ≥{n:>2} 条 → 通过 {ok}/{len(rows)}  ({ok/len(rows):.0%})")
w("")
w("== 3. 同时看「字数 ≥2.5KB」与「条目数 ≥N」的组合 ==")
for n in [5, 6, 8]:
    both = sum(1 for r in rows if r["items"] >= n and r["size"] >= 2500)
    w(f"   字数达标 且 ≥{n} 条 → {both}/{len(rows)} ({both/len(rows):.0%})")
w("")
w("== 4. ⑧按⑫执行：SKILL.md 证据回溯标记（据 0X 稿）==")
tr = [r["trace"] for r in rows]
zero = [r for r in rows if r["trace"] == 0]
w(f"   有回溯标记的包 {len(rows)-len(zero)}/{len(rows)}，无标记 {len(zero)} 个")
w(f"   标记数：中位 {int(statistics.median(tr))}，最多 {max(tr)}")
w("   ⚠ 无回溯标记 ≠ 倒序：多数早期包只是没写标记。故⑧的落地动作是——")
w("      新包/重写包必须带标记；存量包按「倒序快照 39 + 待重来 92」两个队列处理，")
w("      不因「无标记」单独判负。")
w("")
w("== 5. 倒序队列（只读固化快照，共 %d 个）==" % len(snap))
for dyn, sid in sorted(snap):
    r = next((x for x in rows if x["dyn"] == dyn and x["sid"] == sid), None)
    tag = "（同时底稿薄）" if r and r["size"] < 2500 else ""
    w(f"   [{dyn}] {sid}{tag}")
(ES / "_redo_tools/_metric_probe.txt").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out[:14]))
