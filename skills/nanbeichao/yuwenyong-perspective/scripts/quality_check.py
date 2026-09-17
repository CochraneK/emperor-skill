from pathlib import Path
import sys
r=Path(__file__).resolve().parents[1];s=(r/'SKILL.md').read_text(encoding='utf-8')
if 'RICH-EVIDENCE' not in s or '宇文护' not in s or '社会成本' not in s or len(list((r/'references/research').glob('*.md')))!=6:sys.exit(1)
print('PASS')
