from pathlib import Path
import sys
r=Path(__file__).resolve().parents[1]; s=(r/'SKILL.md').read_text(encoding='utf-8')
req=['evidence_level: MODERATE-EVIDENCE','## 核心心智模型','## 诚实边界','高欢','高澄']
missing=[x for x in req if x not in s]
research=list((r/'references/research').glob('*.md'))
if missing or len(research)!=6:
 print('FAIL',missing,len(research)); sys.exit(1)
print('PASS: mechanical MODERATE-EVIDENCE checks; no semantic L3 verdict.')
