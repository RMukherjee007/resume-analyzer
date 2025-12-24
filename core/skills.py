import re
from abc import ABC, abstractmethod
from typing import List, Set
from dataclasses import dataclass
from difflib import SequenceMatcher

from .config import Skill, SkillTaxonomy


@dataclass
class SkillMatch:
    skill: Skill
    match_type: str
    confidence: float
    context: str


class SkillMatcher(ABC):
    """
    Base interface for skill matching strategies.
    """

    @abstractmethod
    def find_matches(
        self, text: str, taxonomy: SkillTaxonomy, seen: Set[str]
    ) -> List[SkillMatch]:
        pass


class ExactMatcher(SkillMatcher):
    def find_matches(self, text: str, taxonomy: SkillTaxonomy, seen: Set[str]) -> List[SkillMatch]:
        matches = []
        text_lower = text.lower()

        for skill in taxonomy:
            key = skill.name.lower()
            if key in seen:
                continue

            if skill.strict_match:
                pattern = rf"\b{re.escape(key)}\b"
                found = re.search(pattern, text_lower)
            else:
                found = key in text_lower

            if found:
                context = self._extract_context(text, skill.name)
                matches.append(SkillMatch(skill, "exact", 1.0, context))
                seen.add(key)

        return matches

    @staticmethod
    def _extract_context(text: str, term: str, window: int = 50) -> str:
        idx = text.lower().find(term.lower())
        if idx == -1:
            return ""
        start = max(0, idx - window)
        end = min(len(text), idx + len(term) + window)
        context = text[start:end].strip()
        if start > 0:
            context = "..." + context
        if end < len(text):
            context += "..."
        return context


class VariantMatcher(SkillMatcher):
    def find_matches(self, text: str, taxonomy: SkillTaxonomy, seen: Set[str]) -> List[SkillMatch]:
        matches = []
        text_lower = text.lower()

        for skill in taxonomy:
            key = skill.name.lower()
            if key in seen:
                continue

            for variant in skill.variants:
                if skill.strict_match:
                    pattern = rf"\b{re.escape(variant)}\b"
                    found = re.search(pattern, text_lower)
                else:
                    found = variant in text_lower

                if found:
                    context = ExactMatcher._extract_context(text, variant)
                    matches.append(SkillMatch(skill, "variant", 0.98, context))
                    seen.add(key)
                    break

        return matches


class FuzzyMatcher(SkillMatcher):
    def __init__(self, threshold: int = 88):
        self.threshold = threshold

    def find_matches(self, text: str, taxonomy: SkillTaxonomy, seen: Set[str]) -> List[SkillMatch]:
        matches = []
        tokens = re.findall(r"\b[\w\+\#\.]{4,}\b", text.lower())

        for skill in taxonomy:
            key = skill.name.lower()
            if key in seen or skill.strict_match:
                continue

            candidates = [skill.name.lower()] + skill.variants

            for candidate in candidates:
                for token in tokens:
                    similarity = fuzz.ratio(token, candidate)
                    if similarity >= self.threshold:
                        context = ExactMatcher._extract_context(text, token)
                        matches.append(
                            SkillMatch(skill, "fuzzy", similarity / 100, context)
                        )
                        seen.add(key)
                        break
                if key in seen:
                    break

        return matches


class SkillExtractor:
    """
    Extracts skills using multiple matching strategies.
    """

    def __init__(self, taxonomy: SkillTaxonomy | None = None):
        self.taxonomy = taxonomy or SkillTaxonomy()
        self.matchers = [
            ExactMatcher(),
            VariantMatcher(),
            FuzzyMatcher(),
        ]

    def extract_skills(self, text: str) -> List[SkillMatch]:
        if not text:
            return []

        seen: Set[str] = set()
        matches: List[SkillMatch] = []

        for matcher in self.matchers:
            matches.extend(matcher.find_matches(text, self.taxonomy, seen))

        return sorted(matches, key=lambda m: m.confidence, reverse=True)
