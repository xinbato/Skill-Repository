#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Deduplication & Semantic Overlap Detection Engine for Skill-Repository.
Evaluates candidate skills against the existing catalog to detect:
1. Exact Name / Content Identity duplicates
2. High Semantic Overlap (likely redundant)
3. Moderate Overlap (alternative approach / subset)
"""

import math
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but",
    "by", "can", "cannot", "could", "did", "do", "does", "doing", "down", "during", "each",
    "few", "for", "from", "further", "had", "has", "have", "having", "he", "her", "here",
    "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it",
    "its", "itself", "me", "more", "most", "my", "myself", "no", "nor", "not", "of", "off",
    "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over",
    "own", "same", "she", "should", "so", "some", "such", "than", "that", "the", "their",
    "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through",
    "to", "too", "under", "until", "up", "very", "was", "we", "were", "what", "when", "where",
    "which", "while", "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself",
    "yourselves", "use", "when", "skill", "agent", "helps", "provides", "instruction", "guide"
}


@dataclass
class ExistingSkill:
    category: str
    name: str
    path: Path
    description: str
    tokens: List[str]


@dataclass
class OverlapReport:
    candidate_name: str
    verdict: str  # "EXACT_NAME", "HIGH_OVERLAP", "PARTIAL_OVERLAP", "UNIQUE"
    closest_skill: Optional[str] = None
    similarity_score: float = 0.0
    overlapping_terms: List[str] = field(default_factory=list)
    recommendation: str = ""

    def to_markdown(self) -> str:
        if self.verdict == "EXACT_NAME":
            return (
                f"### 🛑 Trùng lặp danh tính (Exact Match)\n"
                f"- **Tên skill**: `{self.candidate_name}`\n"
                f"- **Xung đột**: Đã tồn tại trong `{self.closest_skill}`\n"
                f"- **Khuyến nghị**: {self.recommendation}"
            )
        elif self.verdict == "HIGH_OVERLAP":
            terms = ", ".join(f"`{t}`" for t in (self.overlapping_terms or [])[:8])
            return (
                f"### ⚠️ Cảnh báo trùng lặp công năng cao ({int(self.similarity_score * 100)}%)\n"
                f"- **Skill ứng viên**: `{self.candidate_name}`\n"
                f"- **Trùng với skill hiện có**: `{self.closest_skill}`\n"
                f"- **Từ khóa tương đồng**: {terms}\n"
                f"- **Khuyến nghị**: {self.recommendation}"
            )
        elif self.verdict == "PARTIAL_OVERLAP":
            terms = ", ".join(f"`{t}`" for t in (self.overlapping_terms or [])[:6])
            return (
                f"### ℹ️ Trùng một phần / Giải pháp thay thế ({int(self.similarity_score * 100)}%)\n"
                f"- **Skill ứng viên**: `{self.candidate_name}`\n"
                f"- **Giao thoa với**: `{self.closest_skill}`\n"
                f"- **Từ khóa chung**: {terms}\n"
                f"- **Khuyến nghị**: {self.recommendation}"
            )
        else:
            return (
                f"### ✅ Độc nhất / Tính năng mới ({int(self.similarity_score * 100)}% match)\n"
                f"- **Skill ứng viên**: `{self.candidate_name}`\n"
                f"- **Khuyến nghị**: {self.recommendation}"
            )


def tokenize(text: str) -> List[str]:
    """Tokenize and filter text into informative words, normalizing unicode/accents."""
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    words = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", normalized.lower())
    clean = []
    for w in words:
        subterms = w.split("-")
        for sub in subterms:
            if len(sub) >= 2 and sub not in STOPWORDS:
                clean.append(sub)
        if len(w) >= 2 and w not in STOPWORDS and w not in subterms:
            clean.append(w)
    return clean


def cosine_similarity(tokens1: List[str], tokens2: List[str]) -> Tuple[float, List[str]]:
    """Compute cosine similarity between two token bags and return common keywords."""
    if not tokens1 or not tokens2:
        return 0.0, []

    c1 = Counter(tokens1)
    c2 = Counter(tokens2)
    common_words = set(c1.keys()).intersection(set(c2.keys()))
    if not common_words:
        return 0.0, []

    dot_product = sum(c1[w] * c2[w] for w in common_words)
    mag1 = math.sqrt(sum(v * v for v in c1.values()))
    mag2 = math.sqrt(sum(v * v for v in c2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0, []

    raw_score = dot_product / (mag1 * mag2)
    score = max(0.0, min(1.0, raw_score))
    sorted_common = sorted(common_words, key=lambda w: c1[w] + c2[w], reverse=True)
    return round(score, 4), sorted_common


def load_existing_skills(repo_root: Path) -> List[ExistingSkill]:
    """Scan and index all existing skills from skills/ directory."""
    skills_dir = repo_root / "skills"
    indexed: List[ExistingSkill] = []
    if not skills_dir.exists():
        return indexed

    for cat_dir in sorted(skills_dir.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith("."):
            continue
        for skill_dir in sorted(cat_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue

            content = skill_md.read_text(encoding="utf-8", errors="replace")
            desc = ""
            for line in content.splitlines()[:25]:
                if line.strip().startswith("description:"):
                    desc = line.split(":", 1)[1].strip().strip('"').strip("'")
                    break

            combined_text = f"{skill_dir.name} {desc} {content[:1000]}"
            tokens = tokenize(combined_text)
            indexed.append(
                ExistingSkill(
                    category=cat_dir.name,
                    name=skill_dir.name,
                    path=skill_dir,
                    description=desc,
                    tokens=tokens
                )
            )
    return indexed


def check_candidate_overlap(
    candidate_name: str,
    candidate_desc: str,
    candidate_content: str,
    existing_skills: List[ExistingSkill]
) -> OverlapReport:
    """Analyze whether the candidate skill duplicates or overlaps with existing skills."""
    # Normalize candidate name for parity check
    norm_cand_name = re.sub(r"[^a-z0-9]+", "-", candidate_name.lower().strip()).strip("-")

    # Check 1: Exact Name Match
    for existing in existing_skills:
        norm_exist_name = re.sub(r"[^a-z0-9]+", "-", existing.name.lower().strip()).strip("-")
        if norm_exist_name == norm_cand_name:
            return OverlapReport(
                candidate_name=candidate_name,
                verdict="EXACT_NAME",
                closest_skill=f"skills/{existing.category}/{existing.name}",
                similarity_score=1.0,
                overlapping_terms=[candidate_name],
                recommendation=f"Kỹ năng '{candidate_name}' đã tồn tại trong repo tại 'skills/{existing.category}/{existing.name}'. Chặn tạo PR mới hoặc chuyển thành update PR."
            )

    candidate_text = f"{candidate_name} {candidate_desc} {candidate_content[:1500]}"
    cand_tokens = tokenize(candidate_text)

    best_score = 0.0
    best_match: Optional[ExistingSkill] = None
    best_terms: List[str] = []

    for existing in existing_skills:
        score, common = cosine_similarity(cand_tokens, existing.tokens)
        if score > best_score:
            best_score = score
            best_match = existing
            best_terms = common

    closest_rel_path = f"skills/{best_match.category}/{best_match.name}" if best_match else ""

    if best_score >= 0.75:
        return OverlapReport(
            candidate_name=candidate_name,
            verdict="HIGH_OVERLAP",
            closest_skill=closest_rel_path,
            similarity_score=best_score,
            overlapping_terms=best_terms,
            recommendation=f"Skill này có độ tương đồng ngữ nghĩa rất cao ({int(best_score * 100)}%) với '{closest_rel_path}'. Cân nhắc từ chối (Reject) hoặc gộp tính năng vào skill cũ."
        )
    elif best_score >= 0.50:
        return OverlapReport(
            candidate_name=candidate_name,
            verdict="PARTIAL_OVERLAP",
            closest_skill=closest_rel_path,
            similarity_score=best_score,
            overlapping_terms=best_terms,
            recommendation=f"Skill này trùng một phần ({int(best_score * 100)}%) với '{closest_rel_path}'. Nên đánh giá xem đây có phải là cách tiếp cận khác biệt đáng giữ lại không."
        )
    else:
        return OverlapReport(
            candidate_name=candidate_name,
            verdict="UNIQUE",
            closest_skill=closest_rel_path,
            similarity_score=best_score,
            overlapping_terms=best_terms,
            recommendation="Skill mới mang lại năng lực độc lập, không bị trùng lặp. Đủ điều kiện khởi tạo PR."
        )


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent.parent
    existing = load_existing_skills(repo_root)
    print(f"Loaded {len(existing)} existing skills for deduplication index.")
