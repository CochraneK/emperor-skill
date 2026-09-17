# assessment · Emperor Skill 分析与质量层

`assessment/` 是 emperor-skill 的**分析 / 质量 / 比较层**，不是人物名单本身，也不再以早期“78 位帝王人格测验”作为 canonical 设计。

当前 canonical 数据入口是：

- `../data/rulers-person-index.json`：当前人物索引；`candidate_id` 已兼容映射为稳定 `person_id`。
- `../data/ruler-person-id-registry.json`：append-only 稳定人物 ID registry；新增人物追加 ID，既有 ID 不重排。
- `../data/corpus-gap.json`：CORE coverage 与 Skill 对齐。
- `../data/corpus-identity-issues.json`：identity / matching QA。
- `../data/l3-semantic-review-queue.json`：Nuwa L3 语义相似度**审查信号**，不是自动质量裁决。

## 当前规模

由生成数据维护，不应在手写文档里硬编码为固定历史总数。当前 snapshot：

- Candidate persons: **1,312**
- Locked CORE: **913**
- Existing Skills: **267**
- Matched CORE persons: **265**
- Missing CORE persons: **648**
- Existing Skills accounted: **267 / 267**（其中 1 个为明确 scope exception：太丁未即位）

这些数字会随着小国枚举、REVIEW 处理和新 Skill 蒸馏继续变化；稳定的是 person ID 语义，不是 corpus 总量。

## Nuwa QA 分层

### L1 · Provenance / evidence lineage

回答：这个 Skill 的研究底稿是否可追溯、来源类别是否正确、关键事实/引文能否回到证据。

- `PROVENANCE_RECOVERY.md` 已完成历史 39-package mtime suspect 的语义分诊（39/39）。
- mtime、KB、字数只能触发 REVIEW，不能独立证明 provenance 或质量。
- 当前后续动作是逐包执行 `PATCH / TARGETED VERIFY → REDISTILL`，不是继续按 mtime 重新分类。

### L2 · Structure / evidence discipline

回答：研究维度、证据标注、诚实边界、工程结构是否存在明显机械缺口。

`../_redo_tools/_audit_nuwa_all.py` 只提供静态信号；它不能替代 L3。

### L3 · Semantic quality / distinctiveness

回答：人物模型是否真正从其证据中生长出来，还是泛化、模板化、换名字复用；因果推断和人物辨识度是否成立。

- `L3_SEMANTIC_QA.md` / `../data/l3-semantic-review-queue.json` 先用保守词面信号发现需要一起阅读的 Skill。
- 共享的角色扮演规则、激活/退出机制和通用 workflow 属于产品 shell，**不参与人物语义重复判定**。
- lexical similarity 永远只是 REVIEW prioritization；最终分类必须结合 research/provenance 进行模型或人工语义审查。

### L4 · Engineering / delivery

回答：frontmatter、路径、CI、生成数据、Pages 输入、脚本是否可复现且一致。

稳定 person ID、Corpus Sync、Pages QA 和 Nuwa L3 workflow 都属于这一层。

## 目录中的主要报告

| 文件 | 作用 |
|---|---|
| `CORPUS_COVERAGE.md` | CORE / Skill coverage 的自动报告 |
| `CORPUS_QA.md` | identity / matching QA |
| `PROVENANCE_RECOVERY.md` | 历史 39-package provenance suspect 的语义分诊 |
| `L3_SEMANTIC_QA.md` | 人物知识 payload 的重复/模板化审查信号 |
| `CORPUS_GAP_BASELINE.md` | corpus gap 的历史基线 |
| `LEGACY_78_EMPEROR_PERSONALITY_TEST.md` | 已归档的早期 78×10 人格测验构想 |

## Assessment / comparison 的下一阶段

后续真正的“帝王学”分析应建立在稳定 `person_id` 上，而不是目录名或临时排序 ID 上：

1. 为可比较的历史行为/决策建立版本化 feature schema；
2. 将每个 feature 绑定证据、置信度与时间/统治 episode；
3. 做跨人物、跨政权、跨时代比较，而不是单一总分排名；
4. 将 simulation 输入与具体 Skill / person ID / evidence version 绑定，保证结果可复现；
5. 将 corpus coverage、Nuwa QA、人物面板、比较和 simulation 分层展示到 Page。

> 历史人物分析中的评价维度应保持可追溯和可解释。模型输出不能把有争议的史学解释伪装成确定事实。
