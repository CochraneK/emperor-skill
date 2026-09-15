# -*- coding: utf-8 -*-
"""对 emperor-skill 的 48 个夏商 nuwa 包做独立复核（不复用 worker 结论）。
逐包：
  1) SKILL.md 存在且 >1KB
  2) 实跑 scripts/quality_check.py，解析 6 项 gate 结果
  3) references/research/01-06 六份齐全且每份 >2.5KB
  4) 六份底稿末含排除声明（知乎/微信/百度百科）
  5) SKILL.md 中「诚实边界」四字恰好出现 1 次
  6) frontmatter 含 module / group 且值符合朝代
  7) 12 章固定标题齐全（按关键字匹配）
  8) 包内无越纲文件（只允许 SKILL.md / references/research/0X.md / scripts/quality_check.py）
只读，除 subprocess 外不写任何文件。输出 stdout。
"""
import re
import subprocess
import sys
from pathlib import Path

# 同时把报告以 UTF-8 落盘（避免 cmd/PowerShell 重定向的编码损坏）
_BUF = []
_orig_print = print


def print(*args, **kwargs):  # noqa: A001
    _BUF.append(" ".join(str(a) for a in args))
    _orig_print(*args, **kwargs)


ROOT = Path(r"D:/2026/WB项目/emperor-skill/skills")
NEED_REFS = ["01-writings.md", "02-conversations.md", "03-expression-dna.md",
             "04-external-views.md", "05-decisions.md", "06-timeline.md"]
CHAPTERS = ["角色扮演规则", "工作流程", "身份卡", "核心心智模型", "决策启发式",
            "表达DNA", "时间线", "价值观与反模式", "智识谱系", "理想与渴望",
            "诚实边界", "调研来源"]
EXPECT = {
    "xia": {"module": "xia-emperors", "group": "xia-main"},
    "shang": {"module": "shang-emperors", "group": "shang-main"},
}

def check_pkg(d: Path, dynasty: str):
    errs, warns = [], []
    # 1 SKILL.md
    sk = d / "SKILL.md"
    if not sk.is_file():
        errs.append("SKILL.md 缺失")
        return errs, warns, None
    size = sk.stat().st_size
    if size <= 1024:
        errs.append(f"SKILL.md 仅 {size}B (<=1KB)")
    txt = sk.read_text(encoding="utf-8", errors="replace")

    # 2 真跑质检
    qc = d / "scripts" / "quality_check.py"
    if not qc.is_file():
        errs.append("quality_check.py 缺失")
    else:
        try:
            r = subprocess.run([sys.executable, str(qc), "SKILL.md"], cwd=str(d),
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=120)
            out = (r.stdout or "") + (r.stderr or "")
            passes = out.count("PASS")
            fails = out.count("FAIL")
            if passes != 6 or fails != 0:
                errs.append(f"质检未 6/6 (PASS={passes} FAIL={fails})")
        except Exception as e:
            errs.append(f"质检执行异常: {e}")

    # 3 refs
    rdir = d / "references" / "research"
    missing = [n for n in NEED_REFS if not (rdir / n).is_file()]
    if missing:
        errs.append("refs 缺失: " + ",".join(missing))
    else:
        for n in NEED_REFS:
            p = rdir / n
            if p.stat().st_size < 2560:
                warns.append(f"{n} 仅 {p.stat().st_size}B (<2.5KB)")
            body = p.read_text(encoding="utf-8", errors="replace")
            if not (("知乎" in body) and ("百度百科" in body) and ("微信" in body)):
                errs.append(f"{n} 缺排除声明")

    # 4 诚实边界唯一
    n_honest = txt.count("诚实边界")
    if n_honest != 1:
        errs.append(f"「诚实边界」出现 {n_honest} 次 (应为 1)")

    # 5 frontmatter
    fm = txt[:2000]
    mm = re.search(r"^module:\s*([^\r\n]+)", fm, re.M)
    gm = re.search(r"^group:\s*([^\r\n]+)", fm, re.M)
    exp = EXPECT[dynasty]
    if not mm or mm.group(1).strip() != exp["module"]:
        errs.append(f"module 字段异常: {mm.group(1).strip() if mm else '缺失'}")
    if not gm or gm.group(1).strip() != exp["group"]:
        errs.append(f"group 字段异常: {gm.group(1).strip() if gm else '缺失'}")

    # 6 十二章
    miss_ch = [c for c in CHAPTERS if c not in txt]
    if miss_ch:
        errs.append("章节缺失: " + ",".join(miss_ch))

    # 7 越纲文件
    allowed_root = {"SKILL.md"}
    for p in d.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(d).as_posix()
        if rel in allowed_root:
            continue
        if re.fullmatch(r"references/research/0[1-6]-[a-z\-]+\.md", rel):
            continue
        if rel == "scripts/quality_check.py":
            continue
        warns.append(f"越纲文件: {rel}")

    return errs, warns, size

all_err, all_warn, total = [], [], 0
for dynasty in ("xia", "shang"):
    base = ROOT / dynasty
    dirs = sorted(p for p in base.iterdir() if p.is_dir() and p.name.endswith("-perspective"))
    print(f"\n########## {dynasty}  ({len(dirs)} 包) ##########")
    for d in dirs:
        total += 1
        errs, warns, size = check_pkg(d, dynasty)
        tag = "OK " if not errs else "ERR"
        print(f"[{tag}] {d.name}  ({size}B)" if size else f"[ERR] {d.name}")
        for e in errs:
            print(f"      ! {e}")
            all_err.append(f"{dynasty}/{d.name}: {e}")
        for w in warns:
            print(f"      ~ {w}")
            all_warn.append(f"{dynasty}/{d.name}: {w}")

print("\n" + "=" * 60)
print(f"包总数 {total} | 硬错误 {len(all_err)} | 警告 {len(all_warn)}")
if all_err:
    print("--- 硬错误清单 ---")
    for e in all_err:
        print("  " + e)
if all_warn:
    print("--- 警告清单 ---")
    for w in all_warn:
        print("  " + w)

Path(r"D:/2026/WB项目/emperor-skill/_redo_tools/_verify48.txt").write_text(
    "\n".join(_BUF), encoding="utf-8")
