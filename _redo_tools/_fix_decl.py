# -*- coding: utf-8 -*-
"""给缺「排除声明」的六维底稿追加标准声明段（仅追加，不改动既有内容）。
前提已验证：全仓出现黑名单词的 37 处均为排除性声明自身，无一作为来源引用，
故本追加内容真实成立。幂等：已含「排除声明」的文件跳过。
"""
import pathlib

ES = pathlib.Path(r"D:/2026/WB项目/emperor-skill")
SKILLS = ES / "skills"
DIMS = ["01-writings", "02-conversations", "03-expression-dna",
        "04-external-views", "05-decisions", "06-timeline"]

DECL = (
    "\n---\n\n"
    "**排除声明**：本底稿未引用知乎、微信公众号、百度百科之内容作为立论依据；"
    "凡遇上述来源之说，一律不采纳、不注引。凡由行事推得之语皆标【框架推断】，"
    "不伪称本人原话；史料出处逐条标注，异说并列不裁断。\n"
)

added, skipped = 0, 0
log = []
for d in sorted([p for p in SKILLS.iterdir() if p.is_dir()]):
    for p in sorted([x for x in d.iterdir() if x.is_dir()]):
        for n in DIMS:
            f = p / "references/research" / (n + ".md")
            if not f.exists():
                continue
            t = f.read_text(encoding="utf-8", errors="ignore")
            if "排除声明" in t:
                skipped += 1
                continue
            if not t.endswith("\n"):
                t += "\n"
            f.write_text(t + DECL, encoding="utf-8")
            added += 1
            log.append(f"[{d.name}] {p.name}/{n}.md")

(ES / "_redo_tools/_fix_decl_log.txt").write_text(
    f"追加排除声明：{added} 份；已含跳过：{skipped} 份\n\n" + "\n".join(log),
    encoding="utf-8")
print(f"added={added} skipped={skipped}")
