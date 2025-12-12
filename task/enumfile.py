from enum import Enum

class CategoryEnum(str, Enum):
    bug = "bug"
    feature = "feature"
    assignment = "assignment"
    improvement = "improvement"
    other = "other"

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class StatusEnum(str, Enum):
    todo = "todo"
    in_progress = "in-progress"
    review = "review"
    done = "done"
