# HANDOFF.md —— 当前阶段与接力入口

> 先读 `AGENTS.md`、`NUWA_AUDIT_V2.md` 与 `data/distillation-priority-policy.json`。本文件只记录**当前可执行状态**；历史数字不得覆盖生成数据。

## 1. 当前阶段（2026-09-18）

### P0 · Qin→Qing dynastic backbone 已关闭

`data/distillation-priority.json` 是机器验收源：

- P0 backbone CORE persons: **216**
- complete: **216**
- missing: **0**
- completion: **100%**
- mapping issues: **0**

最后一批五代主链已进入 `skills/wudai/`，Corpus Sync 与 Nuwa L3 Semantic Review 均成功。自动 L3 复用信号当前为 0 flagged packages / 0 high-similarity pairs / 0 repeated-long-paragraph groups；该自动检查只是 review signal，不替代人工 L3 verdict。

### 当前 corpus 快照

以 `data/corpus-registry.json` 为准：

- Skill packages: **304**
- candidate persons: **1312**
- stable person IDs active: **1312 / 1312**
- locked CORE persons: **913**
- CORE with Skill: **302**
- CORE missing: **611**
- CORE coverage: **33.08%**
- REVIEW: **365**
- EXTENDED: **15**
- LEGENDARY: **16**
- unresolved existing Skills: **0**
- suspicious canonical names: **0**
- identity collisions: **0**
- scope exception existing Skill: **1**（太丁，未立而卒；保留 package，但不进 ruler CORE denominator）

旧版本中“267 Skills / 648 missing CORE / 26 identity issues / ID 尚未 freeze”的状态已经失效，不得继续据此排工。

## 2. 现在做什么：P1 · Balanced Anchor Tranche

P1 只从 P0 以外、仍缺 Skill 的 post-Qin CORE 中建立一个**跨政权、可复现、非排名式**的首批研究 tranche。候选池当前 **207** 人。

Canonical inputs / outputs：

| 角色 | 路径 |
|---|---|
| 总调度政策 | `data/distillation-priority-policy.json` |
| P1 选择政策 | `data/p1-anchor-selection-policy.json` |
| source review 登记 | `data/p1-anchor-reviews.json` |
| P1 生成计划 | `data/p1-anchor-priority.json` |
| P1 可读报告 | `assessment/P1_ANCHOR_PRIORITY.md` |
| P1 generator | `_redo_tools/_build_p1_anchor_priority.py` |

### P1 原则

P1 **不对人物打总分、不排帝王优劣榜**。机器只建立 deterministic polity round-robin work queue。每个候选人的 source review 只记录：

- evidence state（RICH / MODERATE / LIMITED / UNKNOWN，描述证据，不评价人物）；
- source review 是否完成；
- documented transition contexts；
- comparison links；
- simulation / visualization contexts；
- evidence pointers / note。

初始 research/distillation tranche 目标 **24 人**，至少覆盖 **8 个 polity**。只有 source review 完成的人可以进入 tranche；sequence number 只是队列位置，不是人物排名。

## 3. P1 每个人仍走完整 Nuwa pipeline

`Sources → Research / References → Evidence synthesis → Mental-model distillation → SKILL.md → Audit`

不得：

- 从最终 Skill 倒推 References；
- 用最低字数/文件大小替代语义质量；
- 为凑 6 个模型发明心理、台词或动机；
- 把现代二手标签冒充史料原文；
- 因史料少就删除人物，正确做法是 `LIMITED-EVIDENCE` + 降低推断强度。

## 4. 后续阶段

P1 完成一个平衡 tranche 后：

- **P2**：系统补完剩余 post-Qin CORE（十国、十六国、辽/西辽、西夏、金、南明、平行政权与其他已锁定 CORE）。
- **P3**：再批量完成 early/pre-Qin CORE；史料稀薄时坚持证据约束。
- **Q**：REVIEW / EXTENDED / LEGENDARY 先解决 scope / identity / evidence 再决定是否蒸馏，禁止为了覆盖率直接塞进 CORE。

Simulation / duel / coop / one-life / assessment joint-space / visualization 都保留，但应在人物知识层持续扩展和质量稳定的基础上推进，而不是替代 corpus 建设。

## 5. Canonical 文件

| 角色 | 路径 |
|---|---|
| Nuwa 质量正典 | `NUWA_AUDIT_V2.md` |
| Worker 规则 | `WORKER_BRIEF_V2.md` |
| 最大 scope | `data/RULER_CORPUS_SCOPE.md` |
| stable ID registry | `data/ruler-person-id-registry.json` |
| 人物索引 | `data/rulers-person-index.json` |
| 覆盖缺口 | `data/corpus-gap.json` |
| identity QA | `data/corpus-identity-issues.json` |
| 总 work queue | `data/corpus-work-queue.json` |
| 总调度 | `data/distillation-priority.json` |
| Page registry | `data/corpus-registry.json` |
| L3 review signals | `data/l3-semantic-review-queue.json` |
| provenance recovery | `data/provenance-repair-registry.json` |

生成文件不要手改；修改上游 policy/master/review registry/builder 后让 `Corpus Sync` 重建。

## 6. 下一位 agent 的第一动作

不要再回头处理已经归零的“26 identity issues”，也不要重复统计 P0。

直接：

1. 打开 `assessment/P1_ANCHOR_PRIORITY.md`；
2. 按 deterministic review sequence 做 source/evidence review；
3. 把描述性审阅写入 `data/p1-anchor-reviews.json`；
4. 让 Corpus Sync 重建 P1 plan；
5. 24-person tranche 达到至少 8-polity diversity 后，开始 research → distill → audit。
