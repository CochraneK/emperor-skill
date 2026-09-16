# Canonical corpus gap baseline

Status: **ACTIVE — enumeration before mass distillation**

The repository currently contains **267 Skill packages across 16 dynasty directories**. This is an implementation snapshot, **not** the canonical denominator.

## Confirmed structural gaps

The current top-level Skill taxonomy has no dedicated directories for the Spring-and-Autumn state rulers, Warring-States parallel states, Xin, the Sixteen Kingdoms as a complete polity set, Five Dynasties and Ten Kingdoms, Liao, Western Xia, Jurchen Jin, Western Liao, Dali, late-Tang rival sovereign regimes, Yuan-transition rival regimes, Southern Ming as a distinct lineage, Dashun, Daxi, Taiping Heavenly Kingdom, or Republican competing central governments. These must be resolved against the canonical master before any claim of corpus completeness.

## Early-batch reconciliation

- Xia: canonical transmitted sequence currently enumerates 17; registry has 17. Identity matching still required.
- Shang: current enumeration has 30 reigning entries while registry has 31 Skill packages. **Do not force-match.** Investigate the extra package/variant (likely a succession-tradition issue) before final denominator.
- Zhou royal house: current enumeration has 37 kings and registry has 37 packages. This does **not** cover Spring-and-Autumn/Warring-States parallel rulers.

## Completion formula

`historical CORE coverage = matched canonical historical persons / all canonical historical CORE persons`

`legendary coverage` is reported separately and never inflates historical completion.

A person with multiple rule episodes is counted once as a person. Episodes remain separately queryable for simulation and visualization.

## Stop conditions before new bulk Nuwa distillation

1. Enumerate polity/ruler universe.
2. Normalize person identities and aliases.
3. Classify CORE / EXTENDED / LEGENDARY and evidence level.
4. Match existing 267 packages.
5. Produce exact missing-person queue.
6. Only then research/distill missing persons and repair existing packages.
