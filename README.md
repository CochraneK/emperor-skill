# 帝王工程（emperor-skill）

把中国主要王朝帝王蒸馏为可运行的 `-perspective` Skill，并在其上做**模拟场**与**人格测验**。
本仓库与蒸馏主项目（nuwa-skill）解耦，便于独立分发与复用。

## 三大块

```
emperor-skill/
├── skills/        # ① 帝王 Skill 库（按朝代）
│   ├── tang/ song/ yuan/ ming/ qing/ donghan/ sui/
│   └── _audit/            # Skill 质量审计报告
├── simulation/    # ② 模拟场（穿越推演的报告与引擎）
│   ├── by-dynasty/        #    容器 A：每朝单独穿越（不跨代，开局满血）
│   │   ├── solo/ duel/ coop/
│   ├── one-life/          #    容器 B：一条命，唐→宋→元→明→清 连续推进
│   │   ├── solo/ duel/ coop/
│   ├── validity/          #    效度检验报告
│   └── _engine/           #    推演/评分脚本与数据
└── assessment/    # ③ 人格测验（测完输出「你本人的 Skill」）
    ├── engine/            #    题库与计分引擎
    ├── archetypes/        #    帝王人格原型映射
    └── reports/           #    样例报告
```

## ① skills/ —— 帝王 Skill 库

**共 94 个帝王包**（每包一个 `<id>-perspective/` 目录）：

| 目录 | 朝代 | 数量 | 年代 |
|---|---|---|---|
| `donghan/` | 东汉 | 13 | 25–220 |
| `sui/` | 隋 | 3 | 581–618 |
| `tang/` | 唐 | 21 | 618–907（含武周武则天） |
| `song/` | 宋 | 18 | 960–1279（北宋 9 + 南宋 9） |
| `yuan/` | 元 | 11 | 1271–1368 |
| `ming/` | 明 | 16 | 1368–1644 |
| `qing/` | 清 | 12 | 1616–1912（含后金大汗努尔哈赤、皇太极） |

每个帝王子目录结构一致：

```
<id>-perspective/
├── SKILL.md                 # 12 章固定结构：核心心智模型 / 表达DNA / 诚实边界 / 调研来源 …
├── references/research/     # 六份底稿（著作·对话·表达DNA·他者视角·决策·时间线），逐条标注出处
└── scripts/quality_check.py # 本地质量门禁（6 项）
```

## ② simulation/ —— 模拟场

两种**容器** × 三种**模式** = 6 个格子，详见 [`simulation/README.md`](simulation/README.md)。

- 容器：`by-dynasty/`（每朝单独、不跨代、开局满血）｜`one-life/`（一条命跨五朝苟活）
- 模式：`solo/`（单人轮值）｜`duel/`（双人对抗，相互阻碍）｜`coop/`（双人合作）

**已完成**：`by-dynasty/solo/` —— 78 帝全量推演（78 × 77 = **6006 条处置**），产出
`solo-<key>.html` × 78 + `solo-index.html` 总目录 + `solo-ranking.html` 总排名报告；
另有效度检验 `validity/reversal-validity-report.html`。
**未建**：`duel/` 与 `coop/` 引擎、`one-life/` 血量推进。

## ③ assessment/ —— 人格测验

基于全部 Skill 与事件设计人格测验，测完输出**用户本人的 Skill（含心智报告）** + **最相似的帝王** + **若你穿越到历朝历代的结果**。设计见 [`assessment/README.md`](assessment/README.md)。

## 蒸馏方法与质量门禁（作用于 ① skills/）

- **六维调研流水线**：著作 / 对话 / 表达DNA / 他者视角 / 决策 / 时间线 → 框架提炼 → 构建 → 质检。
- **一手史料优先**：东汉取《后汉书》《东观汉记》；隋取《隋书》《北史》；唐取两《唐书》《资治通鉴》《唐会要》《册府元龟》《唐大诏令集》《全唐文》；宋取《宋史》《续资治通鉴长编》《建炎以来系年要录》《三朝北盟会编》《文献通考》《全宋文》；元取《元史》《元典章》《新元史》；明取《明史》《明实录》；清取《清史稿》《清实录》。各帝一手来源占比均 >50%。
- **框架零污染**：不以外来心理 / 系统框架作透镜嵌入正文。
- **质量门禁（6/6）**：心智模型 3–7（含局限）｜表达DNA ≥3 项｜诚实边界 ≥3 条｜内在张力 ≥2 处｜一手占比 >50%。

**全库 94 位帝王，audit 100% 通过（6/6），零质量债务。**

## 使用

将某帝王子目录作为 Skill 载入支持 `-perspective` 的 agent 框架即可。触发示例：
「用朱棣的视角看迁都」「以忽必烈之心度之」「若乾隆面临 AI，他会怎么想」。

## 目录约定

- 一次性脚本、推演数据、报告生成器进 `simulation/_engine/`；渲染产物进 `simulation/<容器>/<模式>/`。
- 引擎脚本**只依赖 Python 3.13 标准库**（无第三方包），见 [`requirements.txt`](requirements.txt)。
- 接手 / 换电脑请看 [`HANDOFF.md`](HANDOFF.md)；给 AI 的约束入口是 [`AGENTS.md`](AGENTS.md)。

## 版权与来源

- 帝王为历史公众人物，所引《后汉书》《隋书》两《唐书》《宋史》《元史》《明史》《清史稿》等均为公有领域文献。
- 本仓库的蒸馏文本（SKILL.md 及底稿的原创归纳）以 **CC BY 4.0** 授权；引用史料原文归原文献所有。
- 本仓库仅含历史帝王，不涉及任何虚构角色版权内容。
