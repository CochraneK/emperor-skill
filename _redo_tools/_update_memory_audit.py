# -*- coding: utf-8 -*-
"""记忆更新：MEMORY.md 新增硬规则⑨（nuwa 合规真口径 + 全仓实测）；日志追加"""
import pathlib
MS = pathlib.Path(r"D:/2026/WB项目/蒸馏skill")
MEM = MS / ".workbuddy/memory/MEMORY.md"
LOG = MS / ".workbuddy/memory/2026-09-16.md"

def rep(t, old, new, n=1):
    c = t.count(old)
    assert c == n, f"锚点命中 {c} 次(期望{n}): {old[:50]}"
    return t.replace(old, new)

t = MEM.read_text(encoding="utf-8")
anchor = "**不得直接补底稿交付**，须以六维为唯一依据重写 SKILL.md（旧版降为对照稿，不参与交付）。"
new9 = anchor + """

⑨ **nuwa 合规「真口径」（2026-09-16 全仓实测，此前「184/184」「265/265」均为**旧口径**、已作废）**：
- 旧口径只查「六维齐全 + SKILL.md>1KB + 包内有 quality_check.py」，**从未真正跑门禁**，故长期虚报全合规。
- **真口径（六项全过才算合规）**：① 包内恰 8 文件；② 六维各 ≥2.5KB **且末页含「排除声明」**；
  ③ `quality_check.py` 实跑 **6/6**；④ SKILL.md >1KB；⑤ 「诚实边界」四字全文**恰 1 次**；⑥ frontmatter module/group 非空。
- **实测**：266 包 → 合规 **128**；批量补排除声明（655 份，安全性已验证：全仓 37 处黑名单词**均为排除性声明自身**，
  无一作为来源引用）后 → 合规 **174**，剩 **92 包**卡点纯粹是「底稿体量不足 2.5KB」（每包 1–3 份），需实质扩写。
- 工具：`emperor-skill/_redo_tools/_audit_nuwa_all.py`（全仓体检，复用官方 qc 函数）、`_fix_decl.py`（幂等补声明）。
- **倒序嫌疑 39 个**（SKILL.md mtime 早于底稿 = 先出 SKILL 后补底稿）清单见
  `emperor-skill/_redo_tools/_order_suspects_39.md`。⚠️ 该 mtime 判据在补声明后**已失效**（计数虚增至 166），
  以该 md 快照为准；这批结构合规、内容可用，仅流程是倒的，优先级低于 92 个扩写包。
- ⚠️ 副作用：`_fix_decl.py` 用 `read_text/write_text` 重写，底稿换行由 CRLF 转 LF（diff 变大但内容无改）。"""
t = rep(t, anchor, new9)
MEM.write_text(t, encoding="utf-8")
print("MEMORY.md updated")

add = """

## 全仓 nuwa 合规体检（重大口径纠正）

- **发现**：此前「184/184」「265/265 合规」是**旧口径**（六维齐全+SKILL>1KB+有 qc 脚本），从未实跑门禁，长期虚报。
  新写 `_audit_nuwa_all.py`（真跑 quality_check 6 项 + 8 文件 + 六维 ≥2.5KB + 排除声明 + 「诚实边界」=1 + module/group）。
- **结果**：266 包 → 合规 128。主因：早期批次（周 2/37、唐 0/21、宋 0/18、东汉 0/13、清 0/12、明 1/16、元 3/15）
  底稿缺「排除声明」且普遍 <2.5KB；后期重跑的夏 17/17、两晋 15/15、三国 11/11、南北朝 36/37 全合规。
- **修复第一步**：先验证「老底稿是否真引过黑名单」——37 处命中经查**全部是排除性声明自身**（禁用/未使用/未引），
  无一作为来源引用 → 追加标准排除声明是安全且真实的。批量补 655 份后合规 **128→174**（剩 92 包，卡点纯为体量不足）。
- **倒序证据**：追加前 mtime 比对得 39 个「SKILL.md 早于底稿」包（商 12、南��朝 13、两晋 7…），
  已固化到 `_redo_tools/_order_suspects_39.md`（补声明后该判据失效，计数虚增到 166）。
- **同步**：emperor-skill `7e02b0b`（659 files）已 push。
- **下一步待办**：① 92 个体量不足包扩写（worker 批次，间断回收）② 39 个倒序包按六维重蒸馏 SKILL.md ③ 继续新增北朝（元恭已开工）。
"""
LOG.write_text(LOG.read_text(encoding="utf-8").rstrip() + "\n" + add, encoding="utf-8")
print("log appended")
