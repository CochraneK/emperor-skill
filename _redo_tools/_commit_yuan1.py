# -*- coding: utf-8 -*-
"""提交 + 推送 emperor-skill：元太祖/太宗两包 + 后世帝王简报 + 体检脚本。"""
import subprocess, os, tempfile

REPO = r"D:/2026/WB项目/emperor-skill"

MSG = """补元前四汗之二：元太祖铁木真、元太宗窝阔台

- 新增 skills/yuan/temujin-perspective（元太祖 铁木真，1206–1227）
- 新增 skills/yuan/ogodei-perspective（元太宗 窝阔台，1229–1241）
- 两包均 6/6 通过；经 _verify_pkgs.py 独立复核：硬错误 0、警告 0
- 史料门禁已守：
  · 两人「生前均未称帝」，庙号系忽必烈建元后追尊（1266 年追谥），身份卡与诚实边界均已明写
  · 无亲笔文书传世；「札撒」原文已佚，凡引一律标「系征引，非原文」
  · 《元史》/《蒙古秘史》/《史集》/《圣武亲征录》四源歧异并列不调和，04 卷各设歧异表
  · 《蒙古秘史》标为明初汉字音写本（旁译+总译），不得视为逐字原文
  · 1227–1229 拖雷监国空档单列，明写「非在位期」
  · 因生前未称帝，角色自称用「我/吾」而非汉制的「朕」，并单列称谓纪律说明

- 新增 _nuwa_brief_later.md：后世帝王 nuwa 蒸馏简报（秦以后各朝通用），
  含各朝一手史料清单表与 module/group 命名对照表
- 新增 _redo_tools/_verify_pkgs.py：按朝代目录的通用包体检脚本（自跑质检，不复用上报数据）
- 新增 _redo_tools/_coverage.py：帝王覆盖度与站点登记一致性盘点脚本
"""

ADD = [
    "skills/yuan/temujin-perspective",
    "skills/yuan/ogodei-perspective",
    "_nuwa_brief_later.md",
    "_redo_tools/_verify_pkgs.py",
    "_redo_tools/_coverage.py",
]


def run(args):
    p = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


# 防误删：先确认无 index.lock
lock = os.path.join(REPO, ".git", "index.lock")
if os.path.exists(lock):
    os.remove(lock)
    print("[clean] index.lock removed")

for a in ADD:
    rc, out, err = run(["git", "add", "--", a])
    print(f"[add {a}] rc={rc}", err or "")

rc, out, err = run(["git", "status", "--porcelain"])
print("\n[status]")
print(out)

msg_path = os.path.join(tempfile.gettempdir(), "_es_msg3.txt")
open(msg_path, "w", encoding="utf-8").write(MSG)
rc, out, err = run(["git", "commit", "-F", msg_path])
print("\n[commit] rc=", rc)
print(out or "(no output)")
if err:
    print("STDERR:", err)

if rc == 0:
    rc, out, err = run(["git", "push", "origin", "main"])
    print("\n[push] rc=", rc)
    print(out or "")
    if err:
        print("STDERR:", err)

rc, out, err = run(["git", "log", "--oneline", "-1"])
print("\n[HEAD]", out)
rc, out, err = run(["git", "ls-remote", "origin", "main"])
print("[remote]", out)
