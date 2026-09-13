# -*- coding: utf-8 -*-
"""「帝王遍历」HTML 报告生成器：读 eval_scores.json + 李世民评语，产出可离线打开的评测报告。"""
import json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "eval_scores.json"), encoding="utf-8"))
by = {r["key"]: r for r in rows}
OUT = r"D:/2026/WB项目/emperor-skill/skills/_audit/skill-quality-report.html"

# 遍历者李世民对 78 帝的评语（以史为鉴视角）
V = {
 # 唐
 "liyuan": "起兵晋阳有开创之功，然玄武门之日不能制其子——朕之起点，即是明证。",
 "lishimin": "此即朕也。功业足以自证，而蹀血禁门之惭，终身难掩。",
 "lizhi": "承贞观之遗而失之柔，武氏之兴，朕之《帝范》未足训也。",
 "wuzetian": "牝鸡司晨固违常，然酷吏之后能任贤纳谏、开殿试，治国之才不可尽以女子废之。",
 "lixian": "中宗再起而受制于妇，暴崩于妇手，非守成之器。",
 "lidan": "睿宗三让两登，知退知进，然终为太平公主所制。",
 "lilongji": "开元之治可比贞观，而天宝之乱自作其孽——朕之晚年亦有此渐变，痛哉。",
 "liheng_s": "灵武自立，虽有复国之志，然借兵回纥、宠任宦官，遗祸不浅。",
 "liyu": "收拾残局尚可，然姑息藩镇、纵容宦官，积弊自此深。",
 "lishi": "两税一法善矣，而猜忌刻薄、聚敛无度，奉天之变非无因。",
 "lisong": "永贞革新有锐气，惜在位仅八月，言之易而行之难。",
 "lichun": "中兴削藩，可谓有为之主；然佞佛饵丹，终不克终。",
 "liheng_m": "怠政纵乐，河朔再失，牛李之党自此相倾，唐之衰自长庆始。",
 "lizhan": "童昏嬉游、视朝稀阔，遇弑于内侍，可叹可恨。",
 "liang": "甘露一决而谋泄，去河北贼易、去朝中宦官难——其言痛切，其行则疏。",
 "liyan": "会昌灭佛、专任德裕、平泽潞，是唐末难得的振作之君。",
 "lichen": "大中之治，史称小太宗；然察察为明，晚惑方士，朕不取苛察。",
 "licui": "游宴无度、佞佛耗国，裘甫一乱，唐祚已薄。",
 "lixuan": "嬉戏失国，黄巢破京而奔蜀，非人君之度。",
 "liye": "有志兴复而无实力，受制强藩，终见弑于朱温之手，朕为之恻然。",
 "lizhu": "白马之祸，唐祚遂终。非一帝之罪，乃积弊百年之总崩。",
 # 宋
 "zhaokuangyin": "杯酒释兵权、重文抑武，解唐末五代之乱是其所长；然强干弱枝，亦开积弱之端。",
 "zhaoguangyi": "得位有烛影之疑，北伐屡挫，然文治可称。",
 "zhaoheng": "澶渊以岁币换安，封禅天书徒耗国力，非善继者。",
 "zhaozhen": "宽仁有度、士大夫乐为之用，庆历新政虽止，仁宗之世可谓宋之盛。",
 "zhaoshu": "濮议之争几摇朝局，在位日浅，未见大略。",
 "zhaoxu_s": "锐意变法，安石之志可嘉，然操之过急、新法扰民，北宋之变关由于此。",
 "zhaoxu_z": "元祐绍圣翻覆无常，党争白热，国是数变则民不聊生。",
 "zhaoji": "瘦金花石，风雅有余而治国无术，靖康之耻其召之也。",
 "zhaohuan": "受命于危，割地纳贡终不免北狩，非一帝之罪，乃积弱之果。",
 "zhaogou": "南渡开基而偏安江左，杀岳飞、称臣纳贡，苟安之讥难辞。",
 "zhaoshen": "南宋最有为之君，锐意恢复而力不逮，乾道淳熙之治可称。",
 "zhaodun": "受制悍后，父子相猜，竟以不孝见讥，人伦之变令人叹。",
 "zhaokuo": "庆元党禁、开禧北伐皆失，权臣迭起，国势日下。",
 "zhaoyun": "联蒙灭金而邀功，端平入洛轻启边衅，贾似道之渐兆于斯。",
 "zhaoqi": "荒于酒色、权归贾氏，襄阳告急而不知，亡国之象已露。",
 "zhaoxian": "幼冲逊国，临安出降，非其罪，乃大势之倾。",
 "zhaoshi": "流亡播迁，未及有为而殂于碙州。",
 "zhaobing": "崖山一决，负幼投海，君臣俱没——存统之愿终成殉国之节。",
 # 元
 "hubilie": "定鼎燕京、混一南北，虽起于夷狄而能用汉法，有帝王之略。",
 "temuer": "守成之主，能与民休息，然滥赏致国用不足。",
 "haishan": "以军功入践大位，封赏无度，朝政颇紊。",
 "ayurbarwada": "在位勤于文治，行科举、尊儒学，元世之贤者。",
 "shidibala": "锐意汉法改革而触怒权贵，南坡遇弑——变法之难如是。",
 "yesuntemuer": "守成少变，处诸王之间而得不乱，中庸之姿。",
 "ashuqibu": "两都之战中的幼主，帝位月余而败，天命之无常。",
 "hoshila": "自漠北南归，未及都城而暴崩，天不假年。",
 "tutemuer": "初让复夺，挟权臣柄政，虽崇文而内多惭愧。",
 "yilinzhiban": "幼年即位，月余而殂，国统之乱可见。",
 "toghontemur": "北遁大漠，元祚遂终；河患民变并起，非一帝能挽。",
 # 明
 "zhuyuanzhang": "布衣取天下，重典治吏，草根雄主；然猜忌屠戮，亦失宽仁。",
 "zhuyunwen": "削藩太急，仁柔而失国，非无志，乃无术。",
 "zhudi": "靖难夺位而颇有太宗之迹，迁都、下西洋、修大典，功业赫赫。",
 "zhugaochi": "在位十月而施仁政、罢西洋，惜天不假年。",
 "zhuzhanji": "仁宣之治，守成得体；然设内书堂教宦官，遗祸深远。",
 "zhuqizhen": "土木之变几倾社稷，复辟后又杀忠臣，功过两分。",
 "zhuqiyu": "临危受命、任用于谦挽危局，惜夺门之后身后蒙冤。",
 "zhujianshen": "宽仁而设西厂、宠万贵妃，朝政渐弛。",
 "zhuyoutang": "一夫一妻、勤政纳谏，可与仁宗比肩，明之贤主。",
 "zhuhouzhao": "豹房嬉游，自号将军，视国事如儿戏。",
 "zhuhoucong": "议礼夺权、崇道怠政，严嵩弄权二十年，帝实主之。",
 "zhuzaihou": "开关互市、任用高拱张居正，短祚而有作为。",
 "zhuyijun": "居正遗泽可称，而晚年怠政三十载，国本之争伤元气。",
 "zhuchangluo": "一月天子，红丸暴崩，明之党争阉祸自此炽。",
 "zhuyouxiao": "木匠皇帝，宠信魏忠贤，阉党荼毒东林。",
 "zhuyoujian": "勤政而多疑、刚愎而误杀，非亡国之君而当天亡之运。",
 # 清
 "nurhaci": "十三甲起兵，创八旗、建后金，夷狄之创业雄主。",
 "hongtaiji": "改国号、仿明制、收汉臣，为入关奠基。",
 "fulin": "冲龄入关，亲政后慕汉崇文，惜早逝。",
 "xuanye": "平三藩、收台湾、御沙俄、定朔漠兼修文教——守成兼开创之圣主。",
 "yinzhen": "勤政严苛、革除积弊、密折治吏，承前启后之枢纽。",
 "hongli": "十全武功、编纂四库，然晚年奢靡、宠和珅，盛世之巅亦衰之始。",
 "yongyan": "诛和珅而未能挽颓势，勤政而乏大略。",
 "minning": "俭朴自守而昧于外势，鸦片一战而国门洞开。",
 "yizhu": "内忧外患并至，圆明园一炬，仓皇北狩。",
 "zaichun": "冲龄在位，母后垂帘，所谓中兴者实非帝力。",
 "zaitian": "戊戌变法有心振作而无权，囚于瀛台，可悲可叹。",
 "puyi": "三起三落，终为末代；旧制之终结，非一人能回。",
}

DN = {"唐": "#b45309", "宋": "#0f766e", "元": "#1d4ed8", "明": "#a83232", "清": "#6d28d9"}
ORDER = ["唐", "宋", "元", "明", "清"]

# 各朝代平均画像
dyn_avg = {}
for d in ORDER:
    sub = [r for r in rows if r["dyn"] == d]
    dyn_avg[d] = [
        round(sum(r["faithfulness"] for r in sub) / len(sub) / 30 * 100, 1),
        round(sum(r["reliability"] for r in sub) / len(sub) / 30 * 100, 1),
        round(sum(r["thinking"] for r in sub) / len(sub) / 25 * 100, 1),
        round(sum(r["transfer"] for r in sub) / len(sub) / 15 * 100, 1),
    ]

tot = [r["total"] for r in rows]
grade = collections.Counter(r["band"] for r in rows)
top10 = sorted(rows, key=lambda x: -x["total"])[:10]

cards = []
for d in ORDER:
    sub = sorted([r for r in rows if r["dyn"] == d], key=lambda x: -x["total"])
    inner = []
    for r in sub:
        inner.append(f'''<div class="card">
  <div class="card-h"><span class="rk">#{r['rank']}</span><span class="nm">{r['key']}</span>
    <span class="bd b{r['band']}">{r['band']}</span><span class="sc">{r['total']}</span></div>
  <div class="dims"><span>角色 {r['faithfulness']}</span><span>史识 {r['reliability']}</span>
    <span>思维 {r['thinking']}</span><span>遍历 {r['transfer']}</span></div>
  <p class="verdict">{V.get(r['key'],'')}</p></div>''')
    cards.append(f'<h3 class="dyn" style="color:{DN[d]}"><span style="background:{DN[d]}"></span>{d}朝 · {len(sub)} 帝</h3><div class="grid">' + "".join(inner) + '</div>')

trows = "".join(
    f"<tr data-t='{r['total']}'><td>{r['rank']}</td><td>{r['dyn']}</td><td class='k'>{r['key']}</td>"
    f"<td>{r['faithfulness']}</td><td>{r['reliability']}</td><td>{r['thinking']}</td><td>{r['transfer']}</td>"
    f"<td class='t'>{r['total']}</td><td><span class='bd b{r['band']}'>{r['band']}</span></td></tr>" for r in rows)

HTML = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>帝王遍历评测报告 · 78 帝</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
:root{{--bg:#f6f6f3;--panel:#fff;--ink:#1f2937;--mut:#6b7280;--line:#e5e7eb;--teal:#0f766e}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.7 -apple-system,"Segoe UI","Microsoft YaHei",sans-serif}}
.wrap{{max-width:1040px;margin:0 auto;padding:32px 24px 64px}}
h1{{font-size:24px;font-weight:600;margin:0 0 6px}}
.sub{{color:var(--mut);font-size:13px;margin:0 0 24px}}
h2{{font-size:17px;font-weight:600;margin:36px 0 14px;padding-left:10px;border-left:3px solid var(--teal)}}
.meta{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:16px 0}}
.m{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px}}
.m .l{{color:var(--mut);font-size:12px}} .m .n{{font-size:22px;font-weight:600;margin-top:2px}}
.quote{{background:#eff6f4;border-left:3px solid var(--teal);border-radius:0 8px 8px 0;padding:14px 18px;color:#134e4a;font-size:13.5px;margin:14px 0}}
.panel{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} @media(max-width:760px){{.two{{grid-template-columns:1fr}}}}
.chart{{position:relative;height:300px}}
table{{width:100%;border-collapse:collapse;font-size:13px;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden}}
th,td{{padding:7px 10px;border-bottom:1px solid var(--line);text-align:right}}
th:nth-child(2),td:nth-child(2),th:nth-child(3),td:nth-child(3){{text-align:left}}
th{{background:#f0f1ef;font-weight:500;color:var(--mut);position:sticky;top:0}}
td.k{{font-family:ui-monospace,Consolas,monospace;font-size:12px}}
td.t{{font-weight:600}}
tr:hover td{{background:#fafaf8}}
.bd{{display:inline-block;padding:1px 8px;border-radius:20px;font-size:12px;font-weight:500}}
.bS{{background:#d1fae5;color:#065f46}} .bA{{background:#dbeafe;color:#1e40af}}
.bB{{background:#fef3c7;color:#92400e}} .bC{{background:#fee2e2;color:#991b1b}} .bD{{background:#e5e7eb;color:#374151}}
h3.dyn{{font-size:15px;font-weight:600;margin:26px 0 12px;display:flex;align-items:center;gap:8px}}
h3.dyn span{{width:10px;height:10px;border-radius:3px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:13px 15px}}
.card-h{{display:flex;align-items:center;gap:8px}}
.rk{{color:var(--mut);font-size:12px}} .nm{{font-family:ui-monospace,Consolas,monospace;font-size:12.5px;flex:1}}
.sc{{font-weight:600;font-size:15px}}
.dims{{display:flex;flex-wrap:wrap;gap:10px;color:var(--mut);font-size:11.5px;margin:7px 0}}
.verdict{{margin:0;font-size:12.5px;color:#374151}}
.legend{{display:flex;flex-wrap:wrap;gap:14px;font-size:12px;color:var(--mut);margin:8px 0}}
.legend i{{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px}}
.foot{{color:var(--mut);font-size:12px;margin-top:28px;border-top:1px solid var(--line);padding-top:16px}}
</style></head><body><div class="wrap">
<h1>帝王遍历评测报告</h1>
<p class="sub">遍历者：唐太宗李世民 · 对象：78 位帝王 -perspective Skill · 标准：帝王遍历评分卡 v0.1（满分 100）</p>

<div class="quote">朕尝谓「以古为镜，可以知兴替」。今纵览七十八帝之终始，见开创者多雄而守成者多弛，纳谏者昌而独断者亡——兴亡之枢，不在兵甲之利，而在民心之向背、人主之自省耳。</div>

<div class="meta">
  <div class="m"><div class="l">受评帝王</div><div class="n">{len(rows)}</div></div>
  <div class="m"><div class="l">平均总分</div><div class="n">{sum(tot)/len(tot):.1f}</div></div>
  <div class="m"><div class="l">最高 / 最低</div><div class="n">{max(tot)} / {min(tot)}</div></div>
  <div class="m"><div class="l">A 级 / B 级 / C 级</div><div class="n">{grade.get('A',0)} / {grade.get('B',0)} / {grade.get('C',0)}</div></div>
</div>

<h2>一、五朝平均画像（雷达）</h2>
<div class="panel"><div class="legend">{''.join(f'<span><i style="background:{DN[d]}"></i>{d}</span>' for d in ORDER)}<span>（各维已归一到满分百分比）</span></div>
<div class="chart"><canvas id="radar" role="img" aria-label="五朝四维平均分雷达图"></canvas></div></div>

<h2>二、总分榜 · TOP 10</h2>
<div class="panel"><div class="chart" style="height:340px"><canvas id="bar" role="img" aria-label="总分前十柱状图"></canvas></div></div>

<h2>三、得分总表（78 帝）</h2>
<table><thead><tr><th>#</th><th>朝代</th><th>key</th><th>角色</th><th>史识</th><th>思维</th><th>遍历</th><th>总分</th><th>级</th></tr></thead>
<tbody>{trows}</tbody></table>

<h2>四、李世民逐帝评语</h2>
{''.join(cards)}

<div class="foot">
方法说明：角色保真/史识可靠/思维可用三维由 SKILL.md 的可量化结构指标（第一人称密度、心智模型数、一手占比、引证密度、张力条数等）折算；
遍历适应为迁移素材代理量。评语由「李世民」视角定性给出。<br>
诚实边界：本报告是<b>基于技能文件的静态评测</b>，非真实逐帝对话压测；史实准确度未逐条复核原文，分数仅供横向比较，不构成对该人物历史地位的评价。
</div>
</div>
<script>
new Chart(document.getElementById('radar'),{{type:'radar',data:{{labels:['角色保真','史识可靠','思维可用','遍历适应'],
 datasets:[{','.join(f"{{label:'{d}',data:{json.dumps(dyn_avg[d])},borderColor:'{DN[d]}',backgroundColor:'{DN[d]}22',borderWidth:2,pointRadius:2}}" for d in ORDER)}]}},
 options:{{responsive:true,maintainAspectRatio:false,scales:{{r:{{min:0,max:100,ticks:{{stepSize:20,backdropColor:'transparent'}},grid:{{color:'#e5e7eb'}},pointLabels:{{font:{{size:12}}}}}}}},plugins:{{legend:{{display:false}}}}}}}});
new Chart(document.getElementById('bar'),{{type:'bar',data:{{labels:{json.dumps([r['key'] for r in top10])},
 datasets:[{{data:{json.dumps([r['total'] for r in top10])},backgroundColor:{json.dumps([DN[r['dyn']] for r in top10])},borderRadius:4}}]}},
 options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,scales:{{x:{{min:60,max:92,grid:{{color:'#e5e7eb'}}}}}},
 plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:c=>c.parsed.x+' 分'}}}}}}}}}});
</script></body></html>'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(HTML)
print("报告已生成 ->", OUT, f"({len(HTML)} 字节, {len(rows)} 帝)")
