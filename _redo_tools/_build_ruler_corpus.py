#!/usr/bin/env python3
"""Build deterministic ruler-corpus coverage artifacts.

Mechanical only: this script never invents rulers, promotes REVIEW to CORE, or treats
coverage as Nuwa semantic quality. It scans segmented master files + Skill frontmatter,
performs conservative identity matching, and writes reproducible coverage outputs.
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

SEGMENT_PATTERNS = ["rulers-master-h*.json", "legendary-rulers.json", "ruler-candidates-preqin-other.json"]
PERSON_KEYS = {
    "persons", "candidates", "parallel_review", "predecessor_review", "restoration_review",
    "extended", "extended_or_review", "late_parallel_review", "interlude", "successor_review",
    "regency_extended", "competing_succession", "review", "transmitted_persons",
    "later_genealogy_candidates", "bronze_candidates", "known_persons",
}
REVIEWISH = ("REVIEW", "PARTIAL", "RECONCILIATION", "DISCOVERY", "NEXT", "OPEN", "SOURCE_")
STATUS_ORDER = {"CORE": 5, "REVIEW": 4, "EXTENDED": 3, "LEGENDARY": 2, "EXCLUDED_REVIEW": 1}

CANONICAL_ALIAS = {
    "秦王政": "嬴政", "始皇帝": "嬴政",
    "楚弃疾/陈君弃疾": "楚平王熊居", "楚弃疾/蔡公弃疾": "楚平王熊居",
    "朱温/朱晃": "朱温", "李茂贞/宋文通": "李茂贞", "杨诏/杨明": "杨诏",
    "阿速吉八/阿剌吉八": "阿速吉八", "阿速吉八/阿剌吉八/Ragibagh": "阿速吉八",
    "神农/炎帝": "神农氏", "武曌": "武则天", "汪兆铭": "汪精卫", "蒋中正": "蒋介石",
}
SKILL_NAME_ALIAS = {
    "义帝": "熊心", "秦始皇": "嬴政", "秦二世": "胡亥", "汉高祖": "刘邦",
    "汉光武帝": "刘秀", "唐高祖": "李渊", "唐太宗": "李世民", "武则天": "武则天",
}

# Existing legacy directory -> candidate polity lanes that may be matched using title/name hints.
DIR_POLITY_HINTS = {
    "xia": {"夏"}, "shang": {"商"}, "zhou": {"周王室"},
    "qin": {"秦帝国"}, "chuhan": {"秦末楚汉竞争政权"}, "xihan": {"西汉"}, "donghan": {"东汉"},
    "sanguo": {"曹魏", "蜀汉", "孙吴"}, "jin": {"西晋", "东晋"},
    "nanbeichao": {"刘宋", "南齐", "南梁", "陈", "北魏"},
    "sui": {"隋"}, "tang": {"唐", "武周"}, "song": {"北宋", "南宋"},
    "yuan": {"大蒙古国", "大元"}, "ming": {"明"}, "qing": {"后金", "清"},
}

DYNASTY_PREFIXES = [
    "周", "夏", "商", "秦", "汉", "晋", "魏", "蜀", "吴", "唐", "宋", "元", "明", "清",
    "齐", "楚", "燕", "韩", "赵", "郑", "鲁", "卫", "陈", "蔡", "曹", "越", "辽", "金",
    "北魏", "东魏", "西魏", "北齐", "北周", "南齐", "刘宋", "西夏", "后梁", "后唐", "后晋", "后汉", "后周",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_scalar(value: Any) -> str | None:
    if value is None or isinstance(value, (list, dict)):
        return None
    s = str(value).strip().strip("'\"")
    return s or None


def normalize_name(name: str | None) -> str | None:
    if not name:
        return None
    s = re.sub(r"\s+", "", str(name).strip()).replace("／", "/")
    # Skill cn often stores "司马炽（晋怀帝）" while master uses "司马炽".
    s = re.sub(r"[（(][^）)]*[）)]$", "", s)
    return CANONICAL_ALIAS.get(s, SKILL_NAME_ALIAS.get(s, s)) or None


def parse_skill(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    out: dict[str, Any] = {"name": None, "cn": None, "en": None, "era": None, "name_hints": []}
    if not text.startswith("---"):
        return out
    end = text.find("\n---", 3)
    block = text[3:end if end >= 0 else min(len(text), 4000)]
    for key in ("name", "cn", "en", "era"):
        m = re.search(rf"(?m)^{re.escape(key)}:\s*([^\n]+)", block)
        out[key] = clean_scalar(m.group(1)) if m else None

    hints: set[str] = set()
    cn = out.get("cn")
    if cn:
        hints.add(str(cn))
        base = re.split(r"[（(]", str(cn), 1)[0]
        hints.add(base)
        par = re.search(r"[（(]([^）)]+)", str(cn))
        if par:
            hints.add(re.split(r"[，,·;；]", par.group(1))[0])

    # First indented description line usually has "personal name（dynastic title, dates...）".
    dm = re.search(r"(?ms)^description:\s*\|\s*\n\s+([^\n]+)", block)
    if dm:
        first = dm.group(1).strip()
        base = re.split(r"[（(]", first, 1)[0].strip()
        if 1 <= len(base) <= 16:
            hints.add(base)
        pm = re.search(r"[（(]([^）)]+)", first)
        if pm:
            first_par = re.split(r"[，,·;；]", pm.group(1))[0].strip()
            if first_par:
                hints.add(first_par)
                # "周武王" -> "武王"; useful only with dynasty-dir restriction later.
                for prefix in sorted(DYNASTY_PREFIXES, key=len, reverse=True):
                    if first_par.startswith(prefix) and len(first_par) > len(prefix) + 1:
                        hints.add(first_par[len(prefix):])
                        break

    hm = re.search(r"(?m)^#\s+([^\n·|｜]+)", text[end + 4 if end >= 0 else 0:])
    if hm:
        h = hm.group(1).strip()
        if 1 <= len(h) <= 16:
            hints.add(h)

    out["name_hints"] = sorted({x for x in (normalize_name(h) for h in hints) if x})
    return out


def status_for(item: Any, parent: dict[str, Any] | None, source: Path, key: str) -> str:
    if source.name == "legendary-rulers.json":
        return "LEGENDARY"

    # Review/candidate containers stay REVIEW unless the item explicitly says CORE.
    key_review = "review" in key.lower() or "candidate" in key.lower()
    if isinstance(item, dict):
        status = str(item.get("status", "")).upper()
        layer = str(item.get("layer", "")).upper()
        if "EXCLUDE" in status:
            return "EXCLUDED_REVIEW"
        if status == "CORE":
            return "CORE"
        if "EXTENDED" in status or layer == "EXTENDED":
            return "EXTENDED"
        if any(token in status for token in REVIEWISH) or "REVIEW" in layer:
            return "REVIEW"
        if layer == "CORE":
            return "CORE"
        if layer == "LEGENDARY":
            return "LEGENDARY"

    if key_review:
        return "REVIEW"

    if parent:
        layer = str(parent.get("layer", "")).upper()
        status = str(parent.get("status", "")).upper()
        default_layer = str(parent.get("default_layer", "")).upper()
        if default_layer == "CORE_IF_AUTONOMOUS":
            return "REVIEW"
        if any(token in status for token in REVIEWISH) or "REVIEW" in layer:
            return "REVIEW"
        if layer in {"CORE", "EXTENDED", "LEGENDARY"}:
            return layer
    return "CORE"


def emit_person(item: Any, parent: dict[str, Any], key: str, source: Path, out: list[dict[str, Any]]) -> None:
    # A plain string under generic `candidates` is frequently a polity discovery queue,
    # not a person. Person-candidate lists in the corpus use dicts with a name field.
    if key == "candidates" and isinstance(item, str) and not (parent.get("name") or parent.get("id")):
        return
    status = status_for(item, parent, source, key)
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
                "name": name, "raw_name": raw, "aliases": aliases, "status": status,
                "polity": clean_scalar(item.get("polity")) or polity,
                "source_file": str(source.relative_to(ROOT)), "source_key": key,
                "existing_skill": clean_scalar(item.get("existing_skill")),
                "title": item.get("title") or item.get("titles"),
                "episode": item.get("episode") or item.get("episodes"),
                "reason": item.get("reason") or item.get("basis"),
            })
    if isinstance(item.get("names"), list):
        for raw in item["names"]:
            if isinstance(raw, str) and normalize_name(raw):
                out.append({"name": normalize_name(raw), "raw_name": raw, "aliases": [], "status": status,
                            "polity": clean_scalar(item.get("group")) or polity,
                            "source_file": str(source.relative_to(ROOT)), "source_key": key})


def collect_people(node: Any, source: Path, out: list[dict[str, Any]]) -> None:
    if isinstance(node, list):
        for value in node:
            collect_people(value, source, out)
        return
    if not isinstance(node, dict):
        return
    for key, value in node.items():
        if key in PERSON_KEYS and isinstance(value, list):
            for item in value:
                emit_person(item, node, key, source, out)
        elif isinstance(value, (dict, list)):
            collect_people(value, source, out)


def segment_paths() -> list[Path]:
    paths: set[Path] = set()
    for pattern in SEGMENT_PATTERNS:
        paths.update(DATA.glob(pattern))
    return sorted(p for p in paths if p.name != "rulers-master.json")


def final_status(signals: set[str]) -> str:
    # Any explicit REVIEW signal blocks accidental promotion unless a separate source
    # explicitly locks CORE. CORE wins only when actually present.
    if "CORE" in signals:
        return "CORE"
    return max(signals or {"REVIEW"}, key=lambda x: STATUS_ORDER.get(x, 0))


def person_alias_hints(name: str, aliases: list[str]) -> set[str]:
    hints = {normalize_name(name)} | {normalize_name(a) for a in aliases}
    # Slash-separated variant spellings are safe as identity hints.
    for raw in [name, *aliases]:
        for part in re.split(r"[/／]", str(raw)):
            if normalize_name(part):
                hints.add(normalize_name(part))
    hints.discard(None)
    return {str(h) for h in hints if h}


def build_candidate_index() -> dict[str, Any]:
    raw: list[dict[str, Any]] = []
    sources = segment_paths()
    for source in sources:
        collect_people(load_json(source), source, raw)

    merged: dict[str, dict[str, Any]] = {}
    for rec in raw:
        name = rec["name"]
        m = merged.setdefault(name, {
            "canonical_name": name, "aliases": set(), "status_signals": set(), "polities": set(),
            "source_files": set(), "existing_skill_paths": set(), "raw_names": set(), "episodes": [],
        })
        m["raw_names"].add(rec.get("raw_name") or name)
        m["aliases"].update(rec.get("aliases", []))
        m["status_signals"].add(rec["status"])
        if rec.get("polity"):
            m["polities"].add(rec["polity"])
        m["source_files"].add(rec["source_file"])
        if rec.get("existing_skill"):
            m["existing_skill_paths"].add(rec["existing_skill"])
        if rec.get("episode"):
            m["episodes"].append(rec["episode"])

    people = []
    for i, name in enumerate(sorted(merged), 1):
        m = merged[name]
        aliases = sorted(m["aliases"] | (m["raw_names"] - {name}))
        people.append({
            "candidate_id": f"ruler-{i:04d}", "canonical_name": name, "aliases": aliases,
            "identity_hints": sorted(person_alias_hints(name, aliases)),
            "corpus_status": final_status(m["status_signals"]), "status_signals": sorted(m["status_signals"]),
            "polities": sorted(m["polities"]), "source_files": sorted(m["source_files"]),
            "existing_skill_paths": sorted(m["existing_skill_paths"]), "episodes": m["episodes"],
            "identity_status": "CANDIDATE_ID_NOT_LOCKED",
        })
    counts = Counter(p["corpus_status"] for p in people)
    return {
        "schema_version": "0.3", "status": "GENERATED_CANDIDATE_INDEX_NOT_YET_ID_LOCKED",
        "warning": "candidate_id is temporary. REVIEW/EXTENDED and cross-polity identities must be QA'd before final IDs are frozen.",
        "generated_from": [str(p.relative_to(ROOT)) for p in sources],
        "stats": {"total_unique_candidates": len(people), **{k.lower(): v for k, v in sorted(counts.items())}},
        "persons": people,
    }


def build_skill_inventory() -> dict[str, Any]:
    rows = []
    for skill_file in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        fm = parse_skill(skill_file)
        rel = skill_file.relative_to(ROOT)
        parts = rel.parts
        rows.append({
            "skill_path": str(rel.parent), "skill_file": str(rel), "dynasty_dir": parts[1],
            "package_slug": parts[2], "cn": fm.get("cn"), "normalized_cn": normalize_name(fm.get("cn")),
            "name_hints": fm.get("name_hints", []), "en": fm.get("en"), "era": fm.get("era"),
            "frontmatter_name": fm.get("name"),
        })
    dup = Counter(r["normalized_cn"] for r in rows if r["normalized_cn"])
    return {
        "schema_version": "1.1", "status": "EXACT_FRONTMATTER_INVENTORY",
        "count": len(rows), "missing_cn_count": sum(not r["cn"] for r in rows),
        "duplicate_normalized_cn": [{"name": k, "count": v} for k, v in sorted(dup.items()) if v > 1],
        "skills": rows,
    }


def allowed_for_dir(person: dict[str, Any], dynasty_dir: str) -> bool:
    hints = DIR_POLITY_HINTS.get(dynasty_dir)
    if not hints:
        return False
    return bool(set(person.get("polities", [])) & hints)


def match(candidate: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    by_hint: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in inventory["skills"]:
        for hint in set(row.get("name_hints", [])) | {row.get("normalized_cn")}:
            if hint:
                by_hint[hint].append(row)

    matched_skills: set[str] = set()
    person_rows = []
    for p in candidate["persons"]:
        matches: dict[str, dict[str, Any]] = {}
        identity_hints = set(p.get("identity_hints", [])) | {normalize_name(p["canonical_name"])}
        for hint in identity_hints:
            if not hint:
                continue
            for row in by_hint.get(hint, []):
                # Exact personal-name matches are accepted. Short dynastic titles such as 武王
                # require the legacy-directory/polity restriction to avoid cross-dynasty collisions.
                if len(hint) <= 3 and row["normalized_cn"] != hint and not allowed_for_dir(p, row["dynasty_dir"]):
                    continue
                matches[row["skill_path"]] = row
        for explicit in p.get("existing_skill_paths", []):
            norm_path = explicit.removesuffix("/SKILL.md")
            for row in inventory["skills"]:
                if row["skill_path"] == norm_path:
                    matches[row["skill_path"]] = row
        ms = sorted(matches)
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
    extended = [p for p in person_rows if p["corpus_status"] == "EXTENDED"]
    legendary = [p for p in person_rows if p["corpus_status"] == "LEGENDARY"]
    return {
        "schema_version": "0.2", "status": "AUTOMATED_CONSERVATIVE_IDENTITY_MATCH_V2",
        "matching_policy": "Exact normalized cn/name-hint/explicit-path matching; short title hints require compatible legacy dynasty-dir. No fuzzy matching.",
        "summary": {
            "candidate_persons": len(person_rows), "locked_core_persons": len(locked_core),
            "matched_core_persons": len(matched_core), "missing_core_persons": len(missing_core),
            "review_persons": len(review), "extended_persons": len(extended), "legendary_persons": len(legendary),
            "existing_skills": inventory["count"], "matched_existing_skills": len(matched_skills),
            "unmatched_existing_skills": len(unmatched_skills),
            "core_coverage_ratio": round(len(matched_core) / len(locked_core), 4) if locked_core else None,
        },
        "missing_core": missing_core, "review_queue": review, "unmatched_existing_skills": unmatched_skills,
        "person_matches": person_rows,
    }


def write_report(gap: dict[str, Any]) -> None:
    s = gap["summary"]
    ratio = f"{s['core_coverage_ratio']:.1%}" if s["core_coverage_ratio"] is not None else "n/a"
    lines = [
        "# Ruler Corpus Coverage · 自动覆盖报告", "",
        "> Machine-generated by `_redo_tools/_build_ruler_corpus.py`. Coverage/identity only; **not** a Nuwa semantic-quality PASS.", "",
        "## Working denominator", "",
        f"- Candidate persons: **{s['candidate_persons']}**",
        f"- Locked historical CORE: **{s['locked_core_persons']}**",
        f"- REVIEW: **{s['review_persons']}**",
        f"- EXTENDED: **{s['extended_persons']}**",
        f"- LEGENDARY: **{s['legendary_persons']}**",
        "", "## Existing Skill coverage", "",
        f"- Existing Skills scanned: **{s['existing_skills']}**",
        f"- Existing Skills matched to a master person: **{s['matched_existing_skills']}**",
        f"- Existing Skills still needing identity normalization: **{s['unmatched_existing_skills']}**",
        f"- Matched CORE persons: **{s['matched_core_persons']}**",
        f"- Missing CORE persons: **{s['missing_core_persons']}**",
        f"- Working CORE coverage: **{ratio}**", "",
        "## Interpretation", "",
        "These are engineering counts, not final historical totals. Small-polity discovery, REVIEW decisions and cross-polity identity QA remain open. REVIEW is excluded from locked CORE until evidence resolves it.",
        "",
        "One person may have multiple rule episodes/titles/polities but must ultimately receive one stable person ID. Coverage is deliberately separate from Nuwa provenance and semantic-quality audit.",
        "", "## Automated next gates", "",
        "1. Resolve unmatched existing Skill identities conservatively; no fuzzy guessing.",
        "2. Resolve REVIEW candidates and cross-polity aliases, then freeze stable IDs.",
        "3. Recompute `CORE − matched Skill persons` as the research/distillation queue.",
        "4. Feed only that queue into research → evidence synthesis → Nuwa distillation.",
        "", "See `data/corpus-gap.json`, `data/existing-skill-person-map.json`, and `data/rulers-person-index.json`.",
    ]
    ASSESSMENT.mkdir(parents=True, exist_ok=True)
    (ASSESSMENT / "CORPUS_COVERAGE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_registry(gap: dict[str, Any], candidate: dict[str, Any]) -> None:
    path = DATA / "corpus-registry.json"
    reg = load_json(path) if path.exists() else {"schema_version": "1.0"}
    reg["master_corpus"] = {
        "status": candidate["status"], "candidate_index": "data/rulers-person-index.json",
        "coverage_report": "assessment/CORPUS_COVERAGE.md", "gap_file": "data/corpus-gap.json",
        **gap["summary"],
        "note": "Provisional until identity QA and remaining polity discovery close; REVIEW excluded from locked CORE.",
    }
    dump_json(path, reg)


def write_manifest(candidate: dict[str, Any]) -> None:
    path = DATA / "rulers-master.json"
    old = load_json(path) if path.exists() else {}
    dump_json(path, {
        "schema_version": "2.1", "title": old.get("title", "Chinese Historical Rulers Corpus — Canonical Master"),
        "status": "SEGMENTED_MASTER_IDENTITY_NORMALIZATION_IN_PROGRESS",
        "canonical_scope": "data/RULER_CORPUS_SCOPE.md", "build_plan": "data/corpus-build-plan.json",
        "person_index": "data/rulers-person-index.json", "segments": candidate["generated_from"],
        "candidate_stats": candidate["stats"],
        "identity_rule": "one person = one final stable ID; reigns/titles/polities are rule episodes",
        "completion_rule": "matched locked CORE persons / all locked CORE persons; REVIEW/EXTENDED/LEGENDARY separate",
        "warning": "Do not publish candidate counts as final historical totals until polity discovery and identity QA close.",
    })


def build(write: bool) -> dict[str, Any]:
    candidate = build_candidate_index()
    inventory = build_skill_inventory()
    gap = match(candidate, inventory)
    if write:
        dump_json(DATA / "rulers-person-index.json", candidate)
        dump_json(DATA / "existing-skill-person-map.json", inventory)
        dump_json(DATA / "corpus-gap.json", gap)
        write_report(gap)
        update_registry(gap, candidate)
        write_manifest(candidate)
        for temp in DATA.glob("_tmp-skill-map-*.json"):
            temp.unlink()
    return {"candidate_stats": candidate["stats"], "coverage": gap["summary"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build(write=not args.check), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
