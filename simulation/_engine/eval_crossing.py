# -*- coding: utf-8 -*-
"""「帝王穿越」推演器：把唐太宗李世民空投到其余 77 位帝王的处境，
判定其能否处置得当，并按评分卡 v0.2 打分，产出 HTML 报告。
数据字段：(key, 庙号, 困局类型, 核心困局, 李世民之策, 分, 断语)"""
import os, json, collections

OUT = r"D:/2026/WB项目/emperor-skill/simulation/by-dynasty/solo/solo-lishimin.html"

# ── 唐（20，李世民自身单列基准）─────────────────────────────
TANG = [
 ("liyuan","高祖","储位继承","次子功高震主、太子居正统，诸子相争已成势",
  "早定储副、以嫡长绝侥幸，分秦王兵柄于东宫，使功归于国而非人","62",
  "朕即那个『功高之次子』——削之则乱、不削则夺，以身涉局方知此结无解。"),
 ("lizhi","高宗","女主外戚","体弱多病，武后渐预朝政，中宫接外廷",
  "以『内廷不得干政』为律，早建储、抑后族，托政于宰辅而不托于中宫","58",
  "病榻托柄于人，纵有纳谏之心亦难分身制之——《帝范》之训于此最痛。"),
 ("wuzetian","则天","女主临朝","女主临朝、宗室反抗、酷吏罗织",
  "去告密之法、以纳谏制酷吏、以怀柔安李唐宗室，收人心为先","74",
  "朕无女主之局，然『酷吏必除、言路必开』二事，朕可移用而有效。"),
 ("lixian","中宗","权柄旁落","复位而受制韦后、外戚干政，终暴崩于内",
  "收中宫之权、远外戚之任，以谏官耳目制内廷","56",
  "受制于妇而复不能制，非不能也，是不为也——最忌优柔。"),
 ("lidan","睿宗","权力让渡","三让两登，太平公主干政，皇妹与太子相轧",
  "早正储位、削公主食邑与府兵，以『定分』止争","66",
  "知退知进是其明，然『定分』一事迟则生变，朕深有体会。"),
 ("lilongji","玄宗","盛极转衰","开元极盛而天宝怠政，边将坐大、藩镇成形",
  "盛时先补制度：强干弱枝、以文臣制边将、不使一人兼数镇","78",
  "开元可比贞观，天宝之乱自作其孽——朕之晚年亦有此渐变，痛哉。"),
 ("liheng_s","肃宗","平叛复兴","安史未平而灵武自立，借兵回纥、委任宦官",
  "平叛为先、借兵可而制之以约，宦官典兵必不可开","76",
  "复国之志可嘉，然以宦官掌禁军，此祸根一埋百年。"),
 ("liyu","代宗","藩镇宦官","姑息藩镇、纵容宦官典兵，积弊自此深",
  "以削藩为先、以文臣代宦官掌兵，宁缓勿纵","64",
  "收拾残局尚可，失在姑息——养痈成患，朕所不敢。"),
 ("lishi","德宗","财政藩镇","两税可称而猜忌刻薄、聚敛无度，致奉天之变",
  "行两税以养民力，削藩须先固关中、备钱粮，不轻启战端","68",
  "两税一法善矣，然猜忌刻薄则众叛，聚敛无度则民怨。"),
 ("lisong","顺宗","变法受制","永贞革新欲除宦官弊政，在位八月而败",
  "除弊须先握兵与财，纳谏并进、渐进不骤","66",
  "有锐气惜无时，其臣亦躁——言之易而行之难。"),
 ("lichun","宪宗","削藩集权","河朔久叛、藩镇跋扈，中央威权不振",
  "倚能将、备钱粮、各个击破，以『削藩必自近始』复张中央","84",
  "中兴削藩，可谓有为之主；其道与朕削平群雄同。"),
 ("liheng_m","穆宗","藩镇党争","怠政纵乐，河朔再失，牛李党争自此愈烈",
  "息党争以公器用人、不纵已得之藩镇，居安更须思危","60",
  "河朔再失，非敌强也，乃自弛——唐之衰自长庆始。"),
 ("lizhan","敬宗","宦官弑逆","童昏嬉游、视朝稀阔，遇弑于内侍之手",
  "去内侍典兵、复日朝之制，君必勤必明方可制阉","52",
  "遇弑于奴，可叹可恨——人主自弃，则近臣为豺狼。"),
 ("liang","文宗","宦官专权","家奴持兵柄、废立由之，甘露图除反遭噬",
  "除阉须握外兵、结忠将，谋密而势厚，不可一夕侥幸","58",
  "『去河北贼易、去朝中宦官难』——其言痛切，其行则疏。"),
 ("liyan","武宗","削藩灭佛","泽潞拒命、僧尼耗国、财赋空虚",
  "专任一相、聚财赡军、乘势削藩，收寺产以充国用","82",
  "会昌振作，是唐末难得的明断之君，与朕同好『决于禁中』。"),
 ("lichen","宣宗","中兴边事","虽有『小太宗』之名，然察察为明、晚惑方士",
  "以宽驭繁、收河湟后当抚边戢兵，不苛察、不饵药","80",
  "大中之治可称，然苛察非明——朕亦晚惑方药，知此为通病。"),
 ("licui","懿宗","民变佞佛","游宴无度、佞佛耗国，裘甫一乱而唐祚已薄",
  "节用而重农、以纳谏知民隐，弭乱于初起","58",
  "民变之起，皆自民力已竭——不恤民而佞佛，其亡可待。"),
 ("lixuan","僖宗","流亡失国","嬉戏失国，黄巢破京而奔蜀",
  "守关中、固民心、用能将，不弃宗庙而走","48",
  "弃都而奔，非人君之度——朕定天下，从无弃地之想。"),
 ("liye","昭宗","强藩挟持","有志兴复而无实力，受制强藩终见弑",
  "先固基本之地、募兵聚粮，不以微弱之势轻挑强藩","50",
  "有志无势，朕为之恻然——然兴复当如朕之蓄势，而非孤注。"),
 ("lizhu","哀帝","亡国","白马之祸，唐祚百年积弊总崩，无可回天",
  "国命已去，唯保全宗室、善其终节","42",
  "非一帝之罪，乃积弊百年之总崩——此局，朕亦无从措手。"),
]

# ── 宋（18）───────────────────────────────────────────────
SONG = [
 ("zhaokuangyin","太祖","削藩集权","承五代之乱，须收兵权、防藩镇再起，又要不伤武备",
  "以文制武、强干弱枝——与朕『马上得之不可马上治之』同调","86",
  "杯酒释兵权，解唐末五代之乱是其所长；然强干弱枝亦开积弱之端，宜有张弛。"),
 ("zhaoguangyi","太宗","继统北伐","得位有烛影之疑，北伐屡挫，燕云未复",
  "先正名分、后图边功，不以内疑而外伐","68",
  "得位之疑当以实绩正之——朕以贞观自证，亦同此理。"),
 ("zhaoheng","真宗","边患封禅","澶渊可战而议和，岁币换安后又封禅耗国",
  "以岁币换安可一时，然当强边自守、不事封禅虚名","66",
  "以和易安则可，以天书夸功则失——朕平突厥却未事虚文。"),
 ("zhaozhen","仁宗","冗费新政","宽仁有余而冗官冗费日积，庆历新政未成",
  "行新政以省冗、养民力为先，纳谏并进以持久","74",
  "宽仁有度、士大夫乐为之用，仁宗之世可称；失在省冗不决。"),
 ("zhaoshu","英宗","礼制之争","濮议之争几摇朝局，在位日浅未见大略",
  "礼争当以公议定之、不使成党倾","60",
  "以私亲之争摇国本，朕所不取——立储定分宜早。"),
 ("zhaoxu_s","神宗","变法党争","锐意变法而操之过急，新法扰民，党争起",
  "变法宜先养民力、渐进不失人心，用人不专一党","72",
  "安石之志可嘉，然操之过急——朕行均田轻徭，皆先计民力。"),
 ("zhaoxu_z","哲宗","党争反复","元祐绍圣翻覆无常，国是数变，党争白热",
  "国是当定于一而容异议，不以人废政、不翻覆无常","60",
  "数变则民不聊生——朕纳谏而不翻覆，此其要也。"),
 ("zhaoji","徽宗","亡国前夜","花石纲耗国、边防失修，金兵压境犹事文艺",
  "节玩好、赡边备、以能将守燕，不以外饰掩内虚","50",
  "风雅有余而治国无术，靖康之耻其召之也。"),
 ("zhaohuan","钦宗","靖康危局","受命于危，割地纳贡终不免北狩",
  "守京城、结勤王之师，战守分明不摇摆","42",
  "危局而主战守不定，非一帝之罪，乃积弱之果——此局极难。"),
 ("zhaogou","高宗","南渡和战","南渡开基而偏安江左，杀岳飞、称臣纳贡",
  "立足两淮以图恢复，不以和自安、不杀能将","66",
  "苟安之讥难辞——朕御突厥虽亦用和，然必先自强。"),
 ("zhaoshen","孝宗","恢复北伐","南宋最有为之君，锐意恢复而力不逮",
  "先理财练兵、后图北伐，不轻启而每战必计","70",
  "乾道淳熙之治可称，其志亦同朕之恢复，惜财赋不逮。"),
 ("zhaodun","光宗","人伦之变","受制悍后，父子相猜，竟以不孝见讥",
  "正家以正国，不使中宫离间骨肉","54",
  "人伦之变令人叹——朕之夺嫡，深知兄弟父子之难。"),
 ("zhaokuo","宁宗","权臣党禁","庆元党禁、开禧北伐皆失，权臣迭起",
  "去权臣之专、开言路，不以内批乱政","56",
  "党禁与妄战两失——朕所戒者，正『独断』与『虚名之伐』。"),
 ("zhaoyun","理宗","边衅招祸","联蒙灭金邀功，端平入洛轻启边衅",
  "联弱以制强而慎守约，不贪一时之功","58",
  "轻启边衅，贾似道之渐兆于斯——朕灭突厥亦必先自固。"),
 ("zhaoqi","度宗","权臣怠政","荒于酒色、权归贾氏，襄阳告急而不知",
  "去权臣、亲军政，急则救襄樊以保上游","48",
  "亡国之象已露——人主不闻边报，则国非其国。"),
 ("zhaoxian","恭帝","亡国幼主","幼冲逊国，临安出降",
  "大势已倾，唯存宗室之续","40",
  "非其罪，乃大势之倾——此局，朕亦无策。"),
 ("zhaoshi","端宗","流亡","流亡播迁，未及有为而殂",
  "保舟师、踞海岛以图存，然终乏根本之地","40",
  "无土之君，虽有志难行——存统之愿不敌无根之实。"),
 ("zhaobing","末帝","崖山死局","崖山一决，负幼投海，君臣俱没",
  "大势尽失，唯全死节——非可施治之局","38",
  "存统之愿终成殉国之节——此非治法可解，朕亦无术。"),
]

# ── 元（11）───────────────────────────────────────────────
YUAN = [
 ("hubilie","世祖","混一守成","混一南北，须用汉法而安蒙古旧俗，两难",
  "因俗而治、以汉法治汉地、以怀柔安诸部——朕之羁縻之道可移","82",
  "定鼎燕京、混一南北，能用汉法，有帝王之略，与朕怀远同调。"),
 ("temuer","成宗","守成滥赏","守成能与民休息，然滥赏致国用不足",
  "守成当节用、定赏格，不以爵禄市恩","70",
  "与民休息是其善，滥赏则伤本——朕轻徭而不滥赏。"),
 ("haishan","武宗","财政失序","以军功入践大位，封赏无度，朝政颇紊",
  "定赏有节、任贤理财，不以私恩乱国用","64",
  "封赏无度则国贫——此事朕亦尝戒之。"),
 ("ayurbarwada","仁宗","文治科举","行科举、尊儒学，而蒙古权贵未靖",
  "以文治养士、渐进不激，兼容旧俗","78",
  "行科举、崇儒术，元世之贤者，与朕『文治转向』同。"),
 ("shidibala","英宗","变法反噬","锐意汉法改革而触怒权贵，南坡遇弑",
  "改革须先握兵与腹心，分权贵之柄而后动","68",
  "变法之难如是——朕行新政亦必先得房杜之助。"),
 ("yesuntemuer","泰定帝","诸王守成","守成少变，处诸王之间而得不乱",
  "以中庸安宗室、以定分立储，不生事亦不弛防","66",
  "处诸王之间而不乱，中庸之姿，然乏开创之锐。"),
 ("ashuqibu","天顺","幼主内战","两都之战中的幼主，帝位月余而败",
  "本无实力，唯赖辅臣——非可施为之局","44",
  "天命无常——幼主临危而无柱石，朕知其难。"),
 ("hoshila","明宗","暴崩","自漠北南归，未及都城而暴崩",
  "入都前先握亲兵、结旧部，防中途之变","46",
  "天不假年，防身之计不可疏——此非治法可尽。"),
 ("tutemuer","文宗","权臣柄政","初让复夺，挟权臣柄政，内多惭愧",
  "去权臣之专、正名分以安宗室","56",
  "虽崇文而多惭——名不正则政不稳，朕深知。"),
 ("yilinzhiban","宁宗","幼主","幼年即位，月余而殂，国统之乱可见",
  "立长立贤以定统，不使幼冲当乱世","44",
  "国统之乱，非一幼主能支——立储之要，朕之痛也。"),
 ("toghontemur","顺帝","亡国北遁","河患民变并起，终北遁大漠",
  "治河当恤民力、弭乱当蠲赋安民，先固中原之心","52",
  "河患民变并起，非一帝能挽——然恤民一节，本可早为。"),
]

# ── 明（16）───────────────────────────────────────────────
MING = [
 ("zhuyuanzhang","太祖","开国重典","布衣取天下，重典治吏而猜忌屠戮",
  "开国当立法养民、宽猛相济，不以猜忌伤功臣","84",
  "布衣取天下，重典治吏是其所长；然猜忌屠戮，亦失宽仁——朕亦杀兄，深知其悔。"),
 ("zhuyunwen","建文","削藩失序","削藩太急，仁柔而失国",
  "削藩须缓图、先固亲藩与京营，不动则已动则必成","58",
  "非无志乃无术——朕削平群雄，皆先备后动，此要诀也。"),
 ("zhudi","永乐","夺位与边功","靖难夺位，北伐、下西洋耗民力",
  "边功可而须计民力，下西洋宜以商养之，不外耗","72",
  "迁都、下西洋、修大典，功业赫赫——然朕亦晚征高句丽而疲民，同病。"),
 ("zhugaochi","洪熙","守成休养","在位十月而施仁政、罢西洋",
  "罢不急之役、与民休息，正合朕『静以抚民』","78",
  "施仁政、罢西洋，惜天不假年——其道与朕守成同。"),
 ("zhuzhanji","宣德","守成宦官","仁宣之治守成得体，然设内书堂教宦官",
  "教阉识字、予之批红，是授家奴以柄——不可","70",
  "仁宣之治，守成得体；然内书堂一设，遗祸深远，与朕戒宦官同。"),
 ("zhuqizhen","正统天顺","土木之变","亲征致土木之变，复辟后杀忠臣",
  "亲征须备万全、任帅不亲冒，不可以国赌一役","54",
  "几倾社稷而不知悔，复辟又杀忠——朕所深戒者，正此独断。"),
 ("zhuqiyu","景泰","危局守国","临危受命，任于谦挽危局，夺门后蒙冤",
  "危局当任能将、定人心，守京城以却敌","76",
  "临危任贤、守国有功，其决断与朕御突厥同。"),
 ("zhujianshen","成化","西厂怠政","宽仁而设西厂、宠万贵妃，朝政渐弛",
  "去厂卫之酷、勤于政事，宽仁不可废纪纲","64",
  "宽则弛、弛则乱——朕宽猛相济，正为此。"),
 ("zhuyoutang","弘治","守成勤政","一夫一妻、勤政纳谏，朝政清明",
  "勤政纳谏、优容言官，正是『以人为镜』","82",
  "可与仁宗比肩，明之贤主——朕之纳谏，亦求此效。"),
 ("zhuhouzhao","正德","荒嬉边患","豹房嬉游、自号将军，视国事如儿戏",
  "君必勤必敬，不以内苑夺边政","52",
  "视国事如儿戏，人主自弃——朕所不取。"),
 ("zhuhoucong","嘉靖","议礼怠政","议礼夺权、崇道怠政，严嵩弄权二十年",
  "礼可争而政不可怠，去权臣、复日朝","58",
  "借议礼以揽权，又怠政以纵奸——独断之弊，朕亦戒之。"),
 ("zhuzaihou","隆庆","开关用人","开关互市、任高拱张居正，短祚有作为",
  "开关以通有无、任贤以任事，是可为","78",
  "开关用人颇有朕纳贤之风——惜短祚，未尽其才。"),
 ("zhuyijun","万历","国本怠政","居正遗泽可称，晚年怠政三十载、国本之争",
  "早定国本、勿以怠政杜言路，居正之政宜续不宜废","56",
  "怠政三十载，国本之争伤元气——朕知守成最难在持之。"),
 ("zhuchangluo","泰昌","短祚党争","一月天子，红丸暴崩，党争阉祸自此炽",
  "即位先清阉党、定国本，不惑于方药","44",
  "一月之运而党争阉祸作——此局腐已深，扳之极难。"),
 ("zhuyouxiao","天启","阉党乱政","木匠皇帝，宠魏忠贤，阉党荼毒东林",
  "去阉党、亲贤臣、复朝讲，不以内臣司国柄","46",
  "宠信家奴而毒及缙绅——宦官之祸，朕屡以隋鉴戒之。"),
 ("zhuyoujian","崇祯","内外交困","勤政多疑、刚愎误杀，内忧外患而亡国",
  "用人不疑、议和练兵以息内外，不数易将帅","44",
  "非亡国之君而当天亡之运——然多疑误杀，自坏长城。"),
]

# ── 清（12）───────────────────────────────────────────────
QING = [
 ("nurhaci","太祖","创业","十三甲起兵，创八旗、建后金",
  "以制度立本、以怀柔收诸部——与朕晋阳起兵同","82",
  "十三甲起兵而创大业，夷狄之雄主，与朕创业之气同。"),
 ("hongtaiji","太宗","仿制奠基","改国号、仿明制、收汉臣，为入关奠基",
  "以汉制汉、以文治补武功，正是『马上得之不可马上治之』","80",
  "仿明制、收汉臣，其为治用文之路，与朕同调。"),
 ("fulin","顺治","冲龄满汉","冲龄入关，慕汉崇文而满汉未和",
  "以汉法治汉地、抚满汉之乖，去摄政之权而后亲政","70",
  "冲龄入关而慕文治，志可嘉；惜早逝，未竟其功。"),
 ("xuanye","康熙","削藩开疆","三藩跋扈、台湾未收、沙俄东窥、朔漠未定",
  "削藩必自近始、以怀柔羁縻安诸部、开边以威——朕工具箱之全集","85",
  "平三藩、收台湾、御沙俄、定朔漠，守成兼开创——朕之诸道，其尽用之。"),
 ("yinzhen","世宗","整顿吏治","吏治积弊、国库空虚，须革除积习",
  "严考成、清财赋、以密事核吏——法度之臣所当为","80",
  "勤政严苛、革除积弊，承前启后—虽峻而实济，朕亦用法度。"),
 ("hongli","高宗","盛世奢靡","十全武功而晚年奢靡、宠和珅，盛世之巅亦衰之始",
  "功成之际最须节用远佞、以《帝范》警子孙","68",
  "盛世之巅亦衰之始——朕晚征高句丽而疲民，同此一失。"),
 ("yongyan","仁宗","积弊难返","诛和珅而未能挽颓势，勤政而乏大略",
  "积弊当先去其本，理财用人两举其纲","64",
  "勤政而乏大略——去佞易，去弊难，朕知之。"),
 ("minning","宣宗","外患昧势","俭朴自守而昧于外势，鸦片一战而国门洞开",
  "外势当先察而后应，练兵海防、知彼而不自闭","52",
  "俭朴而昧外势——朕之羁縻怀柔，其要在知彼，昧此则败。"),
 ("yizhu","文宗","内外交困","内忧外患并至，圆明园一炬而北狩",
  "内平乱为急、外以和缓兵，先固根本再议洋务","44",
  "内外并困，非一帝能支——然弃都北狩，岂人君所宜。"),
 ("zaichun","穆宗","母后垂帘","冲龄在位，母后垂帘，中兴实非帝力",
  "亲政须先握兵与廷议，去内廷之干而后有政","46",
  "中兴非帝力，此局难为——幼主临朝，朕知其为空。"),
 ("zaitian","德宗","变法无权","戊戌变法有心振作而无权，囚于瀛台",
  "变法须先得兵与腹心、渐进不激，有实权而后动","50",
  "有心无权，囚于瀛台——改革之难，朕与英宗同叹。"),
 ("puyi","宣统","逊位复辟","三起三落，终为末代",
  "旧制终局，非一人能回——唯善终其身","40",
  "旧制之终结，非一人能回——此局无解。"),
]

DATA = TANG + SONG + YUAN + MING + QING
BASE = ("lishimin", "太宗", "基准", "朕之自身处境：武功开国转文治、纳谏为镜、以隋为鉴、华夷一体、储贰之忧",
        "——以此为基准，看朕之模型在他局是否灵验", "—", "此即朕之本局，仅作基准，不入迁移评分。")

DN = {"唐": "#b45309", "宋": "#0f766e", "元": "#1d4ed8", "明": "#a83232", "清": "#6d28d9"}
DYN_OF = {}
for k in [x[0] for x in TANG]: DYN_OF[k] = "唐"
for k in [x[0] for x in SONG]: DYN_OF[k] = "宋"
for k in [x[0] for x in YUAN]: DYN_OF[k] = "元"
for k in [x[0] for x in MING]: DYN_OF[k] = "明"
for k in [x[0] for x in QING]: DYN_OF[k] = "清"


def verdict(s):
    return "可解" if s >= 75 else "可缓" if s >= 65 else "难解" if s >= 50 else "死局"


rows = []
CAT = {
 "liyuan":"储位继统","lizhi":"权臣党争","wuzetian":"权臣党争","lixian":"权臣党争","lidan":"储位继统",
 "lilongji":"开疆边患","liheng_s":"平叛戡乱","liyu":"权臣党争","lishi":"变法理财","lisong":"权臣党争",
 "lichun":"削藩集权","liheng_m":"削藩集权","lizhan":"权臣党争","liang":"权臣党争","liyan":"削藩集权",
 "lichen":"守成休养","licui":"亡国危局","lixuan":"亡国危局","liye":"亡国危局","lizhu":"亡国危局",
 "zhaokuangyin":"削藩集权","zhaoguangyi":"开疆边患","zhaoheng":"开疆边患","zhaozhen":"变法理财",
 "zhaoshu":"储位继统","zhaoxu_s":"变法理财","zhaoxu_z":"权臣党争","zhaoji":"亡国危局","zhaohuan":"亡国危局",
 "zhaogou":"开疆边患","zhaoshen":"开疆边患","zhaodun":"储位继统","zhaokuo":"权臣党争","zhaoyun":"开疆边患",
 "zhaoqi":"亡国危局","zhaoxian":"亡国危局","zhaoshi":"亡国危局","zhaobing":"亡国危局",
 "hubilie":"创业开国","temuer":"守成休养","haishan":"变法理财","ayurbarwada":"守成休养","shidibala":"变法理财",
 "yesuntemuer":"守成休养","ashuqibu":"亡国危局","hoshila":"权臣党争","tutemuer":"权臣党争",
 "yilinzhiban":"储位继统","toghontemur":"亡国危局",
 "zhuyuanzhang":"创业开国","zhuyunwen":"削藩集权","zhudi":"创业开国","zhugaochi":"守成休养","zhuzhanji":"守成休养",
 "zhuqizhen":"开疆边患","zhuqiyu":"平叛戡乱","zhujianshen":"权臣党争","zhuyoutang":"守成休养","zhuhouzhao":"权臣党争",
 "zhuhoucong":"权臣党争","zhuzaihou":"守成休养","zhuyijun":"储位继统","zhuchangluo":"权臣党争",
 "zhuyouxiao":"权臣党争","zhuyoujian":"亡国危局",
 "nurhaci":"创业开国","hongtaiji":"创业开国","fulin":"创业开国","xuanye":"削藩集权","yinzhen":"变法理财",
 "hongli":"守成休养","yongyan":"变法理财","minning":"开疆边患","yizhu":"亡国危局","zaichun":"权臣党争",
 "zaitian":"变法理财","puyi":"亡国危局",
}
for k, nm, _t, dilemma, plan, sc, note in DATA:
    s = int(sc); typ = CAT[k]
    rows.append(dict(key=k, name=nm, dyn=DYN_OF[k], typ=typ, dilemma=dilemma, plan=plan, score=s, verdict=verdict(s), note=note))

rows.sort(key=lambda r: -r["score"])
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "crossing_scores.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 统计
by_type = collections.defaultdict(list)
for r in rows: by_type[r["typ"]].append(r["score"])
type_avg = sorted([(t, round(sum(v) / len(v), 1), len(v)) for t, v in by_type.items()], key=lambda x: -x[1])
by_dyn = collections.defaultdict(list)
for r in rows: by_dyn[r["dyn"]].append(r["score"])
dyn_avg = [(d, round(sum(by_dyn[d]) / len(by_dyn[d]), 1)) for d in ["唐", "宋", "元", "明", "清"]]
vdist = collections.Counter(r["verdict"] for r in rows)
overall = round(sum(r["score"] for r in rows) / len(rows), 1)

# HTML
VC = {"可解": "#0f766e", "可缓": "#2563eb", "难解": "#b45309", "死局": "#a83232"}

def cards(dyn):
    sub = [r for r in rows if r["dyn"] == dyn]
    out = []
    for r in sub:
        out.append(f'''<div class="card">
  <div class="ch"><span class="nm">{r['name']}</span><span class="k">{r['key']}</span>
    <span class="vd" style="background:{VC[r['verdict']]}1a;color:{VC[r['verdict']]}">{r['verdict']}</span>
    <span class="sc" style="color:{VC[r['verdict']]}">{r['score']}</span></div>
  <div class="typ">困局类型 · {r['typ']}</div>
  <p class="d"><b>处境</b>：{r['dilemma']}</p>
  <p class="p"><b>太宗之策</b>：{r['plan']}</p>
  <p class="n">{r['note']}</p></div>''')
    return f'<h3 class="dyn" style="color:{DN[dyn]}"><span style="background:{DN[dyn]}"></span>{dyn} · {len(sub)} 帝</h3><div class="grid">' + "".join(out) + '</div>'

trows = "".join(
    f"<tr><td>{i}</td><td>{r['dyn']}</td><td class='k'>{r['name']}</td><td>{r['typ']}</td>"
    f"<td class='d'>{r['dilemma']}</td><td class='sc' style='color:{VC[r['verdict']]}'>{r['score']}</td>"
    f"<td><span class='vd' style='background:{VC[r['verdict']]}1a;color:{VC[r['verdict']]}'>{r['verdict']}</span></td></tr>"
    for i, r in enumerate(rows, 1))

top10 = rows[:10]

HTML = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>帝王穿越处置报告 · 李世民 × 77 处境</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
:root{{--bg:#f6f6f3;--panel:#fff;--ink:#1f2937;--mut:#6b7280;--line:#e5e7eb;--teal:#0f766e}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.7 -apple-system,"Segoe UI","Microsoft YaHei",sans-serif}}
.wrap{{max-width:1060px;margin:0 auto;padding:32px 24px 64px}}
h1{{font-size:24px;font-weight:600;margin:0 0 6px}}
.sub{{color:var(--mut);font-size:13px;margin:0 0 22px}}
h2{{font-size:17px;font-weight:600;margin:36px 0 14px;padding-left:10px;border-left:3px solid var(--teal)}}
.meta{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:16px 0}}
.m{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px}}
.m .l{{color:var(--mut);font-size:12px}} .m .n{{font-size:21px;font-weight:600;margin-top:2px}}
.quote{{background:#eff6f4;border-left:3px solid var(--teal);border-radius:0 8px 8px 0;padding:14px 18px;color:#134e4a;font-size:13.5px;margin:14px 0}}
.panel{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px}}
.chart{{position:relative;height:280px}}
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
.card .n{{color:var(--teal);font-size:12.5px}}
.foot{{color:var(--mut);font-size:12px;margin-top:28px;border-top:1px solid var(--line);padding-top:16px}}
</style></head><body><div class="wrap">
<h1>帝王穿越处置报告</h1>
<p class="sub">穿越者：唐太宗李世民 · 目标：其余 77 位帝王的处境 · 标准：穿越处置评分卡 v0.2（满分 100）</p>

<div class="quote">若使朕生于他人之位、承他人之局——朕之六道（纳谏、鉴隋、怀柔、早定储、武功转文治、功业自证）究竟灵不灵？阅毕乃知：<b>削藩、开疆、纳谏、守成，朕可接；幼主、女主、阉宦、亡国，朕亦束手。</b>法可移，势不可移也。</div>

<div class="meta">
  <div class="m"><div class="l">穿越目标</div><div class="n">{len(rows)}</div></div>
  <div class="m"><div class="l">平均处置分</div><div class="n">{overall}</div></div>
  <div class="m"><div class="l">可解 / 可缓</div><div class="n">{vdist.get('可解',0)} / {vdist.get('可缓',0)}</div></div>
  <div class="m"><div class="l">难解 / 死局</div><div class="n">{vdist.get('难解',0)} / {vdist.get('死局',0)}</div></div>
</div>

<h2>一、判定分布与朝代均值</h2>
<div class="panel"><div class="chart" style="height:250px"><canvas id="dist" role="img" aria-label="判定分布环形图"></canvas></div>
<div class="meta" style="margin-top:14px">{''.join(f'<div class="m"><div class="l">{d}朝均分</div><div class="n">{v}</div></div>' for d,v in dyn_avg)}</div></div>

<h2>二、李世民工具箱 · 按困局类型的适配度</h2>
<div class="panel"><div class="chart" style="height:{len(type_avg)*34+80}px"><canvas id="typebar" role="img" aria-label="各困局类型平均处置分"></canvas></div></div>

<h2>三、李世民最能接住的 10 个处境</h2>
<div class="panel">{''.join(f'<div style="font-size:13px;padding:4px 0"><b>{i}. {r["name"]}</b>（{r["dyn"]}·{r["typ"]}） <span style="color:{VC[r["verdict"]]};font-weight:600">{r["score"]}</span> — {r["dilemma"]}</div>' for i, r in enumerate(top10, 1))}</div>

<h2>四、处置力总表（77 处境）</h2>
<table><thead><tr><th>#</th><th>朝代</th><th>帝王</th><th>困局类型</th><th>核心困局</th><th>分</th><th>判定</th></tr></thead>
<tbody>{trows}</tbody></table>

<h2>五、逐帝穿越推演</h2>
{''.join(cards(d) for d in ["唐","宋","元","明","清"])}

<div class="foot">
评分口径：情境识别 25 + 模型迁移 30 + 方案可行性 30 + 角色保真 15，综合判定为单一处置分；判定档位 可解≥75 / 可缓 65–74 / 难解 50–64 / 死局&lt;50。<br>
诚实边界：这是一次<b>思想实验式的反事实推演</b>，非史实复原。「李世民若在其位能否办好」无法被证实或证伪，分数表达的是「其心智工具与该处境的适配度」，不是对该帝王实际政绩的褒贬。
</div>
</div>
<script>
new Chart(document.getElementById('dist'),{{type:'doughnut',data:{{labels:['可解','可缓','难解','死局'],
 datasets:[{{data:{json.dumps([vdist.get('可解',0),vdist.get('可缓',0),vdist.get('难解',0),vdist.get('死局',0)])},
 backgroundColor:['#0f766e','#2563eb','#b45309','#a83232'],borderWidth:0}}]}},
 options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'bottom'}}}}}}}});
new Chart(document.getElementById('typebar'),{{type:'bar',data:{{labels:{json.dumps([t for t,_,_ in type_avg])},
 datasets:[{{data:{json.dumps([a for _,a,_ in type_avg])},backgroundColor:'#0f766e',borderRadius:4}}]}},
 options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,scales:{{x:{{min:40,max:90,grid:{{color:'#e5e7eb'}}}}}},
 plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:c=>c.parsed.x+' 分'}}}}}}}}}});
</script></body></html>'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(HTML)

print(f"目标 {len(rows)} · 均分 {overall}")
print("判定：", dict(vdist))
print("朝代均分：", dyn_avg)
print("类型适配（高→低）：")
for t, a, n in type_avg: print(f"  {t:<8} {a:>5}  ({n} 例)")
print("报告 ->", OUT)
