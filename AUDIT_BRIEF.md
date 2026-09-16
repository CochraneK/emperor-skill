# emperor-skill — 外部审查交接说明

> 生成于 2026-09-17 · `HEAD = 417ffc1` · 与 GitHub 远端 `main` **逐字节一致**（已 push）
> **本文用途**：让外部审查者在不了解本项目历史的前提下，快速判断「哪些是核心资产、哪些是生成产物、
> 哪些是一次性流程残留、哪些可以直接删除」。审查结论可以推翻本文的任何分类。

---

## 一、项目是什么（30 秒版）

把中国历代帝王蒸馏成可运行的 **人物视角 Skill 包**（`-perspective`）。每位帝王一个包，包内固定 8 个文件：

| 文件 | 角色 | 说明 |
|---|---|---|
| `SKILL.md` | **产物** | 12 章结构：心智模型 / 决策启发式 / 表达DNA / 诚实边界 / 内在张力 等 |
| `references/research/01-writings.md` | **源** | 六维底稿之一：著作与文本 |
| `…/02-conversations.md` | 源 | 对话与言论 |
| `…/03-expression-dna.md` | 源 | 表达 DNA |
| `…/04-external-views.md` | 源 | 他者视角 |
| `…/05-decisions.md` | 源 | 决策与行事 |
| `…/06-timeline.md` | 源 | 时间线 |
| `scripts/quality_check.py` | 门禁 | 6 项自动质检 |

**核心口径（重要，审查时请据此判断内容是否合格）**：
1. **六维底稿是「源」，`SKILL.md` 是从六维蒸馏出的「产物」**——不允许先写 SKILL.md 再回填底稿。
2. 每份底稿 **≥2.5KB**，且末页必须含「排除声明」（声明未采用知乎／微信公众号／百度百科等来源）。
3. `SKILL.md` 中「诚实边界」四字全文**恰出现 1 次**；一手材料占比须 >50%。
4. 传说／半信史时期（夏、商）**不得伪称「一手确证」**；甲骨卜辞只证「有其人、在其祀典」，不证其事。

仓库另外两大块：

- **`simulation/`** — 帝王穿越模拟（2 容器 × 3 模式），含 Python 引擎**与已生成好的 HTML 产物**。
- **`assessment/`** — 人格测验模块，目前**只有空骨架**（3 个 `.gitkeep` + 1 个 README）。

---

## 二、文件盘点（已跟踪 **2431** 个文件 / 约 20 MB）

| 目录 | 文件数 | 大小 | 性质 | 可删性 |
|---|---:|---:|---|---|
| `skills/` | 2137 | 13.4 MB | **核心资产**（267 个帝王包 + 1 个散落报告文件） | ❌ 不可删 |
| `simulation/` | 193 | 6.7 MB | 引擎 40 个 + **生成产物 153 个** | ⚠️ 产物可重建 |
| `_redo_tools/` | 81 | 0.4 MB | 流程工具与清单 | ⚠️ 多为一次性 |
| `assessment/` | 4 | 4 KB | 空骨架 | ❓ 待决策 |
| 根目录 | 16 | 40 KB | 文档 + 流程草稿 | ⚠️ 草稿可清 |

`skills/` 分朝明细：`chuhan:2 donghan:13 jin:15 ming:16 nanbeichao:38 qin:3 qing:12 sanguo:11 shang:31 song:18 sui:3 tang:21 xia:17 xihan:15 yuan:15 zhou:37` ＋ 1 个非包目录（见下文 §5）。

---

## 三、逐目录说明

### 3.1 `skills/` — 核心资产（2137 文件 / 267 个 SKILL.md）

17 个朝代目录，每目录下若干 `<id>-perspective/` 包。包内结构统一，无冗余文件。
**除 `skills/_audit/` 外，全部不可删。**

### 3.2 `simulation/` — 引擎 + 产物

| 子目录 | 内容 | 说明 |
|---|---|---|
| `_engine/` | 40 个 `.py` + 数据 `.json` | **引擎与数据源**，不可删 |
| `by-dynasty/solo/` | **80 个 html / 5.7 MB** | **生成产物**，可由 `_engine/eval_*` 重建 |
| `one-life/` `by-dynasty/coop|duel/` | 6 个 `.gitkeep` | 空占位 |

> 判定参考：`simulation/by-dynasty/solo/solo-*.html` 全部为 ~74KB 的机器生成页；
> `solo-ranking.html`（142KB）与 `solo-index.html`（35KB）是排行与索引页。
> 若要缩减仓库体积，这是唯一有实际收益的地方（5.7 MB），但会使站点无法直接浏览。

### 3.3 `_redo_tools/` — 流程工具（81 个文件）

这是本项目为「批量补齐 267 个包的底稿」而累积的工作目录，**分类如下**（供审查者判断去留）：

| 分类 | 数量 | 典型文件 | 建议 |
|---|---:|---|---|
| ① 一次性提交脚本 | 5 | `_commit_yuan1.py` `_commit_push.py` | 🗑️ 可删（已执行完） |
| ② 一次性记忆写入脚本 | 6 | `_update_memory_bei1.py` | 🗑️ 可删（已执行完） |
| ③ 一次性站点登记脚本 | 12 | `_register_jin.py` `_register_yuan4.py` | 🗑️ 可删（操作的是**另一个仓库** `蒸馏skill` 的 `modules.json`，与本仓无关） |
| ④ 一次性暂存/检查脚本 | 3 | `_stage_bei3_partial.py` | 🗑️ 可删（已执行完） |
| ⑤ 复核/验收脚本 | 22 | `_verify_*.py` `_precommit_check.py` | ⚠️ 建议留 3–5 个通用的，其余可删 |
| ⑥ 全仓审计脚本 | 2 | `_audit_nuwa_all.py` | ✅ 留（可复用） |
| ⑦ 待办清单（数据） | 5 | `_todo_92.txt` `_todo92_tiers.txt` `_order_suspects_39.md` | ✅ 留（当前排期依据） |
| ⑧ 其他/常驻 | 26 | `quality_check.py` `_fix_decl.py` `_coverage.py` | ✅ 多数留 |

**关键文件（务必保留）**：
- `quality_check.py` — 官方 6 项质量门禁，每个包内都有一份副本，这里是母本。
- `_audit_nuwa_all.py` — 全仓合规体检脚本（复用官方门禁函数）。
- `_todo92_tiers.py` — 未达标包的工作量分档（A/B/C）。

### 3.4 根目录文件

| 文件 | 大小 | 性质 | 可删性 |
|---|---:|---|---|
| `README.md` | 5.7 KB | 项目说明 | ❌ |
| `AGENTS.md` | 4.5 KB | 给 AI 协作者的工作约定 | ⚠️ 审查者判断 |
| `NUWA_AUDIT_V2.md` | 9.9 KB | **验收正典**（合规判定标准） | ❌ |
| `CHANGELOG.md` / `HANDOFF.md` / `LICENSE.md` | 2.2/3.9/0.7 KB | 常规文档 | ❌ |
| `requirements.txt` | 616 B | Python 依赖 | ❌ |
| `_nuwa_brief.md` | 5.7 KB | **当前蒸馏简报**（规范来源） | ✅ 留 |
| `_nuwa_brief_later.md` | 9.2 KB | 后世帝王版本简报 | ✅ 留 |
| `_distill_prehan_brief.md` | 18.9 KB | **早期简报**，未设字数下限（是"底稿偏薄"的历史根因） | ⚠️ 留作证据 or 删 |
| `_distill_quality_check.py` | 4.2 KB | 早期质检脚本 | ⚠️ 已被 `_redo_tools/quality_check.py` 取代 |
| `_register_prehan.py` | 5.1 KB | 一次性登记脚本 | 🗑️ 可删 |
| `_fix_g5_honesty.py` | 1.4 KB | 一次性修补脚本 | 🗑️ 可删 |

---

## 四、**未同步到 git 的内容**（3 类，被 `.gitignore` 有意排除）

审查者若只通过 GitHub 查看，**看不到以下 57 个文件**：

| 类别 | 数量 | 大小 | 内容 | 说明 |
|---|---:|---:|---|---|
| `_redo_tools/*.txt` | 37 | 0.36 MB | 脚本中间输出（`_yearscan.txt` 109KB、`_dump_s1.txt` 88KB 等） | 可由 `.py` 重新生成 |
| `_pending/bei3/` | 19 | 0.12 MB | **北魏末 5 个残缺包**（详见下表） | 因 API 限流中断而暂存，**待重派补全，不是垃圾** |
| `.workbuddy/closeout-audit.json` | 1 | 7.4 KB | 收尾审计缓存 | 可重建 |

`_pending/bei3/` 明细（这 5 个包**都不完整**，缺什么一目了然）：

| 包名 | 缺什么 | 判断 |
|---|---|---|
| `yuanguan-perspective` | 六维底稿 01–06 齐全 + `quality_check.py`，**缺 `SKILL.md`** | 前半段完成，补 SKILL.md 即可 |
| `yuanlang-perspective` | 只有底稿 01–04，**缺 05、06 与 `SKILL.md`** | 需补 3 件 |
| `yuanxiu-perspective` | 只有底稿 01–03，**缺 04、05、06 与 `SKILL.md`** | 需补 4 件 |
| `yuanye-perspective` | **只有光杆 `SKILL.md`**，六维底稿全无 | ⚠️ **倒序残件**：按项目口径，其 SKILL.md 不得作为依据，须以六维为源重写 |
| `yuanzhao-perspective` | **只有光杆 `SKILL.md`**，六维底稿全无 | ⚠️ 同上（倒序残件） |

另有 **`.git.bak_rebase/`（28 文件 / 1.04 MB）**：一次 git 仓库损坏事故（`git pull --rebase` 删空
`.git/refs`）的修复备份，已在 `.gitignore` 内。**事故已完全修复、远端已校验一致，此备份可删。**

---

## 五、已知瑕疵 / 待清理项（请审查者裁定）

1. **`skills/_audit/skill-quality-report.html`（53 KB）散落在技能目录根下**
   它不是帝王包，是审计报告 HTML，落在 `skills/` 直系（不是任何朝代的子目录里）。
   建议移到仓库根或删除。除此之外，`skills/` 下 **267 个包全部齐备，无一缺 `SKILL.md`**（已实测）。

2. **`.gitignore` 与实际跟踪不一致**
   `.gitignore` 声明排除 `_redo_tools/*.txt`，但 `_todo_92.txt`（19 KB）与
   `_todo92_tiers.txt`（9 KB）**已被跟踪**（在规则加入前 add 的，git 不再对其生效）。
   若严格执行规则应 `git rm --cached`，但这两个是当前排期依据，建议保留并改规则为白名单。

3. **`_redo_tools/` 内 ~48 个一次性脚本**（见 §3.3 的 ①②③④）历史使命已完成，是仓库最主要的
   "无用信息"来源（约 130 KB）。

4. **`assessment/` 为空骨架**（只有 `.gitkeep`）——保留或删除待定。

5. **`skills/` 未覆盖所有朝代**：缺 新莽 / 十六国 / 五代十国 / 辽 / 西夏 / 金 / 北朝余部
   （约 60–160 位帝王）。这是**内容缺口，不是文件问题**。

---

## 六、给审查者的操作提示

- 仓库已全部 push，`git status` 干净，可直接 clone 审查。
- 若决定删除文件，建议**分类提交**（一次 commit 一类），便于回滚。
- 内容质量审查请以 §1 的四条口径为准；`NUWA_AUDIT_V2.md` 是完整验收标准。
- 本文件本身如被认为无用，可直接删除。
