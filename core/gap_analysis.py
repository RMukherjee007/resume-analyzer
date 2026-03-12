from dataclasses import dataclass
from typing import List
from .skills import SkillMatch

@dataclass
class GapReport:
    matched_count: int
    missing_skills: List[str]
    coverage: float

class GapAnalyzer:
    """Compares extracted resume skills against job description requirements."""
    def analyze(self, resume_skills: List[SkillMatch], jd_skills: List[SkillMatch]) -> GapReport:
        resume_set = {s.skill.name for s in resume_skills}
        jd_set = {s.skill.name for s in jd_skills}

        matched = resume_set & jd_set
        missing = jd_set - resume_set
        
        jd_total = max(len(jd_set), 1)
        coverage = len(matched) / jd_total

        return GapReport(
            matched_count=len(matched),
            missing_skills=[skill.title() for skill in missing],
            coverage=coverage
        )
