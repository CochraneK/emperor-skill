# -*- coding: utf-8 -*-
"""全仓 nuwa 合规体检（不采信自报，全部自跑）
判据：
 A 结构：包内恰好 8 文件（SKILL.md + 6 底稿 + scripts/quality_check.py）
 B 六维：01-06 齐全，各 ≥2500B，末页含「排除声明」
 C 质检：复用 quality_check.py 的 6 个 check 函数，须 6/6
 D 体量：SKILL.md > 1KB
 E 纪律：SKILL.md 中「诚实边界」四字恰好 1 次
 F frontmatter：module / group 存在且非空
 G 顺序（用户关注）：SKILL.md mtime 是否早于任一底稿 → 倒序嫌疑；mtime 全部相同 → 无法判定
输出落盘 _audit_nuwa_all.txt
"""
import pathlib, re, importlib.util, sys

ES = pathlib.Path(r"D:/2026/WB项目/emperor-skill")
SKILLS = ES / "skills"
QC_SRC = None  # 延迟：取第一个找到的 quality_check.py
out = []
def w(s=""): out.append(str(s))

def load_qc(path):
    spec = importlib.util.spec_from_file_location("qc_mod", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

DIMS = ["01-writings", "02-conversations", "03-expression-dna",
        "04-external-views", "05-decisions", "06-timeline"]

pkgs = []
for d in sorted([p for p in SKILLS.iterdir() if p.is_dir()]):
    for p in sorted([x for x in d.iterdir() if x.is_dir()]):
        if (p / "SKILL.md").exists():
            pkgs.append((d.name, p))

qc_mod = None
bad, suspect_order, ok = [], [], []
reasons_stat = {}

for dyn, p in pkgs:
    sid = p.name
    files = sorted([f for f in p.rglob("*") if f.is_file()])
    rel = [str(f.relative_to(p)).replace("\\", "/") for f in files]
    issues = []

    # A 结构
    if len(files) != 8:
        issues.append(f"文件数={len(files)}(应8): {rel}")

    # B 六维
    dims_ok = True
    for n in DIMS:
        f = p / "references/research" / (n + ".md")
        if not f.exists():
            issues.append(f"缺 {n}.md"); dims_ok = False; continue
        b = f.stat().st_size
        if b < 2500:
            issues.append(f"{n}.md 仅 {b}B"); dims_ok = False
        if "排除声明" not in f.read_text(encoding="utf-8", errors="ignore"):
            issues.append(f"{n}.md 无排除声明"); dims_ok = False

    # D/E/F
    sk = p / "SKILL.md"
    t = sk.read_text(encoding="utf-8", errors="ignore")
    if sk.stat().st_size <= 1024:
        issues.append(f"SKILL.md 仅 {sk.stat().st_size}B")
    n_hb = t.count("诚实边界")
    if n_hb != 1:
        issues.append(f"「诚实边界」出现 {n_hb} 次(应1)")
    m = re.search(r'^module:\s*(.+?)[ \t\r]*$', t, re.M)
    g = re.search(r'^group:\s*(.+?)[ \t\r]*$', t, re.M)
    if not (m and m.group(1).strip()): issues.append("module 缺失")
    if not (g and g.group(1).strip()): issues.append("group 缺失")

    # C 质检（复用官方脚本）
    qc = p / "scripts/quality_check.py"
    if not qc.exists():
        issues.append("缺 quality_check.py")
    else:
        if qc_mod is None:
            qc_mod = load_qc(qc)
        res = []
        for name, fn in [("心智模型", qc_mod.check_mental_models),
                         ("局限", qc_mod.check_limitations),
                         ("表达DNA", qc_mod.check_expression_dna),
                         ("诚实边界", qc_mod.check_honest_boundary),
                         ("张力", qc_mod.check_tensions),
                         ("一手占比", qc_mod.check_primary_sources)]:
            passed, detail = fn(t)
            if not passed:
                res.append(f"{name}:{detail}")
        if res:
            issues.append("质检未过 → " + " | ".join(res))

    # G 顺序（mtime）
    sk_m = sk.stat().st_mtime
    dim_ms = []
    for n in DIMS:
        f = p / "references/research" / (n + ".md")
        if f.exists():
            dim_ms.append(f.stat().st_mtime)
    order_note = "无法判定(时间相同/缺底稿)"
    if dim_ms:
        if max(dim_ms) > sk_m + 1:
            order_note = f"倒序嫌疑(SKILL早于底稿 {int(max(dim_ms)-sk_m)}s)"
            suspect_order.append((dyn, sid, order_note))
        elif min(dim_ms) == sk_m and max(dim_ms) == sk_m:
            order_note = "无法判定(时间相同)"
        else:
            order_note = "正序(SKILL不早于底稿)"

    if issues:
        bad.append((dyn, sid, issues))
        for i in issues:
            key = i.split("(")[0].split(":")[0][:28]
            reasons_stat[key] = reasons_stat.get(key, 0) + 1
    else:
        ok.append((dyn, sid, order_note))

w(f"== 全仓 nuwa 合规体检（emperor-skill / skills） ==")
w(f"扫描包数: {len(pkgs)}")
w(f"合规: {len(ok)}")
w(f"不合规: {len(bad)}")
w(f"倒序嫌疑(结构仍合规): {len(suspect_order)}")
w("")
if bad:
    w("== 不合规清单 ==")
    for dyn, sid, iss in bad:
        w(f"  [{dyn}] {sid}")
        for i in iss:
            w(f"       - {i}")
    w("")
    w("== 问题类型统计 ==")
    for k, v in sorted(reasons_stat.items(), key=lambda x: -x[1]):
        w(f"   {k:<30} {v}")
    w("")

if suspect_order:
    w("== 倒序嫌疑（SKILL.md 早于底稿，结构合规但可能未按 nuwa 正序） ==")
    for dyn, sid, note in suspect_order:
        w(f"  [{dyn}] {sid}  {note}")
    w("")

w("== 各朝代合规/总数 ==")
stat = {}
for dyn, p in pkgs:
    stat[dyn] = stat.get(dyn, [0, 0])
    stat[dyn][1] += 1
okset = {(d, s) for d, s, _ in ok}
for dyn, p in pkgs:
    if (dyn, p.name) in okset:
        stat[dyn][0] += 1
for k in sorted(stat):
    w(f"   {k:<14} {stat[k][0]}/{stat[k][1]}")

(ES / "_redo_tools/_audit_nuwa_all.txt").write_text("\n".join(out), encoding="utf-8")
print(f"包数 {len(pkgs)} 合规 {len(ok)} 不合规 {len(bad)} 倒序嫌疑 {len(suspect_order)}")
