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
- **AI**: OpenAI GPT-4o-mini (Current), LLaMA 3.1 / DeepSeek recommended for upgrade.
- **Dependencies**: See `requirements.txt`.

🧠 **Best Open-Source AI Models for Diet Planning (2026)**
🥇 **1. LLaMA-based models (Best overall foundation)**
Examples: LLaMA 3.1 (8B / 70B), fine-tuned variants
Why:
Strong reasoning for nutrition constraints (calories, macros)
Works well with RAG + structured prompts
Evidence: LLM-based systems like NutriGen show very low error (~1.5%) in calorie alignment when using models like LLaMA 3.1

👉 Use this as your core brain

🥈 **2. DeepSeek (Very strong + cheaper compute)**
Example: DeepSeek-V3 / DeepSeek-Coder
Why:
Great reasoning + cheaper inference vs LLaMA
Ranked high in diet-plan evaluations (second tier but stable)
Good for:
Scaling + production cost optimization
🥉 **3. Phi-3 / Phi-3.5 (Best lightweight / local)**
Used in real projects like AI Diet Assistant with LM Studio
Why:
Runs locally (important for privacy in health apps)
Fast inference
Limitation:
Needs strong prompt engineering + external nutrition DB

👉 Perfect for MVP or on-device apps

🧪 **4. Mistral / Mixtral (Best for multi-agent setups)**
Why:
Works very well in multi-agent orchestration
Advanced research shows:
Multi-agent systems outperform single LLMs in nutrition planning (e.g., NutriOrion)

👉 Use if you're building:

"Coach + nutritionist + planner" system
🧩 **CRITICAL: Model Alone Is NOT Enough**

This is where most people fail.

Diet planning = system problem, not just model

You NEED:
1. Nutrition Knowledge Layer (RAG)
USDA / Indian food DB
Custom macros + recipes
Because:
LLMs alone can hallucinate nutrition info
2. Personalization Engine

Inputs:

Age, weight, BMI
Activity level
Medical conditions
Preferences (veg, Jain, keto, etc.)

AI systems today use:

Behavioral + biometric data for personalization
3. Dynamic Feedback Loop (IMPORTANT)
Track user response
Adjust diet daily

Modern systems:

Continuously adapt meal plans in real time
⚙️ **Best Architecture (What YOU should build)**

Since you mentioned TurboQuant, here's a strong stack:

🔥 **Recommended Stack**

Model Layer

LLaMA 3.1 / DeepSeek (primary)
Phi-3 (fallback / local)

Serving

TurboQuant (for quantized fast inference)
LM Studio / vLLM

Pipeline

User Input → Profile Builder → RAG (nutrition DB)
          → LLM (diet generation)
          → Constraint Validator (macros, allergies)
          → Feedback Loop (progress tracking)
🧠 **Pro-Level Upgrade (What top builders do)**

If you want to be serious:

Use Multi-Agent Setup:
Agent 1: Nutrition science
Agent 2: Meal planner
Agent 3: Behavior coach

This approach:

Reduces hallucinations
Improves clinical accuracy
🧪 **Real Open Source Projects You Can Study**
1. AI Diet Assistant (GitHub)
Uses:
Local LLM (Phi-3)
React + Flask
Features:
Personalized plans
Nutrition tracking
2. ChatDiet (Research Framework)
Combines:
Personal + population models
Achieves:
~92% effectiveness in recommendations
🚀 **Final Recommendation (Simple)**

If you want the best setup TODAY:

👉 Core model: LLaMA 3.1 (8B or 70B)
👉 Infra: TurboQuant + vLLM
👉 Add-ons:

RAG (nutrition DB)
Constraint engine
Feedback loop

👉 Later upgrade:

Multi-agent system (like NutriOrion)

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

