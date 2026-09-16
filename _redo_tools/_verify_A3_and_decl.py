# -*- coding: utf-8 -*-
"""① 复核 fixA3 交付的 6 份底稿 ② 全仓排查「缺排除声明」的底稿。"""
import os, re, collections

ROOT = r'D:/2026/WB项目/emperor-skill/'
PREF = re.compile(r'【(?:原话|史料原文|框架推断|史论|文本|出土文献)[^】]*】')
BAN = re.compile(r'(知乎|微信公众号|百度百科)')
SEC = re.compile(r'^##\s*([一二三四五六七八九十]+)、', re.M)
DIMS = ['01-writings.md', '02-conversations.md', '03-expression-dna.md',
        '04-external-views.md', '05-decisions.md', '06-timeline.md']

A3 = [
    (r'skills/yuan/haishan-perspective/references/research/04-external-views.md', '海山 04'),
    (r'skills/yuan/yilinzhiban-perspective/references/research/06-timeline.md', '懿璘质班 06'),
    (r'skills/zhou/jianwang-perspective/references/research/04-external-views.md', '周简王 04'),
    (r'skills/zhou/shenjingwang-perspective/references/research/02-conversations.md', '周慎靓王 02'),
    (r'skills/zhou/xiaowang-zhou-perspective/references/research/02-conversations.md', '周孝王 02'),
    (r'skills/zhou/youwang-perspective/references/research/05-decisions.md', '周幽王 05'),
]

out = ['== ① fixA3 交付复核（实测磁盘）==\n']
for rel, label in A3:
    p = ROOT + rel
    b = os.path.getsize(p)
    t = open(p, encoding='utf-8').read()
    n = len(PREF.findall(t))
    tail = '排除声明' in t[-400:] or '未采纳/排除声明' in t[-400:]
    sec = SEC.findall(t)
    dup = [k for k, v in collections.Counter(sec).items() if v > 1]
    paras = [l.strip() for l in t.splitlines() if len(l.strip()) >= 30]
    dpar = sum(1 for k, v in collections.Counter(paras).items() if v > 1)
    ban = [l.strip()[:40] for l in t.splitlines()
           if BAN.search(l) and not ('排除声明' in l or '不采纳' in l or '未引用' in l)]
    flag = []
    if b < 2500: flag.append('体量不足')
    if n < 5: flag.append('条目不足')
    if not tail: flag.append('声明不在末尾')
    if dup: flag.append('节号重复%s' % dup)
    if dpar: flag.append('段落重复%d' % dpar)
    if ban: flag.append('黑名单%s' % ban[:1])
    out.append('  %s %-14s %6dB 条目 %2d 声明 %s %s' % (
        'OK ' if not flag else '⚠ ', label, b, n, 'OK' if tail else 'NO',
        ('/ '.join(flag)) if flag else ''))

out.append('\n== ② 全仓排查：底稿缺「排除声明」==\n')
missing = []
total = 0
for dyn in sorted(os.listdir(ROOT + 'skills')):
    dp = ROOT + 'skills/' + dyn
    if not os.path.isdir(dp) or dyn.startswith('_'):
        continue
    for sid in sorted(os.listdir(dp)):
        rp = dp + '/' + sid + '/references/research'
        if not os.path.isdir(rp):
            continue
        for d in DIMS:
            p = rp + '/' + d
            if not os.path.exists(p):
                continue
            total += 1
            t = open(p, encoding='utf-8').read()
            if '排除声明' not in t[-500:]:
                missing.append('%s/%s/%s' % (dyn, sid, d))

out.append('  已扫描底稿 %d 份，缺声明 %d 份' % (total, len(missing)))
for m in missing:
    out.append('    ❌ ' + m)
if not missing:
    out.append('    ✅ 无遗漏')

txt = '\n'.join(out)
op = ROOT + '_redo_tools/_verify_A3_and_decl.txt'
open(op, 'w', encoding='utf-8').write(txt)
print(txt)
