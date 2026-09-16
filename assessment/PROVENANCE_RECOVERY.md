# Provenance Recovery · Nuwa Audit v2

> 旧 `_redo_tools/_order_suspects_39.md` 是 forensic snapshot，不是失败名单。mtime 只触发 REVIEW。

## Recovery rule

逐包问四件事：research 是否能独立于 Skill 成立；是否包含 Skill 未采用的材料/异说/限制；来源层级是否诚实；是否出现旧 size gate 驱动的 filler。然后采用最小充分修复：

- research 独立且可靠 → `REDISTILL`（必要时先 `PATCH`）；
- research 明显由 Skill 倒推 → `RERESEARCH`；
- 证据缺口局部 → `RESEARCH-GAP`；
- 仅冗余 → `CLEAN`；
- 无法确认 → `REVIEW`。

## Batch A · Jin legacy mtime suspects

旧 snapshot 的晋包共 7 个：`simadewen`, `simadezong`, `simashao`, `simaye`, `simayi`, `simayu`, `simazhong`。

### simadewen-perspective

**Action: PATCH → REDISTILL. RERESEARCH not currently required.**

六维 research 有独立 evidence views、异说和限制信息，不只是六模型反写；但存在 taxonomy 与推断强度问题，例如把后世编纂史书机械标作“一手”，以及把谶语心理、出生环境等写成较强心理因果。当前 Skill 又早于当前 references，因此不能直接 KEEP。

### simadezong-perspective

**Action: PATCH → REDISTILL; targeted source verification required.**

Research 对“安帝本人无可靠可归属言语、诏令多为执政者拟进”这一关键限制处理得较好，说明 evidence base 并非单纯 Skill 反写。但 04 external views 暴露明显 taxonomy/事实风险：唐修《晋书》论赞仍被标“一手”；《十六国春秋》辑本、《洛阳伽蓝记》等被过宽地归入同期/域外证据。先修证据分类和可疑旁证，再重蒸馏，不需要把全部六维推倒重搜。

### simashao-perspective

**Action: PATCH → REDISTILL-CANDIDATE.**

04 research 明确区分《晋书》论赞、王夫之、司马光、现代门阀政治解释，并保留微服察敦等异文，独立研究结构较明显。主要问题仍是“正史/载记 = 一手”的粗分类，以及部分轶事需定向核验。暂不判 RERESEARCH。

### simaye-perspective

**Action: PATCH → REDISTILL-CANDIDATE.**

04 research 有世系考辨、十六国视角、现代归因争议和纪年异说，超出 Skill 模型的简单反写；但“《晋书》本纪 = 一手”“辑本 = 近一手”等 taxonomy 过宽。先 PATCH taxonomy；若其他五维抽查未出现来源失实，则复用 research 重蒸馏。

### simayi-perspective

**Action: PATCH → REDISTILL-CANDIDATE.**

04 research 有痿疾构陷、复位异说、胡三省/王夫之/现代研究等独立层次；同时把唐修《晋书》史臣论断标为“一手/近一手”，并使用宽泛考古旁证。属于可修 evidence base，而非目前已有证据足以判定的 reverse-engineered research。

### simayu-perspective

**Action: PATCH → REDISTILL-CANDIDATE.**

04 research 保留“傀儡 vs 守成”“让国 vs 被迫”“清谈误国 vs 清谈系士”等张力，独立研究价值明显；主要风险是把《晋书》正文/《世说新语》笼统当一手，以及《淳化阁帖》等旁证的归属强度。先定向核验再重蒸馏。

### simazhong-perspective

**Action: PATCH → REDISTILL-CANDIDATE.**

04 research 有八王之乱制度解释、崩因异说、贾后评价张力等独立信息，不宜因 mtime 直接重搜；但同样存在“唐修《晋书》= 一手/近一手”、宽泛实物旁证等问题。先 PATCH evidence taxonomy。

## Batch finding

晋 7/7 个旧 mtime suspect **目前都没有足够证据支持“references 是从 Skill 倒推，因此必须全量 RERESEARCH”**。相反，抽查显示它们普遍具有独立研究层次；共同缺陷是 WorkBuddy 旧 brief 的 evidence taxonomy 太粗，把“正史/通行史籍”与“同期/本人一手”混在一起。

因此晋批次从旧的“倒序待重做”改为：**7 个进入 PATCH/REDISTILL recovery，0 个因 mtime 自动 RERESEARCH。** 每个包在真正改 Skill 前仍需对六维做 source-specific spot verification，避免把旧标签错误带入新 Skill。

## Remaining legacy snapshot

39 个旧信号中，晋 7 个已完成 recovery classification；剩余 32 个：南北朝 14、三国 2、商 13、夏 1、周 2。下一阶段按朝代批处理，而不是按文件大小排序。
