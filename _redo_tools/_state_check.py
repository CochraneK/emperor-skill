# -*- coding: utf-8 -*-
import os, json, re, sys

ROOT = "D:/2026/WB项目/emperor-skill"
XIHAN = os.path.join(ROOT, "skills", "xihan")
YUAN = os.path.join(ROOT, "skills", "yuan")

def pkginfo(p):
    out = {"path": p, "skill_md": None, "research": [], "out_txt": [], "frontmatter_module": None, "frontmatter_group": None}
    skill = os.path.join(p, "SKILL.md")
    if os.path.isfile(skill):
        sz = os.path.getsize(skill)
        out["skill_md"] = sz
        try:
            txt = open(skill, encoding="utf-8").read()
            m = re.search(r"module:\s*(.+?)\s*$", txt, re.M)
            g = re.search(r"group:\s*(.+?)\s*$", txt, re.M)
            if m: out["frontmatter_module"] = m.group(1).strip()
            if g: out["frontmatter_group"] = g.group(1).strip()
        except Exception as e:
            out["read_err"] = str(e)
    ref = os.path.join(p, "references", "research")
    if os.path.isdir(ref):
        out["research"] = sorted(os.listdir(ref))
    for f in os.listdir(p) if os.path.isdir(p) else []:
        if f == "_out.txt":
            out["out_txt"].append(f)
    return out

print("===== XIHAN PACKAGES =====")
if os.path.isdir(XIHAN):
    for name in sorted(os.listdir(XIHAN)):
        p = os.path.join(XIHAN, name)
        if os.path.isdir(p):
            info = pkginfo(p)
            print(f"\n[{name}]")
            print(f"  SKILL.md: {info['skill_md']} bytes")
            print(f"  module={info['frontmatter_module']} group={info['frontmatter_group']}")
            print(f"  research({len(info['research'])}): {info['research']}")
            if info['out_txt']:
                print(f"  !! STRAY _out.txt: {info['out_txt']}")
else:
    print("XIHAN dir NOT FOUND")

print("\n===== YUAN 前四汗 称谓条款检查 =====")
for name in ["guyuk-perspective", "mongke-perspective", "temujin-perspective", "ogodei-perspective"]:
    p = os.path.join(YUAN, name)
    skill = os.path.join(p, "SKILL.md")
    has = os.path.isfile(skill)
    txt = open(skill, encoding="utf-8").read() if has else ""
    # 称谓纪律关键词
    kw = ["称谓纪律", "追尊", "译写", "汗"]
    hits = {k: (k in txt) for k in kw}
    print(f"\n[{name}] skill_md={os.path.getsize(skill) if has else 'MISSING'}")
    print(f"  称谓纪律={hits['称谓纪律']} 追尊={hits['追尊']} 译写={hits['译写']} 汗={hits['汗']}")
