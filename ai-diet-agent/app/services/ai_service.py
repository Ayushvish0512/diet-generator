from openai import AsyncOpenAI
from app.config import settings
from app.utils.prompt_builder import build_diet_prompt
from app.models.user import UserPreferences
from app.models.meal import MealPlan

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_meal_plan(preferences: UserPreferences) -> MealPlan:
    prompt = build_diet_prompt(preferences)
    
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    # Parse response to MealPlan (in production, use structured output)
    meal_plan_str = response.choices[0].message.content
    # Simplified parsing - replace with proper JSON extraction
    return MealPlan.model_validate_json(meal_plan_str)

