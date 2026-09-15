# -*- coding: utf-8 -*-
"""年表一致性独立复核（口径 C-定稿）：只读，检查 skills/shang 逐王 era 链。
规则（公元前的数字越大＝越早）：
  相邻 i → i+1（后世）要求：起年[i+1] <= 止年[i]   → 否则为「重叠」（错）
                             起年[i+1] <  起年[i]   → 否则为「倒置」（错）
  止年[i] - 起年[i+1] = 空档（允许，商前期不可闭合）
  另外：era 必须含限定语（含「非定点」或「仅示相对先后」），且 description 中的年份区间须与 era 一致。
输出同时写 UTF-8 到 _era_check.txt。
"""
import re
from pathlib import Path

_BUF = []
_op = print


def print(*a, **k):  # noqa: A001
    _BUF.append(" ".join(str(x) for x in a))
    _op(*a, **k)


ROOT = Path(r"D:/2026/WB项目/emperor-skill/skills/shang")

# 商王世次（《殷本纪》序）
ORDER = [
    ("tang-shang-perspective", "汤"), ("taiding-shang-perspective", "太丁"),
    ("waibing-perspective", "外丙"), ("zhongren-shang-perspective", "中壬"),
    ("taijia-perspective", "太甲"), ("woding-perspective", "沃丁"),
    ("taigeng-perspective", "太庚"), ("xiaojia-shang-perspective", "小甲"),
    ("yongji-perspective", "雍己"), ("taiwu-perspective", "太戊"),
    ("zhongding-perspective", "中丁"), ("wairen-perspective", "外壬"),
    ("hedanja-perspective", "河亶甲"), ("zuyi-perspective", "祖乙"),
    ("zuxin-perspective", "祖辛"), ("wojia-perspective", "沃甲"),
    ("zuding-shang-perspective", "祖丁"), ("nangeng-perspective", "南庚"),
    ("yangjia-perspective", "阳甲"), ("pangeng-perspective", "盘庚"),
    ("xiaoxin-shang-perspective", "小辛"), ("xiaoyi-shang-perspective", "小乙"),
    ("wuding-perspective", "武丁"), ("zugeng-perspective", "祖庚"),
    ("zujia-perspective", "祖甲"), ("linxin-perspective", "廪辛"),
    ("kangding-perspective", "康丁"), ("wuyi-perspective", "武乙"),
    ("wending-shang-perspective", "文丁"), ("diyi-perspective", "帝乙"),
    ("dixin-perspective", "帝辛"),
]

RANGE_RE = re.compile(r"约前(\d{3,4})\s*[–\-—~至]\s*约前(\d{3,4})")
SINGLE_RE = re.compile(r"约前(\d{3,4})")
CENTURY_RE = re.compile(r"约前(\d{1,2})世纪")


def get_field(txt, key):
    m = re.search(r"^" + key + r":\s*(.+)$", txt, re.M)
    return m.group(1).strip() if m else ""


rows = []
for pkg, name in ORDER:
    d = ROOT / pkg
    sk = d / "SKILL.md"
    if not sk.is_file():
        rows.append((pkg, name, None, None, "缺 SKILL.md", "", ""))
        continue
    txt = sk.read_text(encoding="utf-8", errors="replace")
    era = get_field(txt, "era")
    desc = get_field(txt, "description")
    m = RANGE_RE.search(era)
    if m:
        hi, lo = int(m.group(1)), int(m.group(2))
    else:
        mc = CENTURY_RE.search(era)
        ms = SINGLE_RE.search(era)
        hi = lo = None
        note = "世纪式" if mc else ("单点" if ms else "无可解析区间")
    lim = ("非定点" in era) or ("仅示相对先后" in era)
    dm = RANGE_RE.search(desc)
    desc_ok = (dm is None) or (m and (int(dm.group(1)), int(dm.group(2))) == (hi, lo))
    rows.append((pkg, name, hi, lo, "", era, f"desc={desc_ok} 限定语={lim}"))

print("=" * 100)
print("商王 era 链（口径 C-定稿复核）")
print("=" * 100)
print(f"{'#':>2} {'王':<6} {'起':>5} {'止':>5} {'空档':>5}  状态 / era")
prev_hi = prev_lo = None
prev_name = ""
errs, warns = [], []
for idx, (pkg, name, hi, lo, hard, era, extra) in enumerate(rows, 1):
    if hard:
        print(f"{idx:>2} {name:<6} {'-':>5} {'-':>5} {'-':>5}  ! {hard}")
        errs.append(f"{name}: {hard}")
        continue
    if hi is None:
        if pkg == "taiding-shang-perspective":
            # 太丁「未立而卒」，无在位区间，单点＋相对位置表述属合规写法
            print(f"{idx:>2} {name:<6} {'单点':>5} {'-':>5} {'-':>5}  OK（未立而卒，单点式合规）")
            prev_name = name
            continue
        print(f"{idx:>2} {name:<6} {'-':>5} {'-':>5} {'-':>5}  ! 无区间式 era（{era[:40]}）")
        errs.append(f"{name}: era 非区间式 -> {era[:60]}")
        prev_hi = prev_lo = None
        prev_name = name
        continue
    gap = "-"
    status = []
    if prev_lo is not None:
        gapv = prev_lo - hi          # 止年[前] - 起年[本]
        gap = str(gapv)
        if gapv < 0:
            status.append(f"!! 重叠 {abs(gapv)} 年（起年晚于前王止年）")
            errs.append(f"{name} 与 {prev_name} 重叠 {abs(gapv)} 年")
        if hi >= prev_hi:
            status.append("!! 倒置（起年不早于前王起年）")
            errs.append(f"{name} 起年 {hi} >= {prev_name} 起年 {prev_hi}")
    if "限定语=False" in extra:
        status.append("!! 缺限定语")
        errs.append(f"{name}: era 缺 C1/C2 限定语")
    if "desc=False" in extra:
        status.append("!! description 年份与 era 不一致")
        errs.append(f"{name}: description 年份与 era 不一致")
    print(f"{idx:>2} {name:<6} {hi:>5} {lo:>5} {gap:>5}  {'OK' if not status else ' | '.join(status)}")
    if status:
        print(f"      era: {era[:110]}")
    prev_hi, prev_lo, prev_name = hi, lo, name

print("\n" + "=" * 100)
print(f"硬错误 {len(errs)}")
for e in errs:
    print("  ! " + e)
print("（空档【允许】：商前期积年不可闭合，空档＝诚实；重叠/倒置＝错误）")

Path(r"D:/2026/WB项目/emperor-skill/_redo_tools/_era_check.txt").write_text("\n".join(_BUF), encoding="utf-8")
