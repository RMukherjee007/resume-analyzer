from typing import List, Dict
from dataclasses import dataclass, field

from .config import Priority, SkillCategory, CATEGORY_WEIGHTS
from .skills import SkillMatch


@dataclass
class SkillGap:
    skill_match: SkillMatch
    priority: Priority
    impact_score: float

    @property
    def skill_name(self) -> str:
        return self.skill_match.skill.name

    @property
    def category(self) -> SkillCategory:
        return self.skill_match.skill.category


@dataclass
class CategoryAnalysis:
    category: SkillCategory
    coverage: float
    matched_count: int
    weak_count: int
    missing_count: int


@dataclass
class Recommendation:
    priority: str
    title: str
    description: str
    action: str


@dataclass
class GapAnalysisReport:
    overall_score: float
    confidence_score: float
    matched_skills: List[SkillMatch] = field(default_factory=list)
    missing_skills: List[SkillGap] = field(default_factory=list)
    weak_matches: List[SkillMatch] = field(default_factory=list)
    category_analysis: Dict[SkillCategory, CategoryAnalysis] = field(default_factory=dict)
    recommendations: List[Recommendation] = field(default_factory=list)


class GapAnalyzer:
    """
    Performs skill gap analysis between resume and job description skills.
    """

    def analyze(self, resume_skills: List[SkillMatch], jd_skills: List[SkillMatch]) -> GapAnalysisReport:
        resume_map = {m.skill.name.lower(): m for m in resume_skills}
        jd_map = {m.skill.name.lower(): m for m in jd_skills}

        resume_keys = set(resume_map.keys())
        jd_keys = set(jd_map.keys())

        matched_keys = resume_keys & jd_keys
        missing_keys = jd_keys - resume_keys

        matched, weak = self._classify_matched(matched_keys, resume_map)
        missing = self._analyze_missing(missing_keys, jd_map)

        category_analysis = self._analyze_categories(matched, weak, missing)
        recommendations = self._generate_recommendations(missing, weak, category_analysis)

        overall = self._compute_overall_score(matched, weak, jd_keys)
        confidence = self._compute_confidence_score(matched, weak)

        return GapAnalysisReport(
            overall_score=overall,
            confidence_score=confidence,
            matched_skills=matched,
            missing_skills=missing,
            weak_matches=weak,
            category_analysis=category_analysis,
            recommendations=recommendations
        )

    @staticmethod
    def _classify_matched(keys: set, resume_map: Dict[str, SkillMatch]):
        strong, weak = [], []
        for key in keys:
            match = resume_map.get(key)
            if not match:
                continue
            (strong if match.confidence >= 0.9 else weak).append(match)
        return strong, weak

    def _analyze_missing(self, keys: set, jd_map: Dict[str, SkillMatch]) -> List[SkillGap]:
        gaps = []
        for key in keys:
            match = jd_map.get(key)
            if not match:
                continue
            impact = self._compute_impact(match)
            priority = self._determine_priority(impact)
            gaps.append(SkillGap(match, priority, impact))
        return sorted(gaps, key=lambda g: g.impact_score, reverse=True)

    @staticmethod
    def _compute_impact(match: SkillMatch) -> float:
        skill_weight = match.skill.weight
        category_weight = CATEGORY_WEIGHTS.get(match.skill.category, 1.0)
        return min((skill_weight * category_weight) / 1.5, 1.0)

    @staticmethod
    def _determine_priority(impact: float) -> Priority:
        if impact >= 0.8:
            return Priority.CRITICAL
        if impact >= 0.6:
            return Priority.HIGH
        if impact >= 0.4:
            return Priority.MEDIUM
        return Priority.LOW

    def _analyze_categories(self, matched, weak, missing) -> Dict[SkillCategory, CategoryAnalysis]:
        categories = {}

        all_categories = {
            m.skill.category for m in matched + weak
        } | {g.category for g in missing}

        for cat in all_categories:
            cat_matched = [m for m in matched if m.skill.category == cat]
            cat_weak = [m for m in weak if m.skill.category == cat]
            cat_missing = [g for g in missing if g.category == cat]

            total = len(cat_matched) + len(cat_weak) + len(cat_missing)
            coverage = (
                (len(cat_matched) + 0.5 * len(cat_weak)) / total
                if total > 0 else 0
            )

            categories[cat] = CategoryAnalysis(
                category=cat,
                coverage=coverage,
                matched_count=len(cat_matched),
                weak_count=len(cat_weak),
                missing_count=len(cat_missing)
            )

        return categories

    @staticmethod
    def _compute_overall_score(matched, weak, jd_keys: set) -> float:
        if not jd_keys:
            return 0.0
        return (len(matched) + 0.5 * len(weak)) / len(jd_keys)

    @staticmethod
    def _compute_confidence_score(matched, weak) -> float:
        if not matched and not weak:
            return 0.0

        total_weighted = sum(
            m.confidence * m.skill.weight for m in matched + weak
        )
        total_weights = sum(m.skill.weight for m in matched + weak)

        return total_weighted / total_weights if total_weights else 0.0

    @staticmethod
    def _generate_recommendations(missing, weak, categories) -> List[Recommendation]:
        recs = []

        critical = [g for g in missing if g.priority == Priority.CRITICAL]
        if critical:
            skills = ", ".join(g.skill_name for g in critical[:3])
            recs.append(
                Recommendation(
                    "Critical",
                    "Add Critical Skills",
                    f"Missing essential skills: {skills}",
                    f"Gain experience with {critical[0].skill_name}"
                )
            )

        high = [g for g in missing if g.priority == Priority.HIGH]
        if high:
            skills = ", ".join(g.skill_name for g in high[:3])
            recs.append(
                Recommendation(
                    "High",
                    "Strengthen Core Skills",
                    f"Important skills missing: {skills}",
                    f"Build projects using {high[0].skill_name}"
                )
            )

        if weak:
            skills = ", ".join(m.skill.name for m in weak[:3])
            recs.append(
                Recommendation(
                    "Medium",
                    "Strengthen Weak Matches",
                    f"Low-confidence matches: {skills}",
                    "Add concrete examples and metrics"
                )
            )

        low_coverage = [
            c for c in categories.values() if c.coverage < 0.5
        ]
        if low_coverage:
            cat = low_coverage[0].category.value
            recs.append(
                Recommendation(
                    "Medium",
                    "Improve Category Coverage",
                    f"Low coverage in {cat}",
                    f"Focus learning in {cat} technologies"
                )
            )

        return recs[:5]
