# HANDOFF.md —— 换台电脑 / 换个人怎么接上

> 先读 `AGENTS.md` 与 `NUWA_AUDIT_V2.md`。本文件只记录**当前可执行状态与停点**，不要把历史数字当永久规范。

## 1. 环境与重建入口

- Python 3.13 优先；当前 corpus build / QA 只依赖标准库。
- 无 `.env` 依赖；脚本从仓库文件和命令行参数读取输入。
- GitHub Actions `Corpus Sync` 会在 master corpus / builder 相关文件变更后自动重建 coverage、identity QA 与 work queue。

本地检查：

```bash
python _redo_tools/_build_ruler_corpus.py
python _redo_tools/_build_corpus_queue.py
```

Simulation 的历史 solo 子集另有自己的重建链，见 `simulation/README.md`。

## 2. 2026-09-17 当前 corpus 快照

### 已有 Perspective Skills

- **267** 个 Skill package。
- **16** 个朝代 corpus 目录；`skills/_audit` 是非朝代目录，因此 `skills/` 顶层目录总数为 17。
- 266 个现有 Skill 已匹配统治者人物。
- 1 个现有 Skill（太丁）是明确 scope exception：保留 evidence/history package，但因“未立而卒”不进入 ruler CORE 分母。
- 现有 Skill unresolved = **0**；Skill → 多人物冲突 = **0**；人物 → 多 Skill 冲突 = **0**。

### 最大统治者候选主名单

机器索引 `data/rulers-person-index.json` 当前包含：

| 状态 | 数量 |
|---|---:|
| Candidate persons | 1312 |
| Locked-candidate CORE | 913 |
| CORE 已有 Skill | 265 |
| CORE 缺失 | 648 |
| REVIEW | 365 |
| EXTENDED | 15 |
| LEGENDARY | 16 |

CORE coverage 当前约 **29.03%**。REVIEW / EXTENDED / LEGENDARY 不得静默进入 CORE 分母。

### 当前缺口队列

`data/corpus-work-queue.json` 当前拆成：

- `A_CORE_MAJOR_SEQUENCE_MISSING`: **70**
- `B_CORE_PARALLEL_POLITY_MISSING`: **174**
- `D_CORE_EARLY_OR_PREQIN_MISSING`: **404**
- `Q1_SCOPE_OR_IDENTITY_REVIEW`: **365**

A + B + D = 648，正好等于当前缺失 CORE。

## 3. 现在真正卡在哪

### P0 — identity / canonical-name QA，然后冻结 ID

`candidate_id` 仍是临时编号，当前由候选规范名排序生成。**在 ID freeze 前修改 canonical name 会引发后续 ID 漂移。**

`data/corpus-identity-issues.json` 当前有 **26 个 suspicious canonical-name strings**。这里既有：

- 多个名称/别名被塞进一个 `canonical_name`；
- “称号 + 人名”拼接；
- 可能不是单一人物的 placeholder；
- REVIEW 身份仍需史料确认。

执行顺序：

1. 对 26 个 identity/name issue 做人工/来源核验；
2. 把 canonical name 与 aliases 分开表达，不丢原始写法和 provenance；
3. 重新跑 corpus builder + queue；
4. 确认无新的跨人物碰撞；
5. 冻结 stable person ID；
6. 冻结后才允许大规模生成下游外键、Skill、simulation matrix。

**不要为了尽快补 648 人而跳过这一步。**

### P1 — 补 locked CORE，而不是无差别补候选

ID freeze 后，优先顺序是：

1. `A_CORE_MAJOR_SEQUENCE_MISSING` 70；
2. `B_CORE_PARALLEL_POLITY_MISSING` 174；
3. `D_CORE_EARLY_OR_PREQIN_MISSING` 404。

每个人都必须走：

`Sources → Research / References → Evidence synthesis → Nuwa distillation → Audit`

不得从旧 Skill 倒推 References。证据稀薄者降低推断强度，不靠 filler 补六个模型。

### P1 — REVIEW 队列不批量蒸馏

365 个 Q1 先解决“这个人是否在 scope、是不是同一人物、是否确有 qualifying sovereign episode”。未解决前不进入 CORE denominator，也不批量建 Skill。

### P2 — provenance recovery 继续，但不要把历史快照当全库 PASS

历史 39 个 mtime provenance signal 已经全部分类，remaining snapshot review = 0；这只是 forensic triage，不代表 267 个包 L1–L3 全部合格。全库 Nuwa semantic audit 仍是 in-progress。

## 4. Simulation 当前状态怎么理解

旧 `HANDOFF` 曾写“94 个包、78 个处境”。那是 **solo simulation 历史子集**，不是当前 corpus 总量。

当前已有 solo 报告、ranking 与 reversal validity；旧引擎的 78 situations / 94 mapped packages 仍可作为 simulation regression fixture，但在 1,312 人主名单完成 identity freeze 前，不应把“扩到 94×93”当项目 P0。

后续 simulation 方向仍保留：

- 评分卡去结局化 / 机会利用度；
- duel；
- coop；
- one-life；
- assessment 与帝王模型共同空间。

但这些属于 Skill/corpus 基础层稳定后的下游实验。

## 5. Canonical 数据与生成物

| 角色 | 路径 |
|---|---|
| 质量正典 | `NUWA_AUDIT_V2.md` |
| Worker 规则 | `WORKER_BRIEF_V2.md` |
| 最大候选 scope | `data/RULER_CORPUS_SCOPE.md` |
| 候选人物索引 | `data/rulers-person-index.json` |
| 覆盖缺口 | `data/corpus-gap.json` |
| identity issues | `data/corpus-identity-issues.json` |
| work queue | `data/corpus-work-queue.json` |
| Page / overview registry | `data/corpus-registry.json` |
| Coverage 报告 | `assessment/CORPUS_COVERAGE.md` |
| QA 报告 | `assessment/CORPUS_QA.md` |
| provenance recovery | `assessment/PROVENANCE_RECOVERY.md` |
| corpus builder | `_redo_tools/_build_ruler_corpus.py` |
| queue builder | `_redo_tools/_build_corpus_queue.py` |

生成文件不要手改；改上游 master / builder 后重建。

## 6. 已知坑

- `candidate_id` 未冻结前不要作为永久外键发布。
- 不要把 `/` 连接的多个名字直接当一个规范姓名；canonical 与 aliases 要分层。
- 不要把“文件够大 / checker 全绿 / mtime 合理”当 Nuwa 质量证明。
- 不要在同一轮对同一文件做并行写入；GitHub contents API 会产生 SHA 冲突或覆盖。
- Simulation 生成 HTML 不是 canonical data source。
- 史料稀薄人物允许 `LIMITED-EVIDENCE`；不要为完整感发明心理、台词或确定性动机。
- 任何 corpus 自动化都只能机械维护 scope / identity / coverage；历史身份与来源质量仍需人工/agent evidence review。

## 7. 下一位 agent 的第一动作

直接打开：

1. `data/corpus-identity-issues.json`
2. `data/RULER_CORPUS_SCOPE.md`
3. `data/ruler-corpus-sources.md`
4. `_redo_tools/_build_ruler_corpus.py`

从 **26 个 canonical-name / identity issue** 开始收口；不要退回去重复统计 267 个 Skill，也不要先扩 solo matrix。
