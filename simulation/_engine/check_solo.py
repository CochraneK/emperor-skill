# -*- coding: utf-8 -*-
"""solo 推演产物结构质检（只读，不修改任何文件）
用法：
  python check_solo.py            # 检查 travelers/ 下全部文件
  python check_solo.py --strict   # 有任一问题即以退出码 1 结束
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TV = os.path.join(HERE, 'travelers')
SITS = os.path.join(HERE, 'situations.json')

TYPES = {'创业开国', '平叛戡乱', '削藩集权', '守成休养', '变法理财',
         '开疆边患', '储位继统', '权臣党争', '亡国危局'}
DYNS = {'唐', '宋', '元', '明', '清'}


def load_situations():
    d = json.load(open(SITS, encoding='utf-8'))
    sits = d['situations'] if isinstance(d, dict) else d
    return sits


def main():
    sits = load_situations()
    keys = [s['key'] for s in sits]
    key2typ = {s['key']: s.get('typ', '') for s in sits}
    allset = set(keys)

    strict = '--strict' in sys.argv
    problems = []
    ok_files = []
    stat = []

    for fn in sorted(os.listdir(TV)):
        if not fn.endswith('.json'):
            continue
        k = fn[:-5]
        p = os.path.join(TV, fn)
        try:
            d = json.load(open(p, encoding='utf-8'))
        except Exception as e:
            problems.append((k, 'JSON 解析失败: %s' % e))
            continue

        rows = d.get('rows')
        if not isinstance(rows, dict):
            problems.append((k, 'rows 不是对象'))
            continue

        # 1) 条数 = 77
        if len(rows) != 77:
            problems.append((k, 'rows 条数 %d != 77' % len(rows)))
        # 2) key 集合 = 全集减自身
        want = allset - {k}
        got = set(rows)
        miss = want - got
        extra = got - allset
        self_in = k in rows
        if miss:
            problems.append((k, '缺 %d 条: %s' % (len(miss), sorted(miss)[:6])))
        if extra:
            problems.append((k, '含未知 key: %s' % sorted(extra)[:6]))
        if self_in:
            problems.append((k, 'rows 里含自身 key'))

        # 3) 值形状 / 分数 / 字数
        bad_shape, bad_score, bad_len_c, bad_len_n = [], [], [], []
        scores = []
        for tk, cell in rows.items():
            if not (isinstance(cell, (list, tuple)) and len(cell) == 3):
                bad_shape.append(tk)
                continue
            plan, sc, note = cell
            if not isinstance(sc, int) or isinstance(sc, bool) or not (0 <= sc <= 100):
                bad_score.append('%s=%r' % (tk, sc))
                continue
            scores.append(sc)
            if not isinstance(plan, str) or len(plan) > 22:
                bad_len_c.append(tk)
            if not isinstance(note, str) or len(note) > 22:
                bad_len_n.append(tk)
        if bad_shape:
            problems.append((k, '值非三元数组: %d 条' % len(bad_shape)))
        if bad_score:
            problems.append((k, '分数越界/非整数: %s' % bad_score[:5]))
        if bad_len_c:
            problems.append((k, '策 >22 字: %d 条 %s' % (len(bad_len_c), bad_len_c[:5])))
        if bad_len_n:
            problems.append((k, '断语 >22 字: %d 条 %s' % (len(bad_len_n), bad_len_n[:5])))

        # 4) 元字段
        if d.get('dyn') not in DYNS:
            problems.append((k, 'dyn 非法: %r' % d.get('dyn')))
        for f in ('name', 'cn', 'tagline', 'summary'):
            if not d.get(f):
                problems.append((k, '缺字段 %s' % f))

        if scores:
            ok_files.append(k)
            stat.append((k, d.get('dyn', ''), round(sum(scores) / len(scores), 1),
                         min(scores), max(scores)))

    print('=== 已落盘 %d 份，结构通过 %d 份 ===' % (
        len([f for f in os.listdir(TV) if f.endswith('.json')]), len(ok_files)))
    if problems:
        print('\n--- 问题清单 ---')
        for k, msg in problems:
            print('  [%s] %s' % (k, msg))
    else:
        print('无结构问题。')

    print('\n--- 均分（低→高） ---')
    for k, dyn, avg, lo, hi in sorted(stat, key=lambda x: x[2]):
        print('  %-14s %s  均分 %5.1f  区间 %d-%d' % (k, dyn, avg, lo, hi))

    if stat:
        avgs = [s[2] for s in stat]
        print('\n全库均分：min %.1f  max %.1f  mean %.1f' % (
            min(avgs), max(avgs), sum(avgs) / len(avgs)))

    if strict and problems:
        sys.exit(1)


if __name__ == '__main__':
    main()
