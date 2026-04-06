from app.models.user import UserPreferences, GoalEnum, DietaryRestrictionEnum

def build_diet_prompt(preferences: UserPreferences) -> str:
    restrictions = ", ".join(preferences.dietary_restrictions) if preferences.dietary_restrictions else "none"
    allergies = ", ".join(preferences.allergies) if preferences.allergies else "none"
    
    return f"""
    Generate a personalized 1-day meal plan for a {preferences.age} year old, 
    {preferences.weight_kg}kg, {preferences.height_cm}cm tall person with {preferences.activity_level} activity level.
    
    Goal: {preferences.goal.value}
    Dietary restrictions: {restrictions}
    Allergies: {allergies}
    
    Provide breakfast, lunch, dinner, and 2 snacks. Include:
    - Recipe name
    - Ingredients list
    - Instructions
    - Estimated calories
    - Macros (protein/carbs/fat grams)
    
    Return as valid JSON matching this schema:
    {{
        "date": "YYYY-MM-DD",
        "breakfast": {{...}},
        "lunch": {{...}},
        "dinner": {{...}},
        "snacks": [{{...}}, {{...}}],
        "total_calories": 1100
    }}
    
    Each meal: {{"name": "...", "ingredients": [...], "instructions": "...", "calories": 500, "macros": {{"protein": 30, "carbs": 60, "fat": 20}}}}
    Target ~{preferences.calories_per_day or 2200} calories total.
    """

