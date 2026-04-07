from openai import AsyncOpenAI, OpenAI
import json
from app.config import settings
from app.utils.prompt_builder import build_diet_prompt
from app.models.user import UserPreferences
from app.models.meal import MealPlan
from app.utils.prompt_builder import build_prompt

if settings.USE_LOCAL_MODEL:
    from app.services.local_model_service import get_local_model
    # The local model uses its own singleton to manage memory
    local_ai = get_local_model()
else:
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    sync_client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_meal_plan(preferences: UserPreferences) -> MealPlan:
    prompt = build_diet_prompt(preferences)
    
    if settings.USE_LOCAL_MODEL:
        # MedGemma expects JSON instructions in the prompt
        result = local_ai.generate_json(prompt)
        return MealPlan.model_validate(result)
    else:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        meal_plan_str = response.choices[0].message.content
        return MealPlan.model_validate_json(meal_plan_str)

def generate_meal_from_ai(prompt: str) -> dict:
    if settings.USE_LOCAL_MODEL:
        return local_ai.generate_json(prompt)
    else:
        response = sync_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content
        # ... rest of the existing JSON parsing logic
    
    try:
        meal = json.loads(content)
        if isinstance(meal, dict):
            return meal
        else:
            # Fallback if list or str
            return {"name": "AI Generated Meal", "ingredients": [], "instructions": content, "calories": 500, "macros": {"protein": 25, "carbs": 50, "fat": 20}}
    except json.JSONDecodeError:
        return {"name": "Simple Meal Suggestion", "ingredients": ["basic ingredients"], "instructions": content[:300], "calories": 500, "macros": {"protein": 25, "carbs": 50, "fat": 20}}
