# -*- coding: utf-8 -*-
"""从各帝王 SKILL.md 的 frontmatter 抽出 module / group，生成 modules_solo.json。

用于 solo 排名报告的「分模块」排序维度。
用法：python build_module_map.py
"""
import json
import os
import re

ENG = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(ENG))
SKILLS = os.path.join(REPO, 'skills')
OUT = os.path.join(ENG, 'modules_solo.json')


def field(head, name):
    m = re.search(r'^' + name + r':\s*(.+)$', head, re.M)
    return m.group(1).strip() if m else ''


def main():
    out = {}
    for dyn in sorted(os.listdir(SKILLS)):
        dpath = os.path.join(SKILLS, dyn)
        if not os.path.isdir(dpath) or dyn.startswith('_'):
            continue
        for pk in sorted(os.listdir(dpath)):
            if not pk.endswith('-perspective'):
                continue
            fp = os.path.join(dpath, pk, 'SKILL.md')
            if not os.path.exists(fp):
                continue
            head = open(fp, encoding='utf-8').read()[:2500]
            key = pk[:-len('-perspective')]
            out[key] = {
                'dir': dyn,
                'module': field(head, 'module'),
                'group': field(head, 'group'),
                'cn': field(head, 'cn'),
                'era': field(head, 'era'),
            }
    json.dump(out, open(OUT, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1, sort_keys=True)
    print('modules_solo.json ->', len(out), '包')
    miss = [k for k, v in out.items() if not v['module']]
    if miss:
        print('⚠️ 缺 module 字段:', miss)


if __name__ == '__main__':
    main()
