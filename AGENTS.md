# AGENTS.md —— 给 AI 与接手者的约束入口

> 只写「必须知道的」。细节看 `README.md`，交接事项看 `HANDOFF.md`。

## 定位

把中国历代帝王蒸馏为 `-perspective` Skill，并在其上跑**穿越模拟场**与**人格测验**。
本仓库是独立分发的成品仓，**不含**蒸馏主项目（nuwa-skill）的人物/角色库。

## Nuwa 蒸馏验收（必须先读）

所有新建、补救、重蒸馏和全库审核统一遵循 [`NUWA_AUDIT_V2.md`](NUWA_AUDIT_V2.md)。

唯一认可的知识血缘是：

`Sources → Research / References → Evidence synthesis → Mental-model distillation → SKILL.md → Audit`

**禁止**用既有 `SKILL.md` 倒推/扩写 References 后宣称完成 Nuwa 蒸馏；若后来已有独立且合格的 References，应直接以其为上游重新蒸馏 Skill，无需重复 research。

现有 G1–G11 / `quality_check.py` 主要属于 **L4 Engineering Compliance**，不能单独证明 Nuwa 蒸馏质量。验收还必须考虑 L1 Provenance、L2 Evidence、L3 Semantic Distillation Quality。

不得把最低字数、字符数、KB/文件大小、关键词次数或来源数量等 proxy 擅自升级为 Nuwa 硬门禁；不得为了过门禁制造 filler。工具若新增工程约束，必须明确标注 `PROJECT/TOOLING RULE — NOT NUWA QUALITY`。

修复遵循最小修改原则：`KEEP / CLEAN / PATCH / REDISTILL / RESEARCH-GAP / RERESEARCH / REBUILD / REVIEW`，不要因模型不同或格式差异就全量重跑。

## 技术栈

- **纯 Python 3.13 标准库**（无第三方依赖，故无 `pip install` 步骤）。见 `requirements.txt`。
- 报告是**单文件离线 HTML**（内联 CSS/JS，图表走 Chart.js CDN）。

## 常用命令

```bash
python simulation/_engine/check_solo.py                 # 单份推演结构质检（条数=77、分数 0–100 等）
python simulation/_engine/check_solo.py --strict        # 有问题即以退出码 1 结束
python simulation/_engine/cross_check_solo.py           # 全库交叉检验（越界 / 极差 / 分布 / 口径）
python simulation/_engine/eval_crossing_solo.py --all   # 全量重渲 78 份报告 + 总目录
python simulation/_engine/eval_solo_rank.py             # 重生成总排名报告 solo-ranking.html
python simulation/_engine/build_module_map.py           # 重生成 modules_solo.json（模块映射）
python skills/<朝代>/<id>-perspective/scripts/quality_check.py   # 单个帝王包的 L4 工程门禁（不能替代 L1–L3）
```

> `python` 不在 PATH 时，用本机 Python 3.13 的绝对路径替换；**不要**把绝对路径写进脚本或文档。

## 目录约定

| 路径 | 放什么 |
|---|---|
| `skills/<朝代>/<id>-perspective/` | 帝王包；不同历史批次可采用不同 packaging profile，是否必须有 `references/` 以对应任务规范和真实 provenance 为准，不能仅凭目录结构判断 Nuwa 合规性 |
| `simulation/_engine/` | 引擎脚本、`travelers/<key>.json`（推演数据）、处境与年表 JSON |
| `simulation/<容器>/<模式>/` | **渲染产物**（HTML），由引擎脚本生成，不手改 |
| `assessment/` | 人格测验（引擎 / 原型 / 样例报告） |

## 硬约束

1. **产物（HTML）是生成的**：改内容要改生成器再重渲，不要直接编辑 HTML。
2. **推演数据一人一份**：`simulation/_engine/travelers/<key>.json`，每条处境一条记录；具体数量以当前 registry/engine 为准，不把历史固定数量当永久规范。
3. **改动后必过门禁**：跑结构/口径检查；涉及 Skill 时还必须按 `NUWA_AUDIT_V2.md` 判断 L1–L4，不能以旧 checker 全绿替代语义审核。
4. **排序口径不可想当然**：报告一律**按时间顺序**（朝代先后 → 即位年 → 同年次序），依据 `_engine/reign_order.json`；「总分」与「均分」同序，「全库均分（合并）」与「人均极差」不同源。
5. **不引入第三方依赖**；确实需要时先讨论。
6. **不做未经确认的删除或大重构**；历史交给 git。
7. **低优先级 agent 不得静默改 canonical quality standard**：Nuwa 官方方法论 > `NUWA_AUDIT_V2.md` > emperor-skill domain profile > WorkBuddy/agent/local script 实现。

## 状态说明

仓库规模、已蒸馏人物数和 simulation 覆盖数会持续变化。README / HANDOFF / registry/engine 数据应作为当前状态来源；历史 WorkBuddy memory 中的 94/78 等数字仅代表当时快照，不应作为永久断言。
