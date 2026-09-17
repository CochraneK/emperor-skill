#!/usr/bin/env python3
"""Build machine-generated ruler-corpus coverage artifacts.

This script is intentionally mechanical. It does NOT decide historical truth, promote
REVIEW candidates to CORE, or invent missing ruler identities. It scans the segmented
master files and existing Skill frontmatter, performs conservative exact/alias matching,
and writes deterministic coverage outputs.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSESSMENT = ROOT / "assessment"

SEGMENT_PATTERNS = [
    "rulers-master-h*.json",
    "legendary-rulers.json",
    "ruler-candidates-preqin-other.json",
]

PERSON_KEYS = {
    "persons", "candidates", "parallel_review", "predecessor_review",
    "restoration_review", "extended", "extended_or_review", "late_parallel_review",
    "interlude", "successor_review", "regency_extended", "competing_succession",
    "review", "transmitted_persons", "later_genealogy_candidates", "bronze_candidates",
    "known_persons",
}

# Explicit high-confidence same-person aliases discovered during corpus construction.
# Keep this small and evidence-based; fuzzy matching is deliberately avoided.
CANONICAL_ALIAS = {
    "秦王政": "嬴政",
    "始皇帝": "嬴政",
    "楚弃疾/陈君弃疾": "楚平王熊居",
    "楚弃疾/蔡公弃疾": "楚平王熊居",
    "朱温/朱晃": "朱温",
    "李茂贞/宋文通": "李茂贞",
    "杨诏/杨明": "杨诏",
    "阿速吉八/阿剌吉八": "阿速吉八",
    "阿速吉八/阿剌吉八/Ragibagh": "阿速吉八",
    "神农/炎帝": "神农氏",
    "武曌": "武则天",
    "汪兆铭": "汪精卫",
    "蒋中正": "蒋介石",
}

# Existing Skill cn values that use titles/short forms rather than the master name.
SKILL_NAME_ALIAS = {
    "义帝": "熊心",
    "秦始皇": "嬴政",
    "秦二世": "胡亥",
    "汉高祖": "刘邦",
    "汉光武帝": "刘秀",
    "唐高祖": "李渊",
    "唐太宗": "李世民",
    "武则天": "武则天",
}

STATUS_ORDER = {"CORE": 5, "REVIEW": 4, "EXTENDED": 3, "LEGENDARY": 2, "EXCLUDED_REVIEW": 1}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_scalar(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (list, dict)):
        return None
    s = str(value).strip().strip("'\"")
    return s or None


def parse_frontmatter(path: Path) -> dict[str, str | None]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {"name": None, "cn": None, "en": None, "era": None}
    end = text.find("\n---", 3)
    block = text[3:end if end >= 0 else min(len(text), 3000)]
    out: dict[str, str | None] = {}
    for key in ("name", "cn", "en", "era"):
        m = re.search(rf"(?m)^{re.escape(key)}:\s*([^\n]+)", block)
        out[key] = clean_scalar(m.group(1)) if m else None
    return out


def normalize_name(name: str | None) -> str | None:
    if not name:
        return None
    s = name.strip()
    s = re.sub(r"\s+", "", s)
    s = s.replace("／", "/")
    return CANONICAL_ALIAS.get(s, SKILL_NAME_ALIAS.get(s, s))


def status_for(item: Any, parent: dict[str, Any] | None, source: Path) -> str:
    if source.name == "legendary-rulers.json":
        return "LEGENDARY"
    if isinstance(item, dict):
        status = str(item.get("status", "")).upper()
        layer = str(item.get("layer", "")).upper()
        if "EXCLUDE" in status:
            return "EXCLUDED_REVIEW"
        if status == "CORE":
            return "CORE"
        if "REVIEW" in status or "DISCOVERY" in status or "PARTIAL" in status:
            return "REVIEW"
        if "EXTENDED" in status:
            return "EXTENDED"
        if layer == "CORE":
            return "CORE"
        if "REVIEW" in layer:
            return "REVIEW"
        if layer == "EXTENDED":
            return "EXTENDED"
        if layer == "LEGENDARY":
            return "LEGENDARY"
    if parent:
        layer = str(parent.get("layer", "")).upper()
        status = str(parent.get("status", "")).upper()
        if "REVIEW" in layer or "REVIEW" in status or "PARTIAL" in status:
            return "REVIEW"
        if layer in {"CORE", "EXTENDED", "LEGENDARY"}:
            return layer
    return "CORE"


def emit_person(item: Any, parent: dict[str, Any], key: str, source: Path, out: list[dict[str, Any]]) -> None:
    status = status_for(item, parent, source)
    polity = clean_scalar(parent.get("name")) or clean_scalar(parent.get("id"))
    if isinstance(item, str):
        name = normalize_name(item)
        if name:
            out.append({"name": name, "raw_name": item, "aliases": [], "status": status,
                        "polity": polity, "source_file": str(source.relative_to(ROOT)), "source_key": key})
        return
    if not isinstance(item, dict):
        return
    if item.get("name"):
        raw = str(item["name"])
        name = normalize_name(raw)
        aliases = [str(x) for x in item.get("aliases", []) if x]
        if name:
            out.append({
                "name": name, "raw_name": raw, "aliases": aliases,
                "status": status, "polity": clean_scalar(item.get("polity")) or polity,
                "source_file": str(source.relative_to(ROOT)), "source_key": key,
                "existing_skill": clean_scalar(item.get("existing_skill")),
                "title": item.get("title") or item.get("titles"),
                "episode": item.get("episode") or item.get("episodes"),
                "reason": item.get("reason") or item.get("basis"),
            })
    if isinstance(item.get("names"), list):
        for raw in item["names"]:
            if not isinstance(raw, str):
                continue
            name = normalize_name(raw)
            if name:
                out.append({"name": name, "raw_name": raw, "aliases": [], "status": status,
                            "polity": clean_scalar(item.get("group")) or polity,
                            "source_file": str(source.relative_to(ROOT)), "source_key": key})


def collect_people(node: Any, source: Path, out: list[dict[str, Any]], parent: dict[str, Any] | None = None) -> None:
    if isinstance(node, list):
        for value in node:
            collect_people(value, source, out, parent)
        return
    if not isinstance(node, dict):
        return
    for key, value in node.items():
        if key in PERSON_KEYS and isinstance(value, list):
            for item in value:
                emit_person(item, node, key, source, out)
        elif isinstance(value, (dict, list)):
            collect_people(value, source, out, node)


def segment_paths() -> list[Path]:
    paths: set[Path] = set()
    for pattern in SEGMENT_PATTERNS:
        paths.update(DATA.glob(pattern))
    # Canonical manifest itself is intentionally excluded to prevent recursion.
    return sorted(p for p in paths if p.name != "rulers-master.json")


def build_candidate_index() -> dict[str, Any]:
    raw: list[dict[str, Any]] = []
    sources = segment_paths()
    for source in sources:
        collect_people(load_json(source), source, raw)

    merged: dict[str, dict[str, Any]] = {}
    for rec in raw:
        name = rec["name"]
        m = merged.setdefault(name, {
            "canonical_name": name, "aliases": set(), "status_signals": set(),
            "polities": set(), "source_files": set(), "existing_skill_paths": set(),
            "raw_names": set(), "episodes": [],
        })
        m["raw_names"].add(rec.get("raw_name") or name)
        for alias in rec.get("aliases", []):
            m["aliases"].add(alias)
        m["status_signals"].add(rec["status"])
        if rec.get("polity"):
            m["polities"].add(rec["polity"])
        m["source_files"].add(rec["source_file"])
        if rec.get("existing_skill"):
            m["existing_skill_paths"].add(rec["existing_skill"])
        if rec.get("episode"):
            m["episodes"].append(rec["episode"])

    def final_status(signals: set[str]) -> str:
        return max(signals or {"REVIEW"}, key=lambda x: STATUS_ORDER.get(x, 0))

    people = []
    for i, name in enumerate(sorted(merged), 1):
        m = merged[name]
        people.append({
            "candidate_id": f"ruler-{i:04d}",
            "canonical_name": name,
            "aliases": sorted(m["aliases"] | (m["raw_names"] - {name})),
            "corpus_status": final_status(m["status_signals"]),
            "status_signals": sorted(m["status_signals"]),
            "polities": sorted(m["polities"]),
            "source_files": sorted(m["source_files"]),
            "existing_skill_paths": sorted(m["existing_skill_paths"]),
            "episodes": m["episodes"],
            "identity_status": "CANDIDATE_ID_NOT_LOCKED",
        })
    counts = Counter(p["corpus_status"] for p in people)
    return {
        "schema_version": "0.2",
        "status": "GENERATED_CANDIDATE_INDEX_NOT_YET_ID_LOCKED",
        "warning": "candidate_id is temporary. REVIEW/EXTENDED and unresolved cross-polity identities must be QA'd before final IDs are frozen.",
        "generated_from": [str(p.relative_to(ROOT)) for p in sources],
        "stats": {"total_unique_candidates": len(people), **{k.lower(): v for k, v in sorted(counts.items())}},
        "persons": people,
    }


def build_skill_inventory() -> dict[str, Any]:
    rows = []
    for skill_file in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        fm = parse_frontmatter(skill_file)
        rel = skill_file.relative_to(ROOT)
        parts = rel.parts
        cn = fm.get("cn")
        rows.append({
            "skill_path": str(rel.parent),
            "skill_file": str(rel),
            "dynasty_dir": parts[1],
            "package_slug": parts[2],
            "cn": cn,
            "normalized_cn": normalize_name(cn),
            "en": fm.get("en"), "era": fm.get("era"), "frontmatter_name": fm.get("name"),
        })
    dup = Counter(r["normalized_cn"] for r in rows if r["normalized_cn"])
    return {
        "schema_version": "1.0", "status": "EXACT_FRONTMATTER_INVENTORY",
        "count": len(rows), "missing_cn_count": sum(not r["cn"] for r in rows),
        "duplicate_normalized_cn": [{"name": k, "count": v} for k, v in sorted(dup.items()) if v > 1],
        "skills": rows,
    }


def match(candidate: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    by_name: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in inventory["skills"]:
        if row["normalized_cn"]:
            by_name[row["normalized_cn"]].append(row)

    matched_skills: set[str] = set()
    matched_people: set[str] = set()
    person_rows = []
    for p in candidate["persons"]:
        keys = {normalize_name(p["canonical_name"])}
        keys |= {normalize_name(a) for a in p.get("aliases", [])}
        keys.discard(None)
        matches: dict[str, dict[str, Any]] = {}
        for key in keys:
            for row in by_name.get(key, []):
                matches[row["skill_path"]] = row
        for explicit in p.get("existing_skill_paths", []):
            norm_path = explicit.removesuffix("/SKILL.md")
            for row in inventory["skills"]:
                if row["skill_path"] == norm_path:
                    matches[row["skill_path"]] = row
        ms = sorted(matches)
        if ms:
            matched_people.add(p["candidate_id"])
            matched_skills.update(ms)
        person_rows.append({
            "candidate_id": p["candidate_id"], "canonical_name": p["canonical_name"],
            "corpus_status": p["corpus_status"], "polities": p["polities"],
            "matched_skill_paths": ms, "match_status": "MATCHED" if ms else "MISSING",
        })

    unmatched_skills = [r for r in inventory["skills"] if r["skill_path"] not in matched_skills]
    locked_core = [p for p in person_rows if p["corpus_status"] == "CORE"]
    matched_core = [p for p in locked_core if p["match_status"] == "MATCHED"]
    missing_core = [p for p in locked_core if p["match_status"] == "MISSING"]
    review = [p for p in person_rows if p["corpus_status"] == "REVIEW"]
    return {
        "schema_version": "0.1", "status": "AUTOMATED_EXACT_ALIAS_MATCH_V1",
        "matching_policy": "Conservative exact normalized-name/explicit-path match only; no fuzzy matching. Unmatched does not prove absence until identity QA.",
        "summary": {
            "candidate_persons": len(person_rows), "locked_core_persons": len(locked_core),
            "matched_core_persons": len(matched_core), "missing_core_persons": len(missing_core),
            "review_persons": len(review), "existing_skills": inventory["count"],
            "matched_existing_skills": len(matched_skills), "unmatched_existing_skills": len(unmatched_skills),
            "core_coverage_ratio": round(len(matched_core) / len(locked_core), 4) if locked_core else None,
        },
        "missing_core": missing_core,
        "review_queue": review,
        "unmatched_existing_skills": unmatched_skills,
        "person_matches": person_rows,
    }


def write_report(gap: dict[str, Any], inventory: dict[str, Any], candidate: dict[str, Any]) -> None:
    s = gap["summary"]
    lines = [
        "# Ruler Corpus Coverage · 自动覆盖报告", "",
        "> Machine-generated by `_redo_tools/_build_ruler_corpus.py`. This is a coverage/identity report, **not** a Nuwa semantic-quality PASS.", "",
        "## Current denominator", "",
        f"- Candidate person records: **{s['candidate_persons']}**",
        f"- Locked historical CORE: **{s['locked_core_persons']}**",
        f"- REVIEW (not counted as locked CORE): **{s['review_persons']}**",
        f"- Existing Skill packages scanned: **{s['existing_skills']}**",
        "", "## Exact/alias coverage", "",
        f"- Matched CORE persons: **{s['matched_core_persons']}**",
        f"- Missing CORE persons: **{s['missing_core_persons']}**",
        f"- CORE coverage: **{s['core_coverage_ratio']:.1%}**" if s["core_coverage_ratio"] is not None else "- CORE coverage: n/a",
        f"- Existing Skills matched to a master person: **{s['matched_existing_skills']} / {s['existing_skills']}**",
        f"- Existing Skills still needing identity normalization: **{s['unmatched_existing_skills']}**",
        "", "## Interpretation", "",
        "The denominator is intentionally provisional while small-polity discovery and identity QA remain open. Therefore these numbers are **working engineering coverage**, not a claim that the historical master set is final.",
        "",
        "A person can have multiple rule episodes, titles or polities but must ultimately receive one stable person ID. REVIEW/EXTENDED/LEGENDARY are reported separately and never silently mixed into the historical CORE completion percentage.",
        "", "## Next automated gates", "",
        "1. Resolve unmatched existing Skill identities without fuzzy guessing.",
        "2. Resolve REVIEW candidates and cross-polity aliases; freeze stable person IDs only afterward.",
        "3. Recompute `CORE − matched Skill persons` as the research/distillation queue.",
        "4. Keep Nuwa provenance/semantic audit separate from mere coverage.",
        "", "## Largest structural gaps already visible", "",
        "The current repository remains concentrated in the traditional main-dynasty directories. Segment files now explicitly cover Spring/Autumn and Warring States parallel polities, Sixteen Kingdoms, Five Dynasties/Ten Kingdoms, Liao/Western Xia/Jurchen Jin/Western Liao, Nanzhao/Dali, transition rival regimes, and historical Republic-era central-government episodes.",
        "",
        "See `data/corpus-gap.json` for the machine-readable missing/review queues and `data/existing-skill-person-map.json` for the full 267-package inventory.",
    ]
    ASSESSMENT.mkdir(parents=True, exist_ok=True)
    (ASSESSMENT / "CORPUS_COVERAGE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_registry(gap: dict[str, Any], candidate: dict[str, Any]) -> None:
    path = DATA / "corpus-registry.json"
    reg = load_json(path) if path.exists() else {"schema_version": "1.0"}
    reg["master_corpus"] = {
        "status": candidate["status"],
        "candidate_index": "data/rulers-person-index.json",
        "coverage_report": "assessment/CORPUS_COVERAGE.md",
        "gap_file": "data/corpus-gap.json",
        **gap["summary"],
        "note": "Coverage is provisional until identity QA and remaining polity discovery are closed; REVIEW is excluded from locked CORE.",
    }
    dump_json(path, reg)


def write_manifest(candidate: dict[str, Any]) -> None:
    path = DATA / "rulers-master.json"
    old = load_json(path) if path.exists() else {}
    manifest = {
        "schema_version": "2.0",
        "title": old.get("title", "Chinese Historical Rulers Corpus — Canonical Master"),
        "status": "SEGMENTED_MASTER_IDENTITY_NORMALIZATION_IN_PROGRESS",
        "canonical_scope": "data/RULER_CORPUS_SCOPE.md",
        "build_plan": "data/corpus-build-plan.json",
        "person_index": "data/rulers-person-index.json",
        "segments": candidate["generated_from"],
        "candidate_stats": candidate["stats"],
        "identity_rule": "one person = one final stable ID; reigns/titles/polities are rule episodes",
        "completion_rule": "locked CORE persons matched to valid Skill packages / all locked CORE persons; REVIEW, EXTENDED and LEGENDARY remain separate",
        "warning": "Do not use candidate counts as final historical totals until remaining polity discovery and identity QA are closed.",
    }
    dump_json(path, manifest)


def build(write: bool) -> dict[str, Any]:
    candidate = build_candidate_index()
    inventory = build_skill_inventory()
    gap = match(candidate, inventory)
    if write:
        dump_json(DATA / "rulers-person-index.json", candidate)
        dump_json(DATA / "existing-skill-person-map.json", inventory)
        dump_json(DATA / "corpus-gap.json", gap)
        write_report(gap, inventory, candidate)
        update_registry(gap, candidate)
        write_manifest(candidate)
        # Remove obsolete hand-built temp map fragments once canonical inventory exists.
        for temp in DATA.glob("_tmp-skill-map-*.json"):
            temp.unlink()
    return {"candidate_stats": candidate["stats"], "coverage": gap["summary"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compute and print summary without writing")
    args = parser.parse_args()
    summary = build(write=not args.check)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
