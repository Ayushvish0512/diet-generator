from pydantic import BaseModel
from typing import Optional
from app.models.meal import MealPlan
from datetime import date

class AdherenceLog(BaseModel):
    user_id: str
    date: date
    meal_plan: MealPlan
    adherence_score: float  # 0-1
    notes: Optional[str] = None

