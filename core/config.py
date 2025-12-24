from dataclasses import dataclass, field
from typing import List, Dict, Iterable
from enum import Enum


class SkillCategory(Enum):
    LANGUAGES = "languages"
    FRAMEWORKS = "frameworks"
    ML = "ml"
    DEVOPS = "devops"
    CLOUD = "cloud"
    DATABASES = "databases"
    FUNDAMENTALS = "fundamentals"


class Priority(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass(frozen=True)
class Skill:
    """
    Domain object representing a technical skill.
    """
    name: str
    category: SkillCategory
    weight: float = 1.0
    variants: List[str] = field(default_factory=list)
    strict_match: bool = False  # avoids false positives (e.g., Go)

    def __post_init__(self):
        object.__setattr__(self, "variants",
                           [v.lower().strip() for v in self.variants])


class SkillTaxonomy:
    """
    Central registry for all supported skills.
    Single responsibility: skill definition & lookup.
    """

    def __init__(self):
        self._skills: Dict[str, Skill] = {}
        self._variant_index: Dict[str, Skill] = {}
        self._load_skills()

    def _register(self, skill: Skill):
        self._skills[skill.name.lower()] = skill
        for variant in skill.variants:
            self._variant_index[variant] = skill

    def _load_skills(self):
        skills_data = [
            # Languages
            Skill("Python", SkillCategory.LANGUAGES, 1.2, ["python", "python3", "py"]),
            Skill("Java", SkillCategory.LANGUAGES, 1.2, ["java", "java8", "java11"]),
            Skill("JavaScript", SkillCategory.LANGUAGES, 1.2, ["javascript", "js", "es6"]),
            Skill("TypeScript", SkillCategory.LANGUAGES, 1.1, ["typescript", "ts"]),
            Skill("C++", SkillCategory.LANGUAGES, 1.1, ["c++", "cpp", "cplusplus"]),
            Skill("C", SkillCategory.LANGUAGES, 1.0, ["c programming"], strict_match=True),
            Skill("C#", SkillCategory.LANGUAGES, 1.1, ["c#", "csharp"]),

            Skill("Go", SkillCategory.LANGUAGES, 1.0, ["golang"], strict_match=True),

            # Frameworks
            Skill("React", SkillCategory.FRAMEWORKS, 1.0, ["react", "reactjs"]),
            Skill("Angular", SkillCategory.FRAMEWORKS, 0.9, ["angular"]),
            Skill("Vue.js", SkillCategory.FRAMEWORKS, 0.9, ["vue", "vuejs"]),
            Skill("Node.js", SkillCategory.FRAMEWORKS, 1.0, ["nodejs", "node"]),
            Skill("Django", SkillCategory.FRAMEWORKS, 1.0, ["django"]),
            Skill("Flask", SkillCategory.FRAMEWORKS, 0.9, ["flask"]),
            Skill("Spring Boot", SkillCategory.FRAMEWORKS, 1.0, ["spring boot", "spring"]),
            Skill(".NET", SkillCategory.FRAMEWORKS, 1.0, ["dotnet", ".net"]),

            # ML
            Skill("TensorFlow", SkillCategory.ML, 1.0, ["tensorflow", "tf"]),
            Skill("PyTorch", SkillCategory.ML, 1.0, ["pytorch", "torch"]),
            Skill("scikit-learn", SkillCategory.ML, 0.9, ["sklearn"]),

            # DevOps
            Skill("Docker", SkillCategory.DEVOPS, 1.0, ["docker"]),
            Skill("Kubernetes", SkillCategory.DEVOPS, 0.9, ["kubernetes", "k8s"]),
            Skill("Git", SkillCategory.DEVOPS, 0.8, ["git", "github"]),

            # Cloud
            Skill("AWS", SkillCategory.CLOUD, 1.0, ["aws", "amazon web services"]),
            Skill("Azure", SkillCategory.CLOUD, 0.9, ["azure"]),
            Skill("GCP", SkillCategory.CLOUD, 0.9, ["gcp", "google cloud"]),

            # Databases
            Skill("SQL", SkillCategory.DATABASES, 1.1, ["sql"]),
            Skill("MySQL", SkillCategory.DATABASES, 0.9, ["mysql"]),
            Skill("PostgreSQL", SkillCategory.DATABASES, 0.9, ["postgresql", "postgres"]),
            Skill("MongoDB", SkillCategory.DATABASES, 0.9, ["mongodb", "mongo"]),

            # Fundamentals
            Skill("Algorithms", SkillCategory.FUNDAMENTALS, 1.3, ["algorithms", "algo", "dsa"]),
            Skill("Data Structures", SkillCategory.FUNDAMENTALS, 1.3, ["data structures", "dsa"]),
            Skill("OOP", SkillCategory.FUNDAMENTALS, 1.1, ["oop", "object oriented"]),
            Skill("System Design", SkillCategory.FUNDAMENTALS, 1.2, ["system design", "architecture"]),
        ]

        for skill in skills_data:
            self._register(skill)

    def get_all_skills(self) -> Iterable[Skill]:
        return self._skills.values()

    def get_by_variant(self, variant: str) -> Skill | None:
        return self._variant_index.get(variant.lower())

    def __iter__(self):
        return iter(self._skills.values())


CATEGORY_WEIGHTS = {
    SkillCategory.FUNDAMENTALS: 1.3,
    SkillCategory.LANGUAGES: 1.2,
    SkillCategory.FRAMEWORKS: 1.0,
    SkillCategory.ML: 1.0,
    SkillCategory.DEVOPS: 0.9,
    SkillCategory.CLOUD: 1.0,
    SkillCategory.DATABASES: 0.9,
}
