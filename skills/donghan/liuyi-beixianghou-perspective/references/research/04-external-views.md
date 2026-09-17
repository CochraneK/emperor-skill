# 04 外部评价 / 身份定位 · 刘懿

> 刘懿最值得研究的史学问题之一不是“性格评价”，而是**他到底如何被后世史书命名和定位**。

## 1. “少帝”与“北乡侯”的双重称谓

2025年徐鹏、杨戈《少帝与北乡侯：〈后汉书〉本纪所见刘懿的双重称谓发微》专门讨论这一问题。论文指出，自《东观汉记》以来的汉晋史书多以“北乡侯”称刘懿；范晔《后汉书》本纪则同时使用“少帝”与“北乡侯”。

论文的解释是：

- **“北乡侯”**更接近东汉朝廷后来对刘懿政治身份的最终定位；
- **“少帝”**体现范晔在史书编纂中对其曾经即皇帝位这一事实与东汉政治史的理解。

因此 corpus 不应简单把“少帝”和“北乡侯”看成两个不同的人，也不应把某一个称呼当作毫无争议的唯一历史身份。

## 2. 死后的王礼安葬

《后汉纪》卷十七记顺帝即位后，以王礼葬北乡侯。这一处理表明：刘懿曾实际即皇帝位，但新政治秩序没有把他的皇帝身份按正常帝号体系永久固定下来。

这类“生前 episode 与死后 canonical status 不完全一致”的人物，对 emperor-skill 的数据设计非常重要：

- `person_id` 必须保持一个人；
- `reign_episode` 应记录其实际即位与在位；
- `posthumous_status` / historiographical_label 可以另外记录；
- 不能靠一个 `canonical_name` 承担所有政治身份。

## 3. 后世叙事焦点

传统材料几乎没有形成关于刘懿个人品德、能力或政策的稳定评价。叙事焦点集中在：

- 阎氏集团为何选择他；
- 太后临朝；
- 他的早逝如何再次打开继承问题；
- 孙程等拥立刘保后的政治清算。

因此对刘懿做“明君/昏君”“能力高低”式评分在证据上没有基础。

## 4. 对项目的意义

刘懿适合作为未来变量层的一个典型 edge case：

- `reign_length` 可观测；
- `accession_route = elite_selection_under_regency` 可编码；
- `effective_personal_rule` 很可能不可观测或接近零，但不能无证据直接填 0；
- `regency = yes`；
- `succession_crisis_context = yes`；
- 大量 personality / decision-style 变量应为 `STRUCTURALLY_UNOBSERVABLE` 或 `UNKNOWN_NOT_RECORDED`。

## 来源

- 范晔《后汉书·皇后纪下》及相关本纪材料。
- 袁宏《后汉纪》卷十七。
- 徐鹏、杨戈：《少帝与北乡侯：〈后汉书〉本纪所见刘懿的双重称谓发微》，《南都学坛》2025年第5期，DOI: 10.16700/j.cnki.cn41-1157/c.2025.05.001。

核验：
- https://zh.wikisource.org/zh-hans/後漢書/卷10下
- https://zh.wikisource.org/zh-hans/後漢紀/卷17
- https://ldxt.cbpt.cnki.net/portal/journal/portal/client/paper/7c0bca02c9554554306a39fe4b51ac1f
