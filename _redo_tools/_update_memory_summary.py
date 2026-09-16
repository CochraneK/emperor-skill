# -*- coding: utf-8 -*-
"""汇总收尾：更新 MEMORY.md 口径（320→324、元前四汗登记、北朝第三批暂存），并追加日志。"""
import os

MEM = r"D:/2026/WB项目/蒸馏skill/.workbuddy/memory/MEMORY.md"
LOG = r"D:/2026/WB项目/蒸馏skill/.workbuddy/memory/2026-09-16.md"

def rep(path, old, new, n=1):
    s = open(path, encoding="utf-8").read()
    c = s.count(old)
    assert c == n, f"[{os.path.basename(path)}] 期望 {n} 实际 {c}：{old[:32]}"
    open(path, "w", encoding="utf-8").write(s.replace(old, new))
    print(f"  ✓ {os.path.basename(path)}: {old[:26]}…")

rep(MEM,
    "站点上架 **320 人**（09-16：227→243→258→269→284→292→299→305→310→315→320；",
    "站点上架 **324 人**（09-16：227→243→258→269→284→292→299→305→310→315→320→324；")
rep(MEM,
    "主仓 `workbench.py build` → **320 人 / 186 边 / 21 模块页**（09-16 北朝两批登记后：305→310→315→320）；`xia-emperors.html` 17 人、`shang-emperors.html` 31 人、`sanguo-emperors.html` 11 人、`jin-emperors.html` 15 人、`nanbeichao-emperors.html` 36 人（此前均 0）已回填。",
    "主仓 `workbench.py build` → **324 人 / 186 边 / 21 模块页**（09-16 北朝两批 + 元前四汗补登记后：305→310→315→320→324）；`xia-emperors.html` 17 人、`shang-emperors.html` 31 人、`sanguo-emperors.html` 11 人、`jin-emperors.html` 15 人、`yuan-emperors.html` 15 人、`nanbeichao-emperors.html` 36 人（此前均 0）已回填。\n- **2026-09-16 收尾发现并修复**：元前四汗（temujin/ogodei/guyuk/mongke）早已 push emperor-skill 但**从未登记进主仓**，致站点 `yuan-emperors` 仅 11 人（应 15）。`_register_yuan4.py` 补登记后 people 320→324、yuan-emperors.html 15 人。**这是全仓最后一个「有包未登记」缺口**（逐朝核对：仅元差 4，余全对齐）。")
rep(MEM,
    "余北魏5+东魏1+西魏3+北齐6+北周5=20 待补）",
    "余北魏5+东魏1+西魏3+北齐6+北周5=20 待补；⚠️ 北朝第三批（北魏末5：yuanye/yuanguan/yuanlang/yuanxiu/yuanzhao）因 **429 额度限流**中断，残缺包已搬出 skills/ 暂存 `_pending/bei3/`（gitignore），待额度恢复（2026-09-17 17:45）重派补全）")

# 追加日志
appendix = """

---

## 汇总收尾（用户要求「说说蒸馏了多少、剩下多少，也把成果同步 git」）

### 一、emperor-skill 现状：**265 包，100% 合规**
| 朝代 | 包数 | 朝代 | 包数 |
|---|---|---|---|
| 夏 17 | 商 31 | 西周/东周 37 | 秦 3 |
| 楚汉 2 | 西汉 15 | 东汉 13 | 三国 11 |
| 两晋 15 | 南北朝 36（南朝26+北魏10） | 隋 3 | 唐 21 |
| 宋 18 | 元 15 | 明 16 | 清 12 |

`_summary_all.py` 实测：**265/265 合规**（每包恰 8 文件：SKILL.md + references/research/01–06 + scripts/quality_check.py）。

### 二、站点（主仓）：**324 人**（含虚构 59）
- 本会话新增：北朝首批北魏5（47476d2 / 主仓 63b7497）+ 北朝第二批北魏5（8e5204f / 主仓 e424dcc）。
- **补登记元前四汗**（temujin/ogodei/guyuk/mongke）：这是全仓最后一个「有包未登记」缺口，补后 people 320→324、`yuan-emperors.html` 15 人（主仓提交 `4f623f1`）。
- `nanbeichao-emperors.html` = **36 人 / 0 边**。

### 三、北朝第三批（北魏末5）· 被限流中断 ⏸️
- 派单 5 个 worker **全部撞 429**（「使用量已超出频率限制，2026-09-17 17:45:17 UTC+8 重置」）。
- 实测磁盘：worker 在被打断前各写了**部分文件**，形成 5 个**残缺包**（yuanye/yuanzhao 有完整 6/6 SKILL.md 缺六维底稿；yuanguan 有六维底稿缺 SKILL.md；yuanlang/yuanxiu 更少）。
- 处理：**不删除**，用 `_stage_bei3_partial.py` 把 5 个残缺包搬出 `skills/` 到 `_pending/bei3/`（并 gitignore），避免 `_audit_all.py` 把它们误计为「不合规包」而污染 265/265 口径。skills/nanbeichao 回到 36 个干净包。
- **待办**：额度恢复后重派补全这 5 包（可参考 _pending/bei3/ 里已写好的部分）。

### 四、剩余缺口（按主干王朝口径）
- 南北朝·北朝余 **20**：北魏末5（暂存待补）+ 东魏1 + 西魏3 + 北齐6 + 北周5
- 整朝缺：新莽 **1**（王莽）、十六国 **~22**、辽 **9**、西夏 **10**、金 **9**、五代十国（~十几）
- 合计约 **70–90 位**。

### 五、git 同步
- emperor-skill：批次提交 47476d2 → 8e5204f → dc4d404 → **357847f**（含 redo_tools 工具脚本 + .gitignore 新增 `_pending/`），**已 push（远端 main 同步）**。
- 主仓：63b7497 → e424dcc → 8053568 → bb5d6d5 → **4f623f1**，**纯本地无远端，只 commit**。
"""
log = open(LOG, encoding="utf-8").read()
if "汇总收尾" not in log:
    open(LOG, "a", encoding="utf-8").write(appendix)
    print("  ✓ 追加汇总收尾日志")
else:
    print("  (汇总收尾已存在)")
print("\n=== done ===")
