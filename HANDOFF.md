# HANDOFF.md —— 换台电脑 / 换个人怎么接上

## 1. 环境

- **Python 3.13**（只用标准库，无需 `pip install`）。
- 无环境变量依赖（脚本全部走命令行参数），故**没有 `.env` / `.env.example`**。
- 报告里的图表走 Chart.js CDN，离线看图需联网首次加载；其余完全离线。

clone 后直接跑，无需改代码：

```bash
git clone <repo-url> emperor-skill && cd emperor-skill
python simulation/_engine/check_solo.py            # 应输出 78/78 通过
python simulation/_engine/eval_solo_rank.py        # 重生成排名报告，数字应与已提交版本一致
```

## 2. 数据从哪来、长什么样

| 数据 | 位置 | 说明 |
|---|---|---|
| 推演数据 | `simulation/_engine/travelers/<key>.json` | 78 份，每份 `rows` 恰好 77 条（排除自身处境）。一条 = `[策, 分, 断语]`，分为 0–100 整数 |
| 处境全集 | `simulation/_engine/situations.json` | 78 条，含 `key / dyn / typ`（9 类困局受控词表） |
| 即位年表 | `simulation/_engine/reign_order.json` | `{key: [即位年, 同年次序]}`，**时间序排序的唯一依据** |
| 模块映射 | `simulation/_engine/modules_solo.json` | 94 个帝王包 → `module` / `group`，由 `build_module_map.py` 从各 SKILL.md frontmatter 抽取 |
| 报告产物 | `simulation/by-dynasty/solo/*.html` | 生成物，勿手改 |

产出物重建顺序：`build_module_map.py` → `eval_crossing_solo.py --all` → `eval_solo_rank.py`。

## 3. 当前卡在哪

**语料缺口**：`skills/` 里已有 **94** 个帝王包，但 `situations.json` 只有 78 条处境，
故 **东汉 13 帝 + 隋 3 帝（共 16 包）尚未进入 solo 推演**，排名报告里这两个模块标「尚未纳入」。

若补齐，矩阵从 78×77 扩到 **94×93 = 8742 条**，四步：

1. 扩 `situations.json`（+16 条处境，含 `typ` 归类）；
2. 扩 `reign_order.json`（东汉 25–220、隋 581–618）；
3. 78 份旧 `travelers/*.json` **各补 16 条**（且新增处境不能再含自身）；
4. 新增 16 份 travelers，**各 93 条**。

完成后重跑 `check_solo.py`（此时条数断言是 93，需同步改）与 `cross_check_solo.py`。

**下一步（按优先级）**：① 评分卡**去结局化**（补「机会利用度」维度，解决亡国危局档底部塌陷：78 人全压 39–51，组内不可分）→ ② `duel/` 与 `coop/` 引擎 → ③ `one-life/` 血量推进 → ④ `assessment/` 人格测验内容。

## 4. 已知坑（踩过，别再踩）

- ⚠️ **Python 源码字符串内的引号用全角「」**：ASCII 双引号会破坏语法。
- ⚠️ **Windows 传路径参数用 `D:/...`**：git-bash 的 `/d/...` 会被解析成 `D:\d\...`。
- ⚠️ **别在同一轮里对同一文件发多个并行编辑**：会互相覆盖，改完要 grep 复核。
- ⚠️ **预览过的 HTML 会被宿主注入 `data-page-node-id`**，造成 `git diff` 伪变更；重渲即清。
- ⚠️ **同一个词可能是两种口径**：「全库均分（合并）」（合并全部记录求平均，用于难度排行）与「人均极差」（各人均分之间的最高−最低，用于人定胜负）**不同源**，改口径后必须**逐节独立复算**（曾误把后者当「全库均分」写进表，差 0.1）。
- ⚠️ **改排序逻辑后要验证统计量复现**：只改排序时，逐项统计必须分毫不变 —— 先单份试渲比对基准值，再全量。
- ⚠️ **文件写盘后用独立脚本复算**，不要采信子代理口头回报的数字（曾出现回报值与实际落盘不一致）。

## 5. 相关文档

- [`README.md`](README.md) —— 这是什么、三大块结构
- [`AGENTS.md`](AGENTS.md) —— 给 AI 的硬约束与常用命令
- [`simulation/README.md`](simulation/README.md) —— 模拟场规范、引擎清单、效度检验结论
- [`CHANGELOG.md`](CHANGELOG.md) —— 版本叙事
