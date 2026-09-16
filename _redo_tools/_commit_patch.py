# -*- coding: utf-8 -*-
"""提交元太祖/太宗两包的称谓切换说明补丁。"""
import subprocess, os, tempfile

REPO = r"D:/2026/WB项目/emperor-skill"

MSG = """元太祖/太宗：补称谓切换说明（追尊帝自称口径）

按 2026-09-16 裁定的新口径——生前未称帝者（元太祖/太宗/定宗/宪宗）角色自称用
「我/吾」而非「朕」，因「朕」系明初史臣以汉制译写「汗」的结果。

本补丁在两包「角色扮演规则」的称谓纪律末尾各追加两行：
若用户明确要求以汉制帝王口吻作答，可改用「朕」，但首次作答须先说明这是
汉文正史对「汗」的译写称法与追尊庙号，非其生前实际自称。

改动后两包重跑质检仍各 6/6，「诚实边界」四字全文仍各只出现 1 次。
"""

ADD = [
    "skills/yuan/temujin-perspective/SKILL.md",
    "skills/yuan/ogodei-perspective/SKILL.md",
]


def run(args):
    p = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


lock = os.path.join(REPO, ".git", "index.lock")
if os.path.exists(lock):
    os.remove(lock)
    print("[clean] index.lock")

for a in ADD:
    rc, out, err = run(["git", "add", "--", a])
    print(f"[add {a}] rc={rc}", err or "")

rc, out, err = run(["git", "diff", "--cached", "--stat"])
print("\n[diff --cached --stat]")
print(out)

msg_path = os.path.join(tempfile.gettempdir(), "_es_msg4.txt")
open(msg_path, "w", encoding="utf-8").write(MSG)
rc, out, err = run(["git", "commit", "-F", msg_path])
print("\n[commit] rc=", rc)
print(out or "(no output)")
if err:
    print("STDERR:", err)

if rc == 0:
    rc, out, err = run(["git", "push", "origin", "main"])
    print("\n[push] rc=", rc)
    if err:
        print("STDERR:", err)

rc, out, err = run(["git", "log", "--oneline", "-1"])
print("[HEAD]", out)
