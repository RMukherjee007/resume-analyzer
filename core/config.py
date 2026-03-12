from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class SkillCategory(Enum):
    PROGRAMMING = "programming"
    DATA = "data"
    CLOUD = "cloud"
    DEVOPS = "devops"
    FRAMEWORK = "framework"

@dataclass
class Skill:
    name: str
    category: SkillCategory
    weight: float = 1.0
    strict_match: bool = True
    variants: Optional[List[str]] = None

class SkillTaxonomy:
    """Defines the static taxonomy of skills to extract from documents."""
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
            Skill("kubernetes", SkillCategory.DEVOPS, variants=["k8s"]),
            Skill("react", SkillCategory.FRAMEWORK, variants=["reactjs"]),
            Skill("node.js", SkillCategory.FRAMEWORK, variants=["nodejs"]),
        ]

    def __iter__(self):
        return iter(self.skills)
