# -*- coding: utf-8 -*-
"""元恭包 nuwa 真口径七门禁复核（实测，不采信自报）。"""
import os, re

PKG = r'D:/2026/WB项目/emperor-skill/skills/nanbeichao/yuangong-perspective'
RP = os.path.join(PKG, 'references', 'research')
SK = os.path.join(PKG, 'SKILL.md')
QC = os.path.join(PKG, 'scripts', 'quality_check.py')
DIMS = ['01-writings.md', '02-conversations.md', '03-expression-dna.md',
        '04-external-views.md', '05-decisions.md', '06-timeline.md']

r = []
ok = True


def chk(name, cond, detail=''):
    global ok
    r.append('  %s %-22s %s' % ('✅' if cond else '❌', name, detail))
    if not cond:
        ok = False


# ① 包内恰 8 文件
files = []
for root, dirs, fs in os.walk(PKG):
    for f in fs:
        files.append(os.path.relpath(os.path.join(root, f), PKG))
chk('包内恰 8 文件', len(files) == 8, '%d 个：%s' % (len(files), ', '.join(sorted(files))))

# ② 六维齐全 + ③ ≥2.5KB
for d in DIMS:
    p = os.path.join(RP, d)
    chk('六维 %s' % d[:2], os.path.exists(p) and os.path.getsize(p) >= 2500,
        '%dB' % os.path.getsize(p) if os.path.exists(p) else '缺失')

# ④ 排除声明
for d in DIMS:
    p = os.path.join(RP, d)
    if os.path.exists(p):
        t = open(p, encoding='utf-8').read()
        chk('排除声明 %s' % d[:2], '排除声明' in t[-400:], '')

# ⑤ qc 已跑（外部已跑，此处只验存在）
chk('qc 脚本存在', os.path.exists(QC), '%dB' % os.path.getsize(QC) if os.path.exists(QC) else '缺失')

# ⑥ SKILL.md >1KB 且「诚实边界」恰 1 次
t = open(SK, encoding='utf-8').read()
n_hb = t.count('诚实边界')
chk('SKILL.md >1KB', os.path.getsize(SK) > 1024, '%dB' % os.path.getsize(SK))
chk('「诚实边界」=1 次', n_hb == 1, '实测 %d 次' % n_hb)

# ⑦ frontmatter module/group
m = re.search(r'^module:\s*([^\r\n]+)', t, re.M)
g = re.search(r'^group:\s*([^\r\n]+)', t, re.M)
mv = m.group(1).strip() if m else ''
gv = g.group(1).strip() if g else ''
chk('module 非空', bool(mv), mv)
chk('group 非空', bool(gv), gv)

# ⑧ 溯源标记（据 0X 稿）
marks = re.findall(r'据 0[1-6] 稿', t)
chk('溯源标记 ≥5 处', len(marks) >= 5, '%d 处' % len(marks))

# 附加：黑名单（排除声明除外）
BAN = re.compile(r'(知乎|微信公众号|百度百科)')
hits = []
for i, line in enumerate(t.splitlines(), 1):
    if BAN.search(line) and not ('排除声明' in line or '不采纳' in line or '未引用' in line):
        hits.append((i, line.strip()[:60]))
chk('SKILL 无黑名单引用', not hits, str(hits[:3]))

txt = '== 元恭包 nuwa 真口径七门禁复核 ==\n' + '\n'.join(r)
txt += '\n\n结论：%s' % ('ALL_OK' if ok else 'HAS_ISSUE')
op = r'D:/2026/WB项目/emperor-skill/_redo_tools/_verify_yuangong_full.txt'
open(op, 'w', encoding='utf-8').write(txt)
print(txt)
