# -*- coding: utf-8 -*-
"""复核 A 档第 2 组 6 份被并发冲突的底稿：实测字节/条目/声明/章节号重复/段落重复。"""
import os, re, collections

FILES = [
    (r'skills/ming/zhuyunwen-perspective/references/research/01-writings.md', '朱允炆 01'),
    (r'skills/qing/xuanye-perspective/references/research/06-timeline.md', '康熙 06'),
    (r'skills/song/zhaogou-perspective/references/research/06-timeline.md', '赵构 06'),
    (r'skills/song/zhaokuo-perspective/references/research/03-expression-dna.md', '赵扩 03'),
    (r'skills/tang/lilongji-perspective/references/research/06-timeline.md', '李隆基 06'),
    (r'skills/tang/wuzetian-perspective/references/research/06-timeline.md', '武则天 06'),
]
ROOT = r'D:/2026/WB项目/emperor-skill/'
PREF = re.compile(r'【(?:原话|史料原文|框架推断|史论|文本)[^】]*】')
BAN = re.compile(r'(知乎|微信公众号|百度百科)')
H2 = re.compile(r'^##\s*(.+?)\s*$', re.M)

out = ['== A 档第 2 组并发冲突复核（实测磁盘）==\n']
bad = []
for rel, label in FILES:
    p = ROOT + rel
    b = os.path.getsize(p)
    t = open(p, encoding='utf-8').read()
    lines = t.splitlines()

    n_pref = len(PREF.findall(t))
    tail_ok = '排除声明' in t[-400:]

    # 二级标题重复检测
    h2 = H2.findall(t)
    dup_h2 = [k for k, v in collections.Counter(h2).items() if v > 1]

    # 一级分节号重复检测（## 一、/## 二、…）
    sec = re.findall(r'^##\s*([一二三四五六七八九十]+)、', t, re.M)
    dup_sec = [k for k, v in collections.Counter(sec).items() if v > 1]

    # 段落级重复（>=30 字符的非空行出现两次以上）
    paras = [l.strip() for l in lines if len(l.strip()) >= 30]
    dup_para = [(k, v) for k, v in collections.Counter(paras).items() if v > 1]

    # 黑名单（排除声明行除外）
    ban = [l.strip()[:50] for l in lines
           if BAN.search(l) and not ('排除声明' in l or '不采纳' in l or '未引用' in l)]

    flag = []
    if b < 2500: flag.append('体量不足')
    if n_pref < 5: flag.append('条目不足')
    if not tail_ok: flag.append('声明不在末尾')
    if dup_sec: flag.append('分节号重复 %s' % dup_sec)
    if dup_h2: flag.append('标题重复 %s' % dup_h2[:3])
    if dup_para: flag.append('段落重复 %d 处' % len(dup_para))
    if ban: flag.append('黑名单 %s' % ban[:2])

    status = 'OK ' if not flag else '⚠ '
    out.append('%s %-10s %6dB  条目 %2d  声明 %s  节号 %s' % (
        status, label, b, n_pref, 'OK' if tail_ok else 'NO',
        ''.join(sec) if sec else '-'))
    if flag:
        out.append('      ⚠ ' + ' / '.join(flag))
        bad.append((label, flag, p))
        for k, v in dup_para[:3]:
            out.append('        重复 x%d: %s' % (v, k[:60]))

out.append('\n结论：%s' % ('ALL_OK' if not bad else '%d 个文件有问题' % len(bad)))
txt = '\n'.join(out)
op = ROOT + '_redo_tools/_verify_A2.txt'
open(op, 'w', encoding='utf-8').write(txt)
print(txt)
