#!/usr/bin/env python3
"""Derive QA and work queues from generated ruler-corpus coverage.

This script consumes, but does not modify, the hand-researched segmented master files.
It turns identity/coverage state into deterministic queues that humans/agents can work
through without re-deciding scope on every run.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSESSMENT = ROOT / "assessment"

MAJOR_POST_QIN_POLITIES = {
    "秦帝国", "西汉", "东汉", "曹魏", "蜀汉", "孙吴", "西晋", "东晋",
    "刘宋", "南齐", "南梁", "陈", "北魏", "东魏", "西魏", "北齐", "北周",
    "隋", "唐", "武周", "后梁", "后唐", "后晋", "后汉", "后周", "北宋", "南宋",
    "辽", "西辽", "西夏", "金", "大元", "明", "清",
}
EARLY_FILES = {
    "data/rulers-master-h1-early.json", "data/rulers-master-h2-preqin.json",
    "data/ruler-candidates-preqin-other.json", "data/legendary-rulers.json",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def suspicious_name(name: str) -> list[str]:
    reasons: list[str] = []
    if "/" in name or "／" in name:
        reasons.append("VARIANT_STRING_NOT_NORMALIZED")
    if any(x in name for x in ("其他", "等", "不详", "候选")):
        reasons.append("POSSIBLE_NON_PERSON_PLACEHOLDER")
    if len(name) >= 9:
        reasons.append("LONG_COMPOSITE_NAME_REVIEW")
    # Common manual-enumeration artifact: title + personal name concatenated, e.g. 代王嘉赵嘉.
    if re.search(r"(?:王|公|侯|帝).{1,4}(?:赵|刘|李|朱|司马|慕容|拓跋|元|萧|陈|高|宇文|完颜|耶律|段|田|熊|姬|嬴).+", name):
        reasons.append("TITLE_PLUS_PERSON_COMPOSITE_REVIEW")
    return reasons


def queue_class(person: dict[str, Any]) -> str:
    status = person.get("corpus_status")
    sources = set(person.get("source_files", []))
    polities = set(person.get("polities", []))
    if status == "REVIEW":
        return "Q1_SCOPE_OR_IDENTITY_REVIEW"
    if status == "EXTENDED":
        return "Q2_EXTENDED_REVIEW"
    if status == "LEGENDARY":
        return "Q3_LEGENDARY_LIMITED_EVIDENCE"
    if status != "CORE":
        return "Q4_OTHER_REVIEW"
    if sources & EARLY_FILES:
        return "D_CORE_EARLY_OR_PREQIN_MISSING"
    if polities & MAJOR_POST_QIN_POLITIES:
        return "A_CORE_MAJOR_SEQUENCE_MISSING"
    return "B_CORE_PARALLEL_POLITY_MISSING"


def build() -> tuple[dict[str, Any], dict[str, Any], str]:
    gap = load(DATA / "corpus-gap.json")
    index = load(DATA / "rulers-person-index.json")
    inv = load(DATA / "existing-skill-person-map.json")

    by_id = {p["candidate_id"]: p for p in index["persons"]}

    # Reverse mapping: each existing Skill should normally resolve to exactly one candidate person.
    skill_to_people: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    person_multi_skill: list[dict[str, Any]] = []
    for row in gap.get("person_matches", []):
        paths = row.get("matched_skill_paths", [])
        if len(paths) > 1:
            person_multi_skill.append({
                "candidate_id": row["candidate_id"], "canonical_name": row["canonical_name"],
                "matched_skill_paths": paths,
            })
        for path in paths:
            skill_to_people[path].append({"candidate_id": row["candidate_id"], "canonical_name": row["canonical_name"]})
    skill_collisions = [
        {"skill_path": path, "matched_people": people}
        for path, people in sorted(skill_to_people.items()) if len(people) > 1
    ]

    # Candidate identity hints should not silently identify multiple person records.
    hint_to_people: defaultdict[str, set[str]] = defaultdict(set)
    for p in index["persons"]:
        for hint in p.get("identity_hints", []):
            if len(hint) >= 2:
                hint_to_people[hint].add(p["candidate_id"])
    identity_hint_collisions = []
    for hint, ids in sorted(hint_to_people.items()):
        if len(ids) <= 1:
            continue
        people = [{"candidate_id": i, "canonical_name": by_id[i]["canonical_name"], "polities": by_id[i].get("polities", [])} for i in sorted(ids)]
        identity_hint_collisions.append({"identity_hint": hint, "people": people})

    name_issues = []
    for p in index["persons"]:
        reasons = suspicious_name(p["canonical_name"])
        if reasons:
            name_issues.append({
                "candidate_id": p["candidate_id"], "canonical_name": p["canonical_name"],
                "corpus_status": p["corpus_status"], "polities": p.get("polities", []),
                "source_files": p.get("source_files", []), "reasons": reasons,
            })

    unresolved_skills = gap.get("unmatched_existing_skills", [])
    scope_exceptions = gap.get("scope_exception_existing_skills", [])

    issues = {
        "schema_version": "1.0",
        "status": "GENERATED_QA",
        "summary": {
            "skill_to_multiple_person_collisions": len(skill_collisions),
            "person_to_multiple_skill_matches": len(person_multi_skill),
            "identity_hint_collisions": len(identity_hint_collisions),
            "suspicious_canonical_names": len(name_issues),
            "unresolved_existing_skills": len(unresolved_skills),
            "scope_exception_existing_skills": len(scope_exceptions),
        },
        "skill_to_multiple_person_collisions": skill_collisions,
        "person_to_multiple_skill_matches": person_multi_skill,
        "identity_hint_collisions": identity_hint_collisions,
        "suspicious_canonical_names": name_issues,
        "unresolved_existing_skills": unresolved_skills,
        "scope_exception_existing_skills": scope_exceptions,
    }

    work: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in gap.get("missing_core", []):
        p = by_id.get(row["candidate_id"], row)
        cls = queue_class(p)
        work[cls].append({
            "candidate_id": p.get("candidate_id"), "canonical_name": p.get("canonical_name"),
            "polities": p.get("polities", []), "source_files": p.get("source_files", []),
            "action": "RESEARCH_THEN_DISTILL", "existing_skill_paths": p.get("existing_skill_paths", []),
        })
    for row in gap.get("review_queue", []):
        p = by_id.get(row["candidate_id"], row)
        cls = queue_class(p)
        work[cls].append({
            "candidate_id": p.get("candidate_id"), "canonical_name": p.get("canonical_name"),
            "polities": p.get("polities", []), "source_files": p.get("source_files", []),
            "action": "RESOLVE_SCOPE_AND_IDENTITY_BEFORE_DISTILL",
        })

    for values in work.values():
        values.sort(key=lambda x: (x.get("source_files", [""])[0] if x.get("source_files") else "", x.get("polities", [""])[0] if x.get("polities") else "", x.get("canonical_name") or ""))

    queue_order = [
        "A_CORE_MAJOR_SEQUENCE_MISSING", "B_CORE_PARALLEL_POLITY_MISSING",
        "D_CORE_EARLY_OR_PREQIN_MISSING", "Q1_SCOPE_OR_IDENTITY_REVIEW",
        "Q2_EXTENDED_REVIEW", "Q3_LEGENDARY_LIMITED_EVIDENCE", "Q4_OTHER_REVIEW",
    ]
    counts = {k: len(work.get(k, [])) for k in queue_order}
    queue = {
        "schema_version": "1.0",
        "status": "GENERATED_WORK_QUEUE",
        "policy": {
            "coverage_before_distillation": "Do not bulk-distill REVIEW or unresolved identities.",
            "missing_core": "Research must precede Skill generation; no reverse-engineered references.",
            "limited_evidence": "Reduce model claims/count when evidence is sparse; never pad six generic models.",
            "priority_meaning": "Queue letters describe engineering sequence, not historical importance or value ranking.",
        },
        "summary": {
            **counts,
            "missing_core_total": len(gap.get("missing_core", [])),
            "review_total": len(gap.get("review_queue", [])),
            "existing_skill_unresolved": len(unresolved_skills),
            "identity_blockers": len(skill_collisions) + len(identity_hint_collisions),
        },
        "queues": {k: work.get(k, []) for k in queue_order},
    }

    # Compact QA report.
    s = gap["summary"]
    q = issues["summary"]
    lines = [
        "# Corpus QA & Work Queue · 自动化", "",
        "> Generated from the current master candidate index and exact Skill coverage. It does not replace historical/source review or Nuwa semantic audit.", "",
        "## Coverage state", "",
        f"- Candidate persons: **{s['candidate_persons']}**",
        f"- Locked CORE: **{s['locked_core_persons']}**",
        f"- Matched CORE: **{s['matched_core_persons']}**",
        f"- Missing CORE: **{s['missing_core_persons']}**",
        f"- Existing Skills accounted: **{s.get('accounted_existing_skills', s['matched_existing_skills'])} / {s['existing_skills']}**",
        f"- Unresolved existing Skills: **{s.get('unresolved_existing_skills', len(unresolved_skills))}**", "",
        "## Identity QA", "",
        f"- Skill → multiple-person collisions: **{q['skill_to_multiple_person_collisions']}**",
        f"- Person → multiple-Skill matches: **{q['person_to_multiple_skill_matches']}**",
        f"- Shared identity-hint collisions: **{q['identity_hint_collisions']}**",
        f"- Suspicious canonical-name strings: **{q['suspicious_canonical_names']}**", "",
        "## Generated queues", "",
    ]
    for key in queue_order:
        lines.append(f"- `{key}`: **{counts[key]}**")
    lines += [
        "", "## Execution rule", "",
        "Identity/scope blockers are resolved before IDs are frozen. Missing locked CORE can then enter **research → evidence synthesis → Nuwa distillation → audit**. REVIEW, EXTENDED and LEGENDARY do not silently enter the locked CORE denominator.", "",
        "Machine-readable files: `data/corpus-work-queue.json` and `data/corpus-identity-issues.json`.",
    ]
    return issues, queue, "\n".join(lines) + "\n"


def main() -> None:
    issues, queue, report = build()
    dump(DATA / "corpus-identity-issues.json", issues)
    dump(DATA / "corpus-work-queue.json", queue)
    ASSESSMENT.mkdir(parents=True, exist_ok=True)
    (ASSESSMENT / "CORPUS_QA.md").write_text(report, encoding="utf-8")
    print(json.dumps({"identity_qa": issues["summary"], "work_queue": queue["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
