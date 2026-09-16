# -*- coding: utf-8 -*-
"""提交前体检：① 复核全部改动过的底稿 ② 全仓扫描仍不达标的包。
判定：<2500B / 前缀条目 <5 / 排除声明不在末尾 / 章节号重复 / 段落重复。"""
import os, re, collections, subprocess

ROOT = r'D:/2026/WB项目/emperor-skill/'
DIMS = ['01-writings.md', '02-conversations.md', '03-expression-dna.md',
        '04-external-views.md', '05-decisions.md', '06-timeline.md']
PREF = re.compile(r'【(?:原话|史料原文|框架推断|史论|文本|出土文献|传世文献|考古)[^】]*】')
BAN = re.compile(r'(知乎|微信公众号|百度百科)')
SEC = re.compile(r'^##\s*([一二三四五六七八九十]+)、', re.M)
THRESH = 2500

# 从 git status 取改动文件
p = subprocess.run(['git', '-C', ROOT, 'status', '--short'], capture_output=True)
dirty = []
for line in p.stdout.decode('utf-8', errors='replace').splitlines():
    if line.startswith(' M '):
        rel = line[3:].strip()
        if rel.endswith('.md') and 'research' in rel:
            dirty.append(rel)

out = ['== ① 改动文件逐份体检（%d 份）==\n' % len(dirty)]
bad = []
for rel in sorted(dirty):
    fp = ROOT + rel
    b = os.path.getsize(fp)
    t = open(fp, encoding='utf-8').read()
    n = len(PREF.findall(t))
    tail = '排除声明' in t[-400:] or '未采纳/排除声明' in t[-400:]
    sec = SEC.findall(t)
    dup = [k for k, v in collections.Counter(sec).items() if v > 1]
    paras = [l.strip() for l in t.splitlines() if len(l.strip()) >= 30]
    dpar = sum(1 for k, v in collections.Counter(paras).items() if v > 1)
    ban = [l.strip()[:45] for l in t.splitlines()
           if BAN.search(l) and not ('排除声明' in l or '不采纳' in l or '未引用' in l
                                     or '均非' in l or '不注引' in l or '未使用' in l)]
    flag = []
    if b < THRESH: flag.append('体量不足')
    if n < 5: flag.append('条目<5')
    if not tail: flag.append('声明不在末尾')
    if dup: flag.append('节号重复%s' % dup)
    if dpar: flag.append('段落重复%d' % dpar)
    if ban: flag.append('黑名单')
    short = rel.replace('skills/', '').replace('/references/research/', ' · ')
    out.append('  %s %-46s %6dB 条目 %2d %s' % (
        'OK ' if not flag else '⚠ ', short, b, n, ('← ' + '/'.join(flag)) if flag else ''))
    if flag:
        bad.append(rel)

out.append('\n  ⇒ 达标 %d / 有问题 %d' % (len(dirty) - len(bad), len(bad)))

# ② 全仓仍不达标的包
out.append('\n== ② 全仓扫描：仍不达标的包（按朝代）==\n')
rows = []
for dyn in sorted(os.listdir(ROOT + 'skills')):
    dp = ROOT + 'skills/' + dyn
    if not os.path.isdir(dp) or dyn.startswith('_'):
        continue
    for sid in sorted(os.listdir(dp)):
        rp = dp + '/' + sid + '/references/research'
        if not os.path.isdir(rp):
            continue
        sizes = {}
        for d in DIMS:
            f = rp + '/' + d
            if os.path.exists(f):
                sizes[d] = os.path.getsize(f)
        if not sizes:
            continue
        thin = {k: v for k, v in sizes.items() if v < THRESH}
        if thin:
            rows.append((dyn, sid, len(thin), min(thin.values())))

cnt = collections.Counter(r[0] for r in rows)
out.append('  不达标包共 %d 个' % len(rows))
for d, n in cnt.most_common():
    out.append('    %-12s %3d' % (d, n))
out.append('')
for dyn, sid, k, mn in rows:
    out.append('   %-12s %-34s 缺 %d/6  最薄 %dB' % (dyn, sid, k, mn))

txt = '\n'.join(out)
open(ROOT + '_redo_tools/_precommit_check.txt', 'w', encoding='utf-8').write(txt)
print(txt)
