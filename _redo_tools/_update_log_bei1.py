# -*- coding: utf-8 -*-
"""修正 2026-09-16.md 末尾两条陈旧「北朝30」结论，并追加第十批北朝首批记录。"""
import os

LOG = r"D:/2026/WB项目/蒸馏skill/.workbuddy/memory/2026-09-16.md"

# 修正末尾两条陈旧结论（原先写「北朝30」，现北朝首批已落 5）
s = open(LOG, encoding="utf-8").read()
s = s.replace(
    "- ❌ 整朝缺/进行中：新莽1、十六国~22、北朝30、五代十国、辽9、西夏10、金9（合计约 100–200 位）",
    "- ❌ 整朝缺/进行中：新莽1、十六国~22、北朝(北魏10东魏1西魏3北齐6北周5=25)、五代十国、辽9、西夏10、金9（合计约 100–200 位）")
s = s.replace(
    "- **下一优先：北朝30（北魏15东魏1西魏3北齐6北周5），统一共享 nanbeichao module/group，间断性回收。**",
    "- **下一优先：北朝余25（北魏10+东魏1+西魏3+北齐6+北周5），统一共享 nanbeichao module/group，间断性回收。**")
open(LOG, "w", encoding="utf-8").write(s)
print("  ✓ 修正末尾两条陈旧北朝结论")

# 追加第十批
appendix = """

---

## 第十批 · 已回收 ✅（南北朝·北朝第一批·北魏 5 帝）

按「间断性回收」继续推进北朝30——先做北魏前 5 帝（共享 `dir=nanbeichao`、`module=nanbeichao-emperors`、`group=nanbeichao-main`）。5 worker 并行蒸馏，派单写全：北朝一手史料《魏书》《北齐书》《周书》《北史》《资治通鉴》《洛阳伽蓝记》+ 石窟题记/墓志；北魏诸帝孝文前姓拓跋；角色扮演用「朕」并在诚实边界写明其为汉文正史对鲜卑君主译写称法、可改「我/吾」；`references/research/` 硬约束；包内恰好 8 文件；复制 quality_check.py 自跑至 6/6；不得 git/rm。

### 北魏首批5（本会话收尾）
- 5 包：tuobagui(道武帝 386–409)/tuobasi(明元帝 409–423)/tuobatao(太武帝 423–452)/tuobayu(南安王 452)/tuobajun(文成帝 452–465)。各 worker 报 6/6。
- **独立复核（零复用 worker 自报）**：`_verify_bei1.py` 自跑 quality_check.py + 核对 8 文件/排除声明/诚实边界=1/module-group，5 包 ALL_OK=True。
- 提交 **`47476d2`**（41 files）+ 推送 `e6b481c..47476d2`。**北魏首批 5 帝全部 6/6 补齐并推送 emperor-skill。**

### 站点登记（主仓，本地无远端只 commit）
- `_register_bei1.py`：nanbeichao module/group 已存在，本批只追加 5 个新 people 键；people **310 → 315**（+5：拓跋珪/拓跋嗣/拓跋焘/拓跋余/拓跋濬，cn 名均正确）。
- `workbench.py build` 更新 `docs/nanbeichao-emperors.html`（**31 人 / 0 边**，26 南朝 + 5 北魏）。站点现 **315 人 / 186 边 / 21 模块页**。
- 主仓提交 **`63b7497`**（22 files：modules.json + docs 全量重建 + 记忆文件）。

### 当前覆盖结论
- ✅ 齐全：夏17 商31 周37 秦3 楚汉2 西汉15 东汉13 隋3 三国11 两晋15 唐21 宋18 元15 明16 清12 ｜ 南北朝·南朝26（完成）+ 北朝北魏5（进行中，5/15）
- ❌ 整朝缺/进行中：新莽1、十六国~22、北朝余25（北魏10东魏1西魏3北齐6北周5）、五代十国、辽9、西夏10、金9（合计约 100–200 位）
- **下一优先：北朝余25，统一共享 nanbeichao module/group，间断性回收。**
"""
if "第十批" not in s:
    open(LOG, "a", encoding="utf-8").write(appendix)
    print("  ✓ 追加第十批北朝首批记录")
else:
    print("  (第十批记录已存在，跳过)")
print("\n=== log 更新完成 ===")
