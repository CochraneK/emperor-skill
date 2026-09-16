# -*- coding: utf-8 -*-
"""元恭包独立复核：不采信 worker 自报，全部实测磁盘。"""
import os, re

PKG = r'D:/2026/WB项目/emperor-skill/skills/nanbeichao/yuangong-perspective'
RP = os.path.join(PKG, 'references', 'research')
DIMS = ['01-writings.md', '02-conversations.md', '03-expression-dna.md',
        '04-external-views.md', '05-decisions.md', '06-timeline.md']
PREF = re.compile(r'【(原话/一手|史料原文/一手|框架推断|史论/二手)】')
BAN = re.compile(r'(知乎|微信公众号|百度百科)')
DECL = re.compile(r'排除声明')

out = []
out.append('== 元恭包独立复核（实测磁盘，非自报）==\n')

ok_all = True
for d in DIMS:
    p = os.path.join(RP, d)
    if not os.path.exists(p):
        out.append('  %-24s ❌ 缺失' % d)
        ok_all = False
        continue
    b = os.path.getsize(p)
    t = open(p, encoding='utf-8').read()
    n_pref = len(PREF.findall(t))
    n_ban = len([m for m in BAN.finditer(t)])
    # 排除声明行不算黑名单词
    ban_hits = []
    for i, line in enumerate(t.splitlines(), 1):
        if BAN.search(line):
            if '排除声明' in line or '不采纳' in line or '未引用' in line:
                continue
            ban_hits.append((i, line.strip()[:60]))
    # 排除声明是否在末尾
    last = t.strip().splitlines()[-1] if t.strip() else ''
    decl_ok = bool(DECL.search(t)) and ('排除声明' in last or '排除声明' in t[-400:])
    ge = b >= 2500
    out.append('  %-24s %6dB  %s  前缀条目 %2d 条  %s  黑名单 %d 处  声明末尾 %s' % (
        d, b, 'OK ' if ge else '不足', n_pref,
        'OK' if n_pref >= 5 else ('少' if n_pref >= 1 else '零'),
        len(ban_hits), 'OK' if decl_ok else 'NO'))
    if not ge or n_pref < 5 or ban_hits or not decl_ok:
        ok_all = False
    for i, l in ban_hits:
        out.append('        ⚠ 黑名单 L%d: %s' % (i, l))

out.append('')
# 其它文件
out.append('-- 包内文件清单 --')
for root, dirs, files in os.walk(PKG):
    for f in files:
        fp = os.path.join(root, f)
        out.append('   %-60s %7dB' % (os.path.relpath(fp, PKG), os.path.getsize(fp)))

# 交叉核对：生年口径
out.append('\n-- 交叉核对：生年口径（01 稿 vs 06 稿）--')
for d in ('01-writings.md', '06-timeline.md'):
    p = os.path.join(RP, d)
    if not os.path.exists(p):
        continue
    t = open(p, encoding='utf-8').read()
    hits = [l.strip()[:90] for l in t.splitlines() if ('498' in l or '499' in l or '三十四' in l or '时年' in l)]
    out.append('   [%s] 命中 %d 行：' % (d, len(hits)))
    for h in hits[:6]:
        out.append('      ' + h)

out.append('\n结论：%s' % ('ALL_OK' if ok_all else 'HAS_ISSUE'))
txt = '\n'.join(out)
op = r'D:/2026/WB项目/emperor-skill/_redo_tools/_verify_yuangong.txt'
open(op, 'w', encoding='utf-8').write(txt)
print(txt)
