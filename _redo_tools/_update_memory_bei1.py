# -*- coding: utf-8 -*-
"""更新本仓 memory：MEMORY.md 覆盖口径 + 追加 2026-09-16 第十批北朝首批记录。"""
import os

MEM = r"D:/2026/WB项目/蒸馏skill/.workbuddy/memory/MEMORY.md"
LOG = r"D:/2026/WB项目/蒸馏skill/.workbuddy/memory/2026-09-16.md"

def rep(path, old, new, n=1):
    s = open(path, encoding="utf-8").read()
    c = s.count(old)
    assert c == n, f"[{os.path.basename(path)}] 期望命中 {n} 次，实际 {c}：{old[:40]}"
    s = s.replace(old, new)
    open(path, "w", encoding="utf-8").write(s)
    print(f"  ✓ {os.path.basename(path)}: {old[:30]}… -> 已替换")

# ---- MEMORY.md 覆盖口径更新 ----
rep(MEM,
    "站点上架 **310 人**（09-16：227→243→258→269→284→292→299→305→310；",
    "站点上架 **315 人**（09-16：227→243→258→269→284→292→299→305→310→315；")
rep(MEM,
    "  - ✅ 已有：夏17 商31 周37 秦3 楚汉2 ｜ 西汉15 东汉13 隋3 三国11 两晋15 唐21 宋18 元15 明16 清12 ｜ 南北朝·南朝宋8齐7梁6陈5（完成，共26）",
    "  - ✅ 已有：夏17 商31 周37 秦3 楚汉2 ｜ 西汉15 东汉13 隋3 三国11 两晋15 唐21 宋18 元15 明16 清12 ｜ 南北朝·南朝宋8齐7梁6陈5（完成，共26）+ 北朝首批北魏5（进行中，47476d2）")
rep(MEM,
    "  - ❌ **整朝缺失/进行中**：新莽(1)、十六国(~22)、北朝(北魏15东魏1西魏3北齐6北周5)、五代十国、辽(9)、西夏(10)、金(9) → 合计 **100–200 位**",
    "  - ❌ **整朝缺失/进行中**：新莽(1)、十六国(~22)、北朝(北魏5/15·余10 东魏1 西魏3 北齐6 北周5，共25待补)、五代十国、辽(9)、西夏(10)、金(9) → 合计 **100–200 位**")
rep(MEM,
    "⑥ 🔄南北朝（南朝宋8齐7梁6陈5 已落盘登记 emperor-skill 1c011f9/8478772/75c56ba/e6b481c / 主仓本批，南朝共26帝全补齐；北朝30 待补）",
    "⑥ 🔄南北朝（南朝宋8齐7梁6陈5 已落盘登记 emperor-skill 1c011f9/8478772/75c56ba/e6b481c / 主仓本批，南朝共26帝全补齐；北朝首批北魏5 已落盘 emperor-skill 47476d2 / 主仓 63b7497，余北魏10+东魏1+西魏3+北齐6+北周5=25 待补）")
rep(MEM,
    "主仓 `workbench.py build` → **310 人 / 186 边 / 21 模块页**（09-16 南陈登记后：305→310）；`xia-emperors.html` 17 人、`shang-emperors.html` 31 人、`sanguo-emperors.html` 11 人、`jin-emperors.html` 15 人、`nanbeichao-emperors.html` 26 人（此前均 0）已回填。",
    "主仓 `workbench.py build` → **315 人 / 186 边 / 21 模块页**（09-16 北朝首批登记后：305→310→315）；`xia-emperors.html` 17 人、`shang-emperors.html` 31 人、`sanguo-emperors.html` 11 人、`jin-emperors.html` 15 人、`nanbeichao-emperors.html` 31 人（此前均 0）已回填。")
rep(MEM,
    "- ❌ 整朝缺/进行中：新莽1、十六国~22、北朝30、五代十国、辽9、西夏10、金9（合计约 100–200 位）",
    "- ❌ 整朝缺/进行中：新莽1、十六国~22、北朝(北魏10东魏1西魏3北齐6北周5=25)、五代十国、辽9、西夏10、金9（合计约 100–200 位）")
rep(MEM,
    "- **下一优先：北朝30（北魏15东魏1西魏3北齐6北周5），统一共享 nanbeichao module/group，间断性回收。**",
    "- **下一优先：北朝余25（北魏10+东魏1+西魏3+北齐6+北周5），统一共享 nanbeichao module/group，间断性回收。**")

# ---- 2026-09-16.md 追加第十批 ----
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
log = open(LOG, encoding="utf-8").read()
if "第十批" not in log:
    open(LOG, "a", encoding="utf-8").write(appendix)
    print("  ✓ 2026-09-16.md: 追加第十批北朝首批记录")
else:
    print("  (2026-09-16.md 已有第十批记录，跳过)")
print("\n=== memory 更新完成 ===")
