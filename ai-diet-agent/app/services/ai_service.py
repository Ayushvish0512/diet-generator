from openai import AsyncOpenAI, OpenAI
import json
from app.config import settings
from app.utils.prompt_builder import build_diet_prompt
from app.models.user import UserPreferences
from app.models.meal import MealPlan
from app.utils.prompt_builder import build_prompt

if settings.USE_LOCAL_MODEL:
    # Use OpenAI SDK but point it to the local Ollama endpoint
    client = AsyncOpenAI(
        base_url=settings.OLLAMA_BASE_URL,
        api_key="ollama" # Required but ignored by Ollama
    )
    sync_client = OpenAI(
        base_url=settings.OLLAMA_BASE_URL,
        api_key="ollama"
    )
    MODEL_NAME = settings.OLLAMA_MODEL
else:
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    sync_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    MODEL_NAME = "gpt-4o-mini"

async def generate_meal_plan(preferences: UserPreferences) -> MealPlan:
    prompt = build_diet_prompt(preferences)
    
    response = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2 # Lower temperature for medical precision
    )
    
    meal_plan_str = response.choices[0].message.content
    # MedGemma might wrap JSON in ```json blocks
    if "```json" in meal_plan_str:
        meal_plan_str = meal_plan_str.split("```json")[1].split("```")[0]
    
    return MealPlan.model_validate_json(meal_plan_str)

def generate_meal_from_ai(prompt: str) -> dict:
    response = sync_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    
    content = response.choices[0].message.content
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
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
