# Skill Acceptance Gate v1

> Canonical corpus acceptance is **model-agnostic**. A Skill is accepted because it passes the same evidence and semantic standard, not because a preferred model produced it.

## 1. Status vocabulary

Every existing Skill must appear in `data/skill-acceptance-registry.json` with exactly one canonical acceptance status:

- `ACCEPTED` — explicit L1–L4 content-level attestation exists and the action is `KEEP`.
- `UNASSESSED` — no content-level acceptance attestation exists yet. Machine checks passing does **not** upgrade this status.
- `REVIEW` — evidence/provenance cannot yet support a repair decision.
- `PATCH` — research and core distillation are usable, but bounded corrections are required.
- `REDISTILL` — upstream research is reusable, but the Skill must be distilled again after any required targeted verification.
- `RERESEARCH` — the evidence base is missing/unreliable enough that research must be rebuilt before distillation.
- `REBUILD` — both research and Skill are seriously invalid.

`CLEAN` and `RESEARCH-GAP` remain Nuwa repair actions, but the registry normalizes them to `PATCH` and `RERESEARCH` respectively for queueing.

## 2. ACCEPTED is an explicit verdict

A package may become `ACCEPTED` only when an attestation records:

- L1 Provenance = `PASS`
- L2 Evidence = `PASS` or `LIMITED-EVIDENCE`
- L3 Semantic = `PASS`
- Genericity Test = `PASS`
- Counter-evidence Test = `PASS`
- L4 Engineering = `PASS`
- Action = `KEEP`

Static scripts, local `quality_check.py`, file count, source count, size, lexical similarity, CI green status, or a commit message such as “6/6” can only be machine signals. They are never sufficient acceptance evidence.

## 3. Attestation is append-only review evidence

Human/model reviewers add records to `data/skill-acceptance-attestations.json`. Each record identifies the Skill path, optional stable `person_id`, reviewer/model provenance when known, audit dimensions, action, date, and concise evidence note.

Model identity is diagnostic provenance only. It cannot raise or lower the acceptance verdict.

If a later audit supersedes an earlier one, add a new attestation with a later `reviewed_at`; do not rewrite history merely to make the current producer look better.

## 4. Existing legacy corpus

Legacy Skills are not invalid simply because old model provenance is unknown.

- The frozen 39-package provenance cohort keeps its already completed semantic triage.
- Until its recommended repair is explicitly attested complete and a full L1–L4 acceptance review is recorded, it is **not** `ACCEPTED`.
- All other legacy packages begin as `UNASSESSED`, not PASS and not FAIL.

This makes the system conservative without forcing blind full-corpus re-research.

## 5. Generator responsibility

`_redo_tools/_build_skill_acceptance_registry.py` produces:

- `data/skill-acceptance-registry.json` — one row per current Skill.
- `assessment/SKILL_ACCEPTANCE.md` — queue summary.

The generator may consume machine signals and historical triage, but it must never invent an L3 PASS.

## 6. Quality improvement loop

The production loop is:

`produce/repair → attest L1–L4 → ACCEPTED or repair queue → repair → re-attest`

Cross-model comparison is optional diagnostics. Corpus admission depends only on the canonical quality gate.
