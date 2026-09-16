# AGENTS.md —— 给 AI 与接手者的约束入口

> 只写必须知道的。项目介绍看 `README.md`；质量正典看 `NUWA_AUDIT_V2.md`；实际 worker 指令看 `WORKER_BRIEF_V2.md`。

## 定位

把中国历代帝王蒸馏为 `-perspective` Skill，并在其上进行比较分析、模拟与数据可视化。蒸馏是数据生产层，不是项目终点。

## Nuwa 蒸馏验收

所有新建、补救、重蒸馏和全库审核统一遵循 `NUWA_AUDIT_V2.md` 与 `WORKER_BRIEF_V2.md`。

唯一认可的知识血缘：

`Sources → Research / References → Evidence synthesis → Mental-model distillation → SKILL.md → Audit`

不得用既有 `SKILL.md` 倒推 References 后宣称完成 Nuwa 蒸馏。后来若已有独立且合格的 References，可直接以其为上游重新蒸馏 Skill，无需重复 research。

旧 G1–G11 / `quality_check.py` 属 L4 Engineering/static lint，不能单独证明 Nuwa 质量。完整验收还看 L1 Provenance、L2 Evidence、L3 Semantic Distillation。

最低字数、字符数、KB/文件大小、关键词次数、来源数量不是 Nuwa 质量门禁；不得为 proxy 制造 filler。历史 `_nuwa_brief*.md` 中的 ≥2.5KB 要求已经 deprecated，不得继续执行。工程约束必须标注 `PROJECT/TOOLING RULE — NOT NUWA QUALITY`。

修复动作：`KEEP / CLEAN / PATCH / REDISTILL / RESEARCH-GAP / RERESEARCH / REBUILD / REVIEW`。遵循最小充分修复。

## 技术栈

- Python 3.13 标准库优先。
- 报告为单文件离线 HTML；生成产物不要手改，应修改生成器/数据源再重渲。

## 目录约定

| 路径 | 角色 |
|---|---|
| `skills/<朝代>/<id>-perspective/` | 帝王 Skill 与 evidence package |
| `data/` | corpus registry 与未来分析/可视化结构化数据 |
| `simulation/_engine/` | 模拟引擎与数据源 |
| `simulation/.../*.html` | 可重建报告产物 |
| `assessment/` | 质量恢复、未来 assessment 与相关分析层 |

八文件 package 是当前 emperor-skill packaging profile，不是 provenance 证明。历史批次结构不同不能仅凭目录判失败。

## 工作纪律

1. Research 必须先于它所支持的新 Skill 蒸馏；mtime 只能作为 forensic signal，不能单独判 provenance。
2. 修改 Skill 时按 L1–L4 判断；旧 checker 全绿不等于语义合格。
3. 运行 Genericity Test 与 Counter-evidence Test，防止帝王模型模板化。
4. 史料分类要区分同期/出土、传世史书、后世史论、现代研究、框架推断；不要把“正史”机械等同于“本人/同期一手”。
5. 夏商等材料稀疏人物允许 `LIMITED-EVIDENCE`；不得为了丰满人物而制造心理或言语。
6. 保留未来分析需要的结构化可比字段和 provenance，不为清仓或页面好看破坏数据。
7. 删除前区分核心资产、可重建生成物、forensic evidence 与一次性残留。provenance 尚未恢复完的取证文件先保留。
8. canonical authority：Nuwa 官方方法论 > `NUWA_AUDIT_V2.md` > `WORKER_BRIEF_V2.md` / emperor domain profile > WorkBuddy/agent/local scripts。

## 当前恢复工程

- `assessment/PROVENANCE_RECOVERY.md`：逐包 recovery 记录。
- `data/corpus-registry.json`：面向 Page / 分析 / simulation 的结构化 registry。
- `_redo_tools/_order_suspects_39.md`：历史 mtime 快照，只是 REVIEW 线索。
- 旧 92 个“体量不足”队列：已废止为质量返工依据。

不要把历史 WorkBuddy memory、旧 brief 或旧脚本里的数字/规则当永久规范。
