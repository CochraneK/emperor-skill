# -*- coding: utf-8 -*-
"""Nuwa Audit v2 的低成本全仓静态扫描器。

重要：本脚本只做可机械检查的 L1/L2 信号与 L4 工程检查；L3 语义质量必须另行模型/人工审核。
最低字数、KB、文件大小不属于 Nuwa quality gate。
mtime 只允许作为历史线索，不能单独证明正序或倒序。
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
DIMS = ["01-writings", "02-conversations", "03-expression-dna",
        "04-external-views", "05-decisions", "06-timeline"]
TRACE = re.compile(r"据\s*0[1-6]\s*稿")
BAN = ("知乎", "微信公众号", "百度百科")


def packages():
    for dyn in sorted(p for p in SKILLS.iterdir() if p.is_dir() and not p.name.startswith("_")):
        for pkg in sorted(p for p in dyn.iterdir() if p.is_dir()):
            if (pkg / "SKILL.md").exists():
                yield dyn.name, pkg


def scan(dyn, pkg):
    skill = pkg / "SKILL.md"
    text = skill.read_text(encoding="utf-8", errors="ignore")
    research_dir = pkg / "references" / "research"
    present = []
    missing = []
    evidence_flags = []
    for dim in DIMS:
        f = research_dir / f"{dim}.md"
        if not f.exists():
            missing.append(dim)
            continue
        present.append(dim)
        rt = f.read_text(encoding="utf-8", errors="ignore")
        # 黑名单词出现本身不等于违规；只有非排除语境才需要语义复核。
        if any(x in rt for x in BAN) and "排除" not in rt:
            evidence_flags.append(f"{dim}: blacklist term needs review")

    # L1: 只输出 provenance 信号，不凭文件结构宣判。
    if not present:
        provenance = "REVIEW"
        prov_note = "no research files; provenance must be established independently"
    elif missing:
        provenance = "REVIEW"
        prov_note = f"research profile partial ({len(present)}/6); packaging/provenance review required"
    else:
        trace_count = len(TRACE.findall(text))
        provenance = "REVIEW" if trace_count == 0 else "SIGNAL-OK"
        prov_note = f"6/6 research present; explicit trace markers={trace_count}; history still required for final PASS"

    # L4: 工程检查。这里不把恰好 8 文件、SKILL 大小、research 大小当门禁。
    engineering = []
    if not re.search(r"^name:\s*\S+?-perspective\s*$", text, re.M):
        engineering.append("frontmatter name missing/invalid")
    if not re.search(r"^module:\s*\S", text, re.M):
        engineering.append("module missing")
    if not re.search(r"^group:\s*\S", text, re.M):
        engineering.append("group missing")
    if "诚实边界" not in text:
        engineering.append("honesty boundary section missing")

    return {
        "dynasty": dyn,
        "skill": pkg.name,
        "research": f"{len(present)}/6",
        "provenance_signal": provenance,
        "provenance_note": prov_note,
        "evidence_flags": evidence_flags,
        "engineering": engineering,
    }


def main():
    rows = [scan(d, p) for d, p in packages()]
    print(f"packages={len(rows)}")
    print("NOTE: this is a static signal scan, not a Nuwa PASS/FAIL verdict.")
    for r in rows:
        if r["provenance_signal"] != "SIGNAL-OK" or r["evidence_flags"] or r["engineering"]:
            print(f"[{r['dynasty']}] {r['skill']} | research={r['research']} | L1={r['provenance_signal']}")
            print(f"  provenance: {r['provenance_note']}")
            for x in r["evidence_flags"]:
                print(f"  evidence: {x}")
            for x in r["engineering"]:
                print(f"  engineering: {x}")


if __name__ == "__main__":
    main()
