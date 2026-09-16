# -*- coding: utf-8 -*-
"""把北朝第三批（限流中断）5 个残缺包搬出 skills/ 到 _pending/bei3/，避免污染 audit 口径。
保留残缺内容（不删除），待额度恢复后重派补全。
"""
import os, shutil

ES = r"D:/2026/WB项目/emperor-skill/skills/nanbeichao"
PEND = r"D:/2026/WB项目/emperor-skill/_pending/bei3"
os.makedirs(PEND, exist_ok=True)

IDS = ["yuanye", "yuanguan", "yuanlang", "yuanxiu", "yuanzhao"]
for sid in IDS:
    src = os.path.join(ES, sid + "-perspective")
    dst = os.path.join(PEND, sid + "-perspective")
    if not os.path.isdir(src):
        print("  跳过(不存在):", sid); continue
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.move(src, dst)
    n = sum(len(fs) for _, _, fs in os.walk(dst))
    print(f"  移动 {sid}-perspective （{n} 文件） -> _pending/bei3/")

# 追加 .gitignore
gi = r"D:/2026/WB项目/emperor-skill/.gitignore"
s = open(gi, encoding="utf-8").read()
if "_pending/" not in s:
    s = s.rstrip("\n") + "\n\n# 限流中断的残缺包暂存区（待重派补全，不入库）\n_pending/\n"
    open(gi, "w", encoding="utf-8").write(s)
    print("  .gitignore: 追加 _pending/")
else:
    print("  .gitignore: 已含 _pending/")

print("\n=== 残缺包已搬离 skills/ ===")
# 复核 skills/nanbeichao 现存包数
left = [d for d in os.listdir(ES) if os.path.isdir(os.path.join(ES, d))]
print(f"skills/nanbeichao 现存包数: {len(left)}")
