# Ruler Corpus source map

Construction evidence for `rulers-master.json`; not an individual-ruler Nuwa research file.

## Baseline
Taiwan Ministry of Education, *Revised Mandarin Chinese Dictionary*, 中国历代纪年表 / Chronology of Chinese Dynasties: explicitly includes historically non-orthodox regimes such as the Sixteen Kingdoms and Ten Kingdoms for chronological consistency. Use as a high-authority polity/time skeleton, not as the sole person list.

## Why 朝代歌 alone is insufficient
Popular dynasty songs are recall skeletons but compress parallel regimes. The project therefore takes the maximum defensible union of chronology traditions, then applies one ruler inclusion rule.

## Mandatory expansions
- 东周: 周王室 + qualifying Spring-and-Autumn/Warring-States sovereigns.
- 十六国: constituent polities separately.
- 南北朝 and 宋辽夏金: preserve parallel sovereign entities.
- 五代十国: five dynasties and ten kingdoms separately.
- 明清鼎革: Southern Ming plus qualifying Dashun/Daxi.
- Late Qing: Taiping Heavenly Kingdom qualifies.
- Republic: person + rule_episode; qualifying competing central governments can coexist.

## Invariants
Traditional legitimacy is metadata, not a gate. `emperor` is a title, not a gate. Sparse evidence means `LIMITED-EVIDENCE`, never invented mental models. Pure posthumous honors, unsupported claimants, and ordinary regional warlords do not enter CORE merely because a title exists. Borderline cases go to EXTENDED with a reason.

## Enumeration QA
For each polity: obtain a polity-specific ruler sequence; distinguish actual rulers from posthumous/pretender entries; normalize aliases; represent repeated offices as episodes; match existing skills; record unresolved boundary cases instead of silently deciding them.
