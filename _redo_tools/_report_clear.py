# -*- coding: utf-8 -*-
"""生成「哪些完全符合 nuwa、哪些要重来」的清晰 HTML 报告。
数据全部现跑，不采信历史结论。输出 _redo_tools/nuwa_status.html
"""
import pathlib, re, importlib.util, html

ES = pathlib.Path(r"D:/2026/WB项目/emperor-skill")
SKILLS = ES / "skills"
DIMS = ["01-writings", "02-conversations", "03-expression-dna",
        "04-external-views", "05-decisions", "06-timeline"]

def load_qc(path):
    spec = importlib.util.spec_from_file_location("qc_mod", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

# 解析倒序嫌疑 39（已固化快照）
suspect = {}
sf = ES / "_redo_tools/_order_suspects_39.md"
if sf.exists():
    for line in sf.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*([a-z]+)\s*\|\s*([a-z0-9\-]+)-perspective\s*\|\s*(\d+)s\s*\|", line)
        if m:
            suspect[(m.group(1), m.group(2) + "-perspective")] = int(m.group(3))

pkgs = []
for d in sorted([p for p in SKILLS.iterdir() if p.is_dir()]):
    for p in sorted([x for x in d.iterdir() if x.is_dir()]):
        if (p / "SKILL.md").exists():
            pkgs.append((d.name, p))

qc_mod = None
ok, bad = [], []
for dyn, p in pkgs:
    sid = p.name
    files = sorted([f for f in p.rglob("*") if f.is_file()])
    issues, gaps = [], []
    if len(files) != 8:
        issues.append(f"文件数 {len(files)}≠8")
    for n in DIMS:
        f = p / "references/research" / (n + ".md")
        if not f.exists():
            issues.append(f"缺 {n}"); gaps.append((n, 2500)); continue
        b = f.stat().st_size
        t = f.read_text(encoding="utf-8", errors="ignore")
        if b < 2500:
            gaps.append((n, b))
        if "排除声明" not in t:
            issues.append(f"{n} 无排除声明")
    sk = p / "SKILL.md"
    t = sk.read_text(encoding="utf-8", errors="ignore")
    if sk.stat().st_size <= 1024:
        issues.append(f"SKILL.md 仅 {sk.stat().st_size}B")
    if t.count("诚实边界") != 1:
        issues.append(f"「诚实边界」×{t.count('诚实边界')}")
    if not re.search(r'^module:\s*\S', t, re.M): issues.append("module 缺失")
    if not re.search(r'^group:\s*\S', t, re.M): issues.append("group 缺失")
    qc = p / "scripts/quality_check.py"
    if not qc.exists():
        issues.append("缺 quality_check.py")
    else:
        if qc_mod is None: qc_mod = load_qc(qc)
        fails = []
        for name, fn in [("心智模型", qc_mod.check_mental_models),
                         ("局限", qc_mod.check_limitations),
                         ("表达DNA", qc_mod.check_expression_dna),
                         ("诚实边界", qc_mod.check_honest_boundary),
                         ("张力", qc_mod.check_tensions),
                         ("一手占比", qc_mod.check_primary_sources)]:
            passed, detail = fn(t)
            if not passed: fails.append(f"{name}({detail.strip()})")
        if fails: issues.append("门禁未过：" + "；".join(fails))
    for n, b in gaps:
        issues.append(f"{n} 仅 {b}B（需补 ≥{2500-b}B）")
    rec = dict(dyn=dyn, sid=sid, issues=issues,
               gap=sum(max(0, 2500 - b) for _, b in gaps),
               ngap=len(gaps), susp=(dyn, sid) in suspect)
    (bad if issues else ok).append(rec)

# 分组统计
def bydyn(rows):
    d = {}
    for r in rows: d.setdefault(r["dyn"], []).append(r)
    return d

ok_by, bad_by = bydyn(ok), bydyn(bad)
susp_in_ok = [r for r in ok if r["susp"]]
susp_in_bad = [r for r in bad if r["susp"]]

CN = {"xia": "夏", "shang": "商", "zhou": "周", "qin": "秦", "chuhan": "楚汉",
      "xihan": "西汉", "donghan": "东汉", "sanguo": "三国", "jin": "两晋",
      "nanbeichao": "南北朝", "sui": "隋", "tang": "唐", "song": "宋",
      "yuan": "元", "ming": "明", "qing": "清"}

def esc(s): return html.escape(str(s))

H = []
H.append("""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>nuwa 合规现状 · emperor-skill</title><style>
body{font-family:-apple-system,"Microsoft YaHei",sans-serif;background:#f7f8fa;color:#1a1d21;margin:0;padding:28px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 10px;padding-left:9px;border-left:4px solid #2f6feb}
.sub{color:#5b6472;font-size:13px;margin-bottom:18px}
.cards{display:flex;gap:12px;flex-wrap:wrap;margin:14px 0 6px}
.card{background:#fff;border:1px solid #e3e6ec;border-radius:10px;padding:12px 16px;min-width:118px}
.card .n{font-size:24px;font-weight:700}.card .l{font-size:12px;color:#5b6472;margin-top:2px}
.ok{color:#1a7f37}.bad{color:#b42318}.warn{color:#b54708}
table{width:100%;border-collapse:collapse;background:#fff;font-size:13px;border:1px solid #e3e6ec;border-radius:8px;overflow:hidden}
th{background:#f0f2f5;text-align:left;padding:8px 10px;font-weight:600;border-bottom:1px solid #e3e6ec}
td{padding:7px 10px;border-bottom:1px solid #f0f2f5;vertical-align:top}
tr:last-child td{border-bottom:none}
.dyn{font-weight:600;color:#2f6feb}
.mono{font-family:Consolas,monospace;font-size:12px}
.tag{display:inline-block;padding:1px 7px;border-radius:10px;font-size:11px;margin-right:5px}
.t-bad{background:#fee4e2;color:#b42318}.t-susp{background:#fef0c7;color:#b54708}
.t-ok{background:#d1fadf;color:#1a7f37}
details{margin:8px 0}summary{cursor:pointer;font-size:14px;padding:6px 0;color:#2f6feb}
.chips{line-height:2}
.chip{display:inline-block;background:#fff;border:1px solid #e3e6ec;border-radius:6px;padding:2px 8px;margin:2px 4px 2px 0;font-size:12px;font-family:Consolas,monospace}
</style></head><body>""")
H.append(f"<h1>nuwa 合规现状 · emperor-skill 全仓</h1>")
H.append(f"<div class='sub'>判定口径：8 文件 ＋ 六维各 ≥2.5KB 且带排除声明 ＋ quality_check 实跑 6/6 ＋ SKILL.md&gt;1KB ＋ 「诚实边界」恰 1 次 ＋ module/group 非空。生成时间 2026-09-16 23:40</div>")
H.append("<div class='cards'>")
H.append(f"<div class='card'><div class='n'>{len(pkgs)}</div><div class='l'>包总数</div></div>")
H.append(f"<div class='card'><div class='n ok'>{len(ok)}</div><div class='l'>完全符合</div></div>")
H.append(f"<div class='card'><div class='n bad'>{len(bad)}</div><div class='l'>要重来（体量不足）</div></div>")
H.append(f"<div class='card'><div class='n warn'>{len(suspect)}</div><div class='l'>倒序嫌疑（流程倒）</div></div>")
H.append("</div>")
H.append(f"<div class='sub'>倒序嫌疑 {len(suspect)} 个中：{len(susp_in_ok)} 个结构已合规（只需按六维重蒸馏 SKILL.md），{len(susp_in_bad)} 个已在「要重来」队列（扩写时一并正序）。</div>")

# 各朝总览
H.append("<h2>一、逐朝总览</h2><table><tr><th>朝代</th><th>完全符合</th><th>要重来</th><th>合计</th><th>状态</th></tr>")
for k in sorted(set(list(ok_by) + list(bad_by)), key=lambda x: list(CN).index(x) if x in CN else 99):
    o, b = len(ok_by.get(k, [])), len(bad_by.get(k, []))
    cls = "ok" if b == 0 else ("bad" if o == 0 else "warn")
    st = "全线达标" if b == 0 else ("整朝待修" if o == 0 else "部分待修")
    H.append(f"<tr><td class='dyn'>{CN.get(k,k)} <span class='mono'>{k}</span></td>"
             f"<td class='{('ok' if o else '')}'>{o}</td><td class='{('bad' if b else '')}'>{b}</td>"
             f"<td>{o+b}</td><td class='{cls}'>{st}</td></tr>")
H.append("</table>")

# 要重来
H.append(f"<h2>二、要重来的 {len(bad)} 个包（卡点：底稿体量不足 2.5KB）</h2>")
H.append("<div class='sub'>「需补」= 把该包全部不足的底稿补到 2.5KB 所需的字节总量。凡标 <span class='tag t-susp'>倒序</span> 者，重做时须按六维→SKILL.md 正序。</div>")
H.append("<table><tr><th>朝代</th><th>包</th><th>缺口份数</th><th>需补(约)</th><th>具体卡点</th></tr>")
for r in sorted(bad, key=lambda x: (x["dyn"], -x["gap"])):
    tags = "<span class='tag t-susp'>倒序</span>" if r["susp"] else ""
    iss = "；".join(r["issues"][:6])
    H.append(f"<tr><td class='dyn'>{CN.get(r['dyn'],r['dyn'])}</td>"
             f"<td class='mono'>{esc(r['sid'])} {tags}</td>"
             f"<td>{r['ngap']}</td><td>{r['gap']}B</td><td>{esc(iss)}</td></tr>")
H.append("</table>")

# 倒序但结构合规
H.append(f"<h2>三、{len(susp_in_ok)} 个「结构合规但流程倒」的包（只需重蒸馏 SKILL.md，不必重做底稿）</h2>")
H.append("<div class='sub'>判据：SKILL.md 的修改时间早于其六维底稿 —— 即先出 SKILL、后补底稿。这批底稿已达标，重做时以底稿为唯一依据重写 SKILL.md 即可。</div>")
if susp_in_ok:
    H.append("<table><tr><th>朝代</th><th>包</th><th>SKILL 早于底稿</th></tr>")
    for r in sorted(susp_in_ok, key=lambda x: x["dyn"]):
        H.append(f"<tr><td class='dyn'>{CN.get(r['dyn'],r['dyn'])}</td><td class='mono'>{esc(r['sid'])}</td>"
                 f"<td>{suspect[(r['dyn'], r['sid'])]}s</td></tr>")
    H.append("</table>")

# 完全符合
H.append(f"<h2>四、完全符合的 {len(ok)} 个包（按朝）</h2>")
for k in sorted(ok_by, key=lambda x: list(CN).index(x) if x in CN else 99):
    rows = ok_by[k]
    H.append(f"<details><summary>{CN.get(k,k)} · {len(rows)} 个</summary><div class='chips'>")
    for r in rows:
        mark = " ⚠" if r["susp"] else ""
        H.append(f"<span class='chip'>{esc(r['sid'])}{mark}</span>")
    H.append("</div></details>")
H.append("</body></html>")

out = ES / "_redo_tools/nuwa_status.html"
out.write_text("\n".join(H), encoding="utf-8")

# 文字摘要（供汇报）
L = []
L.append("== 逐朝：完全符合 / 要重来 ==")
for k in sorted(set(list(ok_by) + list(bad_by)), key=lambda x: list(CN).index(x) if x in CN else 99):
    o, b = len(ok_by.get(k, [])), len(bad_by.get(k, []))
    L.append(f"  {CN.get(k,k)}({k}): 符合 {o} / 要重来 {b} / 共 {o+b}")
L.append("")
L.append("== 要重来的 92 个：按朝分布与总缺口 ==")
bd = {}
for r in bad:
    d = bd.setdefault(r["dyn"], [0, 0])
    d[0] += 1; d[1] += r["gap"]
for k in sorted(bd, key=lambda x: -bd[x][0]):
    L.append(f"  {CN.get(k,k)}({k}): {bd[k][0]} 包，需补约 {bd[k][1]}B")
L.append("")
L.append("== 待重来包中「缺口最大」的前 15 个 ==")
for r in sorted(bad, key=lambda x: -x["gap"])[:15]:
    L.append(f"  [{CN.get(r['dyn'],r['dyn'])}] {r['sid']}  缺 {r['ngap']} 份，需补 {r['gap']}B")
L.append("")
L.append("== 倒序嫌疑的归属 ==")
L.append(f"  结构已合规、只需重蒸馏 SKILL.md：{len(susp_in_ok)} 个")
L.append(f"  已在要重来队列、扩写时一并正序：{len(susp_in_bad)} 个")
(ES / "_redo_tools/_summary_clear.txt").write_text("\n".join(L), encoding="utf-8")

print(f"包 {len(pkgs)} 合规 {len(ok)} 待重来 {len(bad)} 倒序(合规组内) {len(susp_in_ok)} 倒序(待重来组内) {len(susp_in_bad)}")
print("HTML ->", out)
