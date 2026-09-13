# -*- coding: utf-8 -*-
"""「帝王遍历」评分器：把结构指标折算为四维得分（满分 100）。
说明：史实准确度/迁移能力属判断性指标，此处用可复现的结构代理量近似；
最终解释由「遍历者李世民」的定性评语补充。"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "eval_metrics.json"), encoding="utf-8"))


def c(x, a, b):
    return max(a, min(b, x))


def score(r):
    # 角色保真 30：规则10 + DNA8 + 第一人称密度6 + 零污染6
    faithfulness = 10 + c(r["dna"], 0, 7) / 7 * 8 + c(r["zhen"], 0, 30) / 30 * 6 + 6
    # 史识可靠 30：一手占比12 + 来源条数8 + 引证密度6 + 诚实边界4
    reliability = (c(r["ratio"], 0, 1) * 12 + c(r["one"] + r["two"], 0, 15) / 15 * 8
                   + c(r["cites"], 0, 30) / 30 * 6 + c(r["hb"], 0, 7) / 7 * 4)
    # 思维可用 25：模型10 + 启发8 + 张力4 + 篇幅3
    thinking = (c(r["models"], 0, 7) / 7 * 10 + c(r["heur"], 0, 8) / 8 * 8
                + c(r["tens"] - 5, 0, 4) / 4 * 4 + c((r["chars"] - 6000) / 4000, 0, 1) * 3)
    # 遍历适应 15：模型丰富度7 + 引证厚度5 + 篇幅3（迁移素材代理量）
    transfer = (c((r["models"] - 4) / 3, 0, 1) * 7 + c((r["cites"] - 15) / 15, 0, 1) * 5
                + c((r["chars"] - 6000) / 4000, 0, 1) * 3)
    total = faithfulness + reliability + thinking + transfer
    return dict(faithfulness=round(faithfulness, 1), reliability=round(reliability, 1),
                thinking=round(thinking, 1), transfer=round(transfer, 1), total=round(total, 1))


for r in rows:
    r.update(score(r))

rows.sort(key=lambda x: -x["total"])
for i, r in enumerate(rows, 1):
    r["rank"] = i
    band = "S" if r["total"] >= 90 else "A" if r["total"] >= 80 else "B" if r["total"] >= 70 else "C" if r["total"] >= 60 else "D"
    r["band"] = band

json.dump(rows, open(os.path.join(HERE, "eval_scores.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"{'#':>3} {'朝代':<3}{'key':<16}{'角色':>6}{'史识':>6}{'思维':>6}{'遍历':>6}{'总分':>7} 级")
for r in rows:
    print(f"{r['rank']:>3} {r['dyn']:<3}{r['key']:<16}{r['faithfulness']:>6}{r['reliability']:>6}"
          f"{r['thinking']:>6}{r['transfer']:>6}{r['total']:>7}  {r['band']}")

tot = [r["total"] for r in rows]
print(f"\n均值 {sum(tot)/len(tot):.1f} | 最高 {max(tot)} | 最低 {min(tot)} | 共 {len(rows)}")
for b in "SABCD":
    n = sum(1 for r in rows if r["band"] == b)
    if n:
        print(f"  {b} 级：{n} 个")
