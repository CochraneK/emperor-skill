#!/usr/bin/env python3
"""Nuwa L3 semantic-distinctiveness REVIEW signals.

This scanner never assigns L3 PASS/FAIL. It removes the intentionally shared product
shell (role-play/activation/workflow instructions) and compares only ruler-specific
knowledge payload. High lexical similarity or long paragraph reuse means "read these
packages together", not "these packages are bad".

No third-party dependencies.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
DATA = ROOT / "data"
ASSESSMENT = ROOT / "assessment"

PAYLOAD_HEADINGS = (
    "身份卡", "核心心智模型", "决策启发式", "价值观", "价值排序", "反模式",
    "内在张力", "表达DNA", "表达 DNA", "时间线", "诚实边界", "适用边界", "证据边界",
)
SHELL_HEADINGS = ("角色扮演规则", "工作流程", "触发", "退出角色", "使用方式", "如何使用")

SHINGLE_N = 6
COMMON_DF_RATIO = 0.30
PAIR_JACCARD = 0.34
PAIR_CONTAINMENT = 0.58
MIN_PAIR_OVERLAP = 120
PARAGRAPH_MIN_CHARS = 90
MAX_NEIGHBORS = 3


@dataclass
class SkillDoc:
    path: str
    dynasty: str
    cn: str | None
    payload: str
    paragraphs: list[str]
    shingles: set[str]
    person_id: str | None
    used_legacy_fallback: bool


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.+?)\s*$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip("\"'")
    return out


def body_without_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    return text[end + 4:] if end >= 0 else text


def heading_has(title: str, keys: tuple[str, ...]) -> bool:
    clean = re.sub(r"[*_`#]", "", title).strip().lower()
    return any(k.lower() in clean for k in keys)


def extract_payload(body: str) -> tuple[str, bool]:
    """Return payload and whether legacy fallback was required."""
    selected: list[str] = []
    active = False
    found = False
    lines = body.splitlines()
    for line in lines:
        h2 = re.match(r"^##\s+(.+?)\s*$", line)
        if h2:
            title = h2.group(1)
            if heading_has(title, SHELL_HEADINGS):
                active = False
            elif heading_has(title, PAYLOAD_HEADINGS):
                active = True
                found = True
            else:
                active = False
            if active:
                selected.append(line)
        elif active:
            selected.append(line)
    if found:
        return "\n".join(selected), False

    # Legacy Skills without modern headings: retain body except explicit shell H2s.
    kept: list[str] = []
    skip = False
    for line in lines:
        h2 = re.match(r"^##\s+(.+?)\s*$", line)
        if h2:
            skip = heading_has(h2.group(1), SHELL_HEADINGS)
        if not skip:
            kept.append(line)
    return "\n".join(kept), True


def normalize(text: str, cn: str | None) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    if cn and len(cn) >= 2:
        text = text.replace(cn, "<PERSON>")
    text = re.sub(r"\d+(?:[–—-]\d+)?", "<NUM>", text)
    text = re.sub(r"[#>*_|~]", " ", text)
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[，。；：、！？,.!?;:（）()【】\[\]“”‘’\-—–]", "", text)
    return text


def shingles(text: str) -> set[str]:
    if len(text) < SHINGLE_N:
        return set()
    return {text[i:i + SHINGLE_N] for i in range(len(text) - SHINGLE_N + 1)}


def paragraphs(payload: str, cn: str | None) -> list[str]:
    out = []
    for raw in re.split(r"\n\s*\n", payload):
        norm = normalize(raw, cn)
        if len(norm) >= PARAGRAPH_MIN_CHARS:
            out.append(norm)
    return out


def skill_person_map() -> dict[str, str]:
    path = DATA / "corpus-gap.json"
    if not path.exists():
        return {}
    doc = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for person in doc.get("person_matches", []):
        pid = person.get("candidate_id") or person.get("person_id")
        for skill_path in person.get("matched_skill_paths", []):
            if pid and skill_path:
                out[str(skill_path)] = str(pid)
    return out


def collect() -> list[SkillDoc]:
    pmap = skill_person_map()
    docs: list[SkillDoc] = []
    for f in sorted(SKILLS.glob("*/*/SKILL.md")):
        rel_parts = f.relative_to(SKILLS).parts
        if any(part.startswith("_") for part in rel_parts):
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        fm = frontmatter(text)
        payload, fallback = extract_payload(body_without_frontmatter(text))
        cn = fm.get("cn")
        path = f.parent.relative_to(ROOT).as_posix()
        norm = normalize(payload, cn)
        docs.append(SkillDoc(
            path=path,
            dynasty=f.parent.parent.name,
            cn=cn,
            payload=payload,
            paragraphs=paragraphs(payload, cn),
            shingles=shingles(norm),
            person_id=pmap.get(path),
            used_legacy_fallback=fallback,
        ))
    return docs


def remove_common_shingles(docs: list[SkillDoc]) -> dict[str, set[str]]:
    df: Counter[str] = Counter()
    for d in docs:
        df.update(d.shingles)
    max_df = max(2, int(len(docs) * COMMON_DF_RATIO))
    return {d.path: {s for s in d.shingles if df[s] <= max_df} for d in docs}


def pair_metrics(a: set[str], b: set[str]) -> tuple[float, float, int]:
    if not a or not b:
        return 0.0, 0.0, 0
    overlap = len(a & b)
    if not overlap:
        return 0.0, 0.0, 0
    return overlap / len(a | b), overlap / min(len(a), len(b)), overlap


def similarity_review(docs: list[SkillDoc], filtered: dict[str, set[str]]):
    pairs: list[dict] = []
    neighbors: dict[str, list[dict]] = defaultdict(list)
    for i, left in enumerate(docs):
        for right in docs[i + 1:]:
            j, c, overlap = pair_metrics(filtered[left.path], filtered[right.path])
            if overlap < 30:
                continue
            neighbors[left.path].append({
                "skill_path": right.path, "person_id": right.person_id,
                "jaccard": round(j, 4), "containment": round(c, 4), "overlap_shingles": overlap,
            })
            neighbors[right.path].append({
                "skill_path": left.path, "person_id": left.person_id,
                "jaccard": round(j, 4), "containment": round(c, 4), "overlap_shingles": overlap,
            })
            if overlap >= MIN_PAIR_OVERLAP and (j >= PAIR_JACCARD or c >= PAIR_CONTAINMENT):
                pairs.append({
                    "left": left.path, "left_person_id": left.person_id,
                    "right": right.path, "right_person_id": right.person_id,
                    "same_dynasty": left.dynasty == right.dynasty,
                    "jaccard": round(j, 4), "containment": round(c, 4),
                    "overlap_shingles": overlap,
                    "review_reason": "HIGH_RULER_PAYLOAD_LEXICAL_SIMILARITY",
                })
    for key, rows in neighbors.items():
        rows.sort(key=lambda r: (r["jaccard"], r["containment"], r["overlap_shingles"]), reverse=True)
        neighbors[key] = rows[:MAX_NEIGHBORS]
    pairs.sort(key=lambda r: (r["jaccard"], r["containment"], r["overlap_shingles"]), reverse=True)
    return pairs, neighbors


def paragraph_review(docs: list[SkillDoc]) -> list[dict]:
    owners: dict[str, set[str]] = defaultdict(set)
    sample: dict[str, str] = {}
    for d in docs:
        for p in set(d.paragraphs):
            fp = hashlib.sha256(p.encode("utf-8")).hexdigest()[:16]
            owners[fp].add(d.path)
            sample[fp] = p[:240]
    groups = []
    for fp, paths in owners.items():
        if len(paths) >= 2:
            groups.append({
                "fingerprint": fp, "package_count": len(paths), "skill_paths": sorted(paths),
                "normalized_excerpt": sample[fp], "review_reason": "LONG_NORMALIZED_PARAGRAPH_REUSE",
            })
    groups.sort(key=lambda r: (r["package_count"], len(r["normalized_excerpt"])), reverse=True)
    return groups


def build() -> dict:
    docs = collect()
    filtered = remove_common_shingles(docs)
    pairs, nearest = similarity_review(docs, filtered)
    repeated = paragraph_review(docs)

    pair_by_skill: dict[str, list[dict]] = defaultdict(list)
    for p in pairs:
        pair_by_skill[p["left"]].append({"other": p["right"], "jaccard": p["jaccard"], "containment": p["containment"], "overlap_shingles": p["overlap_shingles"]})
        pair_by_skill[p["right"]].append({"other": p["left"], "jaccard": p["jaccard"], "containment": p["containment"], "overlap_shingles": p["overlap_shingles"]})

    para_by_skill: dict[str, list[str]] = defaultdict(list)
    for group in repeated:
        for path in group["skill_paths"]:
            para_by_skill[path].append(group["fingerprint"])

    queue = []
    for d in docs:
        reasons = []
        if pair_by_skill[d.path]:
            reasons.append("HIGH_RULER_PAYLOAD_LEXICAL_SIMILARITY")
        if para_by_skill[d.path]:
            reasons.append("LONG_NORMALIZED_PARAGRAPH_REUSE")
        if reasons:
            queue.append({
                "skill_path": d.path, "person_id": d.person_id, "cn": d.cn,
                "dynasty": d.dynasty, "reasons": reasons,
                "flagged_neighbors": sorted(pair_by_skill[d.path], key=lambda x: x["jaccard"], reverse=True),
                "repeated_paragraph_fingerprints": para_by_skill[d.path],
                "nearest_neighbors_for_context": nearest.get(d.path, []),
                "required_action": "MODEL_OR_HUMAN_L3_REVIEW",
            })
    queue.sort(key=lambda x: (-len(x["reasons"]), x["dynasty"], x["skill_path"]))

    return {
        "schema_version": "1.0",
        "status": "GENERATED_REVIEW_SIGNALS_NOT_L3_VERDICTS",
        "policy": {
            "automatic_pass_fail": False,
            "meaning": "Lexical reuse is a review signal only; shared history/source wording can be legitimate.",
            "shell_excluded": list(SHELL_HEADINGS),
            "payload_sections": list(PAYLOAD_HEADINGS),
            "next_step": "Read flagged Skill pairs with research/provenance and decide KEEP / PATCH / REDISTILL / RERESEARCH semantically.",
        },
        "thresholds": {
            "character_shingle_n": SHINGLE_N,
            "common_shingle_df_ratio_excluded": COMMON_DF_RATIO,
            "pair_jaccard": PAIR_JACCARD,
            "pair_containment": PAIR_CONTAINMENT,
            "minimum_pair_overlap_shingles": MIN_PAIR_OVERLAP,
            "repeated_paragraph_min_chars": PARAGRAPH_MIN_CHARS,
        },
        "summary": {
            "packages_scanned": len(docs),
            "packages_flagged_for_l3_review": len(queue),
            "high_similarity_pairs": len(pairs),
            "repeated_long_paragraph_groups": len(repeated),
            "packages_with_stable_person_id": sum(1 for d in docs if d.person_id),
            "legacy_payload_fallback_packages": sum(1 for d in docs if d.used_legacy_fallback),
        },
        "review_queue": queue,
        "high_similarity_pairs": pairs,
        "repeated_long_paragraph_groups": repeated,
    }


def write_report(doc: dict) -> None:
    s = doc["summary"]
    lines = [
        "# Nuwa L3 Semantic QA · Review Signals", "",
        "> Generated **review queue**, not an automatic Nuwa L3 PASS/FAIL verdict. Shared role-play/workflow shell is excluded.", "",
        "## Summary", "",
        f"- Skills scanned: **{s['packages_scanned']}**",
        f"- Stable-person-ID linked: **{s['packages_with_stable_person_id']}**",
        f"- Packages flagged for semantic review: **{s['packages_flagged_for_l3_review']}**",
        f"- High payload-similarity pairs: **{s['high_similarity_pairs']}**",
        f"- Reused long normalized paragraph groups: **{s['repeated_long_paragraph_groups']}**",
        f"- Legacy payload extraction fallback: **{s['legacy_payload_fallback_packages']}**", "",
        "## Interpretation", "",
        "A flag only prioritizes closer reading. It may be legitimate shared context/source wording, or it may reveal copy-with-name-swap, generic model language, or duplicated reasoning. Final classification requires reading the Skill with its research/provenance.", "",
        "The intentionally shared product shell—role-play rules, activation/exit instructions and generic workflow—is excluded so UX consistency is not mistaken for semantic duplication.", "",
        "## Review queue", "",
    ]
    if not doc["review_queue"]:
        lines.append("No packages crossed the conservative lexical review thresholds.")
    for row in doc["review_queue"]:
        pid = row.get("person_id") or "unlinked"
        lines.append(f"- `{row['skill_path']}` · {row.get('cn') or '?'} · `{pid}` · {', '.join(row['reasons'])}")
        if row["flagged_neighbors"]:
            n = row["flagged_neighbors"][0]
            lines.append(f"  - strongest flagged neighbor: `{n['other']}` (J={n['jaccard']:.3f}, containment={n['containment']:.3f}, overlap={n['overlap_shingles']})")
    lines += ["", "## Method boundary", "",
              "Character n-gram similarity cannot determine historical validity, source quality, causal justification, or true personality distinctiveness. It is only a triage instrument.", "",
              "Machine-readable details: `data/l3-semantic-review-queue.json`."]
    ASSESSMENT.mkdir(parents=True, exist_ok=True)
    (ASSESSMENT / "L3_SEMANTIC_QA.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    doc = build()
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "l3-semantic-review-queue.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_report(doc)
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
