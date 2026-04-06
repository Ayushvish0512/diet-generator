from app.models.user import UserPreferences, GoalEnum, DietaryRestrictionEnum

def build_prompt(preferences: dict, failed_meals: list[str], feedback_notes: list[str]) -> str:
    restrictions = ", ".join(preferences.get("dietary_restrictions", [])) if preferences.get("dietary_restrictions") else "none"
    allergies = ", ".join(preferences.get("allergies", [])) if preferences.get("allergies") else "none"
    
    failed_section = ""
    if failed_meals:
        failed_section = f"Avoid these previously failed meals: {', '.join(failed_meals)}. "
    if feedback_notes:
        failed_section += f"User feedback from failures: {'; '.join(feedback_notes)}. "
    
    return f"""
    Generate a single daily meal suggestion (breakfast OR lunch OR dinner - pick one primary meal) for a {preferences.get('age', 30)} year old, 
    {preferences.get('weight_kg', 70)}kg, {preferences.get('height_cm', 170)}cm tall person with {preferences.get('activity_level', 'moderate')} activity level.
    
    Goal: {preferences.get('goal', 'maintenance')}
    Dietary restrictions: {restrictions}
    Allergies: {allergies}
    {failed_section}
    
    Provide one main meal with:
    - name
    - ingredients list
    - instructions
    - estimated calories
    - macros (protein/carbs/fat grams)
    
    Return ONLY JSON: {{"name": "Meal Name", "ingredients": ["item1", "item2"], "instructions": "steps...", "calories": 500, "macros": {{"protein": 30, "carbs": 60, "fat": 20}}}}
    
    Keep simple, realistic, under 45 min prep. Target ~{preferences.get('calories_per_day', 2200) / 3} calories.
    """


