# -*- coding: utf-8 -*-
"""通用包校验：对指定朝代目录下的所有 -perspective 包做完整体检。
用法: python _verify_pkgs.py yuan [包1 包2 ...]   (不给包名=全目录)

校验项（自跑，不复用 worker 上报数据）：
  1. scripts/quality_check.py 自跑 -> 6 项全 PASS
  2. references/research/01..06 六份齐全且各 >= 2.5KB
  3. 六份底稿末尾均有排除声明（知乎 / 百度百科 / 微信）
  4. 「诚实边界」四字全文恰好 1 次
  5. frontmatter 的 module / group 与朝代匹配
  6. SKILL.md 12 章标题齐全
  7. 包内无越纲文件（只允许 SKILL.md / 六维底稿 / quality_check.py）
"""
import os, re, sys, subprocess

BASE = r"D:/2026/WB项目/emperor-skill/skills"

ALLOWED = {"SKILL.md", "scripts/quality_check.py"}
for i, n in enumerate(["writings", "conversations", "expression-dna",
                       "external-views", "decisions", "timeline"], start=1):
    ALLOWED.add(f"references/research/0{i}-{n}.md")

CHAPTERS = ["角色扮演规则", "工作流程", "身份卡", "核心心智模型", "决策启发式",
            "表达DNA", "时间线", "价值观与反模式", "智识谱系", "理想与渴望",
            "诚实边界", "调研来源"]

PY = sys.executable


def verify(dyn, pkgs=None):
    d = os.path.join(BASE, dyn)
    if not os.path.isdir(d):
        print("!! 无此目录", d)
        return []
    names = pkgs if pkgs else sorted(p for p in os.listdir(d)
                                     if os.path.isdir(os.path.join(d, p)))
    problems, warns = [], []
    for p in names:
        pd = os.path.join(d, p)
        sk = os.path.join(pd, "SKILL.md")
        if not os.path.exists(sk):
            problems.append(f"{p}: 缺 SKILL.md")
            continue
        size = os.path.getsize(sk)
        text = open(sk, encoding="utf-8", errors="replace").read()

        # 1) 自跑质检
        qc = os.path.join(pd, "scripts", "quality_check.py")
        if not os.path.exists(qc):
            problems.append(f"{p}: 缺 scripts/quality_check.py")
            qres = ""
        else:
            r = subprocess.run([PY, "quality_check.py", "SKILL.md"], cwd=pd,
                               capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            qres = (r.stdout or "") + (r.stderr or "")
            fails = [ln for ln in qres.splitlines() if "FAIL" in ln]
            if fails:
                problems.append(f"{p}: 质检未全过 -> " + " | ".join(x.strip() for x in fails))

        # 2) 六维底稿
        for i in range(1, 7):
            fs = [f for f in os.listdir(os.path.join(pd, "references", "research"))
                  if f.startswith(f"0{i}-")] if os.path.isdir(
                  os.path.join(pd, "references", "research")) else []
            if not fs:
                problems.append(f"{p}: 缺 0{i}-*.md")
                continue
            fp = os.path.join(pd, "references", "research", fs[0])
            if os.path.getsize(fp) < 2560:
                problems.append(f"{p}: {fs[0]} 不足 2.5KB ({os.path.getsize(fp)}B)")
            # 3) 排除声明
            t = open(fp, encoding="utf-8", errors="replace").read()
            miss = [k for k in ("知乎", "百度百科", "微信") if k not in t]
            if miss:
                problems.append(f"{p}: {fs[0]} 排除声明缺 {miss}")

        # 4) 诚实边界计数
        c = text.count("诚实边界")
        if c != 1:
            problems.append(f"{p}: 「诚实边界」出现 {c} 次（应为 1）")

        # 5) frontmatter module / group
        m = re.search(r"^---\r?\n(.*?)\r?\n---", text, re.S | re.M)
        fm = m.group(1) if m else ""
        def g(k):
            r = re.search(r"^" + k + r":[ \t]*([^\r\n]*)", fm, re.M)
            return (r.group(1).strip() if r else "")
        mod, grp = g("module"), g("group")
        if not mod or not grp:
            problems.append(f"{p}: frontmatter 缺 module/group (module={mod!r} group={grp!r})")
        else:
            if not mod.startswith(dyn):
                problems.append(f"{p}: module={mod} 与目录 {dyn} 不匹配")
            if not grp.startswith(dyn):
                problems.append(f"{p}: group={grp} 与目录 {dyn} 不匹配")

        # 6) 12 章
        miss_ch = [c2 for c2 in CHAPTERS if f"## {c2}" not in text]
        if miss_ch:
            problems.append(f"{p}: 缺章节 " + "、".join(miss_ch))

        # 7) 越纲文件
        extra = []
        for root, _, fs in os.walk(pd):
            for f in fs:
                rel = os.path.relpath(os.path.join(root, f), pd).replace("\\", "/")
                if rel not in ALLOWED:
                    extra.append(rel)
        if extra:
            warns.append(f"{p}: 越纲文件 {extra}")

        flag = "ERR" if any(x.startswith(p) for x in problems) else "OK "
        print(f"[{flag}] {dyn}/{p}  ({size}B)  module={mod} group={grp}")

    print()
    print(f"--- {dyn}: 检查 {len(names)} 包 | 硬错误 {len(problems)} | 警告 {len(warns)} ---")
    for x in problems:
        print("  !", x)
    for x in warns:
        print("  ~", x)
    return problems


if __name__ == "__main__":
    dyn = sys.argv[1] if len(sys.argv) > 1 else "yuan"
    pkgs = sys.argv[2:] or None
    verify(dyn, pkgs)
