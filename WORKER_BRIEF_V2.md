# Emperor Skill · Worker Brief v2

This brief implements `NUWA_AUDIT_V2.md` for future generation and repair work.

## Pipeline

`Sources → Research / References → Evidence synthesis → Mental-model distillation → SKILL.md → Audit`

Research must be independently useful evidence. Existing research may be reused for redistillation when it is independently researched; a new search is not required merely because an older Skill predates the current research files.

## Anti-Goodhart

There is no Nuwa minimum for words, characters, KB, paragraph count, keyword count, raw source count, **or mental-model count**. Thinness can be an audit signal, not an automatic failure. Padding to reach a size or model-count target is filler and should be cleaned.

The current eight-file package is an emperor-skill engineering profile, not proof of provenance.

## Evidence taxonomy

Do not collapse all canonical histories into “primary”. Record the useful distinction: contemporaneous/archaeological evidence; transmitted historical text; later historiography/commentary; modern scholarship; framework inference. For legendary and semi-historical periods, never turn later narration into contemporary confirmation.

## Distillation

Mental models must be person-specific, evidence-linked, transferable, bounded, and open to counter-evidence. Run the Genericity Test and Counter-evidence Test before accepting a model.

When evidence is sparse, prefer `LIMITED-EVIDENCE` over invented detail. **Six models are not a requirement.** A well-evidenced ruler may justify six or more distinct models; a child ruler, puppet ruler, ultra-short reign or poorly documented ruler may justify only one to three—or no personal mental model at all.

### LIMITED-EVIDENCE rule

Use a LIMITED-EVIDENCE package when personal agency, speech or decision evidence is too thin for a normal Perspective Skill.

Required behavior:

- distinguish the ruler's own actions from regents, empress dowagers, ministers, eunuchs, military patrons and other elite actors;
- never infer personality merely from holding the imperial title;
- do not convert “no surviving evidence” into a numeric zero;
- use explicit missingness such as `UNKNOWN_NOT_RECORDED`, `STRUCTURALLY_UNOBSERVABLE`, `NOT_OBSERVED`, or `CONTESTED`;
- allow **institutional-position / reign-episode models** when those are better evidenced than the person's psychology;
- state clearly when a model explains the ruler's political episode rather than the ruler's mind;
- keep a stable `person_id` and reign episode even when the person's psychological profile is mostly unknowable;
- never borrow decisions from a regency bloc merely to make the Skill feel complete.

A LIMITED-EVIDENCE Skill is a successful evidence-grounded result, not an incomplete normal Skill.

## Audit

Use L1 Provenance, L2 Evidence, L3 Semantic Distillation, and L4 Engineering from `NUWA_AUDIT_V2.md`. Static `quality_check.py` scripts are L4 helpers only. Repair with the minimum sufficient action: `KEEP`, `CLEAN`, `PATCH`, `REDISTILL`, `RESEARCH-GAP`, `RERESEARCH`, `REBUILD`, or `REVIEW`.

For LIMITED-EVIDENCE packages, L3 should reward **restraint and attribution correctness**, not model count or rhetorical richness. Hallucinated completeness is a more serious failure than an explicitly sparse profile.

Legacy `≥2.5KB` queues and mtime-only reverse-order verdicts are historical forensic signals, not current quality gates.
