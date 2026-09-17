# Emperor Variable Analysis Roadmap

> Future downstream layer. **Do not interrupt the current corpus / distillation backbone work.** Build this after the stable person/reign/event foundation is sufficiently mature.

## Goal

Turn the emperor-skill corpus into an analyzable historical panel dataset without flattening uncertain history into fake precision.

The system should support two complementary representations:

1. **Perspective Skill layer** — evidence-grounded mental models, decision heuristics, voice, constraints, uncertainty.
2. **Feature / variable layer** — structured person, reign, event, network, environment and derived variables for statistics, visualization and simulation.

The variable layer must use stable `person_id` and never parse a Skill's prose as the only source of truth when structured evidence can be recorded directly.

## Unit of analysis

Do not force everything into one emperor-wide row. Use at least four linked tables:

- `person_features`: relatively stable person-level attributes.
- `reign_episode_features`: one person may have multiple reign/rule episodes; time-varying political variables live here.
- `events`: wars, coups, rebellions, reforms, disasters, succession crises, purges, famines, epidemics, etc.
- `relations`: ministers, siblings, spouses, heirs, regents, generals, factions and other person-person ties.

Every table joins through stable `person_id`; events and reigns need their own stable IDs.

## Variable families to support

### A. Basic life-course variables

Examples:

- birth year / date / place
- death year / date / place
- lifespan
- age at accession
- age at first independent rule
- reign length / effective-rule length
- number of reign episodes
- accession route: inheritance / coup / conquest / election / regency-to-rule / restoration / other
- exit route: natural death / deposition / abdication / execution / suicide / killed in war / disappearance / unknown
- cause-of-death confidence

### B. Family and succession variables

Examples:

- number of known full / half siblings
- birth order where recoverable
- number of sons / daughters / known children
- number of spouses / consorts recorded
- designated heirs count
- succession disputes experienced
- succession disputes generated at exit
- kin killed / exiled / purged during succession struggle
- parent predecessor relationship
- dynastic founder / restorer / usurper / short-reign successor flags

Raw counts must include `known_` or `recorded_` semantics when sources are incomplete; never imply total biological counts when only recorded persons are known.

### C. Court / elite-network variables

Examples:

- number of named senior ministers active in the reign
- number of high-impact ministers / generals meeting an explicit inclusion rule
- turnover of top officials
- purge / execution / exile counts
- faction count where a source-backed faction ontology exists
- minister network degree / betweenness / centralization
- ruler dependence on regent / eunuch / empress-dowager / military bloc / clan
- concentration of office-holding among kin or clans

`名臣数量` must never be a subjective fame count. Define a reproducible operational rule, e.g. office rank + duration + source coverage, and preserve alternative definitions.

### D. Crisis and political-environment variables

Examples:

- succession crisis count
- coup / attempted coup count
- rebellion count
- civil-war years
- foreign-war years
- invasion years
- capital-loss / flight events
- hostage / captivity episodes
- regency episodes
- fiscal crisis episodes
- famine / epidemic / flood / drought / earthquake / locust / extreme-cold events
- disaster count and severity
- territory gained/lost where defensibly estimable
- years with major internal crisis
- years with simultaneous crisis types

Counts should normally be exposure-adjusted, e.g. events per 10 reign-years, because a 40-year ruler mechanically has more opportunities for events than a 2-year ruler.

### E. Policy / institutional variables

Examples:

- major reforms count
- tax / land reform episodes
- examination / selection-system changes
- military-system changes
- administrative reorganization
- capital relocation
- legal-code revision
- currency / fiscal reform
- religious policy shifts
- censorship / information-control measures
- centralization / decentralization indicators

Prefer event-coded observations to a single retrospective score.

### F. Skill-derived behavioral / decision variables

Potential dimensions can be extracted from the evidence synthesis and Perspective Skills, but must remain versioned model outputs rather than objective facts. Examples:

- risk tolerance
- information openness
- delegation vs personal control
- punishment severity
- tolerance of dissent
- institutionalization tendency
- short-term vs long-term orientation
- legitimacy strategy
- military aggressiveness
- adaptive flexibility
- succession planning
- crisis response pattern

Each derived value should have:

- model/schema version
- evidence citations
- confidence / uncertainty
- coding method (human, rule, LLM, mixed)
- inter-rater / repeated-model agreement when feasible

Never collapse the Perspective Skill into one opaque personality score.

### G. Historical-context variables

Examples:

- dynasty / polity
- century / macro-period
- unified vs fragmented political environment
- predecessor regime type
- inherited territorial size band
- frontier pressure band
- contemporaneous rival-polity count
- economic / demographic proxy variables where reliable datasets exist
- information/source-density proxy

These variables are crucial controls: rulers from very different centuries are not IID observations.

### H. Calendar / cultural variables

Exploratory variables may include:

- zodiac animal (生肖)
- sexagenary year (干支年)
- birth lunar month/day if recoverable
- year/month/day pillars when the historical date is sufficiently secure
- full 八字 only when **birth year, month, day and hour** are genuinely evidenced and calendar conversion is defensible

Ancient birth hour is usually unavailable, so full 八字 should usually be `UNKNOWN`, not guessed. These variables may be used for exploratory/cultural analyses, but must be visually and analytically separated from evidence-based causal claims.

## Scores / 跑分

Scores are allowed, but every composite score must be transparent and versioned.

Store both:

- raw component variables;
- formula / weights / normalization version;
- final score;
- uncertainty / missingness.

Possible score families include crisis burden, succession stability, institutionalization, military expansion, information openness, evidence confidence, Skill distinctiveness, etc. No single “best emperor” score should become the canonical representation.

## Evidence and uncertainty schema

Every nontrivial variable should support:

- `value`
- `value_type`
- `source_ids`
- `source_span_or_note`
- `confidence`
- `coding_method`
- `coder_or_model_version`
- `observed_vs_inferred`
- `missing_reason`
- `temporal_scope`

Suggested confidence vocabulary: `HIGH / MEDIUM / LOW / CONTESTED / UNKNOWN`.

Missing is data. Distinguish at least:

- `UNKNOWN_NOT_RECORDED`
- `UNKNOWN_SOURCE_CONFLICT`
- `NOT_APPLICABLE`
- `NOT_YET_CODED`
- `STRUCTURALLY_UNOBSERVABLE`

Do not silently convert unknown to zero.

## Statistical analyses enabled later

Once coverage is adequate, the project can support:

- descriptive distributions and dynasty-by-dynasty visualization
- correlation matrices with uncertainty / missingness awareness
- clustering / latent profiles of ruling styles
- PCA / factor exploration for validated numeric dimensions
- multilevel models with rulers nested in dynasties / periods
- count models for rebellions, disasters, reforms, wars
- survival / event-history models for reign termination, deposition, dynasty survival
- sequence analysis of crisis → response → consequence
- network analysis of ministers, clans and factions
- matched comparisons between rulers facing similar crisis environments
- causal-inference-inspired designs only where assumptions and temporal ordering are defensible
- simulation parameters grounded in observed historical distributions

## Guardrails against bad statistics

1. **Exposure matters**: event counts must account for reign length and source density.
2. **Source survival bias**: later dynasties usually have denser records than early periods.
3. **Dynasty clustering**: rulers within one dynasty share institutions and are not independent samples.
4. **Post-treatment bias**: some “context” variables are themselves changed by the ruler.
5. **Outcome leakage**: do not code a behavioral trait from the later outcome and then use it to predict that same outcome.
6. **Fame bias**: “名臣”“大事件”“重大改革” need operational definitions, not modern popularity.
7. **Uncertain dates**: do not manufacture precision for zodiac / calendar / age calculations.
8. **Multiple reigns**: one person may require several reign episodes instead of one flattened row.
9. **Version everything**: feature schema, coding rules, derived scores and model outputs must be reproducible.

## Suggested implementation order

This roadmap is intentionally downstream of the current work:

1. Finish current P0 Qin→Qing backbone distillation and corpus identity/coverage integrity.
2. Freeze a `feature-schema-v1` with person/reign/event/relation tables.
3. Pilot 10–20 rulers across several periods to test variable definitions and source burden.
4. Build automatic extraction only for variables that can be reliably structured; keep contested variables reviewable.
5. Add feature QA + provenance + missingness checks.
6. Scale to the P0 backbone, then P1/P2/P3 corpus.
7. Add statistics, dashboards, cross-ruler comparison, clustering and simulation interfaces.

## Product direction

The long-term Emperor project should therefore become more than a Skill collection:

**Historical sources → provenance → person/reign/event graph → Perspective Skills → structured feature matrix → comparative statistics → simulation → visualization.**

This variable layer should eventually power Page views such as: dynasty timelines, ruler radar/profile cards, crisis heatmaps, network graphs, lifespan/reign distributions, event-rate comparisons, similarity maps, and interactive hypothesis exploration.
