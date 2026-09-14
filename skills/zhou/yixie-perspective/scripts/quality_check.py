#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动检查生成的SKILL.md是否通过Phase 4质量标准（修复版）。
修复原版缺陷：原版 source/边界 section 抓取正则带 re.DOTALL 且 .* 贪婪，
凡文中多次出现「来源」「边界」即跨段吞掉整文、捕获为空，导致「一手占比」门禁
对所有文档都返回「未标记→跳过」。本版改为按行定位「## 段落」精确切片。

用法:
    python3 quality_check.py <SKILL.md路径>
"""

import sys
import re
from pathlib import Path


def extract_section(content: str, keywords) -> str | None:
    """按行定位第一个含任一关键字的 `## ` 段落，截取到下一个 `## ` 之前。"""
    if isinstance(keywords, str):
        keywords = [keywords]
    lines = content.split('\n')
    start = None
    for i, line in enumerate(lines):
        if re.match(r'^##\s+', line) and any(k in line for k in keywords):
            start = i
            break
    if start is None:
        return None
    for j in range(start + 1, len(lines)):
        if re.match(r'^##\s+', lines[j]):
            return '\n'.join(lines[start:j])
    return '\n'.join(lines[start:])


def check_mental_models(content: str) -> tuple[bool, str]:
    models = re.findall(r'^###\s+(?:模型|Model|心智模型)\s*\d', content, re.MULTILINE)
    if models:
        count = len(models)
    else:
        in_section = False
        count = 0
        for line in content.split('\n'):
            if re.match(r'^##\s+.*心智模型|Mental Model', line, re.IGNORECASE):
                in_section = True
                continue
            if in_section and re.match(r'^##\s+', line) and '心智模型' not in line:
                break
            if in_section and re.match(r'^###\s+', line):
                count += 1
        if count == 0:
            return False, "未检测到心智模型section"
    passed = 3 <= count <= 7
    return passed, f"{count}个心智模型 {'✅' if passed else '❌ (应为3-7个)'}"


def check_limitations(content: str) -> tuple[bool, str]:
    has_limitation = bool(re.search(r'局限|失效|不适用|盲区|limitation|blind spot', content, re.IGNORECASE))
    return has_limitation, "有局限性标注 ✅" if has_limitation else "❌ 未找到局限性描述"


def check_expression_dna(content: str) -> tuple[bool, str]:
    dna_section = bool(re.search(r'表达DNA|Expression DNA|表达风格', content, re.IGNORECASE))
    if not dna_section:
        return False, "❌ 未找到表达DNA section"
    style_markers = len(re.findall(r'句式|词汇|语气|幽默|节奏|确定性|引用|口头禅|语簇', content))
    passed = style_markers >= 3
    return passed, f"表达DNA特征: {style_markers}项 {'✅' if passed else '❌ (应≥3项)'}"


def check_honest_boundary(content: str) -> tuple[bool, str]:
    boundary_text = extract_section(content, ['诚实边界', 'Honest Boundary'])
    if not boundary_text:
        return False, "❌ 未找到诚实边界section"
    items = re.findall(r'^[-*]\s+', boundary_text, re.MULTILINE)
    count = len(items)
    passed = count >= 3
    return passed, f"诚实边界: {count}条 {'✅' if passed else '❌ (应≥3条)'}"


def check_tensions(content: str) -> tuple[bool, str]:
    tension_markers = len(re.findall(r'张力|矛盾|tension|paradox|一方面.*另一方面|既.*又', content, re.IGNORECASE))
    passed = tension_markers >= 2
    return passed, f"内在张力: {tension_markers}处 {'✅' if passed else '❌ (应≥2处)'}"


def check_primary_sources(content: str) -> tuple[bool, str]:
    source_text = extract_section(content, ['来源', 'Source', 'Reference'])
    if not source_text:
        return True, "未找到来源section（跳过检查）"
    primary = len(re.findall(r'一手|primary|本人著作|原始|实物|考古|甲骨文|金文|地质', source_text, re.IGNORECASE))
    secondary = len(re.findall(r'二手|secondary|转述|评论|后世文献', source_text, re.IGNORECASE))
    total = primary + secondary
    if total == 0:
        return True, "未标记来源类型（跳过检查）"
    ratio = primary / total
    passed = ratio > 0.5
    return passed, f"一手来源占比: {primary}/{total} ({ratio:.0%}) {'✅' if passed else '❌ (应>50%)'}"


def main():
    if len(sys.argv) < 2:
        print("用法: python3 quality_check.py <SKILL.md路径>")
        sys.exit(1)
    skill_path = Path(sys.argv[1])
    if not skill_path.exists():
        print(f"❌ 文件不存在: {skill_path}")
        sys.exit(1)
    content = skill_path.read_text(encoding='utf-8')
    checks = [
        ("心智模型数量", check_mental_models),
        ("模型局限性", check_limitations),
        ("表达DNA辨识度", check_expression_dna),
        ("诚实边界", check_honest_boundary),
        ("内在张力", check_tensions),
        ("一手来源占比", check_primary_sources),
    ]
    print(f"质量检查: {skill_path.name}")
    print("=" * 50)
    passed_count = 0
    total = len(checks)
    for name, check_fn in checks:
        passed, detail = check_fn(content)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name:<12} {status}  {detail}")
        if passed:
            passed_count += 1
    print("=" * 50)
    print(f"结果: {passed_count}/{total} 通过")
    if passed_count == total:
        print("🎉 全部通过，可以交付")
    elif passed_count >= total - 1:
        print("⚠️ 基本通过，建议修复不通过项后交付")
    else:
        print("❌ 多项不通过，建议回到Phase 2迭代")
    sys.exit(0 if passed_count == total else 1)


if __name__ == '__main__':
    main()
