# HISTORICAL BRIEF — 秦以后 Worker 规范（已取代）

> ⚠️ **归档说明（2026-09-17）**：本文件只保留为 spec-history / provenance 线索。当前唯一审查正典是 [`NUWA_AUDIT_V2.md`](NUWA_AUDIT_V2.md)，当前执行规范是 [`WORKER_BRIEF_V2.md`](WORKER_BRIEF_V2.md)。
>
> 旧版中的 research ≥2.5KB、固定文件数量、字节数上报、关键词/计数等要求已经废止为 Nuwa 质量门禁。不要继续为这些 proxy 补写内容。

## 这份历史规范曾要求什么

当时的秦以后帝王批次使用统一 `-perspective` 包，通常包含 `SKILL.md`、六维 research 与 `quality_check.py`；强调正史、同期文献、简牍碑刻、域外史著等来源，要求异说并列、追尊帝身份说明、史论与本人主张分离、不得编造名言。这些**史料诚实原则仍值得保留**。

但以下只能视为历史工程规则，而非当前 epistemic gate：

- 每份 research ≥2.5KB；
- 必须固定六份文件才能“合格”；
- 固定 6 个心智模型；
- `quality_check.py` 6/6 即代表 Nuwa 合格；
- 上报各底稿字节数；
- 用 mtime/文件体积推断研究顺序或质量。

## 当前迁移规则

历史包不批量推倒重做。按最小充分修复：`KEEP < CLEAN < PATCH < REDISTILL < RESEARCH-GAP/RERESEARCH < REBUILD`，无法确定则 `REVIEW`。

- 已独立完成且证据可用的 research：可直接作为新一轮 REDISTILL 的 evidence base。
- 能证明 research 是从既有 Skill 反向拼装：RERESEARCH。
- 只有 mtime 异常：不足以定罪，进入 provenance REVIEW。
- 只有文件短：不足以判低质；检查 evidence density 与关键事实覆盖。
- 为满足旧阈值产生的 filler：可以 CLEAN，不因此使原 Skill 自动失效。
- 模型是否优秀由 L3 的 Faithfulness / Specificity / Abstraction / Transferability / Evidence linkage / Limitations / Tensions / Counter-evidence / Independence / Decision heuristics / Expression DNA / Honesty / Density 判断。

## 当前 corpus 设计目标

Research 是证据层，Skill 是可调用的认知表示层；二者继续向结构化数据、跨帝王比较、simulation 与 visualization 输出。任何修复都不能为了 Audit 全绿而污染历史证据，也不能为了清理仓库而破坏未来分析所需的数据。

> 原始完整历史文本仍存在 Git history，可用于复盘当时 WorkBuddy 的执行口径；此处压缩正文是为了防止后续 agent 继续执行已经废止的 size-driven workflow。
