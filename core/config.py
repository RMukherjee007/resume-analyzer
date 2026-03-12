from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class SkillCategory(Enum):
    PROGRAMMING = "programming"
    DATA = "data"
    CLOUD = "cloud"
    DEVOPS = "devops"
    FRAMEWORK = "framework"


class Priority(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


CATEGORY_WEIGHTS = {
    SkillCategory.PROGRAMMING: 1.2,
    SkillCategory.DATA: 1.1,
    SkillCategory.CLOUD: 1.1,
    SkillCategory.DEVOPS: 0.9,
    SkillCategory.FRAMEWORK: 1.0,
}


@dataclass
class Skill:
    name: str
    category: SkillCategory
    weight: float = 1.0
    strict_match: bool = True
    variants: Optional[List[str]] = None


class SkillTaxonomy:

    def __init__(self):
        self.skills = [
            Skill("python", SkillCategory.PROGRAMMING, variants=["py"]),
            Skill("java", SkillCategory.PROGRAMMING),
            Skill("c++", SkillCategory.PROGRAMMING, variants=["cpp"]),
            Skill("sql", SkillCategory.DATA),
            Skill("pandas", SkillCategory.DATA),
            Skill("numpy", SkillCategory.DATA),
            Skill("aws", SkillCategory.CLOUD, variants=["amazon web services"]),
            Skill("docker", SkillCategory.DEVOPS),
            Skill("kubernetes", SkillCategory.DEVOPS),
            Skill("react", SkillCategory.FRAMEWORK),
            Skill("node.js", SkillCategory.FRAMEWORK, variants=["nodejs"]),
        ]

    def __iter__(self):
        return iter(self.skills)
