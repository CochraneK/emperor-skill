# emperor-skill — 审查交接说明（Nuwa Audit v2 对齐版）

> 本文是仓库状态/历史线索说明，不是高于 `NUWA_AUDIT_V2.md` 的质量规范。
> 旧 WorkBuddy 报告中的数字与“达标”结论均视为历史快照；当前判断必须按 Nuwa Audit v2 重算。

## 1. 项目定位

`emperor-skill` 不只是 Skill 收藏库，而是一条长期数据链：

`Sources → Research / References → Evidence synthesis → Skill → Structured data → Simulation / Analysis → Visualization`

蒸馏只是第一步。后续核心产品包括跨帝王比较、模拟、人格映射、质量地图与数据可视化。

当前仓库快照：267 个帝王 Skill 包，17 个朝代目录；另有 simulation 引擎/报告与 assessment 骨架。

## 2. Canonical quality rule

唯一仓库级验收正典：[`NUWA_AUDIT_V2.md`](NUWA_AUDIT_V2.md)。

四层：

- L1 Provenance：真实知识血缘；
- L2 Evidence：证据真实性、等级、覆盖与不确定性；
- L3 Semantic：人物特异性、抽象、迁移、反证、张力、局限、信息密度；
- L4 Engineering：schema、目录、角色协议与项目兼容性。

### 已废止为 Nuwa 硬门禁的旧 WorkBuddy proxy

以下规则可以作为历史/工程信号，但不得再单独判定 Nuwa PASS/FAIL：

- 每份 research ≥2.5KB；
- SKILL.md >1KB；
- 包内必须恰好 8 个文件；
- 关键词出现次数；
- 来源数量越多越好；
- 仅凭 mtime 判定正序/倒序。

**不得继续为了达到 2.5KB 或其他长度阈值扩写 filler。** 已经因此补写的材料不自动作废：保留有证据价值的内容，冗余部分在 CLEAN 阶段删除。

## 3. Provenance：我们已经知道什么

正确流程：

`Sources → Research → Distillation → SKILL.md`

错误流程：

`SKILL.md → 倒推/扩写 References`

历史 WorkBuddy 在 2026-09-16 曾在批量修改 references 前固化 `_redo_tools/_order_suspects_39.md`：39 个包的 SKILL mtime 早于底稿。这个列表是**异常线索，不是定罪名单**。后续批量追加“排除声明”已经污染 mtime，因此不能再用当前文件时间重算 provenance。

处理原则：

1. 39 个历史嫌疑包进入 `REVIEW`；
2. 若 references 可证明为独立研究且质量合格 → `REDISTILL` Skill 即可；
3. 若 references 明确由 Skill 倒推 → `RERESEARCH`；
4. 若无法判断 → 保留，不删除，继续 forensic review；
5. 旧 Skill 只能用于 diff/比较，不能作为重建 research 的证据。

## 4. 旧“92 个待扩写包”如何处理

`_todo_92.txt` / `_todo92_tiers.txt` 是按“底稿 <2.5KB”生成的历史工作队列，**不再是当前修复队列**。

因此：

- 不因为 `<2.5KB` 自动补写；
- 不因为 `≥2.5KB` 自动 KEEP；
- 已完成的 A 档补稿不撤回，但需要按 Evidence / Semantic 质量重新判断是否只是 filler；
- B/C 档停止按字节缺口推进；
- 真正的缺口改由 L1–L3 audit 决定：`KEEP / CLEAN / PATCH / REDISTILL / RESEARCH-GAP / RERESEARCH / REBUILD / REVIEW`。

这一步避免继续消耗模型 token 去填“字节缺口”。

## 5. 传说 / 半信史时期

夏、早商等 evidence-sparse 人物不能因材料少而被机械判低质量，也不能通过扩写把不确定性伪装成丰富证据。

要求：

- 明确区分同时代/出土材料、后世传世文献、现代研究与框架推断；
- 甲骨等材料只支持其实际能支持的结论；
- 不把后世记载自动称为“同时代一手确证”；
- 证据不足时降低结论强度，允许 `LIMITED-EVIDENCE`。

## 6. 当前资产与清理策略

### 必须保留

- `skills/` 中的历史人物资产，除非经过 provenance/evidence 审核确认应重建；
- `simulation/_engine/` 与源数据；
- 当前页面需要的 simulation HTML；
- `NUWA_AUDIT_V2.md`、`AGENTS.md`、README、HANDOFF、LICENSE；
- `_nuwa_brief*.md` 与 `_distill_prehan_brief.md`：暂保留为 provenance / rule-drift 历史证据；
- `_redo_tools/_order_suspects_39.md`：保留为 mtime 被污染前的历史快照；
- 通用 audit / coverage / registry 工具。

### 可删除 / 已开始删除

- 已执行完且只服务一次提交、一次登记、一次 memory 修改的脚本；
- 指向另一个本地仓库绝对路径的历史 registration helper；
- git 故障诊断/修复完成后的临时脚本；
- 可重建的临时 dump/cache（若未被 provenance forensic 使用）。

删除前优先确认其不包含唯一 provenance 线索。历史仍可从 git 恢复。

## 7. 已知 WorkBuddy rule drift

历史提交显示曾把以下内容写成“严格 Nuwa 合规”：8 文件、六维各 ≥2500B、SKILL >1KB、诚实边界字符串次数、module/group、mtime 顺序等。这个定义现在已经被 Nuwa Audit v2 纠正：其中多数属于 L4 或 audit signal，而不是 L1–L3 的 epistemic quality。

旧 `_redo_tools/_audit_nuwa_all.py` 已改为 **v2 静态信号扫描器**：不再使用文件大小门禁，也不再凭 mtime 宣判 provenance；它明确不能替代 L3 语义审核。

## 8. Page / 数据产品方向

根 `index.html` 是分层产品入口，目标结构：

1. Corpus overview；
2. Nuwa quality audit / repair map；
3. Emperor Skill explorer；
4. Existing simulation reports；
5. Structured analysis；
6. Visualization lab。

下一阶段应生成机器可读 registry，使页面数字、朝代分布、audit 状态、simulation coverage 都来自数据，而不是手写 HTML。

建议 canonical record 至少包含：

`id, name, dynasty, reign, evidence_status, provenance_status, semantic_status, engineering_status, repair_action, mental_models, source_profile, simulation_coverage`

这将成为未来时间轴、聚类、关系网络、模型地图和 simulation matrix 的共同数据层。

## 9. 当前未解决事项

- 对 267 包执行真正的 L1/L2/L3 recovery audit；
- 对 39 个历史倒序嫌疑做 forensic review，而不是直接重做；
- 废止旧 92 包“按 KB 补稿”排期并转换成 v2 repair queue；
- 识别此前为了长度补出的 filler，执行 CLEAN；
- 建立 corpus registry / audit registry；
- 让 Page 从 registry 读取真实状态；
- 继续清理 `_redo_tools/` 中确认没有 forensic/复用价值的一次性文件；
- 逐步补齐 simulation / assessment / visualization 层。

## 10. 决策原则

**最小充分修复，证据优先，保留不确定性。**

不要因为文件短就扩写，不要因为文件齐就宣称合规，不要因为时间戳异常就删除，不要因为模型不同就全量重跑。
