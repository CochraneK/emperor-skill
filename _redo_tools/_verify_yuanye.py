# -*- coding: utf-8 -*-
"""独立复核 yuanye-perspective：不采信任何自报结果，全部自跑。
检查项：8 文件 / 六维底稿齐全且 ≥2.5KB / 每份末页排除声明 / quality_check 6/6 /
SKILL.md >1KB / 「诚实边界」四字全文仅一次 / frontmatter module·group / 无 stray 文件。
输出落盘 _verify_yuanye.txt"""
import pathlib, re, subprocess, sys

ES = pathlib.Path(r"D:/2026/WB项目/emperor-skill")
PY = r"C:/Users/cunyi/.workbuddy/binaries/python/versions/3.13.12/python.exe"
PKG = ES / "skills/nanbeichao/yuanye-perspective"
out = []
def w(s=""): out.append(str(s))
ok_all = True
def chk(cond, msg):
    global ok_all
    w(("  [OK]   " if cond else "  [FAIL] ") + msg)
    if not cond:
        ok_all = False

w("== 1. 包内文件清单（应为 8 个：SKILL.md + 6 底稿 + scripts/quality_check.py）==")
files = sorted([f for f in PKG.rglob("*") if f.is_file()])
for f in files:
    w(f"      {str(f.relative_to(PKG))}  ({f.stat().st_size}B)")
chk(len(files) == 8, f"文件总数 = {len(files)}（应为 8）")

w("")
w("== 2. 六维底稿齐全性与体量（每份 ≥2.5KB）==")
for n in ["01-writings", "02-conversations", "03-expression-dna",
          "04-external-views", "05-decisions", "06-timeline"]:
    p = PKG / "references/research" / (n + ".md")
    if not p.exists():
        chk(False, f"{n}.md 缺失")
        continue
    b = p.stat().st_size
    t = p.read_text(encoding="utf-8")
    has_excl = ("排除声明" in t)
    chk(b >= 2500 and has_excl, f"{n}.md  {b}B  ≥2.5KB={'Y' if b>=2500 else 'N'}  排除声明={'Y' if has_excl else 'N'}")

w("")
w("== 3. quality_check.py 自跑（须 6/6）==")
r = subprocess.run([PY, str(PKG / "scripts/quality_check.py"), str(PKG / "SKILL.md")],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
w(r.stdout.strip())
chk("全部通过" in r.stdout, "quality_check 6/6 通过")

w("")
w("== 4. SKILL.md 体量与纪律 ==")
sk = PKG / "SKILL.md"
t = sk.read_text(encoding="utf-8")
chk(sk.stat().st_size > 1024, f"SKILL.md {sk.stat().st_size}B >1KB")
n_hb = t.count("诚实边界")
chk(n_hb == 1, f"「诚实边界」四字出现 {n_hb} 次（须为 1）")
m = re.search(r'^module:\s*(.+?)[ \t\r]*$', t, re.M)
g = re.search(r'^group:\s*(.+?)[ \t\r]*$', t, re.M)
chk(bool(m) and m.group(1).strip() == "nanbeichao-emperors", f"module = {m.group(1).strip() if m else None}")
chk(bool(g) and g.group(1).strip() == "nanbeichao-main", f"group = {g.group(1).strip() if g else None}")
# 六维溯源标记（SKILL 基于六维的证据）
n_src = len(re.findall(r'据\s*0[1-6]\s*稿', t))
chk(n_src >= 5, f"SKILL.md 中「据 0X 稿」溯源标记 {n_src} 处（≥5 即视为由六维蒸馏）")

w("")
w("== 5. 与参考合规包体量对照 ==")
ref = ES / "skills/nanbeichao/yuanziyou-perspective/SKILL.md"
w(f"      yuanziyou SKILL.md = {ref.stat().st_size}B ；yuanye = {sk.stat().st_size}B")

w("")
w("RESULT: " + ("ALL_OK" if ok_all else "HAS_FAILURE"))
(ES / "_redo_tools/_verify_yuanye.txt").write_text("\n".join(out), encoding="utf-8")
print("RESULT:", "ALL_OK" if ok_all else "HAS_FAILURE")
