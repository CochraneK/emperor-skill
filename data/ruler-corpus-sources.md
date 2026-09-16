# Ruler Corpus source map

Construction evidence for `rulers-master.json`; this is **not** an individual-ruler Nuwa research file.

## Baseline chronology

Primary chronology skeleton: Taiwan Ministry of Education, *Revised Mandarin Chinese Dictionary*, **中國歷代紀年表 / Chronology of Chinese Dynasties**. It explicitly starts with the Huangdi tradition and states that regimes historically not regarded as orthodox (including the Sixteen Kingdoms and Ten Kingdoms) are still included for chronological consistency. Its chronology includes Huangdi, Shaohao, Zhuanxu, Diku, Dizhi, Yao, Shun, then Xia onward, and separately enumerates the Sixteen Kingdoms and Ten Kingdoms.

The companion **中國歷代帝王年表** supplies a ruler-by-ruler backbone from King Wu of Zhou through the Xuantong Emperor. The companion **中國歷代年號表** is a cross-check for post-Han reign episodes; it contains 521 era-name records and must not be mistaken for 521 persons.

These are authoritative chronology backbones, not the sole source of person inclusion.

## Why 朝代歌 alone is insufficient

Popular dynasty songs are memory skeletons. They systematically compress or omit parallel and defeated regimes, Spring-and-Autumn/Warring-States polities, rival governments, and legendary variants. Therefore the project takes the **maximum defensible union** of chronology/ruler traditions and then applies one common inclusion ontology.

## Maximal-set expansion policy

- Pre-Xia: keep named sovereign/culture-ruler traditions in a separate `LEGENDARY` layer. At minimum seed Fuxi, Nüwa, Shennong/Yandi, Huangdi, Shaohao, Zhuanxu, Diku, Dizhi, Yao, Shun; competing Three Sovereigns/Five Emperors lists are variants, not errors to erase.
- Xia/Shang: enumerate transmitted ruler sequences, but evidence strength remains independent of inclusion.
- Eastern Zhou: enumerate Zhou royal house **and polity-by-polity** Spring-and-Autumn/Warring-States rulers; do not sample only famous hegemons.
- Qin-Han transition: include qualifying rival supreme rulers such as Xiang Yu and competing restoration regimes when they meet the common rule.
- Sixteen Kingdoms and Northern/Southern Dynasties: preserve constituent and parallel polities separately; consider qualifying contemporaneous short regimes such as Ran Wei under the same rule rather than an orthodoxy rule.
- Sui-Tang transition / late Tang: qualifying autonomous rival regimes are candidates; Huang Chao's Great Qi is explicitly CORE.
- Five Dynasties/Ten Kingdoms: enumerate every constituent polity separately.
- Song/Liao/Xia/Jin: preserve parallel sovereign entities; long-lived autonomous polities such as Dali are candidates under the same ontology rather than excluded because they disappear from a short dynasty song.
- Yuan transition: candidate rival regimes are evaluated under the same actual-rule test.
- Ming-Qing transition: Southern Ming plus qualifying Dashun/Daxi and other actual autonomous supreme-rule regimes.
- Late Qing: Taiping Heavenly Kingdom qualifies; other rival regimes require the same evidence of autonomous rule rather than fame alone.
- Republic: use `person + rule_episode`. Qualifying competing central governments may coexist. Sun Yat-sen, Yuan Shikai, and Zhang Zuolin are explicit boundary anchors; ordinary regional warlord status alone is insufficient.

## Evidence/status orthogonality

`Included in master` does not mean `historically certain`, and `historically uncertain` does not mean `omit`.

- `CORE`: historically attested qualifying ruler.
- `EXTENDED`: analytically valuable/borderline sovereign or de-facto edge case.
- `LEGENDARY`: traditional ruler figure tracked without pretending historical certainty.
- `LIMITED-EVIDENCE`: an evidence state, not a reason to fabricate six mental models.

Traditional legitimacy is metadata, not a gate. `Emperor` is a title, not a gate. Defeat, short duration, parallel rule, non-Han identity, or later exclusion from orthodox historiography are not exclusion criteria.

## Exclusion discipline

Pure posthumous honors, unsupported claimants with no governing entity, ordinary regional warlords with no qualifying supreme-rule episode, and deities with no meaningful ruler tradition are excluded from CORE. Every exclusion from a source-derived candidate list must eventually carry an explicit reason in the machine-readable master.

## Enumeration QA

For every polity: obtain at least one polity-specific ruler sequence; cross-check chronology/aliases; distinguish actual rulers from posthumous/pretender entries; normalize duplicate identities; represent repeated offices and title changes as episodes; match existing skills; retain unresolved boundary cases instead of silently deciding them.

## Completion metrics

Never publish one misleading percentage. Report separately:

1. Historical CORE coverage.
2. CORE research-complete coverage.
3. CORE Nuwa-distilled coverage.
4. REDISTILL debt among existing skills.
5. EXTENDED coverage.
6. LEGENDARY/traditional coverage.
7. LIMITED-EVIDENCE count.

Only after person-by-person enumeration and alias normalization may the repository publish a final denominator and missing-person count.
