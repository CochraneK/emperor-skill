# -*- coding: utf-8 -*-
"""「帝王穿越 · solo」通用渲染器。

solo = 单人轮值：一位穿越者，单独遍历其余 77 个处境，不与任何人对照。
（双人对抗属 duel、双人合作属 coop，不在本脚本职责内。）

用法：
  python eval_crossing_solo.py --all        渲染 travelers/ 下全部穿越者
  python eval_crossing_solo.py <key> ...    只渲染指定穿越者
  python eval_crossing_solo.py --index      只重建 solo-index.html 总目录

数据：
  situations.json        78 个处境（key/name/dyn/typ/dilemma）
  travelers/<key>.json   穿越者 {key,name,cn,dyn,tagline,summary,rows:{处境key:{plan,score,note}}}
产物：
  simulation/by-dynasty/solo/solo-<key>.html
  simulation/by-dynasty/solo/solo-index.html
"""

import collections
import datetime
import glob
import json
import os
import sys

ENG = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(ENG))
TV = os.path.join(ENG, 'travelers')
OUTDIR = os.path.join(REPO, 'simulation', 'by-dynasty', 'solo')

SITS = json.load(open(os.path.join(ENG, 'situations.json'), encoding='utf-8'))
SIT = {s['key']: s for s in SITS}
DYN_ORDER = ['唐', '宋', '元', '明', '清']

# 即位年表：{key: [year, seq]}。用于「按时间顺序」呈现。
_RO = json.load(open(os.path.join(ENG, 'reign_order.json'), encoding='utf-8'))
REIGN = {k: tuple(v) for k, v in _RO['order'].items()}
SIT_YEAR = {k: REIGN.get(k, (9999, 0))[0] for k in SIT}


def chrono(k):
    """时间序键：朝代先后 → 即位年 → 同年次序 → key。未知者排在最后。"""
    s = SIT.get(k)
    dyn = DYN_ORDER.index(s['dyn']) if s and s['dyn'] in DYN_ORDER else 99
    yr, sq = REIGN.get(k, (9999, 0))
    return (dyn, yr, sq, k)


def yr_of(k):
    y = SIT_YEAR.get(k, 9999)
    return '—' if y == 9999 else str(y)

VC = {'可解': '#0f766e', '可缓': '#2563eb', '难解': '#b45309', '死局': '#a83232'}
DN = {'唐': '#b45309', '宋': '#0f766e', '元': '#1d4ed8', '明': '#a83232', '清': '#6d28d9'}


def verdict(s):
    return '可解' if s >= 75 else '可缓' if s >= 65 else '难解' if s >= 50 else '死局'


def load(key):
    return json.load(open(os.path.join(TV, key + '.json'), encoding='utf-8'))


def build_rows(tv):
    """把 traveler 的 rows 展开为**按时间顺序**（朝代 → 即位年 → 同年次序）排列的记录表。

    rows 支持两种写法：
      {"<处境key>": {"plan":…, "score":…, "note":…}}   （迁移自旧报告）
      {"<处境key>": ["策", 分, "断语"]}                 （worker 产出的紧凑格式）
    """
    out = []
    for k, cell in tv['rows'].items():
        s = SIT.get(k)
        if s is None:
            continue
        if isinstance(cell, (list, tuple)):
            plan, sc, note = cell[0], cell[1], cell[2]
        else:
            plan, sc, note = cell.get('plan', ''), cell['score'], cell.get('note', '')
        sc = int(sc)
        out.append(dict(key=k, name=s['name'], dyn=s['dyn'], typ=s['typ'], dilemma=s['dilemma'],
                        year=yr_of(k), plan=plan, note=note, score=sc, verdict=verdict(sc)))
    out.sort(key=lambda r: chrono(r['key']))
    return out


CSS = """
:root{--bg:#f6f6f3;--panel:#fff;--ink:#1f2937;--mut:#6b7280;--line:#e5e7eb;--teal:#0f766e}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.7 -apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
.wrap{max-width:1060px;margin:0 auto;padding:32px 24px 64px}
h1{font-size:24px;font-weight:600;margin:0 0 6px}
.sub{color:var(--mut);font-size:13px;margin:0 0 22px}
h2{font-size:17px;font-weight:600;margin:36px 0 14px;padding-left:10px;border-left:3px solid var(--teal)}
.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:16px 0}
.m{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.m .l{color:var(--mut);font-size:12px} .m .n{font-size:21px;font-weight:600;margin-top:2px}
.quote{background:#eff6f4;border-left:3px solid var(--teal);border-radius:0 8px 8px 0;padding:14px 18px;color:#134e4a;font-size:13.5px;margin:14px 0}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px}
.chart{position:relative;height:280px}
table{width:100%;border-collapse:collapse;font-size:12.5px;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden}
th,td{padding:7px 9px;border-bottom:1px solid var(--line);text-align:left}
td.sc{text-align:center;font-weight:600} th{background:#f0f1ef;font-weight:500;color:var(--mut)}
td.k{font-family:ui-monospace,Consolas,monospace;font-size:11.5px;white-space:nowrap}
td.d{color:#4b5563;max-width:340px}
tr:hover td{background:#fafaf8}
.vd{display:inline-block;padding:1px 8px;border-radius:20px;font-size:12px;font-weight:500}
h3.dyn{font-size:15px;font-weight:600;margin:26px 0 12px;display:flex;align-items:center;gap:8px}
h3.dyn span{width:10px;height:10px;border-radius:3px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:13px 15px}
.ch{display:flex;align-items:center;gap:8px}
.nm{font-weight:600} .kk{font-family:ui-monospace,Consolas,monospace;font-size:11px;color:var(--mut);flex:1}
.sco{font-weight:600;font-size:15px}
.typ{color:var(--mut);font-size:11.5px;margin:4px 0 7px}
.card p{margin:0 0 5px;font-size:12.5px;color:#374151} .card p b{color:#111827;font-weight:500}
.card .nt{color:var(--teal);font-size:12.5px}
.foot{color:var(--mut);font-size:12px;margin-top:28px;border-top:1px solid var(--line);padding-top:16px}
.nav{font-size:12.5px;margin:0 0 18px}
.nav a{color:var(--teal);text-decoration:none;margin-right:14px}
"""


def render(tv):
    key = tv['key']
    rows = build_rows(tv)
    n = len(rows)
    by_type = collections.defaultdict(list)
    for r in rows:
        by_type[r['typ']].append(r['score'])
    type_avg = sorted([(t, round(sum(v) / len(v), 1), len(v)) for t, v in by_type.items()], key=lambda x: -x[1])
    by_dyn = collections.defaultdict(list)
    for r in rows:
        by_dyn[r['dyn']].append(r['score'])
    dyn_avg = [(d, round(sum(by_dyn[d]) / len(by_dyn[d]), 1)) for d in DYN_ORDER if by_dyn[d]]
    vdist = collections.Counter(r['verdict'] for r in rows)
    overall = round(sum(r['score'] for r in rows) / n, 1)
    # rows 已按时间顺序；「最能接住/最接不住」按分数另取。
    by_score = sorted(rows, key=lambda r: -r['score'])
    top10, bot10 = by_score[:10], by_score[-10:][::-1]

    def card(r):
        c = VC[r['verdict']]
        return (f'<div class="card"><div class="ch"><span class="nm">{r["name"]}</span>'
                f'<span class="kk">{r["key"]}</span>'
                f'<span class="vd" style="background:{c}1a;color:{c}">{r["verdict"]}</span>'
                f'<span class="sco" style="color:{c}">{r["score"]}</span></div>'
                f'<div class="typ">{r["dyn"]}·{r["name"]} · 即位 {r["year"]} · 困局类型 · {r["typ"]}</div>'
                f'<p><b>处境</b>：{r["dilemma"]}</p>'
                f'<p><b>{tv["name"]}之策</b>：{r["plan"]}</p>'
                f'<p class="nt">{r["note"]}</p></div>')

    def group(d):
        sub = [r for r in rows if r['dyn'] == d]
        if not sub:
            return ''
        return (f'<h3 class="dyn" style="color:{DN[d]}"><span style="background:{DN[d]}"></span>'
                f'{d} · {len(sub)} 处境</h3><div class="grid">' + ''.join(card(r) for r in sub) + '</div>')

    trows = ''.join(
        f'<tr><td>{i}</td><td>{r["dyn"]}</td><td class="k">{r["year"]}</td><td class="k">{r["name"]}</td>'
        f'<td>{r["typ"]}</td>'
        f'<td class="d">{r["dilemma"]}</td><td class="sc" style="color:{VC[r["verdict"]]}">{r["score"]}</td>'
        f'<td><span class="vd" style="background:{VC[r["verdict"]]}1a;color:{VC[r["verdict"]]}">{r["verdict"]}</span></td></tr>'
        for i, r in enumerate(rows, 1))

    def toplist(lst, color):
        return ''.join(
            f'<div style="font-size:13px;padding:4px 0"><b>{i}. {r["name"]}</b>（{r["dyn"]}·{r["typ"]}）'
            f'<span style="color:{color};font-weight:600">{r["score"]}</span> — {r["dilemma"]}</div>'
            for i, r in enumerate(lst, 1))

    today = datetime.date.today().isoformat()
    parts = []
    parts.append('<!DOCTYPE html>\n<html lang="zh-CN"><head><meta charset="utf-8">'
                 '<meta name="viewport" content="width=device-width,initial-scale=1">')
    parts.append(f'<title>帝王穿越处置报告 · {tv["cn"]} × {n} 处境</title>')
    parts.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>')
    parts.append('<style>' + CSS + '</style></head><body><div class="wrap">')
    parts.append('<p class="nav"><a href="solo-index.html">← solo 总目录（78 帝）</a>'
                 '<a href="solo-ranking.html">78 帝总排名报告 →</a></p>')
    parts.append(f'<h1>帝王穿越处置报告 · {tv["cn"]}</h1>')
    parts.append(f'<p class="sub">模式：solo 单人轮值（单独遍历其余 {n} 个处境，无对照）'
                 f' · 穿越者：{tv["cn"]}（{tv["dyn"]}·{tv["name"]}） · 标准：穿越处置评分卡 v0.2（满分 100） · 生成 {today}</p>')
    parts.append(f'<div class="quote">{tv.get("tagline","")}</div>')
    if tv.get('summary'):
        parts.append(f'<div class="quote"><b>总断</b>：{tv["summary"]}</div>')
    parts.append('<div class="meta">'
                 f'<div class="m"><div class="l">穿越目标</div><div class="n">{n}</div></div>'
                 f'<div class="m"><div class="l">平均处置分</div><div class="n">{overall}</div></div>'
                 f'<div class="m"><div class="l">可解 / 可缓</div><div class="n">{vdist.get("可解",0)} / {vdist.get("可缓",0)}</div></div>'
                 f'<div class="m"><div class="l">难解 / 死局</div><div class="n">{vdist.get("难解",0)} / {vdist.get("死局",0)}</div></div>'
                 '</div>')
    parts.append('<h2>一、判定分布与朝代均值</h2>'
                 '<div class="panel"><div class="chart" style="height:250px">'
                 '<canvas id="dist" role="img" aria-label="判定分布环形图"></canvas></div>'
                 '<div class="meta" style="margin-top:14px">'
                 + ''.join(f'<div class="m"><div class="l">{d}处境均分</div><div class="n">{v}</div></div>' for d, v in dyn_avg)
                 + '</div></div>')
    parts.append(f'<h2>二、{tv["name"]}工具箱 · 按困局类型的适配度</h2>'
                 f'<div class="panel"><div class="chart" style="height:{len(type_avg)*34+80}px">'
                 '<canvas id="typebar" role="img" aria-label="各困局类型平均处置分"></canvas></div></div>')
    parts.append(f'<h2>三、{tv["name"]}最能接住的 10 个处境</h2>'
                 f'<div class="panel"><p class="sub" style="margin:0 0 8px">按处置分降序，仅供定位其强项</p>'
                 f'{toplist(top10, "#0f766e")}</div>')
    parts.append(f'<h2>四、{tv["name"]}最接不住的 10 个处境</h2>'
                 f'<div class="panel"><p class="sub" style="margin:0 0 8px">按处置分升序，仅供定位其短板</p>'
                 f'{toplist(bot10, "#a83232")}</div>')
    parts.append(f'<h2>五、处置力总表 · 按时间顺序（{n} 处境）</h2>'
                 f'<div class="panel" style="padding:12px 14px;margin-bottom:12px">'
                 f'<span style="font-size:12.5px;color:var(--mut)">'
                 f'排序规则：朝代先后（唐→宋→元→明→清）→ 该处境帝王的即位年 → 同年次序。'
                 f'「即位」列为该处境所属帝王的即位之年（公元）。</span></div>'
                 '<table><thead><tr>'
                 '<th>#</th><th>朝代</th><th>即位</th><th>帝王</th><th>困局类型</th><th>核心困局</th><th>分</th><th>判定</th>'
                 f'</tr></thead><tbody>{trows}</tbody></table>')
    parts.append('<h2>六、逐帝穿越推演 · 按时间顺序</h2>'
                 '<div class="panel" style="padding:12px 14px;margin-bottom:12px">'
                 '<span style="font-size:12.5px;color:var(--mut)">'
                 '同一下方卡片亦按朝代与即位年排列，可沿时间线自唐至清逐朝看其处置。</span></div>'
                 + ''.join(group(d) for d in DYN_ORDER))
    parts.append('<div class="foot">'
                 '排序：本报告第五节与第六节均按<b>时间顺序</b>呈现（朝代先后 唐→宋→元→明→清，'
                 '朝内按该处境帝王的即位年，同年以次序区分）；第三、四节为按处置分的强弱定位，'
                 '不参与总表排序。<br>'
                 '评分口径：情境识别 25 + 模型迁移 30 + 方案可行性 30 + 角色保真 15，综合判定为单一处置分；'
                 '判定档位 可解≥75 / 可缓 65–74 / 难解 50–64 / 死局&lt;50。<br>'
                 f'诚 实边界：这是一次<b>思想实验式的反事实推演</b>，非史实复原。「{tv["cn"]}若在其位能否办好」'
                 '无法被证实或证伪，分数表达的是「其心智工具与该处境的适配度」，不是对该帝王实际政绩的褒贬。'
                 '本报告为 solo 单人轮值，未与任何其他穿越者对照。</div>')
    parts.append('</div><script>')
    parts.append('new Chart(document.getElementById("dist"),{type:"doughnut",data:{labels:["可解","可缓","难解","死局"],'
                 'datasets:[{data:' + json.dumps([vdist.get('可解', 0), vdist.get('可缓', 0),
                                                  vdist.get('难解', 0), vdist.get('死局', 0)]) +
                 ',backgroundColor:["#0f766e","#2563eb","#b45309","#a83232"],borderWidth:0}]},'
                 'options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:"bottom"}}}});')
    parts.append('new Chart(document.getElementById("typebar"),{type:"bar",data:{labels:'
                 + json.dumps([t for t, _, _ in type_avg]) +
                 ',datasets:[{data:' + json.dumps([a for _, a, _ in type_avg]) +
                 ',backgroundColor:"#0f766e",borderRadius:4}]},'
                 'options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,'
                 'scales:{x:{min:40,max:90,grid:{color:"#e5e7eb"}}},'
                 'plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.parsed.x+" 分"}}}}});')
    parts.append('</script></body></html>')

    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, 'solo-%s.html' % key)
    open(out, 'w', encoding='utf-8').write(''.join(parts))
    return out, dict(n=n, overall=overall, vdist=dict(vdist), dyn=dyn_avg, typ=type_avg)


def all_travelers():
    return sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(TV, '*.json')))


def render_index():
    items = []
    for k in all_travelers():
        tv = load(k)
        rows = build_rows(tv)
        if not rows:
            continue
        overall = round(sum(r['score'] for r in rows) / len(rows), 1)
        vd = collections.Counter(r['verdict'] for r in rows)
        items.append(dict(key=k, cn=tv['cn'], name=tv['name'], dyn=tv['dyn'], n=len(rows),
                          year=yr_of(k),
                          overall=overall, vd=dict(vd), summary=tv.get('summary', '')))
    # 按时间顺序：朝代先后（唐→宋→元→明→清）→ 即位年 → 同年次序
    items.sort(key=lambda x: chrono(x['key']))
    trs = ''.join(
        f'<tr><td>{i}</td><td class="k">{x["year"]}</td>'
        f'<td class="k"><a href="solo-{x["key"]}.html">{x["cn"]}</a></td>'
        f'<td>{x["dyn"]}·{x["name"]}</td><td class="sc">{x["overall"]}</td>'
        f'<td class="sc">{x["vd"].get("可解",0)}</td><td class="sc">{x["vd"].get("可缓",0)}</td>'
        f'<td class="sc">{x["vd"].get("难解",0)}</td><td class="sc">{x["vd"].get("死局",0)}</td>'
        f'<td class="d">{x["summary"][:52]}</td></tr>'
        for i, x in enumerate(items, 1))
    today = datetime.date.today().isoformat()
    html = ('<!DOCTYPE html>\n<html lang="zh-CN"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>帝王穿越 · solo 总目录</title>'
            '<style>' + CSS + '</style></head><body><div class="wrap">'
            '<p class="nav"><a href="solo-ranking.html">78 帝总排名报告 →</a></p>'
            '<h1>帝王穿越 · solo 总目录</h1>'
            f'<p class="sub">单人轮值模式：每位帝王各自单独遍历其余 77 个处境，互不干扰、无对照 · '
            f'已完成 {len(items)} 位 · 生成 {today}</p>'
            '<div class="quote">同一套处境，换不同的工具箱。<b>按时间顺序排列</b>——'
            '朝代先后 唐→宋→元→明→清，朝内按即位年。'
            '「即位」列为该帝王即位之年（公元）；「均分」列为其 77 处境的平均处置分，'
            '分数越高只表示心智工具与该套处境的总体适配度越高，<b>不代表其真实政绩或历史地位排名</b>。</div>'
            '<table><thead><tr><th>#</th><th>即位</th><th>穿越者</th><th>朝代·庙号</th><th>均分</th>'
            '<th>可解</th><th>可缓</th><th>难解</th><th>死局</th><th>总断</th></tr></thead>'
            f'<tbody>{trs}</tbody></table>'
            '<div class="foot">评分口径：情境识别 25 + 模型迁移 30 + 方案可行性 30 + 角色保真 15；'
            '判定档位 可解≥75 / 可缓 65–74 / 难解 50–64 / 死局&lt;50。'
            '诚实边界：反事实思想实验，分数表达心智工具与处境的适配度，非史实复原、非政绩评估。</div>'
            '</div></body></html>')
    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, 'solo-index.html')
    open(out, 'w', encoding='utf-8').write(html)
    return out, items


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or args[0] == '--all':
        keys = all_travelers()
    elif args[0] == '--index':
        p, items = render_index()
        print('index ->', p, len(items), '位')
        sys.exit(0)
    else:
        keys = args
    for k in keys:
        p, st = render(load(k))
        print('%-12s 均分 %5.1f  可解%2d 可缓%2d 难解%2d 死局%2d  -> %s'
              % (k, st['overall'], st['vdist'].get('可解', 0), st['vdist'].get('可缓', 0),
                 st['vdist'].get('难解', 0), st['vdist'].get('死局', 0), os.path.basename(p)))
    if not args or args[0] == '--all':
        p, items = render_index()
        print('index ->', os.path.basename(p), len(items), '位')
