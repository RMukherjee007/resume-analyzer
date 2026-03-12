from dataclasses import dataclass


@dataclass
class GapReport:
    matched: int
    missing: int
    coverage: float


class GapAnalyzer:

    def analyze(self, resume_skills, jd_skills):
        resume_set = {s.skill.name for s in resume_skills}
        jd_set = {s.skill.name for s in jd_skills}

        matched = resume_set & jd_set
        missing = jd_set - resume_set

        coverage = len(matched) / max(len(jd_set), 1)

        return GapReport(
            matched=len(matched),
            missing=len(missing),
            coverage=coverage
        )
