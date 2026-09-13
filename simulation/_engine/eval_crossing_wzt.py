# -*- coding: utf-8 -*-
"""武则天版「帝王穿越」推演：读 crossing_scores.json 取处境与类型，
换上武则天的处置方案与评分，生成报告，并与李世民版做对照。"""
import json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
base = {r["key"]: r for r in json.load(open(os.path.join(HERE, "crossing_scores.json"), encoding="utf-8"))}
OUT = r"D:/2026/WB项目/emperor-skill/simulation/by-dynasty/solo/solo-wuzetian.html"

# 武则天对 77 处境的处置（策, 分, 断语）
W = {
 "liyuan": ("以嫡长定分、早正储位、分诸王兵柄，符命不可轻用", 72, "储位之难，朕以『母子姑侄』一决解之——早断则安。"),
 "lishimin": ("武功已定，宜速转文治、以人为镜；玄武门之后尤须早定储位以塞觊觎", 70, "朕尝侍太宗，习其纳谏之言；然马上之功，非朕所长。"),
 "lizhi": ("居高宗之位，宜早限中宫之权、委政贤相，不使一人独揽", 70, "此局朕最熟——防后权者，须早、须决。"),
 "lixian": ("收中宫与外戚之柄，以新进之臣易旧党，去其凭依", 64, "受制于妇而不能断，朕所不解。"),
 "lidan": ("早正储副、削公主府兵，以『定分』止争", 74, "定分之要在早——朕立庐陵王，即是此意。"),
 "lilongji": ("边将宜以文臣制之、不使兼镇；然朕长于内政、短于边略，姑从守御", 58, "朕未亲戎行，开边非朕所长——守成可，拓土难。"),
 "liheng_s": ("平叛须任能将、聚财赋赡军；朕可调兵食而不能亲战", 56, "戡乱之事，朕不如太宗——然用将得当亦可济。"),
 "liyu": ("去宦官之兵权、以文臣代掌禁军，斩其根株", 68, "宦官之祸，朕朝亦有——锄之宜早、宜狠。"),
 "lishi": ("行两税以养民，削藩先固本；用人不专一党", 74, "理财用人，朕所素习——两税可法。"),
 "lisong": ("除弊先握兵与财、以新进易旧党，循序渐进", 70, "去宦官、用新人，朕之法也——惜其无时。"),
 "lichun": ("削藩当先集权于中枢、以耳目监诸镇，次第翦除", 66, "集权朕所擅长，然阵战之事须倚能将。"),
 "liheng_m": ("息党争、定国是；河朔之地以恩威并施羁縻之", 62, "朕以铜匦知四方、以科举换班底——党争可息。"),
 "lizhan": ("去内侍典兵、复朝参之制，君勤则阉不能为祸", 64, "遇弑于奴，人主自弃耳。"),
 "liang": ("除阉须握外兵、结忠将，谋密势厚，不可以一夕图", 70, "朕以渐进夺权得天下——除奸亦须渐进，骤则反噬。"),
 "liyan": ("集权削藩、收寺产以赡军，专任一相责成", 70, "会昌之振作，与朕集权之道同。"),
 "lichen": ("中兴之后以循吏养民、宽以驭繁，不苛察、不饵药", 76, "大中之治，朕所欣赏——循吏治国，正朕晚年之政。"),
 "licui": ("节用重农、弭乱于初起，以铜匦察民隐", 58, "民变起于民力已竭——不恤民而佞佛，宜其亡。"),
 "lixuan": ("守关中以固根本，用能将、安民心，弃都之举不可为", 52, "弃都奔蜀，朕所不取——虽失势，亦当守根本。"),
 "liye": ("蓄势固本、募兵聚粮，不轻挑强藩", 54, "有志无势，宜蓄不宜发。"),
 "lizhu": ("国命已去，唯存宗室、善其终节，如朕之归葬去帝", 54, "积弊百年之总崩——朕所能者，惟善其终。"),
 "zhaokuangyin": ("收兵权、强干弱枝；以符命与耳目制内，其法可参", 72, "杯酒释兵权，与朕渐进夺权异曲同工，皆不流血。"),
 "zhaoguangyi": ("先正名分、后图边功；然边略非朕所长", 60, "得位之疑，朕深知——正名分者，符命亦可一用。"),
 "zhaoheng": ("强边自守、不事封禅虚名", 56, "以和易安则可，以天书夸功则失。"),
 "zhaozhen": ("行新政以省冗、养民力，擢寒门以易旧党", 76, "庆历新政，与朕科举破阀同其志。"),
 "zhaoshu": ("礼争以公议定之、早正名分，不使成党", 72, "定分之争，朕以『早断』处之。"),
 "zhaoxu_s": ("变法先养民力、以新人行新法，不专一党", 74, "安石变法，惜其操切——朕行新政必先择人。"),
 "zhaoxu_z": ("国是定于一而容异议，不翻覆无常", 64, "党争翻覆，朕以耳目察之、以黜陟平之。"),
 "zhaoji": ("节玩好、赡边备；然外患非朕所长", 50, "风雅而昧于治——此朕所不取。"),
 "zhaohuan": ("守京城、结勤王之师，战守分明", 50, "危局摇摆，非一帝之罪——朕亦难全。"),
 "zhaogou": ("立两淮以图恢复，不杀能将、不以和自安", 58, "苟安之讥难辞——然和战之间，须先自强。"),
 "zhaoshen": ("先理财练兵、后图北伐", 60, "乾道淳熙之治，理财用人正是朕之所长。"),
 "zhaodun": ("正家以正国，不使中宫离间骨肉", 66, "人伦之变——朕于子女亦多惭，知此为至难。"),
 "zhaokuo": ("去权臣之专、开言路，不以内批乱政", 66, "党禁与妄战两失，朕戒独断与虚名。"),
 "zhaoyun": ("联弱制强而守约，不贪一时之功", 56, "轻启边衅，朕所不取。"),
 "zhaoqi": ("去权臣、亲军政，急救襄樊以保上游", 52, "亡国之象——人主不闻边报，则国非其国。"),
 "zhaoxian": ("大势已倾，唯存宗室之续", 48, "非其罪——朕之归葬去帝，亦此意。"),
 "zhaoshi": ("保舟师、踞海岛以图存", 46, "无根之君，难矣。"),
 "zhaobing": ("大势尽失，唯全其节", 42, "崖山之局，朕亦无术——然死节可全。"),
 "hubilie": ("因俗而治、以汉法安汉地；符命可证正统，然亲征非朕长", 66, "混一之业，朕无武功——然立制用人，可参朕法。"),
 "temuer": ("守成节用、定赏格", 74, "与民休息，朕之素政。"),
 "haishan": ("定赏有节、任贤理财", 68, "滥赏伤国——理财者，朕所素习。"),
 "ayurbarwada": ("以文治养士、行科举、兼容旧俗", 80, "行科举、崇儒术——此正朕破阀擢才之道，最合朕意。"),
 "shidibala": ("改革先握腹心、分权贵之柄而后动", 72, "变法之难，朕深知——必先得人、先固权。"),
 "yesuntemuer": ("以中庸安宗室、定分立储", 70, "处诸王之间，朕以黜陟平衡之。"),
 "ashuqibu": ("幼主赖辅臣——非可施为之局", 44, "幼主无柱石，朕知其为空。"),
 "hoshila": ("入都前握亲兵、结旧部，防中途之变", 54, "防身之计不可疏——朕之夺权，正赖周密。"),
 "tutemuer": ("去权臣之专、正名分以安宗室", 62, "名不正则政不稳——朕以符命正名，深知其要。"),
 "yilinzhiban": ("立长立贤以定统", 60, "立储之要，朕以『母子姑侄』一决定之。"),
 "toghontemur": ("治河恤民、蠲赋弭乱，先固中原之心", 56, "恤民一节本可早为——朕之铜匦正为此设。"),
 "zhuyuanzhang": ("立法养民、宽猛相济，不以猜忌伤功臣；然马上之业非朕所长", 68, "布衣取天下，起兵非朕所长——然立制治吏，朕可参。"),
 "zhuyunwen": ("削藩须缓图、先固京营，不动则已、动则必成", 60, "非无志乃无术——朕之渐进，正为此。"),
 "zhudi": ("夺位须先正名分、以符命安人心；边功宜计民力", 62, "靖难正名之事，朕以符命解之；然亲征非朕所长。"),
 "zhugaochi": ("罢不急之役、与民休息", 78, "施仁政、罢役——此朕晚年之政，甚合。"),
 "zhuzhanji": ("守成得体，然阉人不可授柄", 74, "内书堂之设，是授家奴以柄——朕戒之。"),
 "zhuqizhen": ("亲征须备万全，不亲冒矢石；朕长内政、短军旅", 52, "以国赌一役，朕所不取。"),
 "zhuqiyu": ("危局任能将、定人心，守京却敌", 68, "危局任贤守国，其决断可称。"),
 "zhujianshen": ("去厂卫之酷、勤政而优容言官", 68, "厂卫罗织，朕之酷吏亦然——然终当诛之以收人心。"),
 "zhuyoutang": ("勤政纳谏、优容言官", 78, "弘治之治，与朕用循吏、开言路同。"),
 "zhuhouzhao": ("君必勤必敬，不以内苑夺政", 58, "人主自弃——朕所不取。"),
 "zhuhoucong": ("政不可怠，去权臣、复朝参", 66, "借议礼以揽权，又怠政以纵奸——权可用，政不可弛。"),
 "zhuzaihou": ("开关通有无、任贤任事", 76, "用人如朕、开关通商，皆可为。"),
 "zhuyijun": ("早定国本、以耳目通言路，居正之政宜续", 74, "国本之争——朕以『母子姑侄』一决，宜早断。"),
 "zhuchangluo": ("即位先清阉党、定国本，不惑于方药", 48, "一月之运而党争阉祸已成——扳之极难。"),
 "zhuyouxiao": ("去阉党、亲贤臣，不以内臣司国柄", 66, "宠信家奴——朕用酷吏犹知诛之，彼不知也。"),
 "zhuyoujian": ("用人不疑、议和以息内外，不数易将帅", 52, "多疑误杀，自坏长城——朕用人不疑，此其别也。"),
 "nurhaci": ("以制度立本、怀柔收诸部；然起兵非朕所长", 62, "十三甲起兵，朕无此武功——立制收人则可参。"),
 "hongtaiji": ("以汉制汉、以文治补武功", 70, "仿汉制、收汉臣——以文补武，正合朕意。"),
 "fulin": ("以汉法治汉地、抚满汉之乖", 68, "冲龄入关而慕文治——朕知其志。"),
 "xuanye": ("削藩自近始、怀柔安诸部；集权朕所长，亲征非朕所能", 70, "康熙之业伟矣——然亲征之事，朕不能。"),
 "yinzhen": ("严考成、清财赋、以密事核吏", 78, "整顿吏治、密核——与朕耳目核吏同调。"),
 "hongli": ("功成之际节用远佞，盛世更须自省", 70, "盛极而奢——朕晚岁亦能去帝号以自省。"),
 "yongyan": ("去弊当举其纲，理财用人两举", 74, "勤政而乏大略——理财用人，朕所素习。"),
 "minning": ("先察外势而后应，练兵海防、知彼不自闭", 54, "昧于外势——朕之铜匦广听，正为知彼。"),
 "yizhu": ("内平乱为急、外以和缓兵，先固根本", 50, "内外并困——弃都北狩，非人君所宜。"),
 "zaichun": ("亲政须先握兵与廷议，去内廷之干", 60, "母后垂帘——朕即临朝之主，知其难为。"),
 "zaitian": ("变法须先得兵与腹心，有权而后动", 70, "有心无权——然朕以渐进夺权起，变法亦须先固权。"),
 "puyi": ("旧制终局，唯善终其身", 48, "旧制之终，非一人能回——朕之归葬去帝，亦善终之道。"),
}

LISHIMIN = dict(key="lishimin", name="太宗", dyn="唐", typ="创业开国",
                dilemma="武功开国转文治、纳谏为镜、以隋为鉴、华夷一体、储贰之忧")

def verdict(s): return "可解" if s >= 75 else "可缓" if s >= 65 else "难解" if s >= 50 else "死局"

rows = []
for k, (plan, sc, note) in W.items():
    b = base.get(k) or LISHIMIN
    rows.append(dict(key=k, name=b["name"], dyn=b["dyn"], typ=b["typ"],
                     dilemma=b["dilemma"], plan=plan, score=sc, verdict=verdict(sc), note=note))

rows.sort(key=lambda r: -r["score"])
json.dump(rows, open(os.path.join(HERE, "crossing_scores_wuzetian.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

by_type = collections.defaultdict(list)
for r in rows: by_type[r["typ"]].append(r["score"])
TYPE_ORDER = ["创业开国","平叛戡乱","削藩集权","守成休养","变法理财","开疆边患","储位继统","权臣党争","亡国危局"]
wzt_avg = {t: round(sum(by_type[t]) / len(by_type[t]), 1) for t in TYPE_ORDER}
LI_AVG = {"创业开国":78.3,"平叛戡乱":76.0,"削藩集权":75.8,"守成休养":74.4,"变法理财":67.5,
          "开疆边患":64.0,"储位继统":57.0,"权臣党争":56.2,"亡国危局":45.3}
by_dyn = collections.defaultdict(list)
for r in rows: by_dyn[r["dyn"]].append(r["score"])
dyn_avg = [(d, round(sum(by_dyn[d]) / len(by_dyn[d]), 1)) for d in ["唐","宋","元","明","清"]]
vdist = collections.Counter(r["verdict"] for r in rows)
overall = round(sum(r["score"] for r in rows) / len(rows), 1)
VC = {"可解":"#0f766e","可缓":"#2563eb","难解":"#b45309","死局":"#a83232"}
DN = {"唐":"#b45309","宋":"#0f766e","元":"#1d4ed8","明":"#a83232","清":"#6d28d9"}

def cards(dyn):
    sub = [r for r in rows if r["dyn"] == dyn]
    out = []
    for r in sub:
        out.append(f'''<div class="card">
  <div class="ch"><span class="nm">{r['name']}</span><span class="k">{r['key']}</span>
    <span class="vd" style="background:{VC[r['verdict']]}1a;color:{VC[r['verdict']]}">{r['verdict']}</span>
    <span class="sc" style="color:{VC[r['verdict']]}">{r['score']}</span></div>
  <div class="typ">困局类型 · {r['typ']}</div>
  <p><b>处境</b>：{r['dilemma']}</p>
  <p><b>则天之策</b>：{r['plan']}</p>
  <p class="n">{r['note']}</p></div>''')
    return f'<h3 class="dyn" style="color:{DN[dyn]}"><span style="background:{DN[dyn]}"></span>{dyn} · {len(sub)} 帝</h3><div class="grid">' + "".join(out) + '</div>'

trows = "".join(
    f"<tr><td>{i}</td><td>{r['dyn']}</td><td class='k'>{r['name']}</td><td>{r['typ']}</td>"
    f"<td class='d'>{r['dilemma']}</td><td class='sc' style='color:{VC[r['verdict']]}'>{r['score']}</td>"
    f"<td><span class='vd' style='background:{VC[r['verdict']]}1a;color:{VC[r['verdict']]}'>{r['verdict']}</span></td></tr>"
    for i, r in enumerate(rows, 1))

HTML = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>帝王穿越处置报告 · 武则天 × 77 处境</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
:root{{--bg:#f6f6f3;--panel:#fff;--ink:#1f2937;--mut:#6b7280;--line:#e5e7eb;--teal:#0f766e;--pur:#7c3aed}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.7 -apple-system,"Segoe UI","Microsoft YaHei",sans-serif}}
.wrap{{max-width:1060px;margin:0 auto;padding:32px 24px 64px}}
h1{{font-size:24px;font-weight:600;margin:0 0 6px}}
.sub{{color:var(--mut);font-size:13px;margin:0 0 22px}}
h2{{font-size:17px;font-weight:600;margin:36px 0 14px;padding-left:10px;border-left:3px solid var(--pur)}}
.meta{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:16px 0}}
.m{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px}}
.m .l{{color:var(--mut);font-size:12px}} .m .n{{font-size:21px;font-weight:600;margin-top:2px}}
.quote{{background:#f6f1fd;border-left:3px solid var(--pur);border-radius:0 8px 8px 0;padding:14px 18px;color:#4c1d95;font-size:13.5px;margin:14px 0}}
.panel{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px}}
.chart{{position:relative;height:300px}}
table{{width:100%;border-collapse:collapse;font-size:12.5px;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden}}
th,td{{padding:7px 9px;border-bottom:1px solid var(--line);text-align:left}}
td.sc{{text-align:center;font-weight:600}} th{{background:#f0f1ef;font-weight:500;color:var(--mut)}}
td.k{{font-family:ui-monospace,Consolas,monospace;font-size:11.5px;white-space:nowrap}}
td.d{{color:#4b5563;max-width:340px}}
tr:hover td{{background:#fafaf8}}
.vd{{display:inline-block;padding:1px 8px;border-radius:20px;font-size:12px;font-weight:500}}
h3.dyn{{font-size:15px;font-weight:600;margin:26px 0 12px;display:flex;align-items:center;gap:8px}}
h3.dyn span{{width:10px;height:10px;border-radius:3px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:13px 15px}}
.ch{{display:flex;align-items:center;gap:8px}}
.nm{{font-weight:600}} .k{{font-family:ui-monospace,Consolas,monospace;font-size:11px;color:var(--mut);flex:1}}
.sc{{font-weight:600;font-size:15px}}
.typ{{color:var(--mut);font-size:11.5px;margin:4px 0 7px}}
.card p{{margin:0 0 5px;font-size:12.5px;color:#374151}} .card p b{{color:#111827;font-weight:500}}
.card .n{{color:var(--pur);font-size:12.5px}}
.cmp{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} @media(max-width:760px){{.cmp{{grid-template-columns:1fr}}}}
.foot{{color:var(--mut);font-size:12px;margin-top:28px;border-top:1px solid var(--line);padding-top:16px}}
</style></head><body><div class="wrap">
<h1>帝王穿越处置报告 · 武则天版</h1>
<p class="sub">穿越者：武周圣神皇帝武则天 · 目标：其余 77 位帝王的处境 · 标准：穿越处置评分卡 v0.2</p>

<div class="quote">朕以女主之身，处李唐宗法夹缝而终登大位——若置朕于他人之局，朕之六道（符命建国、酷吏罗织、科举破阀、铜匦广听、渐进夺权、归葬去帝）可否一用？阅毕乃知：<b>内廷之争、储位之定、破旧立新，朕可接；开疆拓土、临阵决胜，朕不能。</b>与太宗适成互补。</div>

<div class="meta">
  <div class="m"><div class="l">穿越目标</div><div class="n">{len(rows)}</div></div>
  <div class="m"><div class="l">平均处置分</div><div class="n">{overall}</div></div>
  <div class="m"><div class="l">可解 / 可缓</div><div class="n">{vdist.get('可解',0)} / {vdist.get('可缓',0)}</div></div>
  <div class="m"><div class="l">难解 / 死局</div><div class="n">{vdist.get('难解',0)} / {vdist.get('死局',0)}</div></div>
</div>

<h2>一、双人对照 · 按困局类型的适配度</h2>
<div class="panel"><div class="legend" style="display:flex;gap:16px;font-size:12px;color:#6b7280;margin-bottom:8px">
<span><i style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#0f766e;margin-right:5px"></i>李世民</span>
<span><i style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#7c3aed;margin-right:5px"></i>武则天</span></div>
<div class="chart" style="height:360px"><canvas id="cmp" role="img" aria-label="李世民与武则天各困局类型适配度对比"></canvas></div></div>

<h2>二、判定分布与朝代均值</h2>
<div class="panel"><div class="chart" style="height:250px"><canvas id="dist" role="img" aria-label="判定分布环形图"></canvas></div>
<div class="meta" style="margin-top:14px">{''.join(f'<div class="m"><div class="l">{d}朝均分</div><div class="n">{v}</div></div>' for d,v in dyn_avg)}</div></div>

<h2>三、则天最能接住的 8 个处境</h2>
<div class="panel">{''.join(f'<div style="font-size:13px;padding:4px 0"><b>{i}. {r["name"]}</b>（{r["dyn"]}·{r["typ"]}） <span style="color:{VC[r["verdict"]]};font-weight:600">{r["score"]}</span> — {r["dilemma"]}</div>' for i, r in enumerate(rows[:8], 1))}</div>

<h2>四、处置力总表（77 处境）</h2>
<table><thead><tr><th>#</th><th>朝代</th><th>帝王</th><th>困局类型</th><th>核心困局</th><th>分</th><th>判定</th></tr></thead>
<tbody>{trows}</tbody></table>

<h2>五、逐帝穿越推演</h2>
{''.join(cards(d) for d in ["唐","宋","元","明","清"])}

<div class="foot">
评分卡 v0.2：情境识别 25 + 模型迁移 30 + 方案可行性 30 + 角色保真 15；判定 可解≥75／可缓 65–74／难解 50–64／死局&lt;50。<br>
对照说明：两次推演的目标集合相差一人（李世民版含武则天、无李世民；武则天版含李世民、无武则天），故总分不宜作绝对较；类型适配度基于同一套 9 类困局，可直接比较。<br>
诚实边界：思想实验式反事实推演，非史实复原；分数表达「其心智工具与该处境的适配度」，非对政绩的褒贬。
</div>
</div>
<script>
new Chart(document.getElementById('cmp'),{{type:'bar',data:{{labels:{json.dumps(TYPE_ORDER)},
 datasets:[{{label:'李世民',data:{json.dumps([LI_AVG[t] for t in TYPE_ORDER])},backgroundColor:'#0f766e',borderRadius:3}},
 {{label:'武则天',data:{json.dumps([wzt_avg[t] for t in TYPE_ORDER])},backgroundColor:'#7c3aed',borderRadius:3}}]}},
 options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,scales:{{x:{{min:40,max:90,grid:{{color:'#e5e7eb'}}}}}},
 plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:c=>c.dataset.label+' '+c.parsed.x+' 分'}}}}}}}}}});
new Chart(document.getElementById('dist'),{{type:'doughnut',data:{{labels:['可解','可缓','难解','死局'],
 datasets:[{{data:{json.dumps([vdist.get('可解',0),vdist.get('可缓',0),vdist.get('难解',0),vdist.get('死局',0)])},
 backgroundColor:['#0f766e','#2563eb','#b45309','#a83232'],borderWidth:0}}]}},
 options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'bottom'}}}}}}}});
</script></body></html>'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(HTML)

print(f"目标 {len(rows)} · 均分 {overall} · 判定 {dict(vdist)}")
print("朝代均分：", dyn_avg)
print("类型适配对照（李世民 vs 武则天）：")
for t in TYPE_ORDER:
    print(f"  {t:<8} 李 {LI_AVG[t]:>5}  武 {wzt_avg[t]:>5}   差 {wzt_avg[t]-LI_AVG[t]:+.1f}")
print("报告 ->", OUT)
