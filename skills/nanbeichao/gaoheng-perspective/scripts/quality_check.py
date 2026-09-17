from pathlib import Path
import sys
r=Path(__file__).resolve().parents[1];s=(r/'SKILL.md').read_text(encoding='utf-8')
req=['LIMITED-EVIDENCE','STRUCTURALLY_UNOBSERVABLE','不建立个人表达 DNA','## 诚实边界']
if any(x not in s for x in req) or len(list((r/'references/research').glob('*.md')))!=6:sys.exit(1)
print('PASS')
