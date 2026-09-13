# -*- coding: utf-8 -*-
"""把 travelers/*.json 中 dict 形式的值 {plan,score,note} 归一为 [策,分,断语] 三元数组。
只做形状归一，不改动任何文字内容。
用法：
  python normalize_rows.py          # 试运行，只报告
  python normalize_rows.py --apply  # 实际写入
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TV = os.path.join(HERE, 'travelers')
APPLY = '--apply' in sys.argv


def main():
    changed = []
    for fn in sorted(os.listdir(TV)):
        if not fn.endswith('.json'):
            continue
        p = os.path.join(TV, fn)
        d = json.load(open(p, encoding='utf-8'))
        rows = d.get('rows')
        if not isinstance(rows, dict):
            continue
        n = 0
        for k, cell in list(rows.items()):
            if isinstance(cell, dict) and 'score' in cell:
                rows[k] = [cell.get('plan', ''), cell.get('score', 0),
                           cell.get('note', '')]
                n += 1
        if n:
            changed.append((fn[:-5], n))
            if APPLY:
                json.dump(d, open(p, 'w', encoding='utf-8'),
                          ensure_ascii=False, indent=1)
    print('需归一文件 %d 个：%s' % (len(changed), changed))
    if APPLY:
        print('已写入。')


if __name__ == '__main__':
    main()
