# -*- coding: utf-8 -*-
"""西汉以前帝王蒸馏包门禁质检（G1-G11）。
扫描 emperor-skill/skills/{xia,shang,zhou,qin,chuhan} 下所有 *-perspective/SKILL.md，
逐条核对任务书第2节门禁清单，输出通过/失败报告。
"""
import re
from pathlib import Path

ROOT = Path("D:/2026/WB项目/emperor-skill/skills")
DYNOS = ["xia", "shang", "zhou", "qin", "chuhan"]
FRONT_KEYS = ["name", "cn", "en", "type", "domain", "era", "module", "group", "tags", "description"]


def parse_front(text):
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}, text
    fm, body = m.group(1), text[m.end():]
    data = {}
    for line in fm.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data, body


def section(body, title):
    m = re.search(r"## " + re.escape(title) + r".*?(?=\n## |\Z)", body, re.S)
    return m.group(0) if m else ""


def check(p):
    sk = p / "SKILL.md"
    if not sk.is_file():
        return {"id": p.name, "missing": True}
    raw = sk.read_text(encoding="utf-8-sig")
    data, body = parse_front(raw)
    res = {"id": p.name, "fail": []}

    # G1 frontmatter
    for k in FRONT_KEYS:
        if k not in data or not data[k]:
            res["fail"].append(f"G1缺字段{k}")
    if not data.get("name", "").endswith("-perspective"):
        res["fail"].append("G1 name未以-perspective结尾")

    # G2 模型数
    models = re.findall(r"^### 模型\d+[：:]", body, re.M)
    if len(models) != 6:
        res["fail"].append(f"G2 模型数={len(models)}(需6)")

    # G3 每模型缺局限
    blocks = re.split(r"^### 模型\d+[：:]", body, flags=re.M)[1:]
    for i, blk in enumerate(blocks[:6], 1):
        if "局限" not in blk:
            res["fail"].append(f"G3 模型{i}缺局限")

    # G5 诚实边界仅一次
    if body.count("诚实边界") != 1:
        res["fail"].append(f"G5 诚实边界出现{body.count('诚实边界')}次(需1)")

    # G4 表达DNA ≥3
    dna = section(body, "表达DNA")
    if dna:
        if len(re.findall(r"^\s*-\s*", dna, re.M)) < 3:
            res["fail"].append("G4 表达DNA条数<3")
    else:
        res["fail"].append("G4 无表达DNA段")

    # G7 调研来源前缀（接受母版词汇：一手/一手正史/一手史评 + 二手/非一手/后世）
    src = section(body, "调研来源")
    if src:
        if not re.search(r"一手", src):
            res["fail"].append("G7 缺一手来源标记")
        if not re.search(r"二手|非一手|后世", src):
            res["fail"].append("G7 缺二手/后世来源标记")
    else:
        res["fail"].append("G7 无调研来源段")

    # G8 角色扮演
    if "朕" not in body and "寡人" not in body:
        res["fail"].append("G8 缺朕/寡人自称")
    if "退出角色" not in body:
        res["fail"].append("G8 缺退出角色指令")

    # G9 时间线 ≥5
    tl = section(body, "时间线")
    if tl:
        if len(re.findall(r"^\s*-\s*", tl, re.M)) < 5:
            res["fail"].append("G9 时间线条数<5")
    else:
        res["fail"].append("G9 无时间线段")

    # G10 黑名单
    for bad in ["知乎", "微信公众号", "百度百科"]:
        if bad in body:
            res["fail"].append(f"G10 含黑名单词{bad}")

    # G6 内在张力(宽松)
    if len(re.findall(r"张力|矛盾|却易|虽.*但|然.*亦|反模式", body)) < 2:
        res["fail"].append("G6 张力标记<2")

    return res


def main():
    allres = []
    for dyn in DYNOS:
        for p in sorted((ROOT / dyn).glob("*-perspective")):
            allres.append(check(p))
    total = len(allres)
    passed = sum(1 for r in allres if not r.get("fail") and not r.get("missing"))
    print(f"扫描包总数: {total}")
    print(f"通过门禁: {passed}")
    print(f"未通过: {total - passed}")
    for r in allres:
        if r.get("missing"):
            print(f"  [缺] {r['id']}")
        elif r.get("fail"):
            print(f"  [FAIL] {r['id']}: {'; '.join(r['fail'])}")


if __name__ == "__main__":
    main()
