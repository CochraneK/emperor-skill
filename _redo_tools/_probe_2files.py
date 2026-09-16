# -*- coding: utf-8 -*-
"""两个可疑文件的实况检查。"""
import os, re

ROOT = r'D:/2026/WB项目/emperor-skill/'

print('=' * 70)
print('A. ming/zhuchangluo-perspective/04-external-views.md 的黑名单命中行')
print('=' * 70)
p = ROOT + 'skills/ming/zhuchangluo-perspective/references/research/04-external-views.md'
t = open(p, encoding='utf-8').read()
BAN = re.compile(r'(知乎|微信公众号|百度百科)')
for i, line in enumerate(t.splitlines(), 1):
    if BAN.search(line):
        print('  L%d: %s' % (i, line.strip()))

print()
print('=' * 70)
print('B. zhou/shenjingwang-perspective/06-timeline.md 全文骨架（3390B / 条目仅 1）')
print('=' * 70)
p2 = ROOT + 'skills/zhou/shenjingwang-perspective/references/research/06-timeline.md'
t2 = open(p2, encoding='utf-8').read()
print('  总字节 %d，行数 %d' % (len(t2.encode('utf-8')), len(t2.splitlines())))
print('  --- 所有标题行 ---')
for i, line in enumerate(t2.splitlines(), 1):
    if line.startswith('#'):
        print('   L%d %s' % (i, line.strip()))
print('  --- 全文（截 2600 字符）---')
print(t2[:2600])

# 对照：该包其他五份的条目数
print()
print('  --- 同包其他底稿条目数对照 ---')
PREF = re.compile(r'【(?:原话|史料原文|框架推断|史论|文本|出土文献|传世文献|考古)[^】]*】')
for d in ['01-writings.md', '02-conversations.md', '03-expression-dna.md',
          '04-external-views.md', '05-decisions.md', '06-timeline.md']:
    fp = ROOT + 'skills/zhou/shenjingwang-perspective/references/research/' + d
    if os.path.exists(fp):
        s = open(fp, encoding='utf-8').read()
        print('    %-24s %6dB  条目 %2d' % (d, os.path.getsize(fp), len(PREF.findall(s))))

# git 看 06 的原始版本
import subprocess
r = subprocess.run(['git', '-C', ROOT, 'show', 'HEAD:skills/zhou/shenjingwang-perspective/references/research/06-timeline.md'],
                   capture_output=True)
old = r.stdout.decode('utf-8', errors='replace')
print()
print('  --- git HEAD 版本：%d 字节，条目 %d ---' % (len(old.encode('utf-8')), len(PREF.findall(old))))
print('  旧版标题行：')
for line in old.splitlines():
    if line.startswith('#'):
        print('     ' + line.strip())
