# -*- coding: utf-8 -*-
"""记忆更新：① 项目 MEMORY.md 新增硬规则⑧（先六维后 SKILL.md）+ 人数口径
             ② 今日日志 2026-09-16.md 追加本批记录
替换带 assert，任一锚点不唯一即报错不写入。"""
import pathlib

MS = pathlib.Path(r"D:/2026/WB项目/蒸馏skill")
MEM = MS / ".workbuddy/memory/MEMORY.md"
LOG = MS / ".workbuddy/memory/2026-09-16.md"

def rep(text, old, new, n=1):
    c = text.count(old)
    assert c == n, f"锚点命中 {c} 次（期望 {n}）: {old[:40]}..."
    return text.replace(old, new)

# ---------- 1. MEMORY.md ----------
t = MEM.read_text(encoding="utf-8")

# 1a. 新增硬规则 ⑧（插在 ⑦ 段尾之后）
anchor = "⚠️ 不要试图把正文的「朕」全替换掉——实测四包里「朕」出现 14–170 次，替换成本高且伤文气；加纪律说明即可。"
new_rule = anchor + """

⑧ **六维是源、SKILL.md 是产物（2026-09-16 用户明确纠正，最高优先级）**：nuwa 正序必须是
`01-writings → 02-conversations → 03-expression-dna → 04-external-views → 05-decisions → 06-timeline`
六份底稿先成，**再由六维蒸馏出 SKILL.md**；**严禁「先写 SKILL.md 再回填六维」**——倒果为因，
证据链不可追溯，等于把结论当史料。判据：SKILL.md 每条证据须能在对应底稿追到出处，
正文须带「据 0X 稿」溯源标记（yuanye 包实测 30 处）。已存在的倒序残件（如 `_pending/bei3/`）
**不得直接补底稿交付**，须以六维为唯一依据重写 SKILL.md（旧版降为对照稿，不参与交付）。"""
t = rep(t, anchor, new_rule)

# 1b. 人数口径 324 -> 325
t = rep(t, "**324 人**", "**325 人**")
t = rep(t, "→320→324", "→320→324→325", n=2)
# 1c. nanbeichao 人数
t = rep(t, "`nanbeichao-emperors.html` 36 人", "`nanbeichao-emperors.html` 37 人")
MEM.write_text(t, encoding="utf-8")
print("MEMORY.md updated")

# ---------- 2. 今日日志 ----------
lg = LOG.read_text(encoding="utf-8")
add = """

## 第十二批·北朝第三批之首：元晔（长广王·建明帝，530 冬立 / 531 春废 / 532 见杀）

- **流程纪律纠正（用户指出）**：nuwa 必须「先六维、后 SKILL.md」；此前「先出 SKILL.md 再补六维」属倒果为因，
  已立为 MEMORY.md 硬规则 ⑧。本包按正序重做：六维各 5.6–6.9KB、均带排除声明 → **以六维为唯一依据重写 SKILL.md**
  （25,490B），旧版降为对照稿留在 `_pending/bei3/`（gitignore，不入库）。
- **独立复核**（`_verify_yuanye.py`，不采信自报）：8 文件齐全；六维 ≥2.5KB + 排除声明 6/6；
  quality_check **6/6**（心智模型 6、表达DNA 14 项、诚实边界 9 条、内在张力 4 处、一手 8/13=62%）；
  「诚实边界」四字全文仅 1 次；module/group = nanbeichao-emperors / nanbeichao-main → **ALL_OK**。
- **同步**：emperor-skill `fa4d458` 已 push（6e6dfa1..fa4d458）；主仓 people **324→325**
  （登记脚本按时间序插入 yuanziyou 之后），build 输出 **325 人 / 186 边 / nanbeichao 37 人 / 21 模块页**。
- 本包不援引墓志为立论根基（今所见著录未可确指），《洛阳伽蓝记》仅作时局旁证——已写入诚实边界。
- **待补（北朝余 19）**：元恭（节闵）、元朗（后废帝）、元脩（孝武）+ 东魏 1、西魏 3、北齐 6、北周 5。
  `_pending/bei3/` 内另 4 份残件（yuanguan/yuanlang/yuanxiu/yuanzhao）一律按正序重做，不得补底稿交付。
"""
LOG.write_text(lg.rstrip() + "\n" + add, encoding="utf-8")
print("2026-09-16.md appended")
