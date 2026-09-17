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
| P3-B01 | 赵武灵王赵雍 (`ruler-1076`, 赵) | IN PROGRESS |
| P3-B01 | 魏文侯魏斯 (`ruler-1237`, 魏) | PLANNED |
