# -*- coding: utf-8 -*-
"""78 帝 solo 推演 · 总排名报告生成器（三级排序维度：全体总分 / 分朝代 / 分模块）。

读 travelers/*.json + situations.json + reign_order.json + modules_solo.json，
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

# 帝王包的模块归属（由 build_module_map.py 从 SKILL.md 抽取，权威字段 module）。
MODS = json.load(open(os.path.join(ENG, 'modules_solo.json'), encoding='utf-8'))

_MOD_PREF = ['donghan-emperors', 'sui-emperors', 'tang-emperors',
             'song-emperors', 'yuan-emperors', 'ming-emperors', 'qing-emperors']
MODULE_ORDER = [m for m in _MOD_PREF if any(v['module'] == m for v in MODS.values())]
MODULE_ORDER += sorted({v['module'] for v in MODS.values()} - set(MODULE_ORDER))

MODULE_CN = {'donghan-emperors': '东汉', 'sui-emperors': '隋', 'tang-emperors': '唐',
             'song-emperors': '宋', 'yuan-emperors': '元', 'ming-emperors': '明',
             'qing-emperors': '清'}


def mod_cn(m):
    return MODULE_CN.get(m, m)


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
.dim{background:#f3f4f6;border:1px dashed var(--line);border-radius:10px;padding:10px 16px;
  color:var(--mut);font-size:12.5px;margin-bottom:12px}
.grp{margin:0 0 26px}
.grp h3{margin:18px 0 8px;font-size:15px;display:flex;align-items:baseline;gap:10px;
  border-left:3px solid #0f766e;padding-left:9px}
.grp h3 span{color:var(--mut);font-weight:400;font-size:12.5px}
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
        sc = [r['score'] for r in rows]
        rec = MODS.get(k, {})
        out.append(dict(
            key=k, cn=tv['cn'], name=tv['name'], dyn=tv['dyn'],
            year=E.yr_of(k),
            module=rec.get('module', '未归类'), group=rec.get('group', ''),
            nrows=len(rows), total=sum(sc), overall=round(sum(sc) / len(sc), 1),
            vd=collections.Counter(r['verdict'] for r in rows),
            typeavg={t: round(sum(v) / len(v), 1) for t, v in by_type.items()},
            summary=tv.get('summary', ''), rows=rows))
    return out


def main():
    tvs = collect()
    n = len(tvs)
    all_rows = [r for t in tvs for r in t['rows']]
    nper = sorted({t['nrows'] for t in tvs})

    # ── ① 全体总榜：按总分降序，同分按时间序 ──────────────────
    rank = sorted(tvs, key=lambda x: (-x['total'], E.chrono(x['key'])))
    for i, t in enumerate(rank, 1):
        t['rank'] = i
    rk_all = {t['key']: i for i, t in enumerate(rank, 1)}

    avgs = [t['overall'] for t in tvs]
    mean_all = sum(avgs) / len(avgs)
    sd = (sum((a - mean_all) ** 2 for a in avgs) / len(avgs)) ** 0.5

    # ── ② 分朝代榜：朝内按总分降序 ─────────────────────────
    dyn_rank = collections.OrderedDict()
    for d in E.DYN_ORDER:
        sub = [t for t in tvs if t['dyn'] == d]
        if not sub:
            continue
        dyn_rank[d] = sorted(sub, key=lambda x: (-x['total'], E.chrono(x['key'])))

    # ── ③ 分模块榜：模块内按总分降序 ───────────────────────
    mod_all = collections.defaultdict(list)
    for k, v in MODS.items():
        mod_all[v['module']].append(k)
    mod_rank = collections.OrderedDict()
    for m in MODULE_ORDER:
        sub = sorted([t for t in tvs if t['module'] == m],
                     key=lambda x: (-x['total'], E.chrono(x['key'])))
        mod_rank[m] = (sub, len(mod_all.get(m, [])))

    # ── ④ 分档：按均分四档 ────────────────────────────────
    BANDS = [('强（≥63）', 63, 999), ('中上（60–62.9）', 60, 63),
             ('中（55–59.9）', 55, 60), ('偏弱（<55）', -999, 55)]
    bands = []
    for label, lo, hi in BANDS:
        sub = [t for t in rank if lo <= t['overall'] < hi]
        if sub:
            bands.append((label, sub))

    # ── ⑤ 按困局类型：谁最会 / 最不会 ──────────────────────
    tscore = {}
    for t in TYPES:
        lst = [(t2, t2['typeavg'][t]) for t2 in tvs if t in t2['typeavg']]
        lst.sort(key=lambda x: (-x[1], E.chrono(x[0]['key'])))
        tscore[t] = lst

    # ── ⑥ 人定胜负四档极差 ───────────────────────────────
    # 口径：均分用「合并口径」（该类型全部处置分合起来求平均，与第五节同源），
    #       极差用「人均口径」（各人的类型均分之间的最高-最低差），二者不可混读。
    pooled = collections.defaultdict(list)
    for r in all_rows:
        pooled[r['typ']].append(r['score'])
    pooled_mean = {t: round(sum(v) / len(v), 1) for t, v in pooled.items()}

    gaps = []
    for t in ['守成休养', '变法理财', '权臣党争', '储位继统', '亡国危局']:
        v = [x[1] for x in tscore.get(t, [])]
        if v:
            gaps.append((t, pooled_mean[t], round(max(v) - min(v), 1),
                         tscore[t][-1], tscore[t][0]))

    # ── ⑦ 亡国危局档：结构性困局带 ────────────────────────
    fg = [(t, t['typeavg']['亡国危局']) for t in tvs if '亡国危局' in t['typeavg']]
    fg.sort(key=lambda x: -x[1])
    fg_vals = [v for _, v in fg]
    fg_mean = sum(fg_vals) / len(fg_vals)
    fg_sd = (sum((v - fg_mean) ** 2 for v in fg_vals) / len(fg_vals)) ** 0.5

    # ── ⑧ 朝代构成量 ─────────────────────────────────────
    dyn_g = collections.defaultdict(list)
    for t in tvs:
        dyn_g[t['dyn']].append(t['overall'])
    dyn_avg = [(d, round(sum(dyn_g[d]) / len(dyn_g[d]), 1), len(dyn_g[d]))
               for d in E.DYN_ORDER if dyn_g[d]]

    # ══ 渲染 ──────────────────────────────────────────────
    def barof(v):
        c = E.VC[E.verdict(v)]
        w = max(2.0, (v - 40) / 30 * 100)
        return f'<div class="bar"><i style="width:{min(w,100):.1f}%;background:{c}"></i></div>'

    def din(t):
        return E.DN.get(t['dyn'], '#9ca3af')

    def row(t, rk=None, module=False, brief=False):
        vd = t['vd']
        s = ''
        if rk is not None:
            s += f'<td class="rank">{rk}</td>'
        s += (f'<td class="k">{t["year"]}</td>'
              f'<td class="k"><a href="solo-{t["key"]}.html">{t["cn"]}</a></td>'
              f'<td>{t["dyn"]}·{t["name"]}</td>')
        if module:
            s += f'<td class="k">{mod_cn(t["module"])}</td>'
        s += (f'<td class="sc">{t["total"]}</td>'
              f'<td class="sc" style="color:{E.VC[E.verdict(t["overall"])]}">{t["overall"]}</td>'
              f'<td style="width:78px">{barof(t["overall"])}</td>'
              f'<td class="sc">{vd.get("可解",0)}</td><td class="sc">{vd.get("可缓",0)}</td>'
              f'<td class="sc">{vd.get("难解",0)}</td><td class="sc">{vd.get("死局",0)}</td>')
        if not brief:
            s += f'<td class="d">{t["summary"][:44]}</td>'
        return f'<tr>{s}</tr>'

    H_SUB = ('<thead><tr><th>名次</th><th>即位</th><th>穿越者</th><th>朝代·庙号</th>'
             '<th>总分</th><th>均分</th><th></th><th>可解</th><th>可缓</th><th>难解</th>'
             '<th>死局</th></tr></thead>')
    H_ALL = H_SUB.replace('</tr></thead>', '<th>总断（一句话）</th></tr></thead>')

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
    P.append(f'<p class="sub">数据源：solo 单人轮值全量推演 · {n} 位穿越者 × {nper[0] if len(nper)==1 else nper} '
             f'处境 = <b>{len(all_rows)}</b> 条处置 · 评分卡 v0.2（单条满分 100） · 生成 {today}</p>')
    P.append('<div class="warn"><b>这份排名排的是什么？</b>'
             '排的是<b>「该帝王的心智工具箱」与「其余帝王留下的处境」的适配度</b>，'
             '不是历史功绩排名、不是能力高低、更不是史实复原。'
             '分数高 = 他的思维模型在那套处境里更常能落地；分数低 = 他在那类处境里更常无从下手。'
             '两者都不代表他实际执政的水准。</div>')

    P.append('<div class="kpi">'
             f'<div class="m"><div class="l">参评帝王</div><div class="n">{n}</div></div>'
             f'<div class="m"><div class="l">处置总条数</div><div class="n">{len(all_rows)}</div></div>'
             f'<div class="m"><div class="l">全体均分</div><div class="n">{mean_all:.1f}</div></div>'
             f'<div class="m"><div class="l">均分区间</div><div class="n">{min(avgs):.1f}–{max(avgs):.1f}</div></div>'
             f'<div class="m"><div class="l">标准差</div><div class="n">{sd:.2f}</div></div>'
             f'<div class="m"><div class="l">总分榜首</div><div class="n" style="font-size:16px">'
             f'{rank[0]["cn"]} {rank[0]["total"]}</div></div>'
             '</div>')

    # ── 一、全体总榜 ──────────────────────────────────────
    top20 = rank[:20]
    P.append('<h2>一、全体总榜（按总分降序）</h2>'
             '<div class="panel" style="padding:12px 14px;margin-bottom:12px">'
             '<span style="font-size:12.5px;color:var(--mut)">'
             f'<b>总分</b> = 该帝王 {nper[0] if len(nper)==1 else "全部"} 条处置分之和'
             f'（理论满分 {nper[0] if len(nper)==1 else 100}×100 = {nper[0]*100 if len(nper)==1 else "-"}）；'
             '<b>均分</b> = 总分 ÷ 条数。<b>两者严格同序</b>——每人的条数相同，'
             '所以总分与均分只差一个放大倍数，不存在「总分高但均分低」的情形。'
             '这里以总分为主排序键，是为了让差距看得更清楚。</span></div>')
    P.append('<div class="panel"><div class="chart" style="height:460px">'
             '<canvas id="top20" role="img" aria-label="总分前20名"></canvas></div></div>')
    P.append('<div class="grp"><h3>总榜全表<span>'
             f'{n} 位 · 点击姓名进入该帝王的逐处境报告 · 同分者按时间先后排</span></h3>'
             f'<table>{H_ALL}<tbody>' + ''.join(row(t, rk=t['rank']) for t in rank)
             + '</tbody></table></div>')

    # ── 二、分朝代榜 ──────────────────────────────────────
    P.append('<h2>二、分朝代榜（朝内名次）</h2>'
             '<div class="dim">朝内名次只看同一朝的帝王之间的相对高低，'
             '跨朝不可比——每朝收到的处境集合不同（本朝自己的处境被排除在轮值之外），'
             '所以「唐第 3」与「清第 3」不是一回事。</div>')
    P.append('<div class="panel"><div class="chart" style="height:230px">'
             '<canvas id="dynbar" role="img" aria-label="五朝均分对照"></canvas></div></div>')
    for d, sub in dyn_rank.items():
        tops = sub[0]
        P.append(f'<div class="grp"><h3>{d}　<span>{len(sub)} 位 · '
                 f'朝内均分 {sum(x["overall"] for x in sub)/len(sub):.1f} · '
                 f'朝内榜首 {tops["cn"]} {tops["total"]}</span></h3>'
                 f'<table>{H_SUB}<tbody>'
                 + ''.join(row(t, rk=i, brief=True) for i, t in enumerate(sub, 1))
                 + '</tbody></table></div>')

    # ── 三、分模块榜 ──────────────────────────────────────
    P.append('<h2>三、分模块榜（按 module 字段 · 模块内名次）</h2>'
             '<div class="dim">模块来自每份 SKILL.md frontmatter 的 <code>module</code> 字段'
             '（如 <code>tang-emperors</code>），是「帝王包在仓库里的编目单元」。'
             '当前 <b>module 与朝代恰好一一对应</b>，因此本节的名次与第二节逐一相同；'
             '保留这个维度，是为了将来「一个模块跨多朝」或「一朝拆成多个模块」时自动生效。</div>')
    # 模块总览
    mrows = ''
    for m, (sub, cnt) in mod_rank.items():
        if sub:
            top = sub[0]
            mrows += (f'<tr><td class="k">{mod_cn(m)}</td><td><code>{m}</code></td>'
                      f'<td class="sc">{cnt}</td><td class="sc">{len(sub)}</td>'
                      f'<td class="sc">{round(sum(x["overall"] for x in sub)/len(sub),1)}</td>'
                      f'<td class="sc">{sum(x["total"] for x in sub)}</td>'
                      f'<td class="k"><a href="solo-{top["key"]}.html">{top["cn"]}</a> '
                      f'{top["total"]}</td></tr>')
        else:
            mrows += (f'<tr><td class="k">{mod_cn(m)}</td><td><code>{m}</code></td>'
                      f'<td class="sc">{cnt}</td><td class="sc">0</td>'
                      f'<td class="sc">—</td><td class="sc">—</td>'
                      f'<td class="k" style="color:var(--mut)">尚未纳入 solo 语料</td></tr>')
    P.append('<div class="grp"><h3>模块总览<span>'
             f'共 {len(mod_rank)} 个模块 · {sum(len(v) for v in mod_all.values())} 个帝王包 · '
             f'其中 {n} 位已纳入 solo 推演</span></h3>'
             '<table><thead><tr><th>模块</th><th>module 字段</th><th>帝王包数</th>'
             '<th>已推演</th><th>模块均分</th><th>模块总分</th><th>模块榜首</th>'
             f'</tr></thead><tbody>{mrows}</tbody></table></div>')
    for m, (sub, cnt) in mod_rank.items():
        if not sub:
            P.append(f'<div class="grp"><h3>{mod_cn(m)}　<span>模块 {m} · 共 {cnt} 个帝王包 · '
                     f'<b>尚未纳入 solo 语料</b></span></h3>'
                     f'<div class="dim">该模块的 {cnt} 个帝王包已通过质检并入库，'
                     f'但 <code>situations.json</code> 尚未收录其处境，故无推演数据。'
                     f'若纳入，全库矩阵将由 {n}×{n-1} 扩到 '
                     f'{n+cnt}×{n+cnt-1}（每人处境数 {n-1}→{n+cnt-1}）。</div></div>')
            continue
        P.append(f'<div class="grp"><h3>{mod_cn(m)}　<span>模块 {m} · 已推演 {len(sub)} / 共 {cnt} 包 · '
                 f'模块内均分 {sum(x["overall"] for x in sub)/len(sub):.1f}</span></h3>'
                 f'<table>{H_SUB}<tbody>'
                 + ''.join(row(t, rk=i, brief=True) for i, t in enumerate(sub, 1))
                 + '</tbody></table></div>')

    # ── 四、分档一览 ──────────────────────────────────────
    P.append('<h2>四、分档一览（按均分）</h2>')
    for label, sub in bands:
        chips = ''.join(f'<span class="chip" style="background:{E.VC[E.verdict(x["overall"])]}1a;'
                        f'color:{E.VC[E.verdict(x["overall"])]}">{x["cn"]} {x["overall"]}</span>'
                        for x in sub)
        P.append(f'<div class="tp" style="margin-bottom:12px"><h4>{label}'
                 f'<span>{len(sub)} 位</span></h4>{chips}</div>')

    # ── 五、按困局类型的适配排行 ──────────────────────────
    P.append('<h2>五、按困局类型的适配排行 · 谁最会什么</h2>'
             '<div class="panel" style="padding:12px 14px;margin-bottom:12px">'
             '<span style="font-size:12.5px;color:var(--mut)">'
             '每类取该类型平均处置分最高/最低各 5 位。'
             '人均极差越大，说明这一类越是「人定胜负」；极差越小，说明处境本身的结构压力越强。'
             '标题里的「全库（合并）」= 该类型全部处置分合起来求平均。</span></div>')
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
        P.append(f'<div class="tp"><h4>{t}<span>全库（合并）{pooled_mean[t]:.1f} · 人均极差 {gap:.1f}</span></h4>'
                 f'<div style="font-size:12px;color:#0f766e;margin-bottom:2px">最能接住</div>'
                 f'<ol>{hi}</ol>'
                 f'<div style="font-size:12px;color:#a83232;margin:8px 0 2px">最接不住</div>'
                 f'<ol>{lo}</ol></div>')
    P.append('</div>')

    # ── 六、结构约束 vs 人定胜负 ──────────────────────────
    grows = ''.join(
        f'<tr><td>{t}</td><td class="sc">{m:.1f}</td>'
        f'<td class="sc" style="color:{E.VC[E.verdict(m)]}">{g:.1f}</td>'
        f'<td class="k">{lo[0]["cn"]} {lo[1]}</td>'
        f'<td class="k">{hi[0]["cn"]} {hi[1]}</td></tr>'
        for t, m, g, lo, hi in gaps)
    P.append('<h2>六、结构约束 vs 人定胜负</h2>'
             '<div class="panel" style="padding:12px 14px;margin-bottom:12px">'
             '<span style="font-size:12.5px;color:var(--mut)">'
             '<b>全库均分（合并）</b> = 该类型全部处置分合起来求平均，与第五节同口径；'
             '<b>人均极差</b> = 各人的类型均分之间的最高 − 最低（是「人与人」的口径，'
             '与合并均分不同源，二者不可混读）。'
             '人定胜负档的人均极差应为结构性档的 2–3 倍。'
             '本表按设计只列 9 类中的这 5 类（含唯一的结构性档「亡国危局」作对照）。'
             '另 4 类（创业开国 / 平叛戡乱 / 削藩集权 / 开疆边患）的分布见第五节。</span></div>'
             '<table><thead><tr><th>困局类型</th><th>全库均分（合并）</th><th>人均极差</th>'
             f'<th>最低</th><th>最高</th></tr></thead><tbody>{grows}</tbody></table>')

    # ── 七、亡国危局带 ────────────────────────────────────
    P.append(f'<h2>七、亡国危局档 · 结构性困局的分数带</h2>'
             f'<div class="panel"><div class="chart" style="height:520px">'
             f'<canvas id="fg" role="img" aria-label="亡国危局档各人平均分"></canvas></div>'
             f'<p class="lead">{n} 位穿越者在这一类上的平均分全部落在 '
             f'<b>{min(fg_vals):.1f}–{max(fg_vals):.1f}</b>（极差 {max(fg_vals)-min(fg_vals):.1f}、'
             f'标准差 {fg_sd:.2f}）。<b>没有人突破 52</b> —— '
             f'说明「亡国危局」这一档的分数由处境本身的结构压力决定，换谁进去都难以拉开差距；'
             f'最高为 {fg[0][0]["cn"]}（{fg[0][1]}），最低为 {fg[-1][0]["cn"]}（{fg[-1][1]}）。</p></div>')

    # ── 八、各朝构成量 ────────────────────────────────────
    P.append('<h2>八、各朝穿越者均分（构成量，非朝代强弱）</h2>'
             '<div class="panel"><div class="meta">'
             + ''.join(f'<div class="m"><div class="l">{d}（{c} 位）</div>'
                       f'<div class="n">{v}</div></div>' for d, v, c in dyn_avg)
             + '</div><p class="lead"><b>不要把这个当成「哪个朝代更强」。</b>'
               '它只反映「本库收录的该朝帝王，其工具箱与这套处境的平均适配度」——'
               '收录名单本身就是选择的结果：唐收录了 21 位（含唐末一批幼主与傀儡），'
               '清收录了 12 位（含清末三位幼帝）。名单一变，这个数就变。</p></div>')

    P.append('<div class="foot">'
             '<b>排序与口径</b>：总分 = 每人 77 条处置分之和；均分 = 总分 ÷ 77；'
             '档位 可解≥75 / 可缓 65–74 / 难解 50–64 / 死局&lt;50；'
             '排序主键为总分（与均分同序），同分按时间先后；'
             '分朝代榜与分模块榜均为「组内名次」，跨组不可比；'
             '按困局类型的分组依据受控词表 9 类。<br>'
             '<b>四个必须知道的口径限制</b>：<br>'
             '① <b>类型均分是混合量</b>——它同时反映「处境难度」与「参评者构成」。'
             '实证：「创业开国」在李世民单体基线上排第 1（78.3），扩到全库降到第 5（61.5），'
             '只因全库多了 20 余位对该类几乎无策的幼主。不可当纯难度读。<br>'
             '② <b>组内名次不可跨组比</b>——每位穿越者的处境集合都排除了自己的处境，'
             '故唐末幼主与清初幼主即使分列各朝榜首，也只在各自朝内成立。<br>'
             '③ <b>底部塌陷</b>——亡国危局档 78 人全压 39–52，组内分辨力接近地板，'
             '「还能撑三年」与「明年就亡」在此不可分。评分卡的去结局化改造正是为此。<br>'
             '④ <b>诚实边界</b>——这是一次思想实验式的反事实推演，非史实复原。'
             '「某帝若在其位能否办好」无法被证实或证伪；分数表达的是心智工具与处境的适配度，'
             '不是对该帝王实际政绩的褒贬。<br>'
             '生成器：<code>_engine/eval_solo_rank.py</code>；模块映射 <code>_engine/modules_solo.json</code>；'
             '结构质检 <code>check_solo.py</code>、交叉检验 <code>cross_check_solo.py</code>。</div>')

    # ── scripts ──────────────────────────────────────────
    P.append('</div><script>')
    P.append('new Chart(document.getElementById("top20"),{type:"bar",data:{labels:'
             + json.dumps([f'{t["cn"]} {t["total"]}' for t in top20])
             + ',datasets:[{data:' + json.dumps([t['total'] for t in top20])
             + ',backgroundColor:' + json.dumps([din(t) for t in top20])
             + ',borderRadius:4}]},options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,'
               'scales:{x:{min:4000,max:5300,grid:{color:"#e5e7eb"}}},'
               'plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.parsed.x+" 分"}}}}});')
    P.append('new Chart(document.getElementById("dynbar"),{type:"bar",data:{labels:'
             + json.dumps([d for d, _, _ in dyn_avg])
             + ',datasets:[{data:' + json.dumps([v for _, v, _ in dyn_avg])
             + ',backgroundColor:' + json.dumps([E.DN.get(d, '#9ca3af') for d, _, _ in dyn_avg])
             + ',borderRadius:4}]},options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,'
               'scales:{x:{min:50,max:70,grid:{color:"#e5e7eb"}}},'
               'plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.parsed.x+" 分（构成量）"}}}}});')
    P.append('new Chart(document.getElementById("fg"),{type:"bar",data:{labels:'
             + json.dumps([f'{t["cn"]}' for t, _ in fg])
             + ',datasets:[{data:' + json.dumps([v for _, v in fg])
             + ',backgroundColor:' + json.dumps([din(t) for t, _ in fg])
             + ',borderRadius:3}]},options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,'
               'scales:{x:{min:35,max:55,grid:{color:"#e5e7eb"}}},'
               'plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.parsed.x+" 分"}}}}});')
    P.append('</script></body></html>')

    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, 'solo-ranking.html')
    open(out, 'w', encoding='utf-8').write(''.join(P))

    print('ranking ->', out)
    print('  参评', n, '| 条数', len(all_rows), '| 每人处境数', nper,
          '| 总分域', min(t['total'] for t in tvs), '-', max(t['total'] for t in tvs))
    print('  总榜榜首', rank[0]['cn'], rank[0]['total'], rank[0]['overall'],
          '| 榜尾', rank[-1]['cn'], rank[-1]['total'], rank[-1]['overall'])
    print('  分朝代：', {d: (len(s), s[0]['cn']) for d, s in dyn_rank.items()})
    print('  分模块：', {m: (len(s), c) for m, (s, c) in mod_rank.items()})
    print('  亡国危局带', min(fg_vals), '-', max(fg_vals), 'sd', round(fg_sd, 2))
    print('  类型全库合并均分', {t: pooled_mean[t] for t in TYPES})
    print('  六节表（合并均分 / 人均极差）', [(t, m, g) for t, m, g, _, _ in gaps])
    return out


if __name__ == '__main__':
    main()
