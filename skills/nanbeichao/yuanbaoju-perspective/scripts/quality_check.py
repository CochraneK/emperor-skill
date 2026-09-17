from pathlib import Path
import sys
r=Path(__file__).resolve().parents[1]; s=(r/'SKILL.md').read_text(encoding='utf-8')
req=['evidence_level: MODERATE-EVIDENCE','宇文泰','名分','## 诚实边界']
res=list((r/'references/research').glob('*.md'))
if any(x not in s for x in req) or len(res)!=6: print('FAIL'); sys.exit(1)
print('PASS: mechanical MODERATE-EVIDENCE checks only.')
