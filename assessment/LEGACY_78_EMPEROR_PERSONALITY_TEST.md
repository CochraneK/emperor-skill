# Legacy · 78 帝王人格测验方案

> **ARCHIVED / NOT CANONICAL.** This was the original assessment concept when the repository described a 78-Skill corpus. The live corpus has since expanded and now uses a stable person registry plus corpus-wide QA. Keep this document only as design history; do not use its counts or 78×10 assumptions as current project state.

## 原方案

基于当时全部 78 位帝王 Skill 与其历史事件，设计人格测验：测完输出用户本人的 `-perspective` Skill、相似帝王与穿越模拟。

### 原产出物

- **用户 Skill**：与帝王 Skill 同构的 12 章，包括核心心智模型、表达 DNA、时间线、价值观与反模式、诚实边界等。
- **心智报告**：10 轴雷达图、文字解读与内在张力分析。
- **最相似帝王**：以 10 维向量做余弦相似度 top-3，并设镜像帝王。
- **穿越结果**：把用户 Skill 送入 simulation，比较不同历史环境中的结果。

### 原 10 轴

| # | 轴 | 一端 ←→ 另一端 |
|---|---|---|
| A1 | 权力来源 | 武功开国 ←→ 制度承袭 |
| A2 | 合法性叙事 | 血统正统 ←→ 功业自证 ←→ 天命符命 |
| A3 | 风险偏好 | 激进开拓 ←→ 稳健守成 ←→ 退让避祸 |
| A4 | 用人之道 | 纳谏兼听 ←→ 独断专任 ←→ 破格擢新 |
| A5 | 对异己 | 怀柔包容 ←→ 制衡牵制 ←→ 清洗镇压 |
| A6 | 信息处理 | 广开言路 ←→ 亲察苛细 ←→ 闭塞偏信 |
| A7 | 资源观 | 节用养民 ←→ 集中动员 ←→ 奢靡耗国 |
| A8 | 继嗣交班 | 早定明定 ←→ 悬置拖延 ←→ 争夺倾轧 |
| A9 | 退场姿态 | 恋权不放 ←→ 善终禅让 ←→ 殉国死节 |
| A10 | 时代观 | 以史为鉴 ←→ 因时变通 ←→ 复古守旧 |

原原则：每个轴应至少能在 3 位帝王的实际作为中找到锚点。

### 原题目与计分

- 60 题：情境选择 + 7 点 Likert。
- 每题携带权重向量，累加到 10 轴并标准化至 −3…+3。
- 反向题约占 1/3。
- 用户向量与帝王原型向量做余弦相似度。

### 原伦理边界

- 非临床诊断，仅供自我认知与娱乐。
- 默认匿名，不采集可识别信息。
- 报告需明确“此为测验拟合结果，非你的全部人格”。

## 为什么归档

当前仓库已经不再是“78 位帝王的固定集合”。Assessment 若继续发展，应基于稳定 `person_id`、可追溯 provenance、Nuwa L1–L4 QA 和版本化分析模型，而不能把早期 78×10 向量表当作 canonical ruler ontology。旧 10 轴仍可作为未来分析特征的候选来源，但需要重新验证维度定义、编码信度与适用范围。
