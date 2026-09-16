# Ruler Corpus source map

Construction evidence for `rulers-master.json`; not an individual-ruler Nuwa research file.

## Baseline sources

### Taiwan Ministry of Education — 中国历代纪年表
Use as the high-authority polity/time skeleton. It begins its traditional chronology with 黄帝、少昊、颛顼、帝喾、帝挚、尧、舜 and explicitly includes historically non-orthodox regimes such as the Sixteen Kingdoms and Ten Kingdoms for chronological consistency. The traditional dates in the pre-Xia section are **not** treated here as modern historical proof.

### Taiwan Ministry of Education — 中国历代帝王年表
Use as a ruler-by-ruler baseline/cross-check from Western Zhou through Qing. The table contains repeated reign episodes (for example restored rulers/regencies in some periods), so its row count must never be treated as a unique-person count. It also does not solve Spring-and-Autumn/Warring-States parallel-state coverage by itself.

### China Biographical Database (CBDB)
Use where covered for person identity/alias normalization and cross-reference. CBDB's own documentation reports a substantial emperor authority dataset, but CBDB is a person database rather than the project's canonical ruler-inclusion ontology; it is therefore a cross-check, not the sole denominator.

### Transmitted chronological tables and polity-specific scholarship
For Eastern Zhou parallel states and other fragmented periods, use polity-specific ruler sequences and transmitted chronological tables (e.g. the tradition represented by the *Shiji* chronological tables) with modern scholarship for chronology/identity disputes. Discovery lists may suggest candidates but do not establish CORE status by themselves.

## Why 朝代歌 alone is insufficient
Popular dynasty songs are recall skeletons but compress parallel regimes. The project therefore takes the maximum defensible union of chronology traditions, then applies one ruler inclusion rule.

## Legendary layer
Maximum-set completeness includes named traditional ruler figures before Xia, but `LEGENDARY` is a separate denominator from historical `CORE`. A legendary persona represents the **transmitted cultural model of the figure**, not a verified psychological reconstruction of a historical individual. Conflicting 三皇/五帝 and earlier ruler sequences are stored as tradition variants rather than forcibly harmonized. No legendary date is promoted to historical fact merely because a chronology table prints it.

## Mandatory expansions
- 东周: 周王室 + qualifying Spring-and-Autumn/Warring-States sovereigns, enumerated by polity rather than fame.
- 十六国: constituent polities separately; qualifying contemporaries are evaluated under the same rule.
- 南北朝 and 宋辽夏金: preserve parallel sovereign entities.
- 五代十国: five dynasties and ten kingdoms separately.
- 隋唐、唐末、元末: sustained rival sovereign regimes are evaluated consistently rather than omitted because they lost.
- 明清鼎革: Southern Ming plus qualifying Dashun/Daxi and other actual-rule cases.
- Late Qing: Taiping Heavenly Kingdom qualifies under the same actual-polity rule.
- Republic: person + rule_episode; qualifying competing central governments can coexist. Ordinary regional warlord status alone does not qualify.

## Invariants
Traditional legitimacy is metadata, not a gate. `emperor` is a title, not a gate. Sparse evidence means `LIMITED-EVIDENCE`, never invented mental models. Pure posthumous honors, unsupported claimants, and ordinary regional warlords do not enter CORE merely because a title exists. Borderline cases go to EXTENDED with a reason.

## Enumeration QA
For each polity: obtain a polity-specific ruler sequence; distinguish actual rulers from posthumous/pretender entries; normalize aliases; represent repeated offices as episodes; distinguish sovereigns from regents; match existing skills; record unresolved boundary cases instead of silently deciding them. The build matrix lives in `data/corpus-build-plan.json`.
