# AI Diet Agent

A FastAPI application that generates personalized meal plans using AI (LLM) and stores data in Supabase.

## Setup

1. Copy `.env.example` to `.env` and fill in your secrets.
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload`

## Endpoints

- POST /preferences: Set user preferences
- POST /generate-meal: Generate AI meal plan
- POST /log-adherence: Log meal adherence



## Deploy to Render

Push to Git (exclude .env), connect to Render, set env vars.

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

Use Multi-Agent Setup:
Agent 1: Nutrition science
Agent 2: Meal planner
Agent 3: Behavior coach

🧪 **Real Open Source Projects You Can Study**
1. AI Diet Assistant (GitHub)
2. ChatDiet (Research Framework)

🚀 **Final Recommendation**
👉 Core model: LLaMA 3.1 (8B or 70B)
👉 Infra: TurboQuant + vLLM
👉 Add-ons: RAG (nutrition DB), Constraint engine, Feedback loop

