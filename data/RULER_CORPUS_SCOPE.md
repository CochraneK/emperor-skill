# Canonical Ruler Corpus Scope · 中国历史统治者蒸馏全库口径

> Status: canonical scope v2.0
> Purpose: define **who should eventually have a research → distillation package**. The denominator is broader than a conventional emperor list and broader than the current 267 packages.

## 1. Canonical admission rule

The master corpus is a **Chinese Historical Rulers Corpus**, not merely an orthodox-dynasty emperor list.

A historical person enters `CORE` when the evidence supports all three conditions:
1. the person is treated as a historical person rather than a purely legendary culture hero;
2. the person was the highest sovereign decision-maker of a politically autonomous polity for a rule episode;
3. the polity had observable actual rule/control (territorial, administrative, military or equivalent), rather than only a posthumous title or unsupported throne claim.

Admission does **not** require:
- traditional orthodox recognition;
- the title 皇帝;
- nationwide unification;
- a long reign;
- later historiographical approval.

Therefore parallel sovereign polities are first-class data, not footnotes.

## 2. Person ≠ rule episode

The canonical entity is the **person**. Offices, reigns, titles and polities are represented as `rule_episode`s.

One person must not be duplicated merely because title or constitutional form changed. For example, Yuan Shikai is one person entity; a republican presidency and the Hongxian imperial episode can be encoded as separate episodes. Likewise aliases, temple names and posthumous names do not create duplicate people.

Every episode should encode orthogonal dimensions rather than one overloaded legitimacy label:
- `polity_id`
- `macro_period`
- `start` / `end`
- `title`
- `polity_type`
- `sovereignty_status`
- `control_scope`
- `recognition_status`
- `evidence_level`
- `inclusion_basis`
- `source_refs`

## 3. Scope tiers

### CORE — historical denominator
Every person with at least one qualifying actual-sovereign episode under §1. This includes child rulers, deposed rulers, short reigns, female sovereigns, non-orthodox rival rulers, and rulers with sparse evidence. Sparse evidence produces `LIMITED-EVIDENCE`; it does not justify invention or silent deletion.

### EXTENDED — analytical supplement, not denominator
Borderline actors worth retaining for comparison: regents exercising exceptional autonomous power, claimants whose actual sovereignty is uncertain, very short transitional entities with disputed control, or figures whose political entity falls near the admission boundary. Each requires an explicit reason.

### LEGENDARY — separate traditional-history layer
Pre-Xia culture heroes and legendary sovereign traditions are preserved because they matter to Chinese political memory and the user's maximum-set goal, but are **not counted as historical CORE** unless evidence warrants reclassification. This includes traditions around 盘古、女娲、伏羲、神农/炎帝、黄帝、少昊、颛顼、帝喾、尧、舜 and other tradition-dependent 三皇五帝 lists. Conflicting lists coexist; we do not fabricate a single false genealogy.

### OUT-OF-SCOPE
Purely posthumously elevated ancestors, claim-only pretenders with no demonstrated rule, fictional persons, and subordinate officials/warlords who did not constitute the highest sovereign authority of a qualifying autonomous polity.

## 4. Maximum-set historical backbone

A dynasty mnemonic is only a discovery seed. The corpus expands compressed umbrella periods and overlapping polities.

Historical work batches are:
- Xia, Shang, Western Zhou, Eastern Zhou royal house;
- **Spring-and-Autumn autonomous states**, enumerated by polity sequence rather than fame;
- **Warring States autonomous states**, including but not limited to the Seven Powers when another polity satisfies the same rule;
- Qin, Chu-Han transition, Western Han, Xin, Gengshi, Eastern Han;
- Three Kingdoms, Western/Eastern Jin, Sixteen Kingdoms and qualifying contemporaries;
- Northern/Southern Dynasties, Sui, Tang, Wu Zhou and qualifying Sui–Tang/late-Tang rival sovereign regimes;
- Five Dynasties, Ten Kingdoms and qualifying contemporaries;
- Song, Liao, Western Xia, Jin, Western Liao, Dali and qualifying parallel polities;
- Mongol/Yuan and qualifying late-Yuan rival regimes;
- Ming, Southern Ming, Later Jin/Qing, Dashun, Daxi and qualifying transition regimes;
- Qing and sustained late-Qing rival sovereign regimes such as Taiping;
- competing central-government rule episodes in the early Republic only where the same sovereignty test is met.

This taxonomy does **not** assert one linear orthodox succession.

## 5. Explicit boundary examples

These examples lock the rule so later workers do not revert to an emperor-title filter:
- 齐桓公、晋文公、楚庄王、秦穆公、越王勾践、魏文侯、齐威王、赵武灵王、燕昭王、秦孝公: eligible through autonomous-state rule, subject to systematic polity enumeration rather than fame selection.
- 黄巢: eligible because the Daqi episode involved an asserted sovereign regime plus observable territorial rule; the title alone is not the reason.
- 李自成: eligible through Dashun actual rule.
- 洪秀全: eligible through the sustained Taiping polity; 天王 rather than 皇帝 is irrelevant to admission.
- 袁世凯: one person entity; Hongxian is a distinct rule episode. Republican office alone does not imply that every later president enters this historical ruler corpus.
- 孙中山 and 张作霖 must be resolved through the same episode-level sovereignty test, not fame, ideology or title. Their inclusion/exclusion decision must carry explicit evidence and scope reasoning.

## 6. Evidence policy

Coverage and evidence confidence are independent dimensions.

- Legendary layer: preserve tradition variants; never present mythic chronology as established history.
- Xia: usually `LIMITED-EVIDENCE`; transmitted texts and archaeology are not contemporary personal testimony.
- Shang: distinguish oracle-bone/bronze evidence, transmitted historiography and modern reconstruction.
- Zhou/pre-Qin: distinguish inscriptions/near-contemporaneous evidence from later transmitted histories.
- Imperial and later periods: 正史 is important transmitted evidence but is not automatically contemporary primary evidence.

`LIMITED-EVIDENCE` means reduce claims and model count when necessary. It never means pad six generic mental models.

## 7. Master data model

`data/corpus-registry.json` answers **what Skill packages exist now**.

`data/rulers-master.json` answers **which historical persons are in the canonical ruler universe**.

`data/legendary-rulers.json` answers **which pre-Xia/traditional sovereign figures are preserved outside the historical denominator**.

The person schema should include:
- stable `id`
- `name_zh`
- `aliases`
- `historicity`
- `episodes[]`
- `scope_tier`
- `evidence_level`
- `existing_skill_ids[]`
- `distillation_status`
- `notes`

The episode schema should include the orthogonal fields in §2.

The future missing-work equation is person/entity based, not directory-count based:

`CORE persons − matched existing persons = missing research/distillation queue`

No README/Page should describe the current 267 packages as the complete ruler library until the CORE set difference is zero.

## 8. QA invariants

- no fame filter;
- no orthodoxy filter;
- no emperor-title filter;
- one person, one canonical ID;
- multiple offices/reigns = multiple episodes;
- posthumous title ≠ reign;
- evidence poverty ≠ exclusion;
- evidence poverty ≠ permission to invent;
- every borderline inclusion/exclusion has a reason;
- every polity sequence is enumerated systematically before individual selection;
- historical CORE, EXTENDED and LEGENDARY denominators are never silently mixed.

## 9. Visualization order

The UI must support overlapping timelines rather than force a false single line. Recommended macro lanes:

`传说层 → 三代 → 春秋列国 → 战国列国 → 秦汉 → 三国 → 晋十六国 → 南北朝 → 隋唐及并行政权 → 五代十国 → 宋辽夏金及并行政权 → 元及并行政权 → 明清及竞争政权 → 晚清/民初边界层`

Visualization should be polity-lane + person-episode based, enabling comparisons, simulation selection, evidence-confidence filters and alternative recognition views.