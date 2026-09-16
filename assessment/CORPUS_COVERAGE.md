# Corpus Coverage · 全库覆盖差距

Status: ACTIVE · 2026-09-17

## Current repository denominator

The repository currently contains **267** ruler Skill packages across 16 dynasty directories. This number is an inventory count only; it is not a claim of historical completeness.

Existing directory counts:

| directory | packages |
|---|---:|
| xia | 17 |
| shang | 31 |
| zhou | 37 |
| qin | 3 |
| chuhan | 2 |
| xihan | 15 |
| donghan | 13 |
| sanguo | 11 |
| jin | 15 |
| nanbeichao | 38 |
| sui | 3 |
| tang | 21 |
| song | 18 |
| yuan | 15 |
| ming | 16 |
| qing | 12 |

## Structural finding

The old directory taxonomy is narrower than the canonical v2 ruler ontology. In particular:

- `zhou:37` is a Zhou-royal-house sequence, **not** systematic Spring-and-Autumn/Warring-States polity coverage.
- there are no first-class directories for Xin, Sixteen Kingdoms, Five Dynasties/Ten Kingdoms, Liao, Western Xia, Jurchen Jin, Dali, Southern Ming, Dashun, Daxi, Taiping, or the early-Republic boundary layer;
- legendary/pre-Xia traditions are now tracked separately and must not inflate the historical CORE completion percentage;
- the current 267 therefore cannot be used as the denominator for “complete Chinese ruler corpus”.

## Early-period QA

### Xia
Current repository has 17 packages. Traditional ruler lists vary in whether 羿/寒浞 and other interruption traditions are treated as Xia sovereigns. The existing count must be identity-matched rather than assumed complete from count alone.

### Shang
Current repository has 31 packages. Traditional transmitted sequences and modern tables contain naming/sequence variants; a numerical mismatch is a QA trigger, not a reason to delete or invent a ruler. Each package must be mapped to a canonical person and variant tradition.

### Zhou
Current repository has 37 packages and inspection shows king-style package IDs (e.g. `aiwang`, `anwang`, `chengwang`, `daowang`, `dingwang`, etc.). This confirms the current Zhou set is royal-house oriented. The canonical corpus now separately enumerates autonomous Zhou-period states.

## Spring-and-Autumn / Warring-States expansion

A fame-based shortlist is prohibited. The build starts from polity sequences. The discovery registry now includes at minimum the major `史记·十二诸侯年表` lineages plus additional persistent autonomous states and Warring-States entities. Candidate inclusion is adjudicated by actual autonomous highest-rule episodes, not title or later orthodoxy.

This means figures such as 齐桓公、晋文公、楚庄王、秦穆公、越王勾践、魏文侯、齐威王、赵武灵王、燕昭王 and 秦孝公 are not special celebrity exceptions: they fall out of systematic polity enumeration.

## Rival/competitive polity rule

The same test applies in later fragmentation and rebellion periods. Daqi/Huang Chao, Dashun/Li Zicheng, Daxi/Zhang Xianzhong and Taiping/Hong Xiuquan are not admitted because they are famous rebels; they are candidates because they headed observable sovereign political entities. Pure throne claims without governing control remain outside historical CORE.

## Early-Republic boundary

The project must not drift into “all Chinese political leaders”. Modern-era entries require a supreme-rule episode of a central or competing-central polity under the common rule. A person can have multiple episodes without duplicate identities. Sun Yat-sen, Yuan Shikai and Zhang Zuolin therefore require episode-level mapping; ordinary regional warlord status alone is insufficient.

## Completion metrics

Do not publish a final percentage until person-level enumeration and matching are complete.

Future metrics:

1. `historical_core_total`: all canonical CORE persons.
2. `existing_matched`: CORE persons with an existing Skill package.
3. `missing_research`: CORE persons with no usable research package.
4. `needs_redistill`: matched persons whose evidence is reusable but Skill needs canonical redistillation.
5. `limited_evidence`: CORE persons retained with appropriately reduced claims.
6. `legendary_tracked`: separate traditional-history count, never merged into #1.

## Next machine-readable artifacts

- `data/RULER_CORPUS_SCOPE.md` — admission ontology.
- `data/polities-master.json` — polity discovery/normalization registry.
- `data/rulers-master.json` — canonical person + episode master.
- `data/legendary-rulers.json` — traditional/legendary layer.
- future `data/corpus-gap.json` — exact person-level set difference after enumeration.

The next work is **enumeration → identity normalization → existing-Skill matching**, before resuming bulk Nuwa redistillation.