from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class GoalEnum(str, Enum):
    weight_loss = "weight_loss"
    muscle_gain = "muscle_gain"
    maintenance = "maintenance"

class DietaryRestrictionEnum(str, Enum):
    vegetarian = "vegetarian"
    vegan = "vegan"
    gluten_free = "gluten_free"
    keto = "keto"

class UserPreferences(BaseModel):
    user_id: str
    age: int
    weight_kg: float
    height_cm: int
    activity_level: str = "moderate"
    goal: GoalEnum = GoalEnum.maintenance
    dietary_restrictions: Optional[List[DietaryRestrictionEnum]] = []
    allergies: Optional[List[str]] = []
    calories_per_day: Optional[int] = None

