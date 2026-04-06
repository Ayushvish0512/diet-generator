# diet-generator

Deciding what to cook every day when you live alone is a massive drain on mental energy, especially when you don't actually enjoy intensive cooking. Building an AI agent to handle the decision-making, track your habits, and cater to your laziness (in the best way possible) is a perfect solution.

Here is a combined Business Requirements Document (BRD) and Product Requirements Document (PRD), tailored specifically to your tech stack (FastAPI, Supabase, Render) and low-effort lifestyle, along with a step-by-step execution plan.

Part 1: Business Requirements Document (BRD)
1. Problem Statement
Living alone introduces "meal decision fatigue." The user wants to eat reasonably well but lacks the time, skill, and desire to cook complex meals. Constantly deciding what to eat, buying the right groceries, and actually cooking leads to takeout reliance or skipping meals.

2. Business Objectives
Automate Decision Making: Remove the "what's for dinner?" question entirely by generating an automated, highly personalized meal plan.

Minimize Cooking Friction: Ensure recommended meals require minimal prep time, basic equipment, and low culinary skill.

Create a Feedback Loop: Track whether the user actually followed the diet to train the AI on what meals are actually realistic for them to make, rather than purely aspirational ones.

3. Success Metrics (KPIs)
Adherence Rate: The percentage of generated meals marked as "followed."

Generation Speed: Time taken by the AI to formulate a weekly or daily plan.

Prep Time Limit: 100% of generated meals must fall under the user's defined maximum prep time (e.g., < 20 minutes).

Part 2: Product Requirements Document (PRD)
1. Product Overview
A backend-driven AI Diet Agent that stores user preferences and past eating habits in a database. It uses an LLM (like Gemini or OpenAI) to generate hyper-personalized, ultra-simple meal plans. The system asks the user for feedback on past meals ("Did you eat this?") to continuously refine its future recommendations.

2. Core Features
Preference Engine: Stores macros, allergies, disliked ingredients, and a strict "max prep time."

AI Diet Generator: Fetches past adherence data and current preferences, feeding them into an LLM prompt to output a JSON-formatted meal plan.

Adherence Tracker: A simple mechanism to log binary feedback (Followed / Did Not Follow) or specific feedback (e.g., "Too many pots to clean").

Pantry/Grocery Awareness (V2): Keeps track of common ingredients the user usually has to avoid complex grocery runs.

3. Tech Stack
Framework: FastAPI (Python) - Fast, great for AI/data logic, auto-generates Swagger UI docs.

Database & Auth: Supabase (PostgreSQL) - Handles relational data easily with a great Python client.

Hosting: Render - Easy deployment for FastAPI via Docker or native Python environments.

AI Model: Any LLM API (Gemini, Claude, or OpenAI) for the generation logic.

4. Database Schema (Supabase)
users table:

id (UUID, Primary Key)

dietary_restrictions (Text array - e.g., ["lactose intolerant"])

dislikes (Text array - e.g., ["eggplant", "mushrooms"])

max_prep_time_minutes (Integer - e.g., 20)

meals_library table (Optional, to save AI costs by reusing good meals):

id (UUID)

name (String)

ingredients (JSONB)

instructions (Text)

prep_time (Integer)

diet_history table:

id (UUID)

user_id (UUID, Foreign Key)

meal_name (String)

date_assigned (Date)

followed (Boolean - True/False/Null)

feedback_notes (Text - e.g., "Took too long", "Tasted bland")

5. API Endpoints (FastAPI)
GET /preferences: Fetches current user dietary rules.

PUT /preferences: Updates dislikes, max prep time, etc.

POST /generate-meal: The core AI endpoint. Fetches past diet_history where followed = False (to avoid suggesting failed concepts), fetches preferences, sends a prompt to the LLM, and returns the meal.

POST /log-adherence: Updates the diet_history table with whether the user actually cooked/ate the meal.

Part 3: Step-by-Step Execution Plan
Phase 1: Infrastructure Setup (Day 1)
Supabase: Create a new Supabase project. Execute SQL statements to create the users and diet_history tables. Get your SUPABASE_URL and SUPABASE_KEY.

FastAPI Setup: Initialize a new Python environment.

Run pip install fastapi uvicorn supabase pydantic python-dotenv openai (or your preferred LLM SDK).

Create a main.py file and set up a basic /health endpoint to test.

Phase 2: Database Integration (Day 2)
Connect Supabase: In your FastAPI app, initialize the Supabase client.

Build CRUD Endpoints: * Write the Pydantic models for your user preferences and meal history.

Create endpoints to add preferences and fetch past history.

Test via FastAPI's automatic Swagger UI (/docs).

Phase 3: The AI Brain (Day 3-4)
Construct the Context Prompt: This is the most crucial step. Write a Python function that builds the prompt dynamically.

Example logic: "You are a chef for a lazy single person. Their max prep time is X. They hate Y. Last week, you suggested Z, but they did not cook it because it required too much chopping. Suggest 1 meal for tonight. Output in strict JSON containing 'name', 'ingredients', 'instructions_in_3_steps'."

Integrate LLM API: Call the AI model with the constructed prompt.

Parse & Save: Receive the JSON from the AI, return it to the user via the API, and simultaneously log an entry in the diet_history table with followed = Null.

Phase 4: The Adherence Loop (Day 5)
Build Feedback Endpoint: Create the POST /log-adherence endpoint.

Update Logic: This endpoint should take the meal_id and a boolean (True/False), plus optional text feedback, and update the Supabase row.

Phase 5: Deployment on Render (Day 6)
Prepare for Production: Ensure all API keys (Supabase, LLM) are stored in a .env file and loaded via os.environ or python-dotenv.

Create requirements.txt: pip freeze > requirements.txt.

Deploy: Connect your GitHub repo to Render. Create a new "Web Service". Set the build command to pip install -r requirements.txt and the start command to uvicorn main:app --host 0.0.0.0 --port 10000. Add your environment variables in the Render dashboard.

Phase 6: Front-end / Interaction (Future)
Since you are a solo dev building this for yourself, you don't even need a full front-end initially. You can trigger the FastAPI endpoints using Postman, Apple Shortcuts (Siri), or a simple Telegram Bot to message you your meals and ask for a Yes/No response on adherence.
