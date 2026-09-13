# -*- coding: utf-8 -*-
"""78 帝 solo 推演 · 总排名报告生成器。

读 travelers/*.json + situations.json + reign_order.json，
产出 simulation/by-dynasty/solo/solo-ranking.html（全库聚合排名与适配度分析）。

用法：
  python eval_solo_rank.py
"""
import collections
import datetime
import json
import os

import eval_crossing_solo as E

ENG = E.ENG
OUTDIR = E.OUTDIR

TYPES = ['创业开国', '平叛戡乱', '削藩集权', '守成休养', '变法理财',
         '开疆边患', '储位继统', '权臣党争', '亡国危局']

CSS_EXTRA = """
.bar{height:9px;border-radius:5px;background:#e5e7eb;overflow:hidden;min-width:60px}
.bar i{display:block;height:100%;border-radius:5px}
.rank{font-weight:600;color:#0f766e}
.chip{display:inline-block;padding:1px 8px;border-radius:20px;font-size:11.5px;margin:0 4px 4px 0}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:760px){.two{grid-template-columns:1fr}}
.tp{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.tp h4{margin:0 0 8px;font-size:13.5px;display:flex;justify-content:space-between}
.tp h4 span{color:var(--mut);font-weight:400;font-size:12px}
.tp ol{margin:0;padding-left:20px;font-size:12.5px}
.tp li{margin:3px 0}
.tp b.s{font-weight:600}
.lead{font-size:13.5px;color:#374151;margin:10px 0 0}
.kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:16px 0}
.kpi .m{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.kpi .l{color:var(--mut);font-size:12px}
.kpi .n{font-size:21px;font-weight:600;margin-top:2px}
.warn{background:#fef6ec;border-left:3px solid #b45309;border-radius:0 8px 8px 0;padding:12px 16px;
  color:#7c2d12;font-size:13px;margin:14px 0}
"""


def collect():
    out = []
    for k in E.all_travelers():
        tv = E.load(k)
        rows = E.build_rows(tv)
        if not rows:
            continue
        by_type = collections.defaultdict(list)
        for r in rows:
            by_type[r['typ']].append(r['score'])
        out.append(dict(
            key=k, cn=tv['cn'], name=tv['name'], dyn=tv['dyn'],
            year=E.yr_of(k), overall=round(sum(r['score'] for r in rows) / len(rows), 1),
            vd=collections.Counter(r['verdict'] for r in rows),
            typeavg={t: round(sum(v) / len(v), 1) for t, v in by_type.items()},
            summary=tv.get('summary', ''), rows=rows))
    return out


def main():
    tvs = collect()
    n = len(tvs)
    all_rows = [r for t in tvs for r in t['rows']]

    # ── 总榜（按均分降序，同分按时间序） ────────────────────────
    rank = sorted(tvs, key=lambda x: (-x['overall'], E.chrono(x['key'])))
    for i, t in enumerate(rank, 1):
        t['rank'] = i

    avgs = [t['overall'] for t in tvs]
    mean_all = sum(avgs) / len(avgs)
    sd = (sum((a - mean_all) ** 2 for a in avgs) / len(avgs)) ** 0.5

    # ── 分档：按均分四档 ────────────────────────────────────
    BANDS = [('强（≥63）', 63, 999), ('中上（60–62.9）', 60, 63),
             ('中（55–59.9）', 55, 60), ('偏弱（<55）', -999, 55)]
    bands = []
    for label, lo, hi in BANDS:
        sub = [t for t in rank if lo <= t['overall'] < hi]
        if sub:
            bands.append((label, sub))

    # ── 按困局类型：谁最会 / 最不会 ──────────────────────────
    tscore = {}
    for t in TYPES:
        lst = [(t2, t2['typeavg'][t]) for t2 in tvs if t in t2['typeavg']]
        lst.sort(key=lambda x: (-x[1], E.chrono(x[0]['key'])))
        tscore[t] = lst

    # ── 朝代构成（穿越者均分的朝内均值） ──────────────────────
    dyn_g = collections.defaultdict(list)
    for t in tvs:
        dyn_g[t['dyn']].append(t['overall'])
    dyn_avg = [(d, round(sum(dyn_g[d]) / len(dyn_g[d]), 1), len(dyn_g[d]))
               for d in E.DYN_ORDER if dyn_g[d]]

    # ── 亡国危局档：结构性困局带 ────────────────────────────
    fg = [(t, t['typeavg']['亡国危局']) for t in tvs if '亡国危局' in t['typeavg']]
    fg.sort(key=lambda x: -x[1])
    fg_vals = [v for _, v in fg]
    fg_mean = sum(fg_vals) / len(fg_vals)
    fg_sd = (sum((v - fg_mean) ** 2 for v in fg_vals) / len(fg_vals)) ** 0.5

    # ── 人定胜负四档极差 ───────────────────────────────────
    gaps = []
    for t in ['守成休养', '变法理财', '权臣党争', '储位继统', '亡国危局']:
        v = [x[1] for x in tscore.get(t, [])]
        if v:
            gaps.append((t, round(sum(v) / len(v), 1), round(max(v) - min(v), 1),
                         tscore[t][-1], tscore[t][0]))

    # ══ HTML ═══════════════════════════════════════════════
    today = datetime.date.today().isoformat()
    P = []
    P.append('<!DOCTYPE html>\n<html lang="zh-CN"><head><meta charset="utf-8">'
             '<meta name="viewport" content="width=device-width,initial-scale=1">')
    P.append('<title>帝王穿越 · 78 帝总排名报告</title>')
    P.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>')
    P.append('<style>' + E.CSS + CSS_EXTRA + '</style></head><body><div class="wrap">')
    P.append('<p class="nav"><a href="solo-index.html">← solo 总目录（按时间顺序）</a>'
             '<a href="solo-lishimin.html">示例报告：李世民</a></p>')
    P.append('<h1>帝王穿越 · 78 帝总排名报告</h1>')
    P.append(f'<p class="sub">数据源：solo 单人轮值全量推演 · {n} 位穿越者 × 77 处境 = '
             f'<b>{len(all_rows)}</b> 条处置 · 评分卡 v0.2（满分 100） · 生成 {today}</p>')
    P.append('<div class="warn"><b>这份排名排的是什么？</b>'
             '排的是<b>「该帝王的心智工具箱」与「其余 77 位帝王的处境」的适配度</b>，'
             '不是历史功绩排名、不是能力高低、更不是史实复原。'
             '分数高 = 他的思维模型在那套处境里更常能落地；分数低 = 他在那类处境里更常无从下手。'
             '两者都不代表他实际执政的水准。</div>')

    P.append('<div class="kpi">'
             f'<div class="m"><div class="l">参评帝王</div><div class="n">{n}</div></div>'
             f'<div class="m"><div class="l">处置总条数</div><div class="n">{len(all_rows)}</div></div>'
             f'<div class="m"><div class="l">全体均分</div><div class="n">{mean_all:.1f}</div></div>'
             f'<div class="m"><div class="l">均分区间</div><div class="n">{min(avgs):.1f}–{max(avgs):.1f}</div></div>'
             f'<div class="m"><div class="l">标准差</div><div class="n">{sd:.2f}</div></div>'
             f'<div class="m"><div class="l">榜首</div><div class="n" style="font-size:16px">'
             f'{rank[0]["cn"]} {rank[0]["overall"]}</div></div>'
             '</div>')

    # 一、Top20 条形
    top20 = rank[:20]
    P.append('<h2>一、前 20 名（平均处置分）</h2>'
             '<div class="panel"><div class="chart" style="height:460px">'
             '<canvas id="top20" role="img" aria-label="前20名平均处置分"></canvas></div></div>')

    # 二、总榜
    def barof(v):
        c = E.VC[E.verdict(v)]
        w = max(2.0, (v - 40) / 30 * 100)
        return f'<div class="bar"><i style="width:{min(w,100):.1f}%;background:{c}"></i></div>'

    trs = ''
    for t in rank:
        vd = t['vd']
        trs += (f'<tr><td class="rank">{t["rank"]}</td>'
                f'<td class="k">{t["year"]}</td>'
                f'<td class="k"><a href="solo-{t["key"]}.html">{t["cn"]}</a></td>'
                f'<td>{t["dyn"]}·{t["name"]}</td>'
                f'<td class="sc" style="color:{E.VC[E.verdict(t["overall"])]}">{t["overall"]}</td>'
                f'<td style="width:90px">{barof(t["overall"])}</td>'
                f'<td class="sc">{vd.get("可解",0)}</td><td class="sc">{vd.get("可缓",0)}</td>'
                f'<td class="sc">{vd.get("难解",0)}</td><td class="sc">{vd.get("死局",0)}</td>'
                f'<td class="d">{t["summary"][:44]}</td></tr>')
    P.append(f'<h2>二、总榜（{n} 位 · 按平均处置分降序）</h2>'
             '<div class="panel" style="padding:12px 14px;margin-bottom:12px">'
             '<span style="font-size:12.5px;color:var(--mut)">'
             '「即位」为该帝王即位之年（公元）；「可解/可缓/难解/死局」为其 77 条处置的档位计数；'
             '点击姓名进入该帝王的逐处境报告。同分者按时间先后排。</span></div>'
             '<table><thead><tr><th>名次</th><th>即位</th><th>穿越者</th><th>朝代·庙号</th>'
             '<th>均分</th><th></th><th>可解</th><th>可缓</th><th>难解</th><th>死局</th><th>总断</th>'
             f'</tr></thead><tbody>{trs}</tbody></table>')

    # 三、分档
    P.append('<h2>三、分档一览</h2>')
    for label, sub in bands:
        chips = ''.join(f'<span class="chip" style="background:{E.VC[E.verdict(x["overall"])]}1a;'
                        f'color:{E.VC[E.verdict(x["overall"])]}">{x["cn"]} {x["overall"]}</span>'
                        for x in sub)
        P.append(f'<div class="tp" style="margin-bottom:12px"><h4>{label}'
                 f'<span>{len(sub)} 位</span></h4>{chips}</div>')

    # 四、按困局类型的适配排行
    P.append('<h2>四、按困局类型的适配排行 · 谁最会什么</h2>'
             '<div class="panel" style="padding:12px 14px;margin-bottom:12px">'
             '<span style="font-size:12.5px;color:var(--mut)">'
             '每类取该类型平均处置分最高/最低各 5 位。'
             '跨人极差越大，说明这一类越是「人定胜负」；极差越小，说明处境本身的结构压力越强。</span></div>')
    P.append('<div class="two">')
    for t in TYPES:
        lst = tscore[t]
        v = [x[1] for x in lst]
        gap = max(v) - min(v)
        hi = ''.join(f'<li>{x[0]["cn"]}（{x[0]["dyn"]}·{x[0]["name"]}）'
                     f'<b class="s" style="color:{E.VC[E.verdict(x[1])]}"> {x[1]}</b></li>'
                     for x in lst[:5])
        lo = ''.join(f'<li>{x[0]["cn"]}（{x[0]["dyn"]}·{x[0]["name"]}）'
                     f'<b class="s" style="color:{E.VC[E.verdict(x[1])]}"> {x[1]}</b></li>'
                     for x in lst[-5:][::-1])
        P.append(f'<div class="tp"><h4>{t}<span>全库 {sum(v)/len(v):.1f} · 极差 {gap:.1f}</span></h4>'
                 f'<div style="font-size:12px;color:#0f766e;margin-bottom:2px">最能接住</div>'
                 f'<ol>{hi}</ol>'
                 f'<div style="font-size:12px;color:#a83232;margin:8px 0 2px">最接不住</div>'
                 f'<ol>{lo}</ol></div>')
    P.append('</div>')

    # 五、结构约束 vs 人定胜负
    grows = ''.join(
        f'<tr><td>{t}</td><td class="sc">{m:.1f}</td>'
        f'<td class="sc" style="color:{E.VC[E.verdict(m)]}">{g:.1f}</td>'
        f'<td class="k">{lo[0]["cn"]} {lo[1]}</td>'
        f'<td class="k">{hi[0]["cn"]} {hi[1]}</td></tr>'
        for t, m, g, lo, hi in gaps)
    P.append('<h2>五、结构约束 vs 人定胜负</h2>'
             '<div class="panel" style="padding:12px 14px;margin-bottom:12px">'
             '<span style="font-size:12.5px;color:var(--mut)">'
             '极差 = 该类最高与最低之差。人定胜负档极差应为结构性档的 2–3 倍。</span></div>'
             '<table><thead><tr><th>困局类型</th><th>全库均分</th><th>跨人极差</th>'
             f'<th>最低</th><th>最高</th></tr></thead><tbody>{grows}</tbody></table>')

    # 六、亡国危局带
    P.append(f'<h2>六、亡国危局档 · 结构性困局的分数带</h2>'
             f'<div class="panel"><div class="chart" style="height:520px">'
             f'<canvas id="fg" role="img" aria-label="亡国危局档各人平均分"></canvas></div>'
             f'<p class="lead">{n} 位穿越者在这一类上的平均分全部落在 '
             f'<b>{min(fg_vals):.1f}–{max(fg_vals):.1f}</b>（极差 {max(fg_vals)-min(fg_vals):.1f}、'
             f'标准差 {fg_sd:.2f}）。<b>没有人突破 52</b> —— '
             f'说明「亡国危局」这一档的分数由处境本身的结构压力决定，换谁进去都难以拉开差距；'
             f'最高为 {fg[0][0]["cn"]}（{fg[0][1]}），最低为 {fg[-1][0]["cn"]}（{fg[-1][1]}）。</p></div>')

    # 七、朝代构成
    P.append('<h2>七、五朝穿越者均分（构成量，非朝代强弱）</h2>'
             '<div class="panel"><div class="meta">'
             + ''.join(f'<div class="m"><div class="l">{d}（{c} 位）</div>'
                       f'<div class="n">{v}</div></div>' for d, v, c in dyn_avg)
             + '</div><p class="lead"><b>不要把这个当成「哪个朝代更强」。</b>'
               '它只反映「本库收录的该朝帝王，其工具箱与这套处境的平均适配度」——'
               '收录名单本身就是选择的结果：唐收录了 21 位（含唐末一批幼主与傀儡），'
               '清收录了 12 位（含清末三位幼帝）。名单一变，这个数就变。</p></div>')

    P.append('<div class="foot">'
             '<b>排序与口径</b>：均分 = 该帝王 77 条处置分的算术平均；'
             '档位 可解≥75 / 可缓 65–74 / 难解 50–64 / 死局&lt;50；'
             '按困局类型的分组依据受控词表 9 类。<br>'
             '<b>三个必须知道的口径限制</b>：<br>'
             '① <b>类型均分是混合量</b>——它同时反映「处境难度」与「参评者构成」。'
             '实证：「创业开国」在李世民单体基线上排第 1（78.3），扩到全库降到第 5（61.5），'
             '只因全库多了 20 余位对该类几乎无策的幼主。不可当纯难度读。<br>'
             '② <b>底部塌陷</b>——亡国危局档 78 人全压 39–52，组内分辨力接近地板，'
             '「还能撑三年」与「明年就亡」在此不可分。评分卡的去结局化改造正是为此。<br>'
             '③ <b>诚实边界</b>——这是一次思想实验式的反事实推演，非史实复原。'
             '「某帝若在其位能否办好」无法被证实或证伪；分数表达的是心智工具与处境的适配度，'
             '不是对该帝王实际政绩的褒贬。<br>'
             '生成器：<code>_engine/eval_solo_rank.py</code>；结构质检 <code>check_solo.py</code>、'
             '交叉检验 <code>cross_check_solo.py</code>。</div>')

    # scripts
    P.append('</div><script>')
    P.append('new Chart(document.getElementById("top20"),{type:"bar",data:{labels:'
             + json.dumps([f'{t["cn"]} {t["overall"]}' for t in top20])
             + ',datasets:[{data:' + json.dumps([t['overall'] for t in top20])
             + ',backgroundColor:' + json.dumps([E.DN[t['dyn']] for t in top20])
             + ',borderRadius:4}]},options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,'
               'scales:{x:{min:50,max:70,grid:{color:"#e5e7eb"}}},'
               'plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.parsed.x+" 分"}}}}});')
    P.append('new Chart(document.getElementById("fg"),{type:"bar",data:{labels:'
             + json.dumps([f'{t["cn"]}' for t, _ in fg])
             + ',datasets:[{data:' + json.dumps([v for _, v in fg])
             + ',backgroundColor:' + json.dumps([E.DN[t['dyn']] for t, _ in fg])
             + ',borderRadius:3}]},options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,'
               'scales:{x:{min:35,max:55,grid:{color:"#e5e7eb"}}},'
               'plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.parsed.x+" 分"}}}}});')
    P.append('</script></body></html>')

    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, 'solo-ranking.html')
    open(out, 'w', encoding='utf-8').write(''.join(P))
    print('ranking ->', out, n, '位')
    return out


if __name__ == '__main__':
    main()
