# -*- coding: utf-8 -*-
"""修复前侦察：
1) 在不合规包的底稿里搜信源黑名单字样（知乎/微信公众号/百度百科）——若出现则不可机械补声明
2) 估算「追加标准排除声明(约 300B)」后，有多少底稿能跨过 2.5KB 门槛
输出落盘 _plan_fix.txt
"""
import pathlib, re

ES = pathlib.Path(r"D:/2026/WB项目/emperor-skill")
SKILLS = ES / "skills"
DIMS = ["01-writings", "02-conversations", "03-expression-dna",
        "04-external-views", "05-decisions", "06-timeline"]
BLACK = re.compile(r"知乎|微信公众号|微信公众|百度百科")

out = []
def w(s=""): out.append(str(s))

hit_pkgs, need_expand, fixable_声明 = [], [], []
total_missing, total_small, total_black = 0, 0, 0
detail_small = []

for d in sorted([p for p in SKILLS.iterdir() if p.is_dir()]):
    for p in sorted([x for x in d.iterdir() if x.is_dir()]):
        if not (p / "SKILL.md").exists():
            continue
        for n in DIMS:
            f = p / "references/research" / (n + ".md")
            if not f.exists():
                continue
            t = f.read_text(encoding="utf-8", errors="ignore")
            b = f.stat().st_size
            has = "排除声明" in t
            # 剔除「排除声明」自身所在行（声明里必然提到黑名单词），只判正文引用
            DECL = re.compile(r"排除声明|未引用|未采纳|不采纳|一概不采|不作为立论|不得作为|黑名单")
            real_lines = [l.strip()[:90] for l in t.splitlines()
                          if BLACK.search(l) and not DECL.search(l)]
            blk = BLACK.findall("\n".join(real_lines))
            has_decl = "排除声明" in t
            if not has:
                total_missing += 1
            if b < 2500:
                total_small += 1
                if b + 320 < 2500:   # 补声明后仍不足
                    need_expand.append((d.name, p.name, n, b))
                    detail_small.append(f"  [{d.name}] {p.name}/{n}.md  {b}B → 补声明后仍不足，需实质扩写")
            if blk:
                total_black += 1
                hit_pkgs.append((d.name, p.name, n, set(blk), [l.strip()[:90] for l in t.splitlines() if BLACK.search(l)]))

w("== 修复前侦察 ==")
w(f"缺「排除声明」的底稿数: {total_missing}")
w(f"<2.5KB 的底稿数: {total_small}，其中补声明后仍不足的: {len(need_expand)}")
w(f"底稿中出现信源黑名单字样的份数: {total_black}")
w("")
if hit_pkgs:
    w("== ⚠ 出现黑名单字样的底稿（不可机械补声明，须人工判定） ==")
    for dyn, sid, n, kws, lines in hit_pkgs:
        w(f"  [{dyn}] {sid}/{n}.md  命中: {sorted(kws)}")
        for l in lines[:3]:
            w(f"        {l}")
    w("")
w("== 补声明后仍不足 2.5KB、须实质扩写的底稿（按体量升序，取前 40） ==")
for dyn, sid, n, b in sorted(need_expand, key=lambda x: x[3])[:40]:
    w(f"  [{dyn}] {sid}/{n}.md  {b}B → 补声明后仍不足，需实质扩写")
w("")
w(f"（共 {len(need_expand)} 份需实质扩写）")

(ES / "_redo_tools/_plan_fix.txt").write_text("\n".join(out), encoding="utf-8")
print(f"缺声明 {total_missing} / 体量不足 {total_small} / 补后仍不足 {len(need_expand)} / 黑名单命中 {total_black}")
