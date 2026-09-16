# -*- coding: utf-8 -*-
"""把 _redo_tools 的中间输出 .txt 加进 .gitignore，然后提交 + 推送。"""
import subprocess, os, tempfile

REPO = r"D:/2026/WB项目/emperor-skill"
GI = os.path.join(REPO, ".gitignore")
LINE = "_redo_tools/*.txt"          # 校验脚本中间输出，可由 .py 重新生成
HEADER = "# 校验脚本的中间输出（可由 _redo_tools/*.py 重新生成）"

old = ""
if os.path.exists(GI):
    old = open(GI, encoding="utf-8").read()
if LINE in old:
    print("[gitignore] 规则已存在，跳过写入")
else:
    add = ("\n" if old and not old.endswith("\n") else "") + HEADER + "\n" + LINE + "\n"
    open(GI, "a", encoding="utf-8").write(add)
    print("[gitignore] 已追加:", LINE)

MSG = """chore: 忽略 _redo_tools 中间输出

_redo_tools/*.txt 是 _progress / _verify48 / _audit_all / _era_check / _yearscan
等校验脚本的运行输出，可由脚本重新生成，不进版本库。
"""

def run(args):
    p = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()

rc, out, err = run(["git", "add", ".gitignore"])
print("[add] rc=", rc, out, err)

msg_path = os.path.join(tempfile.gettempdir(), "_es_msg2.txt")
open(msg_path, "w", encoding="utf-8").write(MSG)
rc, out, err = run(["git", "commit", "-F", msg_path])
print("[commit] rc=", rc)
print(out)
if err:
    print("STDERR:", err)
if rc != 0:
    print("（可能无变更可提交）")

rc, out, err = run(["git", "push", "origin", "main"])
print("[push] rc=", rc)
print(out or "(no output)")
if err:
    print("STDERR:", err)

rc, out, err = run(["git", "status", "-sb"])
print("[status -sb]", out)
rc, out, err = run(["git", "log", "--oneline", "-1"])
print("[HEAD]", out)
