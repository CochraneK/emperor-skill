# -*- coding: utf-8 -*-
"""修正 2026-09-16.md 末尾两条北朝结论（=25 → =20），并追加第十一批北朝第二批记录。"""
import os

LOG = r"D:/2026/WB项目/蒸馏skill/.workbuddy/memory/2026-09-16.md"
s = open(LOG, encoding="utf-8").read()
s = s.replace(
    "- ❌ 整朝缺/进行中：新莽1、十六国~22、北朝(北魏10东魏1西魏3北齐6北周5=25)、五代十国、辽9、西夏10、金9（合计约 100–200 位）",
    "- ❌ 整朝缺/进行中：新莽1、十六国~22、北朝(北魏5东魏1西魏3北齐6北周5=20)、五代十国、辽9、西夏10、金9（合计约 100–200 位）")
s = s.replace(
    "- **下一优先：北朝余25（北魏10+东魏1+西魏3+北齐6+北周5），统一共享 nanbeichao module/group，间断性回收。**",
    "- **下一优先：北朝余20（北魏5+东魏1+西魏3+北齐6+北周5），统一共享 nanbeichao module/group，间断性回收。**")
open(LOG, "w", encoding="utf-8").write(s)
print("  ✓ 修正末尾两条北朝结论（=25 → =20）")

appendix = """

---

## 第十一批 · 已回收 ✅（南北朝·北朝第二批·北魏 5 帝）

按「间断性回收」继续推进北朝30——北魏 #6–10（共享 `dir=nanbeichao`、`module=nanbeichao-emperors`、`group=nanbeichao-main`）。5 worker 并行蒸馏，派单同第十批口径（北朝一手史料、拓跋/元姓切换、朕译写称法、references/research/ 硬约束、包内恰 8 文件、复制 quality_check.py 自跑 6/6、不得 git/rm）。

### 北魏第二批5（本会话收尾）
- 5 包：tuobahong(献文帝 465–471)/yuanhong(孝文帝 471–499)/yuanke(宣武帝 499–515)/yuanxu(孝明帝 515–528)/yuanziyou(孝庄帝 528–530)。各 worker 报 6/6。
- **独立复核（零复用 worker 自报）**：`_verify_bei2.py` 自跑 quality_check.py + 核对 8 文件/排除声明/诚实边界=1/module-group，5 包 ALL_OK=True。
- 提交 **`8e5204f`**（41 files）+ 推送 `6cb70b8..8e5204f`。**北魏第二批 5 帝全部 6/6 补齐并推送 emperor-skill（北魏累计 10/15）。**

### 站点登记（主仓，本地无远端只 commit）
- `_register_bei2.py`：nanbeichao module/group 已存在，本批只追加 5 个新 people 键；people **315 → 320**（+5：拓跋弘/元宏/元恪/元诩/元子攸，cn 名均正确）。
- `workbench.py build` 更新 `docs/nanbeichao-emperors.html`（**36 人 / 0 边**，26 南朝 + 10 北魏）。站点现 **320 人 / 186 边 / 21 模块页**。
- 主仓提交 **`e424dcc`**（22 files：modules.json + docs 全量重建 + 记忆文件）。

### 当前覆盖结论
- ✅ 齐全：夏17 商31 周37 秦3 楚汉2 西汉15 东汉13 隋3 三国11 两晋15 唐21 宋18 元15 明16 清12 ｜ 南北朝·南朝26（完成）+ 北朝北魏10（进行中，10/15）
- ❌ 整朝缺/进行中：新莽1、十六国~22、北朝余20（北魏5东魏1西魏3北齐6北周5）、五代十国、辽9、西夏10、金9（合计约 100–200 位）
- **下一优先：北朝余20（北魏末5 + 东魏1 + 西魏3 + 北齐6 + 北周5），统一共享 nanbeichao module/group，间断性回收。**
"""
if "第十一批" not in s:
    open(LOG, "a", encoding="utf-8").write(appendix)
    print("  ✓ 追加第十一批北朝第二批记录")
else:
    print("  (第十一批记录已存在，跳过)")
print("\n=== log 更新完成 ===")
