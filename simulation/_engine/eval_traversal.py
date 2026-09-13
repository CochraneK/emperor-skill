# -*- coding: utf-8 -*-
"""「帝王遍历」评测指标抽取器
从每个帝王 SKILL.md 抽取可量化结构指标，作为评分卡的客观底座。
输出：eval_metrics.json + 控制台紧凑表。
"""
import os, re, json, glob, sys

SKILLS = r"D:/2026/WB项目/蒸馏skill/.workbuddy/skills"
REPO   = r"D:/2026/WB项目/emperor-skill/skills"
DYNASTY = [("tang", "唐"), ("song", "宋"), ("yuan", "元"), ("ming", "明"), ("qing", "清")]


def sec(text, name):
    m = re.search(r'^##\s*' + re.escape(name) + r'.*?$(.*?)(?=^##\s|\Z)', text, re.M | re.S)
    return m.group(1) if m else ""


def analyze(t):
    lines = t.splitlines()
    models = len(re.findall(r'^###\s*模型\s*\d+', t, re.M))
    cites = t.count("【")
    dna = sec(t, "表达DNA");      dna_items = len(re.findall(r'^-\s', dna, re.M))
    hb  = sec(t, "诚实边界");     hb_items  = len(re.findall(r'^-\s', hb, re.M))
    vals = sec(t, "价值观与反模式"); tens_items = len(re.findall(r'^\d+\.\s', vals, re.M))
    heur = sec(t, "决策启发式");   heur_items = len(re.findall(r'^\d+\.\s', heur, re.M))
    src  = sec(t, "调研来源")
    one = len(re.findall(r'^-\s*一手[:：]', t, re.M))
    two = len(re.findall(r'^-\s*二手[:：]', t, re.M))
    quotes = len(re.findall(r'^>', sec(t, "调研来源"), re.M))
    # 同行：底稿合计字数
    return dict(
        lines=len(lines), chars=len(t),
        models=models, cites=cites,
        dna=dna_items, hb=hb_items, tens=tens_items, heur=heur_items,
        one=one, two=two, ratio=round(one / (one + two), 3) if (one + two) else 0.0,
        role_rule=("角色扮演规则" in t), zhen=t.count("朕"), quotes=quotes,
    )


def main():
    rows = []
    for d, cn in DYNASTY:
        for p in sorted(glob.glob(os.path.join(REPO, d, "*-perspective"))):
            key = os.path.basename(p).replace("-perspective", "")
            sk = os.path.join(SKILLS, key + "-perspective", "SKILL.md")
            if not os.path.exists(sk):
                rows.append(dict(dyn=cn, key=key, missing=True)); continue
            m = analyze(open(sk, encoding="utf-8").read())
            m.update(dyn=cn, key=key, missing=False)
            rows.append(m)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eval_metrics.json")
    json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 紧凑表
    print(f"{'朝代':<3}{'key':<16}{'行':>4}{'模型':>5}{'引证':>5}{'DNA':>5}{'边界':>5}{'张力':>5}{'启发':>5}{'一手':>5}{'二手':>5}{'占比':>7}{'朕':>5}")
    for r in rows:
        if r.get("missing"):
            print(f"{r['dyn']:<3}{r['key']:<16}  <缺失>"); continue
        print(f"{r['dyn']:<3}{r['key']:<16}{r['lines']:>5}{r['models']:>6}{r['cites']:>6}{r['dna']:>6}"
              f"{r['hb']:>6}{r['tens']:>6}{r['heur']:>6}{r['one']:>6}{r['two']:>6}{r['ratio']:>8}{r['zhen']:>6}")
    print(f"\n共 {len(rows)} 条；输出 -> {out}")


if __name__ == "__main__":
    main()
