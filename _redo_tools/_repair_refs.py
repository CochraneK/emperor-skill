# -*- coding: utf-8 -*-
"""重建被删除的 .git/refs，然后验证仓库可读。
思路：以远端 FETCH_HEAD(124f8eb) 重建 refs/heads/main；
ORIG_HEAD 里的 sha 另存为 refs/heads/_pre_rebase_backup 以便追查。"""
import os, subprocess

R = r'D:/2026/WB项目/emperor-skill'
G = R + '/.git'

os.makedirs(G + '/refs/heads', exist_ok=True)
os.makedirs(G + '/refs/tags', exist_ok=True)
os.makedirs(G + '/refs/remotes/origin', exist_ok=True)

fetch_head = open(G + '/FETCH_HEAD', encoding='utf-8').read().split()[0].strip()
orig_head = open(G + '/ORIG_HEAD', encoding='utf-8').read().strip()
print('FETCH_HEAD sha =', fetch_head)
print('ORIG_HEAD  sha =', orig_head)

with open(G + '/refs/heads/main', 'w', encoding='utf-8') as f:
    f.write(fetch_head + '\n')
with open(G + '/refs/heads/_before_rebase_backup', 'w', encoding='utf-8') as f:
    f.write(orig_head + '\n')
with open(G + '/refs/remotes/origin/main', 'w', encoding='utf-8') as f:
    f.write(fetch_head + '\n')
print('refs 已重建')


def g(*args):
    p = subprocess.run(['git', '-C', R] + list(args), capture_output=True)
    return p.returncode, (p.stdout + p.stderr).decode('utf-8', errors='replace').strip()


print()
print('=== 验证：git 是否恢复 ===')
print(g('rev-parse', '--short', 'HEAD')[1])
print()
print('=== main 上最近 5 个提交 ===')
print(g('log', '--oneline', '-5')[1])
print()
print('=== ORIG_HEAD 那个 commit 是谁 ===')
print(g('log', '--oneline', '-1', orig_head)[1])
print()
print('=== 它比 main 多什么（若是 rebase 结果，应含我的补稿）===')
rc, out = g('log', '--oneline', '%s ^%s' % (orig_head, fetch_head))
print(out[:600] if out else '(无)')
print()
print('=== 工作树状态（相对 124f8eb）===')
rc, out = g('status', '--short')
lines = out.splitlines()
print('改动条目数:', len(lines))
for l in lines[:40]:
    print('  ' + l)
