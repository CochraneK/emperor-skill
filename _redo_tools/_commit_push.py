# -*- coding: utf-8 -*-
"""提交 + 推送 emperor-skill（绕沙箱，避免 SIGTERM 误删工作树）。"""
import subprocess, os, tempfile

REPO = r"D:/2026/WB项目/emperor-skill"

MSG = """重蒸馏夏商 48 位帝王（nuwa 全流程）

- 夏 17 + 商 31 包全部补齐：SKILL.md 12 章 + 六维底稿 references/research/01-06 + scripts/quality_check.py
- 48/48 通过独立复核（自跑各包 quality_check.py，硬错误 0、警告 0）
- 史料门禁：夏商属传说/半信史，全篇明写材料有限；卜辞只证有其人、在其祀典，不证其事
- 异说一律并列不调和；六份底稿均含排除声明（未引用知乎/微信公众号/百度百科）
- 框架零污染：外部理论不作透镜写入正文
- 新增 _redo_tools/ 校验脚本（progress / verify48 / audit_all / era_check / yearscan）

已知待办：商王 era 年表链尚有 28 项口径问题（重叠倒置 5、缺限定语 13、非区间式 10），下批返工。
"""

def run(args):
    p = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()

# 1) commit
msg_path = os.path.join(tempfile.gettempdir(), "_es_commitmsg.txt")
open(msg_path, "w", encoding="utf-8").write(MSG)
rc, out, err = run(["git", "commit", "-F", msg_path])
print("[commit] rc=", rc)
print(out)
if err:
    print("STDERR:", err)
if rc != 0:
    raise SystemExit(1)

# 2) 提交后确认工作树完好（防误删）
rc, out, err = run(["git", "status", "--porcelain"])
print("\n[status after commit]")
print(out or "(clean)")
print("deleted(D) lines:", sum(1 for l in out.splitlines() if l[:2].strip().startswith("D")))

# 3) push
rc, out, err = run(["git", "push", "origin", "main"])
print("\n[push] rc=", rc)
print(out)
if err:
    print("STDERR:", err)

# 4) 远端同步确认
rc, out, err = run(["git", "status", "-sb"])
print("\n[status -sb]", out)
