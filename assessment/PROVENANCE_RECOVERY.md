# Provenance Recovery · Nuwa Audit v2

> 本文件取代旧的“39 个倒序 = 自动重做”解释。旧 `_redo_tools/_order_suspects_39.md` 仅保留为 2026-09-16 的 forensic snapshot。

## 判定规则

mtime 只产生 `REVIEW` 信号，不证明研究是倒推生成。逐包检查六维底稿本身：

- 是否是独立 evidence base，而非把 SKILL.md 的六个模型换句话写回底稿；
- 是否包含 Skill 未采用的材料、异说、反例、时间线、来源层级；
- 是否区分史实 / 史论 / 框架推断；
- 是否存在明显 filler 或为旧 2.5KB gate 人工膨胀；
- 若 research 可独立成立而 Skill 早于它：`REDISTILL`，不重新 research；
- 若 research 明显由 Skill 倒推：`RERESEARCH`；
- 无法确认：`REVIEW`，禁止误删。

## 已开始逐包复核

### jin / simadewen-perspective

**历史信号**：在旧 39 包 mtime snapshot 中，SKILL 早于底稿 152 秒。

**当前判定：PATCH / REDISTILL-CANDIDATE（不是 RERESEARCH）**

理由：

1. 六维底稿均存在，且不只是 SKILL 六模型的逐段反写；包含诏令、对话、表达、他者史论、决策与时间线等不同 evidence views。
2. 底稿主动区分【史料原文/一手】【史论/二手】【框架推断】，并保留“无可靠域外同期记录”“围棋仅作趣味旁证”等限制性信息，说明其具备一定独立研究结构。
3. 但 research 内存在需要清理的过度推断/不严谨标签，例如把后世编纂的《晋书》《资治通鉴》机械标作“一手”；“谶语导致其心理预期”“出生环境形成守成底色”等推断强度偏高。
4. `SKILL.md` 与 research 高度同构，且历史 mtime 表明当前 Skill 不可能由当前版本 references 正序生成。因此不能直接 `KEEP`。

**最小修复**：先 PATCH evidence taxonomy 与过度推断，再从修正后的六维 research REDISTILL `SKILL.md`；无需重新进行全量 research，除非定向核验发现引用本身失实。

## Queue

其余 38 个旧 mtime 嫌疑包保持 `REVIEW`，逐包按同一规则推进。旧“92 个体量不足”不再构成修复优先级。
