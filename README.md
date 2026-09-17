<div align="center">

# 帝王工程 · emperor-skill

**从历史证据到人物心智模型，再到模拟、分析与数据可视化。**

`267 Perspective Skills · 16 dynasty corpora · Nuwa Audit v2 · Simulation Lab`

[打开项目面板](https://cochranek.github.io/emperor-skill/) · [质量审查正典](NUWA_AUDIT_V2.md) · [Corpus QA](assessment/CORPUS_QA.md) · [模拟说明](simulation/README.md)

</div>

## 这不是帝王百科

`emperor-skill` 把历史人物建模为可运行、可审计、可比较的 Perspective Skills。**蒸馏只是第一步**：这些 Skill 是后续跨帝王比较、历史情境模拟、人格映射、统计分析和数据可视化的数据基础层。

```text
Sources
  ↓
Research / References
  ↓
Evidence synthesis
  ↓
Perspective Skills
  ↓
Structured features / registry
  ↓
Analysis & Simulation
  ↓
Visualization & Interactive Reports
```

## 当前 corpus

当前同步盘点为 **267 个帝王 Skill 包**，覆盖 **16 个朝代 corpus 目录**（`skills/` 另有 `_audit` 非朝代目录）：

| 朝代目录 | 数量 | 朝代目录 | 数量 |
|---|---:|---|---:|
| 夏 `xia` | 17 | 商 `shang` | 31 |
| 周 `zhou` | 37 | 秦 `qin` | 3 |
| 楚汉 `chuhan` | 2 | 西汉 `xihan` | 15 |
| 东汉 `donghan` | 13 | 三国 `sanguo` | 11 |
| 晋 `jin` | 15 | 南北朝 `nanbeichao` | 38 |
| 隋 `sui` | 3 | 唐 `tang` | 21 |
| 宋 `song` | 18 | 元 `yuan` | 15 |
| 明 `ming` | 16 | 清 `qing` | 12 |

主名单工程已经从“已有 Skill 盘点”扩展到**最大候选统治者 corpus**。当前自动化索引包含 **1,312 个候选人物**；其中锁定候选层的 CORE 为 **913**，已有 Skill 匹配 **265**，缺失 CORE **648**。另有 **365 REVIEW / 15 EXTENDED / 16 LEGENDARY**；这三类不会静默进入 CORE 分母。现有 **267 / 267** Skill 均已被 corpus 系统解释：266 个匹配统治者人物，1 个（太丁）作为明确 scope exception 保留证据包但不计入 ruler CORE。

> `candidate_id` 目前仍是临时 ID；在 identity QA、规范名与 scope review 收口前不得把它当永久外键。最新机器状态见 `data/corpus-registry.json`、`data/corpus-identity-issues.json` 与 `data/corpus-work-queue.json`。

## Nuwa Audit v2

统一验收标准见 [`NUWA_AUDIT_V2.md`](NUWA_AUDIT_V2.md)。不同模型、不同 worker 可以参与 corpus；统一的是**出口质量标准，而不是生成模型**。

四层验收：

1. **L1 Provenance** — `Sources → Research → Skill` 的真实知识血缘；禁止从既有 Skill 倒推 References 冒充研究。
2. **L2 Evidence** — 来源真实性、证据等级、事实 / 史评 / 推断边界与不确定性。
3. **L3 Semantic Distillation** — 人物特异性、抽象质量、可迁移性、反证、内在张力、limitations、信息密度。
4. **L4 Engineering** — schema、目录、角色协议、触发规则与 corpus 兼容性。

旧式 `quality_check.py` / G1–G11 主要属于 L4。**工程门禁全绿不等于 Nuwa 蒸馏质量合格。**

### Anti-Goodhart

最低字数、字符数、KB、关键词次数、来源数量都不是 Nuwa 质量本身。不得为了过门禁制造 filler。研究材料应以“是否足以支撑结论”判断；史料天然稀缺的人物应降低推断强度，而不是机械补字。

修复遵循最小充分原则：`KEEP / CLEAN / PATCH / REDISTILL / RESEARCH-GAP / RERESEARCH / REBUILD / REVIEW`。

## Corpus construction

最大主名单采用分段 master files + 确定性生成器维护。当前自动 QA 的核心约束是：**先解 identity/scope blocker，再冻结人物 ID；只对锁定 CORE 缺口进入 research → evidence synthesis → Nuwa distillation → audit。** REVIEW / EXTENDED / LEGENDARY 不批量偷渡进 CORE，也不能为了补数量从旧 Skill 反推 References。

可重建入口：

```bash
python _redo_tools/_build_ruler_corpus.py
python _redo_tools/_build_corpus_queue.py
```

生成状态见 [`assessment/CORPUS_COVERAGE.md`](assessment/CORPUS_COVERAGE.md) 与 [`assessment/CORPUS_QA.md`](assessment/CORPUS_QA.md)。

## Simulation Lab

`simulation/` 是 Skill 之上的实验层。目前仓库已有 `by-dynasty/solo/` 报告、汇总页面和效度检验；后续会继续扩展 duel / coop / one-life 等模式。

- [Solo 总目录](simulation/by-dynasty/solo/solo-index.html)
- [Solo 汇总报告](simulation/by-dynasty/solo/solo-ranking.html)
- [反转效度检验](simulation/validity/reversal-validity-report.html)

这些 HTML 是生成产物；分析逻辑和数据源在 `simulation/_engine/`，不要把生成页面当作 canonical data source。现有 solo 是历史较早的子集实验，不代表当前 1,312 人主名单覆盖率。

## Visualization Layer

项目最终展示层会围绕可计算数据，而不是 Markdown 文件列表。规划中的核心视图包括：

- 历史时间轴与朝代演化；
- mental-model map 与人物聚类；
- 帝王关系 / 思想 / 决策网络；
- 人物 × 情境 × 决策 × 结果模拟矩阵；
- Nuwa L1–L4 corpus 质量地图；
- assessment 用户人格与帝王模型的共同空间。

因此新增或修复 Skill 时，应同时保护未来结构化分析所需的稳定 ID、时代信息、证据边界与可比较字段。

## 仓库结构

```text
emperor-skill/
├── skills/                 # 人物知识与 Skill 层
├── data/                   # 最大统治者主名单、registry、QA 与结构化数据
├── simulation/             # 模拟引擎、数据与生成报告
├── assessment/             # corpus QA、provenance recovery、未来 assessment
├── index.html              # GitHub Pages 分层项目面板
├── NUWA_AUDIT_V2.md        # 当前验收 / recovery 正典
├── AGENTS.md               # AI 协作者入口
├── HANDOFF.md              # 项目交接
└── _redo_tools/            # corpus build / provenance recovery / audit 工具
```

## 给 AI / agent 的原则

开始修改前先读 [`AGENTS.md`](AGENTS.md) 与 [`NUWA_AUDIT_V2.md`](NUWA_AUDIT_V2.md)。规则优先级：

`Nuwa 官方方法论 > NUWA_AUDIT_V2 > emperor-skill domain profile > WorkBuddy / agent / local script`

低优先级工具不得静默创造新的 canonical quality gate。

## License

仓库原创蒸馏文本按 [`LICENSE.md`](LICENSE.md) 说明授权；历史公有领域材料仍归其原始文献体系。引用与史料使用应保留来源边界。
