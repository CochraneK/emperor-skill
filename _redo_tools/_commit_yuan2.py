# -*- coding: utf-8 -*-
"""提交 + 推送：元定宗贵由、元宪宗蒙哥两包。"""
import subprocess, os, tempfile

REPO = r"D:/2026/WB项目/emperor-skill"

MSG = """补元前四汗之三·四：元定宗贵由、元宪宗蒙哥

- 新增 skills/yuan/guyuk-perspective（元定宗 贵由，1246–1248）
- 新增 skills/yuan/mongke-perspective（元宪宗 蒙哥，1251–1259）
- 两包均 6/6；经 _verify_pkgs.py 独立复核：硬错误 0、警告 0
- 我另修 1 处生成杂讯：guyuk 06-timeline.md 的「清old宠」改为「清旧宠」

门禁落实：
· 生前均未称帝，庙号系忽必烈立元后追尊；《元史》本纪「即皇帝位」已注明是明初修史追述语
· 空档未冒充连续：1242–1246 乃马真称制、1248–1251 三岁无君（引《元史》原句）、
  1251 前海迷失后称制，均单列
· 记载稀薄如实交代：贵由本纪不足四百字、无一条君臣问答；唯一存世亲署文书
  （1246 年答英诺森四世诏书）标为波斯文经多层转译、只述其意
· 四源歧异并列不调和：汉文《元史》/《蒙古秘史》/波斯文《史集》《世界征服者史》/
  拉丁文使节行纪
· 死因诸说并存：贵由（病死/鸩毒/为拔都人所害）、蒙哥（本纪只书崩于钓鱼山，
  宋方与域外另有中矢、中炮之说）均不作择一
· 修史者论赞与本人主张分离，蒙哥卷末「刚明雄毅……酷信巫觋卜筮」标注为明初史官评语

元前四汗至此补齐，元朝由 11/15 变为 15/15。
"""

ADD = ["skills/yuan/guyuk-perspective", "skills/yuan/mongke-perspective"]


def run(args):
    p = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


lock = os.path.join(REPO, ".git", "index.lock")
if os.path.exists(lock):
    os.remove(lock)
    print("[clean] index.lock")

for a in ADD:
    rc, out, err = run(["git", "add", "--", a])
    print(f"[add {a}] rc={rc}", err or "")

rc, out, err = run(["git", "status", "--porcelain"])
print("\n[status]")
print(out)

msg_path = os.path.join(tempfile.gettempdir(), "_es_msg5.txt")
open(msg_path, "w", encoding="utf-8").write(MSG)
rc, out, err = run(["git", "commit", "-F", msg_path])
print("\n[commit] rc=", rc)
print(out or "(no output)")
if err:
    print("STDERR:", err)

if rc == 0:
    rc, out, err = run(["git", "push", "origin", "main"])
    print("\n[push] rc=", rc)
    if err:
        print("STDERR:", err)

rc, out, err = run(["git", "log", "--oneline", "-1"])
print("[HEAD]", out)
