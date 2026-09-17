# Corpus QA & Work Queue · 自动化

> Generated from the current master candidate index and exact Skill coverage. It does not replace historical/source review or Nuwa semantic audit.

## Coverage state

- Candidate persons: **1312**
- Locked CORE: **913**
- Matched CORE: **303**
- Missing CORE: **610**
- Existing Skills accounted: **305 / 305**
- Unresolved existing Skills: **0**

## Identity QA

- Skill → multiple-person collisions: **0**
- Person → multiple-Skill matches: **0**
- Shared identity-hint collisions: **0**
- Suspicious canonical-name strings: **0**

## Generated queues

- `A_CORE_MAJOR_SEQUENCE_MISSING`: **34**
- `B_CORE_PARALLEL_POLITY_MISSING`: **173**
- `D_CORE_EARLY_OR_PREQIN_MISSING`: **403**
- `Q1_SCOPE_OR_IDENTITY_REVIEW`: **365**
- `Q2_EXTENDED_REVIEW`: **0**
- `Q3_LEGENDARY_LIMITED_EVIDENCE`: **0**
- `Q4_OTHER_REVIEW`: **0**

## Execution rule

Identity/scope blockers are resolved before IDs are frozen. Missing locked CORE can then enter **research → evidence synthesis → Nuwa distillation → audit**. REVIEW, EXTENDED and LEGENDARY do not silently enter the locked CORE denominator.

Machine-readable files: `data/corpus-work-queue.json` and `data/corpus-identity-issues.json`.
