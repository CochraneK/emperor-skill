import subprocess
py = r"C:/Users/cunyi/.workbuddy/binaries/python/versions/3.13.12/python.exe"
target = r"D:/2026/WB项目/emperor-skill/skills/qin/ziying-perspective/SKILL.md"
qc = r"D:/2026/WB项目/emperor-skill/skills/qin/ziying-perspective/scripts/quality_check.py"
out = subprocess.run([py, qc, target], capture_output=True, text=True, encoding="utf-8")
open(r"D:/2026/WB项目/emperor-skill/skills/qin/ziying-perspective/scripts/_qc_report.txt","w",encoding="utf-8").write("RC=%d\n%s%s"%(out.returncode,out.stdout,out.stderr))
