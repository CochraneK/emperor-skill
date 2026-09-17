# 05 决策 · 刘懿

> **LIMITED-EVIDENCE**：目前没有足够证据支持把具体国家决策归为刘懿本人所作。本维度因此采用“decision attribution audit”，把人物本人决策与围绕其皇位发生的他人决策分开。

## 不应归因给刘懿的关键决策

### 1. 选择刘懿为帝

行动者：阎太后、阎显等摄政集团。

史料明确指出阎太后希望长期专政，倾向选择年幼宗室，因此迎立北乡侯刘懿。这不是刘懿本人“争取皇位”的证据。

### 2. 即位后清洗前朝权力集团

行动者：阎显及阎氏集团。

《后汉书·皇后纪下》叙述阎显排斥耿宝、樊丰、王圣等政治力量。刘懿本人是否参与判断、是否理解这些处置、是否赞成，现有材料不足。

### 3. 病重时另选继承人

行动者：阎显、江京等。

刘懿病重后，阎氏集团担心拥立原废太子刘保会遭报复，因此讨论另选宗室。这同样属于围绕刘懿皇位的精英决策，不是刘懿的 succession planning。

## 能否提炼个人决策模型？

**现阶段不能。**

如果强行从“在位二百余日”提炼出风险偏好、用人、纳谏、财政、外交、改革、危机处理等维度，会把摄政集团行为错误归因于一个史料中几乎没有个人能动性记录的短期幼主。

## 可以提炼的结构模型

虽然不能建立个人决策模型，但可以安全建立三条**制度处境模型**：

1. **被选择的君主**：继承并不总由被继承者本人推动；精英集团会选择最符合自身约束的候选人。
2. **名义权力与实际权力分离**：拥有最高正式头衔不等于拥有可观测的实际决策权。
3. **短统治放大继承脆弱性**：当新君迅速死亡、既有废立争议未解决，继承问题会立即重启并触发精英冲突。

这三条可以用于 simulation / institutional analysis，但必须标注为“从刘懿 episode 抽取的制度机制”，而非“刘懿的心理模型”。

## 数据层建议

未来变量层中建议保留：

- `personal_decision_evidence_density = VERY_LOW`
- `regency_present = TRUE`
- `accession_selected_by_regency_bloc = TRUE`
- `effective_personal_rule = UNKNOWN_STRUCTURALLY_UNOBSERVABLE`
- `succession_crisis_at_accession = TRUE`
- `succession_crisis_at_death = TRUE`

## 来源

- 《后汉书·皇后纪下》
- 《后汉纪》卷十七

核验：
- https://zh.wikisource.org/zh-hans/後漢書/卷10下
- https://zh.wikisource.org/zh-hans/後漢紀/卷17
