# -*- coding: utf-8 -*-
"""78 帝 solo 推演的全库交叉检验（只读）。
检验四件事：
  A. 结构性硬约束：亡国危局一档是否全部落在 38–58，各人分差是否极小
  B. 人定胜负档：权臣党争/储位继统/变法理财/守成休养 四类，跨人分差是否明显
  C. 「均分」是否落在 55–72 主体带，且与工具箱宽度同向
  D. 断语第一人称「朕」使用率
用法：python cross_check_solo.py
"""
import collections
import json
import os
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
TV = os.path.join(HERE, 'travelers')

TYPES = ['创业开国', '平叛戡乱', '削藩集权', '守成休养', '变法理财',
         '开疆边患', '储位继统', '权臣党争', '亡国危局']
# 「人定胜负」四档（指望跨人分差明显）
PERSON_TYPES = ['权臣党争', '储位继统', '变法理财', '守成休养']


def load():
    s = json.load(open(os.path.join(HERE, 'situations.json'), encoding='utf-8'))
    sits = s['situations'] if isinstance(s, dict) else s
    return sits


def main():
    sits = load()
    typ = {x['key']: x.get('typ', '') for x in sits}
    name = {x['key']: x.get('name', '') for x in sits}

    tvs = {}
    for fn in sorted(os.listdir(TV)):
        if fn.endswith('.json'):
            tvs[fn[:-5]] = json.load(open(os.path.join(TV, fn), encoding='utf-8'))

    # 每位 × 每类 的均分
    grid = {}
    for k, d in tvs.items():
        agg = collections.defaultdict(list)
        for sk, cell in d['rows'].items():
            if sk in typ:
                agg[typ[sk]].append(cell[1])
        grid[k] = {t: (sum(v) / len(v) if v else None) for t, v in agg.items()}

    print('=' * 78)
    print('A. 亡国危局档：应全部落 38–58，且跨人分差极小')
    print('=' * 78)
    rows = [(k, grid[k].get('亡国危局')) for k in grid if grid[k].get('亡国危局')]
    vals = [v for _, v in rows]
    out = [(k, round(v, 1)) for k, v in rows if not (38 <= v <= 58)]
    print('  覆盖 %d 位｜均值 %.1f｜极差 %.1f (min %.1f / max %.1f)｜标准差 %.2f'
          % (len(vals), sum(vals) / len(vals), max(vals) - min(vals),
             min(vals), max(vals), st.pstdev(vals)))
    print('  越界者：%s' % (out if out else '无'))
    print('  最高五位：%s' % sorted(rows, key=lambda x: -x[1])[:5])
    print('  最低五位：%s' % sorted(rows, key=lambda x: x[1])[:5])

    print()
    print('=' * 78)
    print('B. 人定胜负四档：跨人分差应当明显')
    print('=' * 78)
    print('  %-8s %6s %6s %7s %7s' % ('类型', '均值', '极差', '最低人', '最高人'))
    for t in PERSON_TYPES + ['亡国危局']:
        rr = [(k, grid[k][t]) for k in grid if grid[k].get(t) is not None]
        vv = [v for _, v in rr]
        lo = min(rr, key=lambda x: x[1])
        hi = max(rr, key=lambda x: x[1])
        print('  %-8s %6.1f %6.1f %7s %7s' % (
            t, sum(vv) / len(vv), max(vv) - min(vv),
            '%s %.0f' % (lo[0], lo[1]), '%s %.0f' % (hi[0], hi[1])))

    print()
    print('=' * 78)
    print('C. 均分分布：主体带 55–72')
    print('=' * 78)
    ov = {}
    for k, d in tvs.items():
        sc = [c[1] for c in d['rows'].values()]
        ov[k] = sum(sc) / len(sc)
    vv = list(ov.values())
    print('  均值 %.1f｜极差 %.1f (min %.1f / max %.1f)｜标准差 %.2f'
          % (sum(vv) / len(vv), max(vv) - min(vv), min(vv), max(vv), st.pstdev(vv)))
    band = [k for k, v in ov.items() if 55 <= v <= 72]
    print('  落 55–72 带内：%d / %d' % (len(band), len(ov)))
    print('  带外（偏低）：%s' % sorted(
        [(k, round(v, 1)) for k, v in ov.items() if v < 55], key=lambda x: x[1]))
    print('  带外（偏高）：%s' % sorted(
        [(k, round(v, 1)) for k, v in ov.items() if v > 72], key=lambda x: -x[1]))
    print('  Top10：%s' % sorted(ov.items(), key=lambda x: -x[1])[:10])
    print('  Bottom10：%s' % sorted(ov.items(), key=lambda x: x[1])[:10])

    print()
    print('=' * 78)
    print('D. 断语口吻：第一人称「朕」使用率')
    print('=' * 78)
    bad = []
    for k, d in tvs.items():
        n = sum(1 for c in d['rows'].values()
                if isinstance(c, (list, tuple)) and '朕' in str(c[2]))
        tot = len(d['rows'])
        if n / tot < 0.8:
            bad.append((k, n, tot))
    print('  「朕」占比低于 80pct 的穿越者：%s' % (bad if bad else '无'))
    allr = [(k, sum(1 for c in d['rows'].values()
                    if isinstance(c, (list, tuple)) and '朕' in str(c[2])),
             len(d['rows'])) for k, d in tvs.items()]
    tot_n = sum(x[1] for x in allr)
    tot_d = sum(x[2] for x in allr)
    print('  全库「朕」占比：%d / %d = %.1f pct' % (tot_n, tot_d, 100.0 * tot_n / tot_d))

    print()
    print('=' * 78)
    print('E. 类型难度排行榜（全库均值，越高越易）')
    print('=' * 78)
    allt = collections.defaultdict(list)
    for k, d in tvs.items():
        for sk, c in d['rows'].items():
            if sk in typ:
                allt[typ[sk]].append(c[1])
    for t in sorted(TYPES, key=lambda x: -sum(allt[x]) / len(allt[x])):
        v = allt[t]
        print('  %-8s n=%-4d 均分 %.1f' % (t, len(v), sum(v) / len(v)))


if __name__ == '__main__':
    main()
