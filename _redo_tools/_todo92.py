# -*- coding: utf-8 -*-
"""列出「待扩写 92 包」的按朝清单 + 每包最薄底稿及字节数，供分朝派单用。
只读，不改任何文件。"""
import os, json, re, collections

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
        missing = []
        for d in DIMS:
            p = os.path.join(rp, d)
            if os.path.exists(p):
                sizes[d] = os.path.getsize(p)
            else:
                missing.append(d)
        if missing:
            continue
        thin = min(sizes.values())
        if thin >= THRESH:
            continue
        thin_names = [k for k, v in sizes.items() if v == thin]
        rows.append({
            'dyn': dyn, 'sid': sid, 'thin': thin,
            'thin_name': thin_names[0],
            'all': sizes,
            'n_thin': sum(1 for v in sizes.values() if v < THRESH),
        })

rows.sort(key=lambda r: (r['dyn'], r['sid']))

out = []
out.append('== 待扩写包（最薄底稿 < 2500B）按朝清单 ==')
out.append('   共 %d 包\n' % len(rows))
cnt = collections.Counter(r['dyn'] for r in rows)
out.append('-- 各朝待办数（多→少）--')
for d, n in cnt.most_common():
    out.append('   %-12s %3d 包' % (d, n))
out.append('')

cur = None
for r in rows:
    if r['dyn'] != cur:
        cur = r['dyn']
        out.append('\n==== %s（%d 包）====' % (cur, cnt[cur]))
    out.append('  %-28s 最薄 %5dB (%s)  六维中未达标 %d/6  |  %s' % (
        r['sid'], r['thin'], r['thin_name'].replace('.md', ''), r['n_thin'],
        ' '.join('%d' % v for v in r['all'].values())))

# 建议分批（每批 6 包 = 2 worker x 3 包）
out.append('\n\n== 建议分批（每批 6 包，2 worker × 3 包）==')
order = [d for d, _ in cnt.most_common()]
flat = []
for d in order:
    flat += [r for r in rows if r['dyn'] == d]
for i in range(0, len(flat), 6):
    chunk = flat[i:i + 6]
    out.append('\n第 %d 批（%d 包）:' % (i // 6 + 1, len(chunk)))
    for r in chunk:
        out.append('   %-12s %-28s 最薄 %5dB  未达标 %d/6' % (
            r['dyn'], r['sid'], r['thin'], r['n_thin']))

txt = '\n'.join(out)
op = r'D:/2026/WB项目/emperor-skill/_redo_tools/_todo_92.txt'
open(op, 'w', encoding='utf-8').write(txt)
print('WROTE', op, len(txt))
print(txt[:3000])
