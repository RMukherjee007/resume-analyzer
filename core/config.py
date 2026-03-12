from dataclasses import dataclass
from enum import Enum


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
    SkillCategory.FRAMEWORK: 1.0
}


@dataclass
class Skill:
    name: str
    category: SkillCategory
    weight: float = 1.0
    variants: list[str] | None = None
