#!/usr/bin/env python3
"""Nuwa L3 semantic-distinctiveness REVIEW queue.

This is deliberately *not* an automatic L3 PASS/FAIL classifier. It only surfaces
packages that deserve model/human semantic review because their ruler-specific
knowledge payload is unusually similar to another package or because long normalized
paragraphs are reused across multiple Skills.

Important design choice: the shared product shell (role-play rules, activation,
workflow, exit instructions) is intentionally excluded from comparison. Reusing that
shell is product consistency, not evidence that two rulers were distilled identically.

No third-party dependencies are required.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
DATA = ROOT / "data"
ASSESSMENT = ROOT / "assessment"

# Only ruler-specific knowledge-bearing sections are compared. Unknown headings inside
# an included section remain included until another top-level H2 begins.
PAYLOAD_HEADINGS = (
    "身份卡",
    "核心心智模型",
    "决策启发式",
    "价值观",
    "价值排序",
    "反模式",
    "内在张力",
    "表达DNA",
    "表达 DNA",
    "时间线",
    "诚实边界",
    "适用边界",
    "证据边界",
)

# Explicitly shared UX/template sections. They are excluded even if wording differs.
SHELL_HEADINGS = (
    "角色扮演规则",
    "工作流程",
    "触发",
    "退出角色",
    "使用方式",
    "如何使用",
)

MIN_SHINGLE = 6
COMMON_DF_RATIO = 0.30
PAIR_REVIEW_JACCARD = 0.34
PAIR_REVIEW_CONTAINMENT = 0.58
MIN_PAIR_OVERLAP = 120
PARAGRAPH_MIN_CHARS = 90
REPEATED_PARAGRAPH_MIN_PACKAGES = 2
MAX_NEIGHBORS = 3


@dataclass
class SkillDoc:
    skill_path: str
    skill_file: str
    dynasty: str
    slug: str
    cn: str | None
    payload: str
    paragraphs: list[str]
    shingles: set[str]
    person_id: str | None = None


def clean_scalar(value: str) -> str:
    value = value.strip().strip('"\'')
    return value


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[3:end]
    out: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.+?)\s*$", line)
        if m:
            out[m.group(1)] = clean_scalar(m.group(2))
    return out


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    return text[end + 4:] if end >= 0 else text


def heading_is_payload(title: str) -> bool:
    t = re.sub(r"[*_`#]", "", title).strip()
    return any(key.lower() in t.lower() for key in PAYLOAD_HEADINGS)


def heading_is_shell(title: str) -> bool:
    t = re.sub(r"[*_`#]", "", title).strip()
    return any(key.lower() in t.lower() for key in SHELL_HEADINGS)


def extract_payload(body: str) -> str:
    """Extract ruler-specific H2 sections while excluding the reusable UX shell."""
    lines = body.splitlines()
    selected: list[str] = []
    active = False
    found_payload_heading = False

    for line in lines:
        h2 = re.match(r"^##\s+(.+?)\s*$", line)
        if h2:
            title = h2.group(1)
            if heading_is_shell(title):
                active = False
            elif heading_is_payload(title):
                active = True
                found_payload_heading = True
            else:
                # H2 boundaries are hard section boundaries. Unknown top-level sections
                # are not silently folded into a previous payload section.
                active = False
            if active:
                selected.append(line)
            continue
        if active:
            selected.append(line)

    if found_payload_heading and selected:
        return "\n".join(selected)

    # Legacy Skills may not use the modern H2 vocabulary. Fall back to the body but
    # remove front-loaded shell sections heuristically; mark this in the output later.
    kept: list[str] = []
    skip = False
    for line in lines:
        h2 = re.match(r"^##\s+(.+?)\s*$", line)
        if h2:
            skip = heading_is_shell(h2.group(1))
            if not skip:
                kept.append(line)
        elif not skip:
            kept.append(line)
    return "\n".join(kept)


def normalize_text(text: str, cn: str | None = None) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    if cn and len(cn) >= 2:
        text = text.replace(cn, "<PERSON>")
    # Dates/numbers should not make otherwise templated prose look distinctive.
    text = re.sub(r"\d+(?:[–—-]\d+)?", "<NUM>", text)
    # Source labels are useful semantically, but markdown decoration is not.
    text = re.sub(r"[#>*_|~]", " ", text)
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[，。；：、！？,.!?;:（）()【】\[\]“”‘’\-—–]", "", text)
    return text


def make_shingles(text: str, n: int = MIN_SHINGLE) -> set[str]:
    if len(text) < n:
        return set()
    return {text[i:i+n] for i in range(len(text) - n + 1)}


def payload_paragraphs(payload: str, cn: str | None) -> list[str]:
    # Markdown blank-line blocks work better than individual bullets for catching
    # copied reasoning. Short boilerplate fragments are ignored.
    paras = []
    for raw in re.split(r"\n\s*\n", payload):
        norm = normalize_text(raw, cn)
        if len(norm) >= PARAGRAPH_MIN_CHARS:
            paras.append(norm)
    return paras


def load_skill_person_map() -> dict[str, str]:
    gap_path = DATA / "corpus-gap.json"
    if not gap_path.exists():
        return {}
    gap = json.loads(gap_path.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for person in gap.get("person_matches", []):
        pid = person.get("candidate_id") or person.get("person_id")
        for path in person.get("matched_skill_paths", []):
            if pid and path:
                out[str(path)] = str(pid)
    return out


def collect_docs() -> list[SkillDoc]:
    person_map = load_skill_person_map()
    docs: list[SkillDoc] = []
    for path in sorted(SKILLS.glob("*/*/SKILL.md")):
        if any(part.startswith("_") for part in path.relative_to(SKILLS).parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        body = strip_frontmatter(text)
        payload = extract_payload(body)
        cn = fm.get("cn")
        normalized = normalize_text(payload, cn)
        rel_dir = path.parent.relative_to(ROOT).as_posix()
        docs.append(SkillDoc(
            skill_path=rel_dir,
            skill_file=path.relative_to(ROOT).as_posix(),
            dynasty=path.parent.parent.name,
            slug=path.parent.name,
            cn=cn,
            payload=payload,
            paragraphs=payload_paragraphs(payload, cn),
            shingles=make_shingles(normalized),
            person_id=person_map.get(rel_dir),
        ))
    return docs


def filtered_shingles(docs: list[SkillDoc]) -> tuple[dict[str, set[str]], Counter[str]]:
    df: Counter[str] = Counter()
    for d in docs:
        df.update(d.shingles)
    max_df = max(2, int(len(docs) * COMMON_DF_RATIO))
    filtered: dict[str, set[str]] = {}
    for d in docs:
        filtered[d.skill_path] = {s for s in d.shingles if df[s] <= max_df}
    return filtered, df


def pair_metrics(a: set[str], b: set[str]) -> tuple[float, float, int]:
    if not a or not b:
        return 0.0, 0.0, 0
    overlap = len(a & b)
    if not overlap:
        return 0.0, 0.0, 0
    union = len(a | b)
    jaccard = overlap / union if union else 0.0
    containment = overlap / min(len(a), len(b))
    return jaccard, containment, overlap


def pair_review(docs: list[SkillDoc], filtered: dict[str, set[str]]) -> tuple[list[dict], dict[str, list[dict]]]:
    flagged_pairs: list[dict] = []
    neighbors: dict[str, list[dict]] = defaultdict(list)
    for i, left in enumerate(docs):
        a = filtered[left.skill_path]
        for right in docs[i+1:]:
            b = filtered[right.skill_path]
            jaccard, containment, overlap = pair_metrics(a, b)
            if overlap < 30:
                continue
            rec_left = {
                "skill_path": right.skill_path,
                "person_id": right.person_id,
                "jaccard": round(jaccard, 4),
                "containment": round(containment, 4),
                "overlap_shingles": overlap,
            }
            rec_right = {**rec_left, "skill_path": left.skill_path, "person_id": left.person_id}
            neighbors[left.skill_path].append(rec_left)
            neighbors[right.skill_path].append(rec_right)
            if overlap >= MIN_PAIR_OVERLAP and (
                jaccard >= PAIR_REVIEW_JACCARD or containment >= PAIR_REVIEW_CONTAINMENT
            ):
                flagged_pairs.append({
                    "left": left.skill_path,
                    "left_person_id": left.person_id,
                    "right": right.skill_path,
                    "right_person_id": right.person_id,
                    "same_dynasty": left.dynasty == right.dynasty,
                    "jaccard": round(jaccard, 4),
                    "containment": round(containment, 4),
                    "overlap_shingles": overlap,
                    "review_reason": "HIGH_RULER_PAYLOAD_LEXICAL_SIMILARITY",
                })
    for path in neighbors:
        neighbors[path].sort(key=lambda x: (x["jaccard"], x["containment"], x["overlap_shingles"]), reverse=True)
        neighbors[path] = neighbors[path][:MAX_NEIGHBORS]
    flagged_pairs.sort(key=lambda x: (x["jaccard"], x["containment"], x["overlap_shingles"]), reverse=True)
    return flagged_pairs, neighbors


def repeated_paragraph_review(docs: list[SkillDoc]) -> list[dict]:
    owners: dict[str, set[str]] = defaultdict(set)
    samples: dict[str, str] = {}
    for d in docs:
        for p in set(d.paragraphs):
            digest = hashlib.sha256(p.encode("utf-8")).hexdigest()[:16]
            owners[digest].add(d.skill_path)
            samples[digest] = p[:240]
    groups = []
    for digest, paths in owners.items():
        if len(paths) < REPEATED_PARAGRAPH_MIN_PACKAGES:
            continue
        groups.append({
            "fingerprint": digest,
            "package_count": len(paths),
            "skill_paths": sorted(paths),
            "normalized_excerpt": samples[digest],
            "review_reason": "LONG_NORMALIZED_PARAGRAPH_REUSE",
        })
    groups.sort(key=lambda x: (x["package_count"], len(x["normalized_excerpt"])), reverse=True)
    return groups


def build_queue() -> dict:
    docs = collect_docs()
    filtered, df = filtered_shingles(docs)
    pairs, neighbors = pair_review(docs, filtered)
    repeated = repeated_paragraph_review(docs)

    repeated_by_skill: dict[str, list[str]] = defaultdict(list)
    for group in repeated:
        for path in group["skill_paths"]:
            repeated_by_skill[path].append(group["fingerprint"])

    pair_by_skill: dict[str, list[dict]] = defaultdict(list)
    for p in pairs:
        pair_by_skill[p["left"]].append({
            "other": p["right"], "jaccard": p["jaccard"],
            "containment": p["containment"], "overlap_shingles": p["overlap_shingles"]
        })
        pair_by_skill[p["right"]].append({
            "other": p["left"], "jaccard": p["jaccard"],
            "containment": p["containment"], "overlap_shingles": p["overlap_shingles"]
        })

    queue = []
    for d in docs:
        reasons = []
        if pair_by_skill[d.skill_path]:
            reasons.append("HIGH_RULER_PAYLOAD_LEXICAL_SIMILARITY")
        if repeated_by_skill[d.skill_path]:
            reasons.append("LONG_NORMALIZED_PARAGRAPH_REUSE")
        if reasons:
            queue.append({
                "skill_path": d.skill_path,
                "person_id": d.person_id,
                "cn": d.cn,
                "dynasty": d.dynasty,
                "reasons": reasons,
                "flagged_neighbors": sorted(pair_by_skill[d.skill_path], key=lambda x: x["jaccard"], reverse=True),
                "repeated_paragraph_fingerprints": repeated_by_skill[d.skill_path],
                "nearest_neighbors_for_context": neighbors.get(d.skill_path, []),
                "required_action": "MODEL_OR_HUMAN_L3_REVIEW",
            })

    queue.sort(key=lambda x: (-len(x["reasons"]), x["dynasty"], x["skill_path"]))
    return {
        "schema_version": "1.0",
        "status": "GENERATED_REVIEW_SIGNALS_NOT_L3_VERDICTS",
        "policy": {
            "meaning": "Lexical reuse is a review signal only. Historical overlap, shared source wording, and intentionally common Skill structure can be legitimate.",
            "shell_excluded": list(SHELL_HEADINGS),
            "payload_sections": list(PAYLOAD_HEADINGS),
            "automatic_pass_fail": False,
            "next_step": "Read flagged Skill pairs with their research/provenance and decide KEEP / PATCH / REDISTILL / RERESEARCH semantically.",
        },
        "thresholds": {
            "character_shingle_n": MIN_SHINGLE,
            "common_shingle_df_ratio_excluded": COMMON_DF_RATIO,
            "pair_jaccard": PAIR_REVIEW_JACCARD,
            "pair_containment": PAIR_REVIEW_CONTAINMENT,
            "minimum_pair_overlap_shingles": MIN_PAIR_OVERLAP,
            "repeated_paragraph_min_chars": PARAGRAPH_MIN_CHARS,
        },
        "summary": {
            "packages_scanned": len(docs),
            "packages_flagged_for_l3_review": len(queue),
            "high_similarity_pairs": len(pairs),
            "repeated_long_paragraph_groups": len(repeated),
            "shingles_seen": len(df),
            "packages_with_stable_person_id": sum(1 for d in docs if d.person_id),
        },
        "review_queue": queue,
        "high_similarity_pairs": pairs,
        "repeated_long_paragraph_groups": repeated,
    }


def write_report(doc: dict) -> None:
    s = doc["summary"]
    lines = [
        "# Nuwa L3 Semantic QA · Review Signals",
        "",
        "> Generated review queue, **not** an automatic Nuwa L3 PASS/FAIL verdict. Shared role-play/workflow shell is excluded from similarity measurement.",
        "",
        "## Summary",
        "",
        f"- Skills scanned: **{s['packages_scanned']}**",
        f"- Stable-person-ID linked: **{s['packages_with_stable_person_id']}**",
        f"- Packages flagged for semantic review: **{s['packages_flagged_for_l3_review']}**",
        f"- High payload-similarity pairs: **{s['high_similarity_pairs']}**",
        f"- Reused long normalized paragraph groups: **{s['repeated_long_paragraph_groups']}**",
        "",
        "## Interpretation",
        "",
        "A flag means only that ruler-specific payload deserves closer reading. It can be legitimate (shared historical context/source wording) or problematic (copy-with-name-swap, generic model language, duplicated reasoning). Final L3 classification requires reading the Skill together with its research/provenance.",
        "",
        "The intentionally shared product shell—role-play rules, activation/exit instructions and generic workflow—is excluded so UX consistency is not mistaken for semantic duplication.",
        "",
        "## Review queue",
        "",
    ]
    if not doc["review_queue"]:
        lines.append("No packages crossed the conservative lexical review thresholds.")
    else:
        for row in doc["review_queue"]:
            pid = row.get("person_id") or "unlinked"
            lines.append(f"- `{row['skill_path']}` · {row.get('cn') or '?'} · `{pid}` · {', '.join(row['reasons'])}")
            if row.get("flagged_neighbors"):
                nearest = row["flagged_neighbors"][0]
                lines.append(
                    f"  - strongest flagged neighbor: `{nearest['other']}` "
                    f"(J={nearest['jaccard']:.3f}, containment={nearest['containment']:.3f}, overlap={nearest['overlap_shingles']})"
                )
    lines += [
        "",
        "## Method boundary",
        "",
        "Character n-gram similarity cannot decide whether a historical interpretation is good, sourced, distinctive or causally justified. It is deliberately used only to prioritize scarce semantic-review attention.",
        "",
        "Machine-readable details: `data/l3-semantic-review-queue.json`.",
    ]
    ASSESSMENT.mkdir(parents=True, exist_ok=True)
    (ASSESSMENT / "L3_SEMANTIC_QA.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    doc = build_queue()
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "l3-semantic-review-queue.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_report(doc)
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
