# Canonical Ruler Corpus Scope · 帝王蒸馏全库口径

> Status: canonical scope v1.0
> Purpose: define **who should eventually have a research → distillation package**. This is broader than the current 267-package corpus and is intentionally separated from `data/corpus-registry.json`.

## 1. Construction rule: 朝代歌取最大集，而不是只取一首

Common dynasty mnemonics compress history differently. The canonical scope therefore uses the **union of major dynasty-song / chronology traditions**, then expands umbrella periods into their constituent regimes.

A minimal mnemonic often gives:

`夏 → 商 → 周 → 秦 → 汉 → 三国 → 两晋 → 南北朝 → 隋 → 唐 → 五代十国 → 宋 → 辽 → 夏 → 金 → 元 → 明 → 清`

For corpus construction this is insufficient because `汉`, `三国`, `两晋`, `南北朝`, `五代十国`, `宋` hide parallel or successor regimes, and many versions omit `新` and `十六国`. Our maximum-set canonical backbone is therefore:

`夏 → 商 → 西周 → 东周 → 秦 → 西汉 → 新 → 东汉 → 三国 → 西晋 → 东晋 / 十六国 → 南北朝 → 隋 → 唐（含武周作为统治序列） → 五代十国 → 北宋 / 南宋 → 辽 → 西夏 → 金 → 元 → 明 → 清`

This is a **corpus taxonomy**, not a claim that all listed regimes formed one linear orthodox succession.

## 2. Expanded regime set

### A. Three Dynasties / pre-imperial royal line
- Xia 夏
- Shang 商
- Western Zhou 西周
- Eastern Zhou 东周

### B. Qin–Han transition
- Qin 秦
- Western Han 西汉
- Xin 新
- Eastern Han 东汉

`楚汉` may remain as a project analytical grouping for the transition, but it is not a substitute for the canonical dynasty/regime registry. Xiang Yu and other non-emperor hegemonic rulers should be tagged separately if retained.

### C. Three Kingdoms
- Cao Wei 曹魏
- Shu Han 蜀汉
- Eastern Wu 孙吴

### D. Jin and Sixteen Kingdoms
- Western Jin 西晋
- Eastern Jin 东晋
- Cheng-Han 成汉
- Han-Zhao / Former Zhao 汉赵（前赵）
- Later Zhao 后赵
- Former Liang 前凉
- Former Yan 前燕
- Former Qin 前秦
- Later Qin 后秦
- Later Yan 后燕
- Western Qin 西秦
- Later Liang 后凉
- Southern Liang 南凉
- Southern Yan 南燕
- Western Liang 西凉
- Northern Liang 北凉
- Xia / Hu Xia 胡夏
- Northern Yan 北燕

`冉魏` is tracked as an **extended parallel regime** because it matters to the political sequence but is not one of the conventional “Sixteen”. Other short-lived parallel regimes can be represented in an extension layer rather than silently omitted.

### E. Northern and Southern Dynasties
South:
- Liu Song 刘宋
- Southern Qi 南齐
- Liang 梁
- Chen 陈

North:
- Northern Wei 北魏
- Eastern Wei 东魏
- Western Wei 西魏
- Northern Qi 北齐
- Northern Zhou 北周

### F. Sui–Tang
- Sui 隋
- Tang 唐
- Wu Zhou 武周 — represented explicitly in ruler metadata so Wu Zetian is not lost inside a Tang-only label

### G. Five Dynasties
- Later Liang 后梁
- Later Tang 后唐
- Later Jin 后晋
- Later Han 后汉
- Later Zhou 后周

### H. Ten Kingdoms
- Former Shu 前蜀
- Later Shu 后蜀
- Yang Wu 杨吴
- Southern Tang 南唐
- Wuyue 吴越
- Min 闽
- Ma Chu 马楚
- Southern Han 南汉
- Jingnan / Nanping 荆南（南平）
- Northern Han 北汉

### I. Song and contemporary major dynasties
- Northern Song 北宋
- Southern Song 南宋
- Liao 辽
- Western Xia 西夏
- Jin 金

### J. Yuan–Ming–Qing
- Yuan 元
- Ming 明
- Qing 清

## 3. Inclusion levels

The master ruler library uses explicit levels so “maximum set” does not become an uncontrolled list of every person who ever claimed a throne.

### CORE — must distill
Include every **actually enthroned / reigning sovereign** in the canonical regimes above, including:
- child rulers;
- deposed rulers;
- very short reigns;
- rulers known by posthumous titles rather than personal names;
- female sovereigns such as Wu Zetian;
- rulers whose historical evidence is sparse, provided the package is marked `LIMITED-EVIDENCE` when necessary.

Sparse evidence is **not** a reason to silently omit a ruler.

### EXTENDED — distill after CORE
Parallel regimes important to the political sequence but outside the conventional dynasty-song maximum set, e.g. Ran Wei, Huan Chu and selected transition regimes. These must be explicitly tagged `scope: extended`, never mixed invisibly into CORE.

### EXCLUDED BY DEFAULT
Do not automatically create emperor-perspective Skills for:
- purely posthumously elevated ancestors who never reigned;
- pretenders with no durable regime/control;
- rebel leaders merely because they briefly adopted an imperial title;
- mythic Three Sovereigns/Five Emperors before Xia;
- princes/regents who never became sovereign;
- modern heads of state.

They can enter separate analytical datasets later.

## 4. Evidence-era policy

Coverage and evidence confidence are separate dimensions.

- Xia: include canonical ruler sequence but normally mark `LIMITED-EVIDENCE`; transmitted texts and archaeology must not be represented as contemporary personal testimony.
- Shang: include canonical ruler sequence; oracle-bone/bronze evidence must be separated from later transmitted historiography and modern reconstruction.
- Zhou/pre-Qin: distinguish contemporaneous/near-contemporaneous inscriptions and transmitted texts from later histories.
- Imperial periods: standard histories are important transmitted evidence, but “正史” does not automatically mean “contemporary primary source”.

The goal is a complete ruler index with honest uncertainty, **not false symmetry of evidence quality across 4,000 years**.

## 5. Relationship to the current repository

`data/corpus-registry.json` answers: **what packages exist now?**

This scope document answers: **what rulers should eventually exist?**

The next canonical data artifact is `data/rulers-master.json`, one row/object per ruler with at least:

- `id`
- `canonical_name`
- `personal_name`
- `regime_id`
- `macro_period`
- `reign_start`
- `reign_end`
- `sequence`
- `scope` (`core` / `extended`)
- `evidence_class`
- `existing_skill_id` or `null`
- `distillation_status`
- `notes`

Then:

`rulers-master.json − corpus-registry = missing distillation queue`

No future README/Page should call the current 267 packages “the complete emperor library” until this set-difference is zero for CORE.

## 6. Canonical macro-period order for UI / visualization

For Page and analysis ordering use:

`三代 → 秦汉 → 三国 → 晋十六国 → 南北朝 → 隋唐 → 五代十国 → 宋辽夏金 → 元 → 明 → 清`

This avoids forcing overlapping regimes into a false single line while remaining readable as a historical timeline.
