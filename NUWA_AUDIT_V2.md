# Nuwa Audit v2 — 帝王 Skill 蒸馏验收与修复标准

> 本文件定义 `emperor-skill` 的统一**出口验收标准**。它用于评估不同模型、不同批次、不同 worker 生成的帝王 Skill，并决定保留、清理、局部修补、重蒸馏或重研究。
>
> 核心原则：**统一质量标准，不强求统一生成模型。**

## 0. Canonical pipeline

唯一认可的知识血缘：

`Sources → Research / References → Evidence synthesis → Mental-model distillation → SKILL.md → Audit`

### 禁止的伪修复

- `SKILL.md → 倒推/扩写 References` **不能**建立 Nuwa provenance。
- 仅仅把缺失目录补齐，不等于重新蒸馏。
- 不得以最低字数、最低 KB、最低文件大小作为质量标准。
- 不得为了通过条数、关键词或长度检查而添加 filler、套话、重复内容。

如果后来已经形成了**独立、真实、质量合格**的 References，即使它晚于旧 Skill，也允许直接：

`Existing qualified References → REDISTILL → New SKILL.md`

无需为了形式重新做一次 research。

---

## 1. 四层 Audit

### L1 — Provenance Gate（硬门禁）

目标：确认 Skill 的知识血缘真实成立，而不只是文件看起来齐全。

检查：

1. 是否存在可识别的 research / references 上游材料；史料极少人物可采用明确记录的 evidence-limited 路径。
2. References 是否独立于最终 Skill，而非根据 Skill 倒推、扩写或伪造。
3. Skill 的关键 mental models、关键事实和人物判断能否回溯到上游材料。
4. 若时间戳可用，仅将其作为 provenance 异常信号，不作为唯一判据。
5. 若 References 晚于 Skill：判断其是否为独立研究。独立研究可用于重蒸馏；倒推生成则 provenance FAIL。

判定：`PASS / UNCERTAIN / FAIL`

- `PASS`：血缘可信。
- `UNCERTAIN`：缺少足够元数据，需进一步核查，禁止直接删除。
- `FAIL`：明确倒推、无研究依据、伪造上游或无法建立证据链。

### L2 — Evidence Gate（硬门禁）

目标：判断材料本身是否足以支撑蒸馏。

检查：

1. 来源是否真实、可核验。
2. 一手、后世史书、现代研究、考古材料、史评与模型推断是否正确区分。
3. 关键引文与关键事实是否有对应来源，而非仅列 bibliography。
4. 是否存在来源与结论不匹配、引用幻觉、二手冒充一手等问题。
5. 是否主动保留不确定性与相互冲突的材料。
6. 传说/半信史人物不得因史料少而被机械判低质量；应评价其是否在现有证据条件下诚实降低结论强度。
7. 来源数量不是独立质量目标；禁止为达到数量而加入低价值材料。

判定：`PASS / PARTIAL / FAIL / LIMITED-EVIDENCE`

`LIMITED-EVIDENCE` 不是失败，而是对可推断强度的约束。

### L3 — Semantic Distillation Quality（核心语义验收）

目标：判断是否真正把材料蒸馏成了一个有辨识度、可迁移、可证伪的人物心智系统。

逐项诊断：

- **Faithfulness**：模型是否忠于证据，没有把后世印象当本人稳定机制。
- **Specificity**：是否具有该人物的特异性，而非通用成功学标签。
- **Abstraction**：是否从事件上升到可解释行为的机制，而非复述生平。
- **Transferability**：模型能否迁移到史料未直接覆盖的新问题，而仍保持人物逻辑。
- **Evidence linkage**：每个关键模型是否有足够证据支持。
- **Limitations**：是否说明模型失效条件、代价和边界。
- **Internal tensions**：是否保留人物真实矛盾，而非把人物磨平成一致人格。
- **Counter-evidence**：是否能处理人物违反自己主要模式的反例。
- **Model independence**：不同 mental models 是否真正不同，而非同义改写。
- **Decision heuristics**：是否能从模型推导出可执行决策逻辑，而非泛泛建议。
- **Expression DNA**：是否有来源/人物风格支撑，而非古风套话。
- **Honesty**：史实、史评、框架推断与未知是否清楚分界。
- **Information density**：是否存在明显 filler、重复背景、换句话凑字数。

#### Genericity Test（必做）

暂时遮掉人物姓名、朝代、专名后检查 mental models：

> 如果大量模型可以无修改地套给许多其他帝王，则判定人物特异性不足。

例如仅有“知人善任 / 审时度势 / 重视民生 / 善于决策”不能单独构成高质量 mental model，必须进一步抽象出该人物独特的触发条件、机制、权衡和失败模式。

#### Counter-evidence Test（必做）

主动寻找与每个核心模型相冲突的行为或事件，并判断：

- 是模型需要限定条件；
- 是人物存在稳定内在张力；
- 还是该模型本身并不成立。

不得只收集支持材料。

判定建议：每项使用 `STRONG / ADEQUATE / WEAK / FAIL`，用于诊断，不计算一个诱导凑分的总分。

### L4 — Emperor Engineering Compliance（工程层）

现有 G1–G11 原则上归入这一层，包括：

- frontmatter / schema；
- 文件路径与 UTF-8；
- emperor-skill 的角色扮演约定；
- trigger / 退出角色；
- 时间线与展示结构；
- 项目自己的来源政策与黑名单；
- 为统一 corpus 选择固定 6 个模型等。

这些规则可以保证兼容性和一致性，但**不得被表述为 Nuwa epistemic quality 本身**。

Nuwa 通用允许 3–7 个 mental models；本项目统一 6 个属于 Emperor Profile，不得以此反推“不是 6 个就不是 Nuwa”。

---

## 2. Anti-Goodhart 规则

任何 worker、agent、WorkBuddy 或脚本不得自行把以下 proxy 升格为 canonical quality gate：

- 最低字数；
- 最低字符数；
- 最低 KB / 文件大小；
- 为过门禁而要求重复关键词；
- 不基于内容需要的固定段落膨胀；
- 来源数量越多越好；
- SKILL 越长越好。

如果工程工具确实需要额外约束，必须明确标为：

`PROJECT/TOOLING RULE — NOT NUWA QUALITY`

且不得导致语义 filler。

**删除 filler 不构成质量退化。** 只要删除后 provenance、evidence、mental models、limitations、tensions、honesty 等核心内容仍成立，应视为质量改善。

---

## 3. Repair decision matrix

Audit 不只报告 PASS/FAIL，而必须给出下一步动作：

| Action | 条件 | 默认修复 |
|---|---|---|
| `KEEP` | L1/L2 可信，L3 达标，L4 兼容 | 不改 |
| `CLEAN` | 内容核心良好，仅有 filler、重复、格式污染 | 删除冗余并复核 |
| `PATCH` | 少数 evidence/model/tension/limitation 有局部缺口 | 只补缺口，不全量重跑 |
| `REDISTILL` | References 合格，但 Skill 抽象/特异性/结构明显不足，或 References 晚于旧 Skill但属于独立研究 | 直接用现有 References 重新生成 Skill |
| `RESEARCH-GAP` | 研究总体可信，但少数关键问题缺证据 | 只补定向 research，再 patch/redistill |
| `RERESEARCH` | References 缺失、不可信、由 Skill 倒推、严重幻觉或无法支撑关键结论 | 重新建立独立 evidence base |
| `REBUILD` | Research 与 Skill 两层均严重失效 | research → distill 全流程重建 |
| `REVIEW` | provenance 无法可靠判断 | 保留现状，人工/进一步证据核查，禁止误删 |

### 最小修改原则

永远选择能够恢复 Nuwa 质量的**最小充分修复**：

`KEEP < CLEAN < PATCH < REDISTILL < RESEARCH-GAP/RERESEARCH < REBUILD`

不得因为模型来源不同、文件时间不同、格式不统一就直接全量重跑。

---

## 4. 模型无关原则

GPT、Claude、Gemini、WorkBuddy 或其他模型/版本可以混合参与同一 corpus。

生成模型只作为 provenance metadata（若已知）记录，不作为质量评分依据。

最终一致性来自：

`same canonical pipeline + same audit standard + same repair policy`

而不是：

`same model everywhere`

---

## 5. 与旧 G1–G11 的关系

旧 G1–G11 **不删除**，但其定位调整为工程/结构检查，不再单独代表“Nuwa 蒸馏成功”。

特别注意：

- “正好 6 个模型”是 emperor-skill corpus 统一规则；Nuwa 通用范围仍为 3–7。
- “诚实边界”字符串只能出现一次属于模板/parser 兼容规则，不是语义质量本身。
- “张力关键词出现 ≥2 次”只能作为低成本静态提示，不能证明存在真实 internal tensions。
- “时间线 ≥5”属于 completeness，不代表 mental-model quality。
- G1–G11 全绿只能说明 L4 大体合规，不能替代 L1–L3。

---

## 6. Audit 输出格式

每个人物至少输出：

```text
<id>-perspective
L1 Provenance: PASS | UNCERTAIN | FAIL
L2 Evidence: PASS | PARTIAL | FAIL | LIMITED-EVIDENCE
L3 Semantic:
  Faithfulness: ...
  Specificity: ...
  Abstraction: ...
  Transferability: ...
  Evidence linkage: ...
  Limitations: ...
  Internal tensions: ...
  Counter-evidence: ...
  Model independence: ...
  Decision heuristics: ...
  Expression DNA: ...
  Honesty: ...
  Information density: ...
Genericity Test: PASS | WEAK | FAIL
Counter-evidence Test: PASS | WEAK | FAIL
L4 Engineering: PASS | PARTIAL | FAIL
Action: KEEP | CLEAN | PATCH | REDISTILL | RESEARCH-GAP | RERESEARCH | REBUILD | REVIEW
Reason: <简洁、可核查理由>
```

全库报告必须同时汇总各 Action 数量，使修复成本可估算。

---

## 7. Canonical authority

规则优先级：

1. Nuwa 官方方法论 / canonical specification；
2. 本文件定义的 audit / recovery policy；
3. emperor-skill domain profile；
4. WorkBuddy / agent / local scripts 的实现细节。

低优先级工具不得静默修改高优先级质量标准。任何新增硬门禁必须说明来源、目的和层级；否则默认只作为 advisory check。
