# AGENTS.md —— 给 AI 与接手者的约束入口

> 只写「必须知道的」。细节看 `README.md`，交接事项看 `HANDOFF.md`。

## 定位

把中国历代帝王蒸馏为 `-perspective` Skill，并在其上跑**穿越模拟场**与**人格测验**。
本仓库是独立分发的成品仓，**不含**蒸馏主项目（nuwa-skill）的人物/角色库。

## 技术栈

- **纯 Python 3.13 标准库**（无第三方依赖，故无 `pip install` 步骤）。见 `requirements.txt`。
- 报告是**单文件离线 HTML**（内联 CSS/JS，图表走 Chart.js CDN）。

## 常用命令

```bash
python simulation/_engine/check_solo.py                 # 单份推演结构质检（条数=77、分数 0–100 等）
python simulation/_engine/check_solo.py --strict        # 有问题即以退出码 1 结束
python simulation/_engine/cross_check_solo.py           # 全库交叉检验（越界 / 极差 / 分布 / 口径）
python simulation/_engine/eval_crossing_solo.py --all   # 全量重渲 78 份报告 + 总目录
python simulation/_engine/eval_solo_rank.py             # 重生成总排名报告 solo-ranking.html
python simulation/_engine/build_module_map.py           # 重生成 modules_solo.json（模块映射）
python skills/<朝代>/<id>-perspective/scripts/quality_check.py   # 单个帝王包的质量门禁
```

> `python` 不在 PATH 时，用本机 Python 3.13 的绝对路径替换；**不要**把绝对路径写进脚本或文档。

## 目录约定

| 路径 | 放什么 |
|---|---|
| `skills/<朝代>/<id>-perspective/` | 帝王包：`SKILL.md` + `references/research/` + `scripts/quality_check.py` |
| `simulation/_engine/` | 引擎脚本、`travelers/<key>.json`（推演数据）、处境与年表 JSON |
| `simulation/<容器>/<模式>/` | **渲染产物**（HTML），由引擎脚本生成，不手改 |
| `assessment/` | 人格测验（引擎 / 原型 / 样例报告） |

## 硬约束

1. **产物（HTML）是生成的**：改内容要改生成器再重渲，不要直接编辑 HTML。
2. **推演数据一人一份**：`simulation/_engine/travelers/<key>.json`，每条处境一条记录，恰好 77 条（排除自己）。
3. **改动后必过门禁**：跑 `check_solo.py`（结构）与 `cross_check_solo.py`（口径），数字要能复现。
4. **排序口径不可想当然**：报告一律**按时间顺序**（朝代先后 → 即位年 → 同年次序），依据 `_engine/reign_order.json`；「总分」与「均分」同序，「全库均分（合并）」与「人均极差」不同源。
5. **不引入第三方依赖**；确实需要时先讨论。
6. **不做未经确认的删除或大重构**；历史交给 git。

## 当前状态（2026-09-13）

- `skills/`：**94 个帝王包**（东汉 13 / 隋 3 / 唐 21 / 宋 18 / 元 11 / 明 16 / 清 12），audit 全 6/6。
- `simulation/by-dynasty/solo/`：**78 帝 solo 全量完成**（6006 条处置）+ 总目录 + 总排名报告。
- **语料缺口**：`situations.json` 仍只有 78 条处境，东汉 + 隋共 16 位帝王包**尚未纳入** solo 推演。
- **未建**：`duel/` `coop/` 引擎、`one-life/` 血量推进、`assessment/` 内容。
