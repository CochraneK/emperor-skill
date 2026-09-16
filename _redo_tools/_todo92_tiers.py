# -*- coding: utf-8 -*-
"""92 包按「工作量」分档：需补几份底稿 / 缺口多少字节。只读。"""
import os, collections

ROOT = r'D:/2026/WB项目/emperor-skill/skills'
THRESH = 2500
DIMS = ['01-writings.md', '02-conversations.md', '03-expression-dna.md',
        '04-external-views.md', '05-decisions.md', '06-timeline.md']

rows = []
for dyn in sorted(os.listdir(ROOT)):
    dp = os.path.join(ROOT, dyn)
    if not os.path.isdir(dp):
        continue
    for sid in sorted(os.listdir(dp)):
        rp = os.path.join(dp, sid, 'references', 'research')
        if not os.path.isdir(rp):
            continue
        sizes = {}
        ok = True
        for d in DIMS:
            p = os.path.join(rp, d)
            if not os.path.exists(p):
                ok = False
                break
            sizes[d] = os.path.getsize(p)
        if not ok:
            continue
        bad = {k: v for k, v in sizes.items() if v < THRESH}
        if not bad:
            continue
        rows.append({
            'dyn': dyn, 'sid': sid,
            'nbad': len(bad),
            'gap': sum(THRESH - v for v in bad.values()),
            'bad': sorted(bad.items(), key=lambda x: x[1]),
        })

out = []
out.append('== 92 个待扩写包 · 按工作量分档 ==\n')

buckets = collections.defaultdict(list)
for r in rows:
    buckets[r['nbad']].append(r)

out.append('-- 按「需补底稿份数」分档 --')
for n in sorted(buckets):
    g = buckets[n]
    out.append('   需补 %d/6 份 : %2d 包   （需补底稿共 %d 份，总缺口 %d KB）' % (
        n, len(g), n * len(g), sum(x['gap'] for x in g) // 1024))
out.append('')

out.append('-- 【A档·临门一脚】只需补 1 份底稿（%d 包）--' % len(buckets.get(1, [])))
for r in sorted(buckets.get(1, []), key=lambda x: (x['dyn'], x['sid'])):
    k, v = r['bad'][0]
    out.append('   %-12s %-28s 补 %s  (%dB → 需 %dB，+%.1fKB)' % (
        r['dyn'], r['sid'], k.replace('.md', ''), v, THRESH, (THRESH - v) / 1024))
out.append('')

out.append('-- 【B档】需补 2-3 份（%d 包）--' % (len(buckets.get(2, [])) + len(buckets.get(3, []))))
for n in (2, 3):
    for r in sorted(buckets.get(n, []), key=lambda x: (x['dyn'], x['sid'])):
        out.append('   %-12s %-28s 补 %d 份: %s' % (
            r['dyn'], r['sid'], n, ', '.join('%s(%dB)' % (k.replace('.md', ''), v) for k, v in r['bad'])))
out.append('')

out.append('-- 【C档·整体塌陷】需补 4-6 份（%d 包）--' % sum(len(buckets.get(n, [])) for n in (4, 5, 6)))
for n in (4, 5, 6):
    for r in sorted(buckets.get(n, []), key=lambda x: (x['dyn'], x['sid'])):
        out.append('   %-12s %-28s 补 %d 份，最薄 %dB' % (
            r['dyn'], r['sid'], n, r['bad'][0][1]))

out.append('\n-- 汇总 --')
out.append('   A档(1份) %d 包 = %d 份底稿' % (len(buckets.get(1, [])), len(buckets.get(1, []))))
ab = len(buckets.get(2, [])) + len(buckets.get(3, []))
out.append('   B档(2-3份) %d 包 ≈ %d 份底稿' % (ab, sum(r['nbad'] for r in buckets.get(2, []) + buckets.get(3, []))))
c = sum(len(buckets.get(n, [])) for n in (4, 5, 6))
out.append('   C档(4-6份) %d 包 ≈ %d 份底稿' % (c, sum(r['nbad'] for r in buckets.get(4, []) + buckets.get(5, []) + buckets.get(6, []))))
out.append('   全仓需补底稿总计 %d 份' % sum(r['nbad'] for r in rows))

txt = '\n'.join(out)
op = r'D:/2026/WB项目/emperor-skill/_redo_tools/_todo92_tiers.txt'
open(op, 'w', encoding='utf-8').write(txt)
print('WROTE', op, len(txt))
print(txt)
