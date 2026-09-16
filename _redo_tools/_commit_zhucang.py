# -*- coding: utf-8 -*-
"""主仓（蒸馏skill，纯本地无远端）提交：登记东汉13+隋3 + 重建站点。"""
import subprocess, os, tempfile

REPO = r"D:/2026/WB项目/蒸馏skill"

MSG = """登记东汉13+隋3 进站点，重建站点（227 → 243 人）

- data/modules.json：新增 donghan-emperors / sui-emperors 两个模块定义、
  donghan-main / sui-main 两个 group、16 条 people 条目
- 这 16 个包此前已按 nuwa 流程完成且 184/184 合规，但从未同步进 modules.json，
  所以站点一直没有东汉、隋两个模块页。本次为纯登记搬运，包内容未改动。
- workbench.py build 重建：243 人 / 186 边；
  新增 docs/donghan-emperors.html (13 人)、docs/sui-emperors.html (3 人)
- 同时补记 2026-09-15 / 09-16 工作日志与长期记忆订正
  （people 实为 227 条 dict，旧记的 137 条已过时）
"""


def run(args):
    p = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


for path in [".workbuddy/data/modules.json", ".workbuddy/memory", "docs"]:
    rc, out, err = run(["git", "add", "--", path])
    print(f"[add {path}] rc={rc}", err or "")

rc, out, err = run(["git", "status", "--porcelain"])
print("\n[暂存后 status]")
print(out)

msg_path = os.path.join(tempfile.gettempdir(), "_zk_commitmsg.txt")
open(msg_path, "w", encoding="utf-8").write(MSG)
rc, out, err = run(["git", "commit", "-F", msg_path])
print("\n[commit] rc=", rc)
print(out)
if err:
    print("STDERR:", err)

rc, out, err = run(["git", "log", "--oneline", "-1"])
print("\n[HEAD]", out)
rc, out, err = run(["git", "status", "--porcelain"])
print("[剩余未提交]")
print(out or "(无)")
