# 04 外部评价 / 史学争议 · 刘准

## 1. 《宋书》：以本纪形式承认其皇帝 episode

沈约《宋书》为刘准立《顺帝纪》，明确记录其出身、即位、升明年间政务、禅位以及死后谥号。这一编纂安排确认他属于刘宋帝统中的实际皇帝 episode。

但《宋书》成书于南齐/梁政治环境之后，其对宋齐易代的措辞需要与《南史》《资治通鉴》及后世史论互校。

## 2. 《南史》：更直接展示强制退位与被杀

《南史》卷三对禅位场景保留更多戏剧性细节：王敬则列兵殿庭，刘准藏于佛盖之下，太后令宦官寻找并扶出；退位后迁居、受兵力监视，最终被守卫杀死。

这些细节使“禅让”不能只按制度文本理解，而必须同时记录 coercion / military pressure。

## 3. 后世史论对“禅让”叙事的质疑

明清以来史家常把魏晋南北朝的禅代与废君被杀联系起来讨论。《史纠》等后世史论批评史书用“薨”“殂”等较中性措辞淡化被杀事实。

这些评价不是刘准时代的一手证据，但说明 historiography 层需要保留：

- official transfer narrative；
- coercive transfer evidence；
- post-transfer killing；
- later moral interpretation。

## 4. 出生与亲生父系的异说

《宋书·顺帝纪》称刘准为宋明帝第三子。后世相关传记材料存在关于宋明帝诸子生父问题的异说。项目当前以本纪的 canonical genealogy 为主，但应允许 `parentage_confidence / contested_genealogy` 字段，而不是把异说静默删掉或直接替换正典身份。

## 5. “亡国之君”标签的边界

刘准确实是刘宋最后一位皇帝，但他在位时年幼，实际政局由萧道成等主导。将刘宋灭亡的制度、军事和精英政治责任全部归给刘准本人属于明显的 attribution error。

## 对项目的意义

刘准是变量层很好的案例：

- `dynasty_terminal_ruler = TRUE`
- `personal_agency_evidence = LOW`
- `effective_power_holder != nominal_ruler`
- `forced_abdication = TRUE`
- `post_abdication_killing = TRUE`
- `court_edicts_exist = TRUE`
- `personal_authorship_of_edicts = UNVERIFIED`

## 来源

- 《宋书》卷十《顺帝纪》
- 《南史》卷三《宋本纪下》
- 后世史论《史纠》相关条目（仅作接受史/史学批评材料）
