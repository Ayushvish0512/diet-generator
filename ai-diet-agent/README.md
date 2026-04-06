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

