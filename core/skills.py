import re
from typing import List
from dataclasses import dataclass
from rapidfuzz import fuzz
from .config import SkillTaxonomy, Skill

@dataclass
class SkillMatch:
    skill: Skill
    match_type: str
    confidence: float

class SkillExtractor:
    """Extracts skills using Exact, Variant, and Fuzzy string matching strategies."""
    def __init__(self, taxonomy=None):
        self.taxonomy = taxonomy or SkillTaxonomy()

    def extract_skills(self, text: str) -> List[SkillMatch]:
        seen = set()
        matches = []
        text_lower = text.lower()
        tokens = re.findall(r"[\w\+\#\.]{4,}", text_lower)

        for skill in self.taxonomy:
            key = skill.name.lower()
            if key in seen: continue

            # 1. Exact Match via negative lookarounds
            escaped_key = re.escape(key)
            if re.search(rf"(?<![\w\+\#\.]){escaped_key}(?![\w\+\#\.])", text_lower):
                matches.append(SkillMatch(skill, "exact", 1.0))
                seen.add(key)
                continue

            # 2. Variant Match
            if skill.variants:
                for variant in skill.variants:
                    escaped_variant = re.escape(variant)
                    if re.search(rf"(?<![\w\+\#\.]){escaped_variant}(?![\w\+\#\.])", text_lower):
                        matches.append(SkillMatch(skill, "variant", 0.97))
                        seen.add(key)
                        break
            
            # 3. Fuzzy Match (Levenshtein distance)
            if key not in seen and len(key) >= 4:
                for token in tokens:
                    score = fuzz.ratio(token, key)
                    if score >= 88:
                        matches.append(SkillMatch(skill, "fuzzy", score / 100))
                        seen.add(key)
                        break

        return sorted(matches, key=lambda m: m.confidence, reverse=True)
