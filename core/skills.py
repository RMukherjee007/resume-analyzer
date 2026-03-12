import re
from abc import ABC, abstractmethod
from typing import List, Set
from dataclasses import dataclass
from rapidfuzz import fuzz

from .config import SkillTaxonomy, Skill


@dataclass
class SkillMatch:
    skill: Skill
    match_type: str
    confidence: float


class SkillMatcher(ABC):
    @abstractmethod
    def find_matches(self, text: str, taxonomy: SkillTaxonomy, seen: Set[str]) -> List[SkillMatch]:
        pass


class ExactMatcher(SkillMatcher):
    def find_matches(self, text, taxonomy, seen):
        matches = []
        text_lower = text.lower()
        for skill in taxonomy:
            key = skill.name.lower()
            if key in seen:
                continue
            
            # Replaced \b with negative lookarounds to allow matching C++ and C#
            escaped_key = re.escape(key)
            pattern = rf"(?<![\w\+\#\.]){escaped_key}(?![\w\+\#\.])"
            
            if re.search(pattern, text_lower):
                matches.append(SkillMatch(skill, "exact", 1.0))
                seen.add(key)
        return matches


class VariantMatcher(SkillMatcher):
    def find_matches(self, text, taxonomy, seen):
        matches = []
        for skill in taxonomy:
            if not skill.variants:
                continue
            key = skill.name.lower()
            if key in seen:
                continue
            
            for variant in skill.variants:
                escaped_variant = re.escape(variant)
                pattern = rf"(?<![\w\+\#\.]){escaped_variant}(?![\w\+\#\.])"
                if re.search(pattern, text.lower()):
                    matches.append(SkillMatch(skill, "variant", 0.97))
                    seen.add(key)
                    break
        return matches


class FuzzyMatcher(SkillMatcher):
    def __init__(self, threshold=88):
        self.threshold = threshold

    def find_matches(self, text, taxonomy, seen):
        matches = []
        # Updated regex to capture terms with symbols
        tokens = re.findall(r"[\w\+\#\.]{4,}", text.lower())
        
        for skill in taxonomy:
            key = skill.name.lower()
            if key in seen or len(key) < 4:
                continue
                
            for token in tokens:
                score = fuzz.ratio(token, key)
                if score >= self.threshold:
                    matches.append(SkillMatch(skill, "fuzzy", score / 100))
                    seen.add(key)
                    break
        return matches


class SkillExtractor:
    def __init__(self, taxonomy=None):
        self.taxonomy = taxonomy or SkillTaxonomy()
        self.matchers = [
            ExactMatcher(),
            VariantMatcher(),
            FuzzyMatcher(),
        ]

    def extract_skills(self, text):
        seen = set()
        matches = []
        for matcher in self.matchers:
            matches.extend(matcher.find_matches(text, self.taxonomy, seen))
        return sorted(matches, key=lambda m: m.confidence, reverse=True)
