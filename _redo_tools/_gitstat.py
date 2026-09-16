# -*- coding: utf-8 -*-
"""用 Python subprocess 跑 git，绕开 bash shim。只读。"""
import subprocess, os

R = r'D:/2026/WB项目/emperor-skill'


def g(*args):
    p = subprocess.run(['git', '-C', R] + list(args), capture_output=True)
    o = (p.stdout + p.stderr).decode('utf-8', errors='replace').strip()
    return p.returncode, o


print('=== HEAD ===')
print(g('log', '--oneline', '-5')[1])
print()
print('=== 状态 ===')
print(g('status', '--short')[1] or '(干净)')
print()
print('=== 本地 vs 远端 ===')
print(g('rev-parse', '--short', 'HEAD')[1], '<- HEAD')
print(g('rev-parse', '--short', 'FETCH_HEAD')[1], '<- FETCH_HEAD')
rc, out = g('rev-list', '--count', 'HEAD..FETCH_HEAD')
print('远端领先 (HEAD..FETCH_HEAD):', out)
rc, out = g('rev-list', '--count', 'FETCH_HEAD..HEAD')
print('本地领先 (FETCH_HEAD..HEAD):', out)
print()
print('=== 远端两个新提交改了什么 ===')
print(g('show', '--stat', '--oneline', '6f05e34')[1][:1500])
print()
print(g('show', '--stat', '--oneline', '124f8eb')[1][:1500])
