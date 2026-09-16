# Provenance Recovery · Nuwa Audit v2

> `_redo_tools/_order_suspects_39.md` is a forensic snapshot, not a failure list. mtime triggers REVIEW only.

## Rule
Research that independently contains evidence, disagreements, limitations, and material not copied from the Skill can be reused. Use the minimum sufficient repair: KEEP / CLEAN / PATCH / REDISTILL / RESEARCH-GAP / RERESEARCH / REBUILD / REVIEW.

## Completed snapshot review · 39/39

The historical mtime queue has now been semantically triaged in full. **No package is assigned RERESEARCH merely because its Skill mtime preceded later research mtimes.** Across the queue, the dominant pattern is reusable research with evidence-taxonomy drift and some claims requiring source-level verification. Therefore the default recovery action is **PATCH / TARGETED VERIFY → REDISTILL**, not blind full research reruns.

### Jin · 7/7
All seven (`simadewen`, `simadezong`, `simashao`, `simaye`, `simayi`, `simayu`, `simazhong`) are research-reusable. Common issues: transmitted histories flattened into “primary”, over-strong psychological inference, and some quotation/source checks. Action: PATCH / VERIFY → REDISTILL.

### Sanguo · 2/2
`caohuan`, `caomao`: independent historiography and variant accounts are present. Action: PATCH → REDISTILL.

### Nanbeichao · 14/14
`chenxuan`, `liushao`, `liuyilong`, `liuyu-ming`, `tuobajun`, `tuobasi`, `tuobatao`, `xiaodong`, `xiaofangzhi`, `xiaogang`, `xiaoyan`, `xiaozhaoye`, `yuanhong`, `yuanziyou`: all show independent layers such as competing explanations, archaeology/material evidence, literary reception, chronology correction or explicit uncertainty. Common repairs: later histories/commentaries are not contemporary primary evidence; reconstructed quotations and inferred motives need verification; material evidence must be separated from interpretation. Action: PATCH / TARGETED VERIFY → REDISTILL.

### Shang · 13/13
All thirteen are research-reusable, but the early-history evidence ontology needs especially careful normalization.

- `diyi`: oracle-bone periodization, `帝乙归妹`, bronze evidence and Renfang debate are independent; patch `Shiji`/received `Zhouyi` labels and verify vessel claims.
- `hedanja`: strong source criticism across received histories, Bamboo Annals, oracle-bone naming, succession and site debates; separate inscriptions from modern scholarship.
- `kangding`: good `甲骨/一手` vs `考订/学界` distinction and explicit exclusion of unsupported internet stories; patch received-text labels and verify catalogue readings.
- `linxin`: rich debate over Zhouji absence, name variants and succession theories; separate Chen Mengjia/Guo Moruo/Dong Zuobin interpretation from inscription evidence.
- `taiding-shang`: excellent negative-evidence discipline; patch later texts/commentaries and verify reconstructed Zhouji placement.
- `taigeng`: strong genealogy/ritual-order criticism; verify `合集36218` reading and remove received histories from the primary bucket.
- `tang-shang`: strong separation of oracle/bronze, ritual memory, later reinterpretation and archaeology; verify Shuyi-bell wording and do not map Erlitou→Erligang directly onto named people/events.
- `waibing`: exceptionally rich competing traditions on whether he reigned, reign length and ritual order. Reusable; patch `Shiji/Mencius/Shangshu` blanket primary labels, distinguish Zhouji inscriptions from modern reconstruction, and keep the “ritual order ≠ accession order” limitation.
- `woding`: independent lost-text, Yi Yin, Zhouji-absence, candidate-inscription and chronology analysis; patch received-history labels and verify candidate `羌丁` claims.
- `xiaojia-shang`: strong ambiguity analysis around the subject of “殷道衰”, genealogy conflicts, chronology variance and ritual-order debate. Reusable; patch received texts/modern reconstructions mislabeled primary and verify specific catalogue/table claims.
- `zhongren-shang`: independent conflict between received traditions, Zhouji absence, modern methodological caution and “absence cannot prove nonexistence”. Reusable; patch the primary taxonomy and verify exact quotations/page-level attributions before redistillation.
- `zujia`: unusually strong contradictory reception history (`无逸` praise vs `国语/史记` blame), Zhouji/reform debate and explicit limits of oracle evidence. Reusable; patch the anachronistic primary labels for later texts and keep reform claims as scholarship/inference, not oracle fact.
- `zuxin`: strong “textual silence vs ritual visibility” model, inscription catalogue evidence, site uncertainty and explicit rejection of fabricated oracle quotations. Reusable; patch received-history labels and verify `合集32385` reading/ritual-status inference.

### Xia · 1/1
`shaojang`: **PATCH + TARGETED VERIFY → REDISTILL.** The package correctly declares Xia semi-historical and no contemporary textual self-evidence, preserves multiple early received traditions and explicitly limits archaeological mapping to the individual. The main taxonomy problem is calling Spring-and-Autumn/Warring-States/Han texts “一手” for a Xia ruler; they are early textual witnesses, not contemporary evidence. Erlitou/Xinzhai/Wangchenggang are archaeological contexts, not “史料原文/一手” for Shao Kang. Keep the uncertainty boundary and verify quotations/chronology claims.

### Zhou · 2/2
- `daowang`: **PATCH + TARGETED VERIFY → REDISTILL.** `Zuo Zhuan` is an important early textual witness, but `Shiji`, Du Yu/Yang Bojun and especially `Zizhi Tongjian` are not all “一手/近手”. The research still contains independent succession-conflict and institutional context, so it is reusable.
- `huiwang`: **PATCH + TARGETED VERIFY → REDISTILL.** Strong chronology comparison and explicit uncertainty are positive signals. Patch `Shiji` and `Zizhi Tongjian` as primary/compiled-primary, distinguish commentary from source text, and verify chronology discrepancies before redistillation.

## Final recovery count for the frozen mtime snapshot

- Classified: **39 / 39**
- Remaining: **0**
- RERESEARCH justified by mtime alone: **0**
- Dominant action: **PATCH / TARGETED VERIFY → REDISTILL**
- Historical 92-item size queue: **deprecated as a quality gate**

## Next phase
The mtime snapshot is now closed as a triage task. Next work is not more classification: patch evidence ontology and high-risk claims, then redistill Skills from corrected research. The wider 267-package corpus still requires L1–L3 screening; the 39-package result must not be generalized into an automatic PASS for the other packages.
