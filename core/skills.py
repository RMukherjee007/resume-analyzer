import re
from dataclasses import dataclass
from typing import List
from rapidfuzz import fuzz

from .config import Skill


@dataclass
class SkillMatch:
    skill: Skill
    confidence: float


class SkillExtractor:

    def __init__(self, taxonomy: List[Skill]):

        self.taxonomy = taxonomy
        self.threshold = 90

    def extract_skills(self, text):

        tokens = re.findall(r"\b[\w\+\#\.]{3,}\b", text.lower())

        matches = []

        for skill in self.taxonomy:

            name = skill.name.lower()

            if re.search(rf"\b{name}\b", text):
                matches.append(SkillMatch(skill, 1.0))
                continue

            for token in tokens:

                score = fuzz.ratio(token, name)

                if score > self.threshold:
                    matches.append(SkillMatch(skill, score / 100))
                    break

        return matches
