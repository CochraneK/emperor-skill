import os, re, io, sys

BASE = r'D:/2026/WB项目/emperor-skill/skills/shang'
PKGS = ['tang-shang-perspective','taiding-shang-perspective','taijia-perspective','woding-perspective',
        'taigeng-perspective','xiaojia-shang-perspective','yongji-perspective','taiwu-perspective']

out = []
for p in PKGS:
    d = os.path.join(BASE, p)
    out.append('='*100)
    out.append('### PACKAGE: ' + p)
    skill = os.path.join(d, 'SKILL.md')
    txt = open(skill, encoding='utf-8').read()
    # frontmatter era
    m = re.search(r'^era:.*$', txt, re.M)
    out.append('--- FM era line: ' + (m.group(0) if m else 'NOT FOUND'))
    # year-like tokens anywhere in frontmatter
    fm = txt.split('---')[1] if txt.startswith('---') else ''
    out.append('--- FM tokens(前\\d+): ' + ' | '.join(sorted(set(re.findall(r'[^|\n]*前\s*\d+[^|\n]*', fm)))))
    # timeline section
    lines = txt.split('\n')
    s = None
    for i, l in enumerate(lines):
        if re.match(r'^##\s+', l) and '时间线' in l:
            s = i; break
    if s is None:
        out.append('--- ## 时间线 NOT FOUND')
    else:
        e = len(lines)
        for j in range(s+1, len(lines)):
            if re.match(r'^##\s+', lines[j]):
                e = j; break
        out.append('--- ## 时间线 (lines %d-%d) ---' % (s+1, e))
        out.extend(lines[s:e])
    # every line containing 前 + digits in whole skill (to catch body mentions)
    out.append('--- ALL 年-like lines in SKILL.md (excl timeline sec already shown) ---')
    for i, l in enumerate(lines):
        if re.search(r'前\s*\d', l) and not (s is not None and s <= i < e):
            out.append('%d: %s' % (i+1, l))
    # 06 file
    f06 = os.path.join(d, 'references', 'research', '06-timeline.md')
    out.append('--- 06-timeline.md ' + ('MISSING' if not os.path.isfile(f06) else '(%d bytes)' % os.path.getsize(f06)))
    if os.path.isfile(f06):
        out.extend(open(f06, encoding='utf-8').read().split('\n'))
    out.append('')

open(r'D:/2026/WB项目/emperor-skill/_redo_tools/_dump_s1.txt','w',encoding='utf-8').write('\n'.join(out))
