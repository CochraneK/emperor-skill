# -*- coding: utf-8 -*-
"""诊断 objects 剩余情况：有哪些 pack、哪些 commit 对象还在。"""
import os, subprocess, glob

R = r'D:/2026/WB项目/emperor-skill'
G = R + '/.git'


def g(*args):
    p = subprocess.run(['git', '-C', R] + list(args), capture_output=True)
    return (p.stdout + p.stderr).decode('utf-8', errors='replace').strip()


print('=== objects/pack ===')
pk = G + '/objects/pack'
if os.path.isdir(pk):
    for f in os.listdir(pk):
        print('  %-40s %10dB' % (f, os.path.getsize(os.path.join(pk, f))))
else:
    print('  ❌ 无 pack 目录')

print()
print('=== objects 松散对象统计 ===')
tot = 0
for d in os.listdir(G + '/objects'):
    p = os.path.join(G + '/objects', d)
    if os.path.isdir(p) and len(d) == 2:
        tot += len(os.listdir(p))
print('  松散对象数:', tot)

print()
print('=== 逐个测试关键 sha 是否存在 ===')
cands = {
    'df478eb (本次补稿提交)': 'df478eb',
    '28e8350 (元恭包)': '28e8350',
    'c707c2a (memo)': 'c707c2a',
    '124f8eb (远端 main)': '124f8eb',
    '5e64dac (ORIG_HEAD)': '5e64dac',
    '6f05e34 (远端 v2 文档)': '6f05e34',
}
for label, sha in cands.items():
    rc, out = g('cat-file', '-t', sha)
    print('  %-30s %s' % (label, ('✅ ' + out) if 'commit' in out or 'tree' in out or 'blob' in out else '❌ ' + out[:50]))

print()
print('=== HEAD 当前指向的对象 ===')
print(g('rev-parse', 'HEAD 2>&1')[:200] if False else g('cat-file', '-t', 'HEAD'))
