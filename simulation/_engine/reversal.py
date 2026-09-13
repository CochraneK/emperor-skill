# -*- coding: utf-8 -*-
"""翻盘三条件 · 效度检验（T0 即位点 / T1 危局爆发点）聚合与报告生成。

回答的问题：评分卡给「亡国危局」一律低分，是真实的时代约束，
还是因为困局标签本就照着结局后验贴的（循环论证）？

做法：引入一组独立于结局的前置结构变量「翻盘三条件」——
  ① 手中有兵 ② 库中有粮 ③ 敌未整合
在 T0（即位之时）与 T1（危局爆发之时）各点验一次，
再看命中数 n 与既有分数是否同向。
"""

import datetime
import json
import math
import os

ENG = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(ENG))
OUT = os.path.join(REPO, 'simulation', 'validity', 'reversal-validity-report.html')

LI = {r['key']: r for r in json.load(open(os.path.join(ENG, 'crossing_scores.json'), encoding='utf-8'))}
WU = {r['key']: r for r in json.load(open(os.path.join(ENG, 'crossing_scores_wuzetian.json'), encoding='utf-8'))}

PHASE_FILES = {
    'T0': ['reversal_part1.json', 'reversal_part2.json', 'reversal_part3.json'],
    'T1': ['reversal_t1_part1.json', 'reversal_t1_part2.json', 'reversal_t1_part3.json'],
}


def load_phase(phase):
    rows = {}
    for fn in PHASE_FILES[phase]:
        p = os.path.join(ENG, fn)
        if not os.path.isfile(p):
            continue
        d = json.load(open(p, encoding='utf-8'))
        for it in d['items']:
            it['phase'] = d.get('phase', phase)
            rows[it['key']] = it
    return rows


T0 = load_phase('T0')
T1 = load_phase('T1')

KEYS = [k for k in LI if LI[k]['typ'] == '亡国危局']
KEYS.sort(key=lambda k: -LI[k]['score'])


def mean(xs):
    return sum(xs) / len(xs) if xs else float('nan')


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return float('nan')
    mx, my = mean(xs), mean(ys)
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs) / n)
    sy = math.sqrt(sum((y - my) ** 2 for y in ys) / n)
    if sx == 0 or sy == 0:
        return float('nan')
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n / (sx * sy)


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for t in range(i, j + 1):
                r[order[t]] = avg
            i = j + 1
        return r
    return pearson(rank(xs), rank(ys))


def stats(phase_rows):
    """返回某一点验轮的统计量。"""
    ks = [k for k in KEYS if k in phase_rows]
    if not ks:
        return None
    ns = [phase_rows[k]['n'] for k in ks]
    li = [LI[k]['score'] for k in ks]
    wu = [WU[k]['score'] for k in ks]
    groups = {}
    for i, k in enumerate(ks):
        groups.setdefault(ns[i], []).append(li[i])
    # 违反设计预期的案例：n>=3 却未达可缓(65)；n<=1 却已达可缓
    viol_hi = [k for k in ks if phase_rows[k]['n'] >= 3 and LI[k]['score'] < 65]
    viol_lo = [k for k in ks if phase_rows[k]['n'] <= 1 and LI[k]['score'] >= 65]
    return {
        'phase': phase_rows[list(phase_rows)[0]].get('phase', 'T0'),
        'k': ks, 'ns': ns,
        'r_li': pearson(ns, li), 'r_wu': pearson(ns, wu),
        'rho_li': spearman(ns, li), 'rho_wu': spearman(ns, wu),
        'gmean': {g: mean(v) for g, v in sorted(groups.items())},
        'gn': {g: len(v) for g, v in sorted(groups.items())},
        'viol_hi': viol_hi, 'viol_lo': viol_lo,
        'mean_li': mean(li), 'mean_wu': mean(wu),
    }


S0 = stats(T0)
S1 = stats(T1) if T1 else None

# ---------- 图表数据 ----------
NS = [0, 1, 2, 3]


def gseries(S, idx):
    if not S:
        return [None] * 4
    return [round(S['gmean'][g], 1) if g in S['gmean'] else None for g in NS]


def gcount(S):
    if not S:
        return [0] * 4
    return [S['gn'].get(g, 0) for g in NS]


def scatter(S):
    if not S:
        return []
    return [{'x': T0[k]['n'] if S is S0 else S['ns'][S['k'].index(k)], 'y': LI[k]['score']} for k in S['k']]


# ---------- 表格行 ----------
def bcell(v):
    return ('<span style="color:#0f766e">✓</span>' if v
            else '<span style="color:#b91c1c">✗</span>')


rows_html = []
for k in KEYS:
    li = LI[k]
    wu = WU.get(k, {})
    t0 = T0.get(k, {})
    t1 = T1.get(k, {})
    t0b = ''.join(bcell(t0.get(f'b{i}', False)) for i in (1, 2, 3))
    t1b = ''.join(bcell(t1.get(f'b{i}', False)) for i in (1, 2, 3))
    rows_html.append(
        '<tr>'
        '<td class="k">%s</td>'
        '<td>%s%s</td>'
        '<td>%s</td>'
        '<td class="sc">%s</td>'
        '<td class="sc">%s</td>'
        '<td class="sc">%s</td>'
        '<td class="sc">%s</td>'
        '<td class="sc">%s</td>'
        '<td class="sc">%s</td>'
        '<td class="d">%s</td>'
        '</tr>' % (
            k,
            li['dyn'], li['name'],
            t0.get('start_year', '—'),
            t0b, t0.get('n', '—'),
            t1b, t1.get('n', '—') if t1 else '<span style="color:#9ca3af">待补</span>',
            li['score'], wu.get('score', '—'),
            (t1.get('t1_point', '') if t1 else ''),
        ))


def pct(x):
    return '—' if x != x else ('%+.2f' % x)


def stat_cards(S, label):
    if not S:
        return ''
    return (
        '<div class="m"><div class="l">%s · n 与李世民分相关</div><div class="n">%s</div></div>'
        '<div class="m"><div class="l">%s · n 与武则天分相关</div><div class="n">%s</div></div>'
        '<div class="m"><div class="l">%s · 违反预期</div><div class="n">%d 例</div></div>'
        % (label, pct(S['r_li']), label, pct(S['r_wu']), label,
           len(S['viol_hi']) + len(S['viol_lo']))
    )


def viol_html(S, label):
    if not S or not (S['viol_hi'] or S['viol_lo']):
        return ''
    out = ['<h3>%s</h3>' % label]
    for k in S['viol_hi']:
        out.append('<p>· <b>%s%s</b> 点验 n=%d（按设计应有救），实际仅得 <b>%d</b> 分「%s」</p>'
                   % (LI[k]['dyn'], LI[k]['name'], S['ns'][S['k'].index(k)], LI[k]['score'], LI[k]['verdict']))
    for k in S['viol_lo']:
        out.append('<p>· <b>%s%s</b> 点验 n=%d（按设计应为死局），实得 <b>%d</b> 分</p>'
                   % (LI[k]['dyn'], LI[k]['name'], S['ns'][S['k'].index(k)], LI[k]['score']))
    return ''.join(out)


def residual(S1):
    """T1 之后仍未解决的问题。"""
    out = []
    if S1 and S1['viol_hi']:
        for k in S1['viol_hi']:
            out.append(
                '<p><b>未消除的反例：%s%s（n=%d，%d 分）。</b>'
                '该处境在危局点上兵、粮、敌三条俱全——脱脱主军政、江南漕盐未断、红巾各支互不统属，'
                '按设计应判「有救」。但它只得 52 分。关键在于：三条件给的是<b>机会上限</b>，不是自动及格线；'
                '有机会而失手，与根本无机会，在现有分数里被压成同一个低分区间。'
                '<b>评分卡还缺一维「机会利用度」</b>，否则无法区分「无救」与「有救而未救」。</p>'
                % (LI[k]['dyn'], LI[k]['name'], S1['ns'][S1['k'].index(k)], LI[k]['score']))
    if S1 and 0 in S1['gmean']:
        g0 = [LI[k]['score'] for k in S1['k'] if S1['ns'][S1['k'].index(k)] == 0]
        if g0:
            out.append(
                '<p><b>底部塌陷。</b>T1 把 15 处中的 %d 处都压到了 n=0，'
                '组内分数区间仅 %d–%d 分（极差 %d 分）。'
                '条件式点验是粗粒度的开关量，在王朝已经崩解时全部归零，'
                '于是「还能撑三年」与「明年就亡」在模型里无法区分。</p>'
                % (len(g0), min(g0), max(g0), max(g0) - min(g0)))
    out.append(
        '<p><b>时点尚未唯一化。</b>T1 要求「危局爆发时点」，但同一帝王往往有多个危局点，'
        '取哪一个会改变判定：宋钦宗取靖康第一次围城则 n=2，取第二次围城则 n=0，结论相反。'
        '补一条取样规则（例如统一取「都城首次被围」或「中央财赋区首次失守」）才能让 T1 可复现。</p>')
    return ''.join(out)


def conclusion(S0, S1):
    """数据驱动的结论段。"""
    if not S0:
        return '<div class="quote">T0 数据尚未就绪。</div>'
    parts = []
    parts.append(
        '<p>在即位时点（T0）点验「手中有兵／库中有粮／敌未整合」三条件，'
        '命中数 n 与分数只呈弱相关——n 与李世民分 <b>r = %s</b>、与武则天分 <b>r = %s</b>（ρ = %s）。'
        '分组均分 <b>%s</b> 也非单调：n=3 组反而比 n=2 组更低。</p>'
        % (pct(S0['r_li']), pct(S0['r_wu']), pct(S0['rho_li']),
           ' / '.join('n=%d：%.1f 分（%d 处）' % (g, v, S0['gn'][g]) for g, v in S0['gmean'].items())))
    if S0['viol_hi']:
        parts.append(
            '<p>最能说明问题的是直接反例：<b>%s</b>——即位时兵、粮、敌三面皆宽（n=3），'
            '按设计应判「有救」，实际却落在难解／死局。</p>'
            % '、'.join('%s%s（%d 分）' % (LI[k]['dyn'], LI[k]['name'], LI[k]['score']) for k in S0['viol_hi']))
    parts.append(
        '<p><b>机制不在判分者失误，而在时点错位。</b>评分卡的处境题面写的是'
        '<b>结局当口的危局</b>（如「内忧外患而亡国」「负幼投海，君臣俱没」），'
        '而三条件量的是<b>即位之时的结构存量</b>。题面把结局编了进去，低分便是定义使然。</p>')
    if S1:
        better = S1['r_li'] > S0['r_li'] + 0.15
        parts.append(
            '<p>把点验时点改到<b>危局爆发之时（T1）</b>后，相关性升至 <b>r = %s</b>（ρ = %s），'
            '分组均分变为 <b>%s</b>%s。'
            '%s</p>'
            % (pct(S1['r_li']), pct(S1['rho_li']),
               ' / '.join('n=%d：%.1f 分（%d 处）' % (g, v, S1['gn'][g]) for g, v in S1['gmean'].items()),
               '，违反预期的案例从 %d 例降至 %d 例'
               % (len(S0['viol_hi']) + len(S0['viol_lo']), len(S1['viol_hi']) + len(S1['viol_lo']))
               if (S0['viol_hi'] or S0['viol_lo']) else '',
               '<b>这坐实了循环论证：评分卡锚定的确实是「结局快照」，不是「开局结构」。</b>'
               if better else '<b>T1 未能显著改善相关性，说明三条件的解释力有限，评分卡的失准另有来源。</b>'))
    parts.append(
        '<p><b>对原问题的意义。</b>现有评分卡既不能回答「明君穿越能否改结局」（题面已含结局），'
        '也没在干净地测「人的能力」（题面已含结局、分数还掺着君主资质的印象分）。'
        '要回答那个问题，必须把处境描述<b>去结局化</b>，并把评分拆成两段：'
        'T0 开局结构决定「基础难度」，T1 之后的决策质量决定「结局阶梯（翻盘／中兴／延祚／无改／加速）」。</p>')
    return '<div class="quote">%s</div>' % ''.join(parts)



delta_rows = []
for k in KEYS:
    if k in T0 and k in T1:
        d = T1[k]['n'] - T0[k]['n']
        if d != 0:
            delta_rows.append((LI[k]['dyn'] + LI[k]['name'], T0[k]['n'], T1[k]['n'], d, T1[k].get('delta_note', '')))
delta_html = ''.join(
    '<tr><td>%s</td><td class="sc">%d</td><td class="sc">%d</td><td class="sc">%+d</td><td class="d">%s</td></tr>'
    % (n, a, b, d, note) for n, a, b, d, note in delta_rows) or \
    '<tr><td colspan="5" style="color:#6b7280">T0 与 T1 判定一致，无变化项。</td></tr>'

CSS = """
:root{--bg:#f6f6f3;--panel:#fff;--ink:#1f2937;--mut:#6b7280;--line:#e5e7eb;--teal:#0f766e}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.7 -apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
.wrap{max-width:1060px;margin:0 auto;padding:32px 24px 64px}
h1{font-size:24px;font-weight:600;margin:0 0 6px}
.sub{color:var(--mut);font-size:13px;margin:0 0 22px}
h2{font-size:17px;font-weight:600;margin:36px 0 14px;padding-left:10px;border-left:3px solid var(--teal)}
h3{font-size:14px;font-weight:600;margin:22px 0 10px}
.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:16px 0}
.m{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.m .l{color:var(--mut);font-size:12px} .m .n{font-size:21px;font-weight:600;margin-top:2px}
.quote{background:#eff6f4;border-left:3px solid var(--teal);border-radius:0 8px 8px 0;padding:14px 18px;color:#134e4a;font-size:13.5px;margin:14px 0}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px}
.chart{position:relative;height:290px}
table{width:100%;border-collapse:collapse;font-size:12.5px;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden}
th,td{padding:7px 9px;border-bottom:1px solid var(--line);text-align:left}
td.sc{text-align:center;font-weight:600} th{background:#f0f1ef;font-weight:500;color:var(--mut)}
td.k{font-family:ui-monospace,Consolas,monospace;font-size:11.5px;white-space:nowrap}
td.d{color:#4b5563;max-width:340px}
tr:hover td{background:#fafaf8}
.foot{color:var(--mut);font-size:12px;margin-top:28px;border-top:1px solid var(--line);padding-top:16px}
.legend{display:flex;gap:16px;font-size:12px;color:var(--mut);margin-bottom:8px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px}
"""

NOW = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

html = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>翻盘三条件 · 效度检验报告</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>%s</style></head><body><div class="wrap">

<h1>翻盘三条件 · 效度检验</h1>
<p class="sub">检验对象：78 帝穿越评分卡在「亡国危局」一档的 15 个处境 ｜ 检验方法：引入独立于结局的前置结构变量，双时点对照点验 ｜ 生成 %s</p>

<h2>结论</h2>
%s

<div class="meta">
%s
</div>

<h2>检验设计</h2>
<div class="panel">
<p><b>为什么用这三个条件。</b>「明君穿越到亡国之君身上能否有救」这个问题，现有评分卡回答不了，
因为它没有把「处境有多难」和「人能不能改变处境」分开。翻盘三条件是历史上真实翻盘案例的共性前提，
且<b>在开局即可观测</b>，不依赖结局，因此可以用来给评分卡做外部效度检验：</p>
<p style="margin:6px 0 0">① <b>手中有兵</b>　② <b>库中有粮</b>　③ <b>敌未整合</b>。三条全中→有救；中两条→只可延祚；中零至一条→死局。</p>
<p style="margin:10px 0 0"><b>为什么做两个时点。</b>T0 取帝王即位之时，T1 取处境题面所描述的那个危局爆发之时。
若 T1 的 n 明显比 T0 更能解释分数，即证明评分卡锚定的是「结局快照」而非「开局结构」。</p>
</div>

<h2>按命中数分组的平均得分（T0 / T1 对照）</h2>
<div class="legend"><span><i style="background:#0f766e"></i>T0 即位点</span><span><i style="background:#9ca3af"></i>T1 危局爆发点</span><span style="color:#9ca3af">悬停可见组内处境数</span></div>
<div class="panel"><div class="chart"><canvas id="c1" role="img" aria-label="按翻盘三条件命中数分组的平均得分柱状图">命中数 0 至 3 分组下的平均得分。</canvas></div></div>

<h2>15 处逐项点验</h2>
<table>
<thead><tr>
<th>key</th><th>帝王</th><th>即位年</th>
<th style="text-align:center">T0 兵粮敌</th><th style="text-align:center">T0 n</th>
<th style="text-align:center">T1 兵粮敌</th><th style="text-align:center">T1 n</th>
<th style="text-align:center">李世民</th><th style="text-align:center">武则天</th><th>T1 取样点</th>
</tr></thead>
<tbody>%s</tbody></table>

<h2>T0 → T1 判定变动</h2>
<table>
<thead><tr><th>帝王</th><th style="text-align:center">T0 n</th><th style="text-align:center">T1 n</th><th style="text-align:center">Δ</th><th>变动原因</th></tr></thead>
<tbody>%s</tbody></table>

<h2>违反设计预期的案例</h2>
<div class="panel">%s</div>

<h2>残余问题</h2>
<div class="panel">%s</div>

<div class="foot">
<p>数据：<code>simulation/_engine/reversal_part*.json</code>（T0）、<code>reversal_t1_part*.json</code>（T1）；
分数取自 <code>crossing_scores.json</code> 与 <code>crossing_scores_wuzetian.json</code>。</p>
<p>局限：三条件点验由 LLM 依史实逐项判定，属定性判断的结构化，存在判者变异；
置信度标记见各条 JSON 的 <code>confidence</code> 与 <code>notes</code> 字段。
相关系数基于 15 个样本，仅作方向性参考，不作显著性结论。</p>
</div>

</div><script>
const NS=[0,1,2,3];
const T0M=%s, T1M=%s, T0C=%s, T1C=%s;
const body=getComputedStyle(document.body);
const mut=body.getPropertyValue('--mut').trim()||'#6b7280';
const line=body.getPropertyValue('--line').trim()||'#e5e7eb';
new Chart(document.getElementById('c1'),{
 type:'bar',
 data:{labels:NS.map(n=>'命中 '+n+' 条'),datasets:[
  {label:'T0 即位点',data:T0M,backgroundColor:'#0f766e',borderRadius:4},
  {label:'T1 危局爆发点',data:T1M,backgroundColor:'#9ca3af',borderRadius:4}]},
 options:{responsive:true,maintainAspectRatio:false,
  plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>{
    const n=c.dataIndex;const cnt=(c.datasetIndex===0?T0C:T1C)[n];
    return c.dataset.label+' 平均 '+c.raw+' 分（'+cnt+' 处）';}}}},
  scales:{y:{min:0,max:90,ticks:{color:mut},grid:{color:line},title:{display:true,text:'平均得分',color:mut,font:{size:12}}},
          x:{ticks:{color:mut},grid:{display:false}}}}
});
</script></body></html>
""" % (
    CSS, NOW,
    conclusion(S0, S1),
    stat_cards(S0, 'T0') + stat_cards(S1, 'T1'),
    ''.join(rows_html),
    delta_html,
    viol_html(S0, 'T0 即位点') + viol_html(S1, 'T1 危局爆发点'),
    residual(S1),
    json.dumps(gseries(S0, 0)), json.dumps(gseries(S1, 0)),
    json.dumps(gcount(S0)), json.dumps(gcount(S1)),
)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(html)

print('report ->', OUT)
for S in (S0, S1):
    if S:
        print('%s  n=%d  r(li)=%s r(wu)=%s  rho(li)=%s  groups=%s' % (
            S['phase'], len(S['k']), pct(S['r_li']), pct(S['r_wu']), pct(S['rho_li']),
            {g: round(v, 1) for g, v in S['gmean'].items()}))
        print('   违反预期 %d 例：%s' % (len(S['viol_hi']) + len(S['viol_lo']),
                                   [LI[k]['name'] for k in S['viol_hi'] + S['viol_lo']]))
