# -*- coding: utf-8 -*-
"""从 eval_crossing.py 抽取「处境全集」，并把已完成的两份报告迁移为通用 traveler 格式。

产物：
  _engine/situations.json   —— 78 个处境（77 帝 + 李世民），字段 key/name/dyn/typ/dilemma
  _engine/situations.md     —— 同上，供 worker 阅读的紧凑表格
  _engine/travelers/<key>.json —— 每个穿越者一份（本轮迁移 lishimin / wuzetian）
"""

import ast
import json
import os

ENG = os.path.dirname(os.path.abspath(__file__))
TV = os.path.join(ENG, 'travelers')
DYN_ORDER = ['唐', '宋', '元', '明', '清']

# ── 1. 用 AST 抽取 eval_crossing.py 中的字面量，避免执行整份脚本 ──
src = open(os.path.join(ENG, 'eval_crossing.py'), encoding='utf-8').read()
tree = ast.parse(src)
want = {'TANG', 'SONG', 'YUAN', 'MING', 'QING', 'BASE', 'CAT'}
vals = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        n = node.targets[0].id
        if n in want:
            vals[n] = ast.literal_eval(node.value)
missing = want - set(vals)
assert not missing, '未抽到: %s' % missing

CAT = vals['CAT']

sits = []
for grp, dyn in [('TANG', '唐'), ('SONG', '宋'), ('YUAN', '元'), ('MING', '明'), ('QING', '清')]:
    for t in vals[grp]:
        key, name, _raw, dilemma = t[0], t[1], t[2], t[3]
        sits.append(dict(key=key, name=name, dyn=dyn, typ=CAT[key], dilemma=dilemma))

b = vals['BASE']
sits.append(dict(key=b[0], name=b[1], dyn='唐', typ='创业开国', dilemma=b[3]))

assert len(sits) == 78, len(sits)
json.dump(sits, open(os.path.join(ENG, 'situations.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

md = ['# 处境全集（78 个）', '',
      '每位穿越者需对**除自己以外**的 77 个处境逐条给出「策 / 分 / 断语」。', '',
      '| # | key | 庙号 | 朝代 | 困局类型 | 核心困局 |', '|---:|---|---|---|---|---|']
for i, s in enumerate(sits, 1):
    md.append('| %d | `%s` | %s | %s | %s | %s |' % (i, s['key'], s['name'], s['dyn'], s['typ'], s['dilemma']))
md += ['', '## 困局类型分布', '']
from collections import Counter
for t, n in Counter(s['typ'] for s in sits).most_common():
    md.append('- %s：%d' % (t, n))
open(os.path.join(ENG, 'situations.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')

print('situations.json / situations.md -> 78 处境')
print(Counter(s['typ'] for s in sits).most_common())

# ── 2. 迁移已有的两位穿越者 ──
os.makedirs(TV, exist_ok=True)

META = {
    'lishimin': dict(name='太宗', cn='李世民', dyn='唐',
                     tagline='若使朕生于他人之位、承他人之局——朕之六道（纳谏、鉴隋、怀柔、早定储、武功转文治、功业自证）究竟灵不灵？',
                     summary='削藩、开疆、纳谏、守成，朕可接；幼主、女主、阉宦、亡国，朕亦束手。法可移，势不可移也。'),
    'wuzetian': dict(name='则天', cn='武则天', dyn='唐',
                     tagline='朕自才人而至天子，历三朝、废二帝、开周室——若置朕于他人之位，朕之诸般手段可还使得？',
                     summary='朕惯于以时间换空间：先固权、后用人、缓图其成。故权臣、储位、变法、守成诸局朕皆可周旋；而马上开国、临阵决胜，非朕所长。'),
}

for key, srcfile in [('lishimin', 'crossing_scores.json'), ('wuzetian', 'crossing_scores_wuzetian.json')]:
    rows = json.load(open(os.path.join(ENG, srcfile), encoding='utf-8'))
    out = dict(META[key])
    out['key'] = key
    out['rows'] = {r['key']: dict(plan=r['plan'], score=r['score'], note=r['note']) for r in rows}
    assert len(out['rows']) == 77, (key, len(out['rows']))
    assert key not in out['rows']
    json.dump(out, open(os.path.join(TV, key + '.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('migrated', key, len(out['rows']), 'rows')
