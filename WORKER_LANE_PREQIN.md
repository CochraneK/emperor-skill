# Worker Lane · WorkBuddy P3 pre-Qin tranche

> Purpose: keep two workers (GPT-side and WorkBuddy-side) from editing the same packages.
> This file only **adds** a lane declaration. It does not modify canonical registry files,
> and it is not a quality standard — `NUWA_AUDIT_V2.md` remains the acceptance authority.

## Division of labour observed from git

| Worker | Current lane | Pool | Source of truth |
|---|---|---|---|
| GPT-side | **P1** balanced anchor tranche (post-Qin CORE, 24-person tranche) | `data/p1-anchor-priority.json` · `data/p1-anchor-reviews.json` | `assessment/P1_ANCHOR_PRIORITY.md` |
| WorkBuddy-side (this file) | **P3** early / pre-Qin CORE | queue `D_CORE_EARLY_OR_PREQIN_MISSING` in `data/corpus-work-queue.json` (404 persons, all from `data/rulers-master-h2-preqin.json`) | this file + `data/work-lane-claims.json` |

WorkBuddy deliberately **avoids** the P1 review sequence and the post-Qin CORE pool
(`A_CORE_MAJOR_SEQUENCE_MISSING`, `B_CORE_PARALLEL_POLITY_MISSING`, and the 207-person
P1 candidate pool), because that is the lane the GPT-side worker is actively pushing to.

## Rules this lane follows

1. **Canonical pipeline only** — `Sources → Research / References → Evidence synthesis → SKILL.md → Audit`.
   No reverse-engineering references from a finished SKILL.md.
2. **Nuwa quality standard** — `NUWA_AUDIT_V2.md` L1–L4 plus `WORKER_BRIEF_V2.md`.
   Sparse pre-Qin rulers are legitimate `LIMITED-EVIDENCE` packages; they are **not** padded to six models.
3. **Evidence gradient is recorded, not smoothed** — for pre-Qin vassal rulers most surviving
   material is transmitted text (《左传》《国语》《史记》《战国策》《资治通鉴》), much of it compiled
   centuries later, plus scattered archaeological evidence. Later historiography is never
   promoted to contemporaneous confirmation.
4. **Small batches, pushed immediately** — one batch = 1–3 persons. Each batch is committed
   and pushed as soon as its own `quality_check.py` passes, so a mid-run failure never
   strands a large amount of unpushed work.
5. **Never hand-edit generated files** — `data/*.json`, `assessment/CORPUS_*.md`,
   `assessment/DISTILLATION_PRIORITY.md`, `assessment/P1_ANCHOR_PRIORITY.md` are rebuilt by
   the `Corpus Sync` workflow. This lane only adds `skills/**` packages (plus this lane file
   and `data/work-lane-claims.json`, which are additive claim records).
6. **Collision rule** — if a package already exists, or the person has since entered the GPT-side
   P1 tranche, the claim is abandoned rather than overwritten.

## Package placement

- Path: `skills/<dynasty-dir>/<slug>-perspective/`, discovered by the corpus builder via
  `skills/*/*/SKILL.md`.
- Pre-Qin vassal rulers currently use `skills/zhou/` with `module: zhou-emperors`, because
  no dynasty directory is registered for Spring-and-Autumn / Warring-States vassal polities
  (`DIR_POLITY_HINTS` in `_redo_tools/_build_ruler_corpus.py` covers Zhou royal house only).
- `cn:` in frontmatter must equal the registry `canonical_name` exactly (for example
  `赵武灵王赵雍`, `魏文侯魏斯`), so the skill maps to the right `person_id` without heuristics.

## Batch log

| Batch | Persons | Status |
|---|---|---|
| P3-B01 | 赵武灵王赵雍 (`ruler-1076`, 赵) | DONE · 6/6 · `skills/zhou/zhaowulingwang-perspective` |
| P3-B01 | 魏文侯魏斯 (`ruler-1237`, 魏) | DONE · 6/6 · `skills/zhou/weiwenhou-perspective` |
| P3-B02 | 勾践 (`ruler-0129`, 越)、夫差 (`ruler-0216`, 吴) | DONE · 6/6 · `skills/zhou/goujian-perspective` · `skills/zhou/fuchai-perspective` |
| P3-B03 | 阖闾 (`ruler-1147`, 吴)、允常 (`ruler-0030`, 越) | NOMINATED |

### P3-B01 交付记录

- 赵雍：`Limited/Rich` 混合证据。核心反证已纳入——洛阳金村错金银狩猎纹镜（约前6–5世纪）显示中原骑兵与鹖冠早于赵雍，故「骑兵始祖」判为后世加誉，写入诚实边界；梁启超「黄帝以后第一伟人」标为近代史论并附语境；沙丘三月无临终言语，`UNKNOWN_NOT_RECORDED`，禁止代拟。
- 魏斯：归因分离处理——尽地力、平籴、《法经》归李悝之学，魏文侯只取「采纳与授权」；元年纪年、《法经》真伪写入存疑；三家分晋的合法性缺口（前403册命为既成事实的追认）写入诚实边界；与子夏无问答实录，`NOT_OBSERVED`。

### P3-B02 交付记录

- 勾践：`MODERATE-EVIDENCE` 混合证据。核心反证已纳入——「卧薪」不见于《左传》《国语》《史记》，标为后世增益；「尝粪诊病」仅见《吴越春秋》，标 `LEGENDARY_OR_INFERRED`，禁止当可信史实演绎；史载其言均标【史载言】。六模型：以耻为资、代际投资（十年生聚十年教训）、卑辞用间（贿伯嚭）、专业分权（范蠡/文种/计然）、伺隙而动（黄池袭虚）、盛极知退（范蠡退 vs 逼种死反面）。与夫差在智识谱系互引为 counter-evidence。
- 夫差：`MODERATE-EVIDENCE`。六模型即其五步败局——复仇立国（完成即空转）、北进忘后（黄池忘侧后之越）、近谗远忠（赐子胥剑、用伯嚭）、骄盈争礼（黄池争先歃）、败而方悟（蒙面「无面见子胥」，标戏剧性存疑），外加 counter-evidence 模型（夫差之败 = 勾践之胜的镜像）。与勾践成对蒸馏，互为反证。本 Skill 强在反面预警，正面模型须回 `goujian-perspective` 取。

### 下一批提名（P3-B02 → P3-B03）

勾践与夫差同属吴越争霸一组，史料以《左传》《国语》《史记·越王勾践世家》为主，成篇晚于事件但叙事互证度高；两人互为 counter-evidence（同一组事件的两端），适合成对蒸馏，本批已完成。

P3-B03 提名**阖闾 (`ruler-1147`, 吴) 与允常 (`ruler-0030`, 越)**——即夫差之父与勾践之父，补全吴越四人弧（父辈→子辈）。阖闾以檇李伤卒、初开吴之强、用伍子胥入郢；允常以与吴结怨之始、勾践嗣位背景。史料浓度低于子辈（吴王诸樊/余祭/僚/阖闾世系、《国语·吴语》片段；越王允常仅《史记》数语），须按 `LIMITED`/`PARTIAL-EVIDENCE` 处理，宁可显式标注缺失，不代拟。仍走 pre-Qin lane，不改 post-Qin P1/P2 池。若改走十国/十六国方向，须先确认 GPT 侧是否已离开 post-Qin P1/P2 池。
