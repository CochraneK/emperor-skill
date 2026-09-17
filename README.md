<div align="center">

# 帝王工程 · emperor-skill

**从历史证据到人物心智模型，再到比较、模拟与数据可视化。**

`304 Perspective Skills · 1,312 stable persons · P0 216/216 complete · Nuwa Audit v2`

[打开项目面板](https://cochranek.github.io/emperor-skill/) · [P1 Anchor Plan](assessment/P1_ANCHOR_PRIORITY.md) · [质量审查正典](NUWA_AUDIT_V2.md) · [Corpus QA](assessment/CORPUS_QA.md)

</div>

## 这不是帝王百科

`emperor-skill` 把历史统治者建模为**可追溯、可审计、可比较**的 Perspective Skills。蒸馏只是知识生产层；稳定人物 ID、来源证据、质量审查、比较分析、历史情境模拟和可视化共同组成完整工程。

```text
Sources
  ↓
Research / References
  ↓
Evidence synthesis
  ↓
Perspective Skills
  ↓
Stable person / corpus registry
  ↓
Analysis & Simulation
  ↓
Visualization & Interactive Reports
```

## 当前状态

当前机器快照：

| 指标 | 状态 |
|---|---:|
| Skill packages | **304** |
| Candidate persons | **1,312** |
| Stable IDs active | **1,312 / 1,312** |
| Locked CORE | **913** |
| CORE with Skill | **302** |
| CORE missing | **611** |
| CORE coverage | **33.08%** |
| REVIEW | **365** |
| EXTENDED | **15** |
| LEGENDARY | **16** |
| Identity / canonical-name blockers | **0** |

现有 304 个包都已被 corpus 系统解释：303 个匹配人物，1 个（太丁）作为明确 scope exception 保留历史证据包，但不计入 ruler CORE denominator。

### P0 已完成

秦→清主链的 locked CORE 已达到 **216 / 216**，`p0_backbone_missing = 0`，mapping issues = 0。五代主链现已作为 `skills/wudai/` 纳入 corpus。

### 当前 P1

P1 从剩余 **207** 个 post-Qin CORE 缺口中建立首批**跨政权平衡研究 tranche**。它不是人物评分榜：生成器只提供 deterministic polity round-robin 工作序列；source review 记录证据状态、转型语境、比较链接和未来 simulation / visualization context，不给人物总分或优劣排名。

初始 research/distillation tranche 目标：**24 人，至少覆盖 8 个 polity**。当前入口：[`assessment/P1_ANCHOR_PRIORITY.md`](assessment/P1_ANCHOR_PRIORITY.md)。

## Nuwa Audit v2

统一验收标准见 [`NUWA_AUDIT_V2.md`](NUWA_AUDIT_V2.md)。不同模型、worker 或 agent 可以参与 corpus；统一的是**知识血缘、证据标准和出口质量**，不是生成模型。

四层验收：

1. **L1 Provenance** — `Sources → Research → Skill` 的真实知识血缘；禁止从 Skill 倒推 References 冒充研究。
2. **L2 Evidence** — 来源真实性、证据等级、事实 / 史评 / 推断与不确定性边界。
3. **L3 Semantic Distillation** — 人物特异性、抽象质量、可迁移性、反证、内在张力、limitations、信息密度。
4. **L4 Engineering** — schema、目录、角色协议与 corpus 兼容性。

当前自动 L3 similarity signal：**0 flagged packages / 0 high-similarity pairs / 0 repeated long-paragraph groups**。这只是 review signal，不等于对全部人物完成了人工 L3 verdict。

### Anti-Goodhart

最低字数、字符数、KB、关键词次数、来源数量都不是 Nuwa 质量。不得为了过门禁制造 filler。史料天然稀缺的人物应降低推断强度，必要时明确 `LIMITED-EVIDENCE`，而不是补写不存在的心理、台词或动机。

## Corpus construction

主名单采用分段 master files + stable person registry + 确定性生成器维护。

```bash
python _redo_tools/_build_ruler_corpus_with_overrides.py
python _redo_tools/_build_corpus_queue.py
python _redo_tools/_build_distillation_priority.py
python _redo_tools/_build_p1_anchor_priority.py
```

核心生成状态：

- [`data/corpus-registry.json`](data/corpus-registry.json)
- [`data/distillation-priority.json`](data/distillation-priority.json)
- [`data/p1-anchor-priority.json`](data/p1-anchor-priority.json)
- [`assessment/CORPUS_COVERAGE.md`](assessment/CORPUS_COVERAGE.md)
- [`assessment/P1_ANCHOR_PRIORITY.md`](assessment/P1_ANCHOR_PRIORITY.md)

生成文件不要手改；修改 master / policy / review registry / builder 后由 `Corpus Sync` 重建。

## Simulation Lab

`simulation/` 是 Skill 之上的实验层。已有 solo 报告、汇总页面与反转效度检查，后续保留 duel / coop / one-life / assessment joint-space 等方向。

- [Solo 总目录](simulation/by-dynasty/solo/solo-index.html)
- [Solo 汇总报告](simulation/by-dynasty/solo/solo-ranking.html)
- [反转效度检验](simulation/validity/reversal-validity-report.html)

这些 HTML 是生成产物，不是 canonical history source。历史 solo 子集也不代表当前 1,312 人主名单覆盖率。

## Visualization Layer

展示层最终围绕可计算数据展开：

- 历史时间轴、政权并行与转型；
- mental-model map 与人物模型聚类；
- 制度 / 决策 / 思想网络；
- 人物 × 情境 × 决策 × 结果模拟矩阵；
- Nuwa L1–L4 corpus 质量地图；
- assessment 与帝王模型的共同空间。

## 仓库结构

```text
emperor-skill/
├── skills/                 # 人物 research + Perspective Skill
├── data/                   # stable IDs、master corpus、queue、P1 plan
├── assessment/             # corpus / Nuwa / P1 reports
├── simulation/             # 模拟引擎、数据与生成报告
├── index.html              # GitHub Pages 项目面板
├── NUWA_AUDIT_V2.md        # 质量 / recovery 正典
├── AGENTS.md               # AI 协作者入口
├── HANDOFF.md              # 当前阶段接力点
└── _redo_tools/            # deterministic generators / QA tools
```

## 给 AI / agent

开始修改前先读 [`AGENTS.md`](AGENTS.md)、[`NUWA_AUDIT_V2.md`](NUWA_AUDIT_V2.md) 与 [`HANDOFF.md`](HANDOFF.md)。当前不要回退到已经解决的 26 identity issues，也不要重新打开 P0；直接沿 P1 source-review → research → distill → audit 推进。

## License

仓库原创蒸馏文本按 [`LICENSE.md`](LICENSE.md) 说明授权；公有领域史料仍归其原始文献体系。引用与史料使用必须保留来源边界。
