# AI Diet Agent - How It Works

## Overview
The AI Diet Agent is a FastAPI web application that generates **personalized daily meal plans** using AI (GPT-4o-mini via OpenAI). It integrates with **Supabase** for data storage and learns from user feedback to improve suggestions over time. The app focuses on iterative refinement based on adherence history.

Key goals:
- Generate meals matching user preferences (e.g., calories, macros, allergies, dietary restrictions).
- Track adherence (did you follow the meal?) and feedback.
- Avoid repeating failed meals and incorporate user notes for better future plans.

## Architecture
```
Frontend/Client → FastAPI Endpoints → Services (AI/Meal/DB) → Supabase DB + OpenAI
```
- **Database**: Supabase PostgreSQL with tables: `preferences`, `meal_history`.
- **AI Integration**: OpenAI GPT for natural language meal generation.
- **Key Components**:
  | Component | Purpose |
  |-----------|---------|
  | `app/routes/*` | API endpoints |
  | `app/services/*` | Business logic (AI prompts, DB ops) |
  | `app/models/*` | Pydantic schemas |
  | `app/utils/prompt_builder.py` | Dynamic AI prompts |
  | `app/db/supabase_client.py` | DB client |

## User Workflow
1. **Set Preferences** (`POST /preferences/{user_id}`):
   - User provides: goals (weight loss/muscle gain), calories, macros, allergies, restrictions (vegan/keto).
   - Stored in `preferences` table.
   ```python
   # Example payload
   {
     "goals": "weight_loss",
     "target_calories": 2000,
     "macros": {"protein": 30, "carbs": 40, "fat": 30},
     "allergies": ["nuts"],
     "dietary_restrictions": ["vegetarian"]
   }
   ```

2. **Generate Meal** (`POST /generate-meal`):
   - Fetches user preferences and **past failed meals** + feedback from `meal_history`.
   - Builds contextual AI prompt: \"Generate a meal avoiding [failed_meals], considering [feedback]. Match [preferences].\"
   - Calls OpenAI → Parses response to meal dict (name, ingredients, instructions, nutrition).
   - Saves to `meal_history` (unmarked adherence).
   - Returns meal plan.

3. **Log Adherence** (`POST /log-adherence`):
   - User reports: `meal_name`, `followed: bool`, optional `feedback`.
   - Updates `meal_history`. Failures + feedback used in future generations.
   ```python
   # Example
   {"meal_name": "Chicken Stir Fry", "followed": false, "feedback": "Too spicy"}
   ```

4. **Repeat**: Next `/generate-meal` uses history for smarter suggestions.

## Data Flow Example
```
1. User sets prefs → DB
2. Generate meal:
   Prefs: vegetarian, 2000cal
   History: failed \"Spicy Curry\" (feedback: too oily)
   → Prompt: \"Vegetarian 2000cal meal, avoid oily like curry...\"
   → AI: \"Lentil Soup\" → Save to history → Return
3. User logs: followed=false, \"Bland\"
4. Next gen avoids soup + curry
```

## Key Features
- **Personalization**: AI uses full context (prefs + history).
- **Learning Loop**: Adherence feedback refines prompts.
- **Structured Output**: Meals include nutrition/macros.
- **Scalable**: Dockerized, deployable to Render/Heroku.

## Tech Stack
- **Backend**: FastAPI, Pydantic, Uvicorn.
- **DB**: Supabase (Postgres + auth).
- **AI**: OpenAI GPT-4o-mini.
- **Dependencies**: See `requirements.txt`.

## Running the App
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Visit `http://localhost:8000/docs` for interactive API docs.

## Future Improvements (from TODO.md)
- Full model validation/tests.
- UI frontend.
- More AI structure (JSON mode).

This app creates an **adaptive diet coach** that gets better with use!

