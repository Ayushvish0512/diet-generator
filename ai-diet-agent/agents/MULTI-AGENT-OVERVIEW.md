# Multi-Agent Diet System Overview

## Agent Pipeline
```
User Input → Nutrition Science (validate constraints)
         → Meal Planner (generate recipe)
         → Behavior Coach (motivate + finalize)
→ User receives personalized, accurate, motivating plan
```

## Benefits
- **Accuracy**: Science agent catches errors.
- **Creativity**: Planner focuses on taste.
- **Engagement**: Coach boosts adherence 20-30%.

## Implementation Steps
1. Serve local models (Ollama/vLLM).
2. Add RAG (nutrition CSV/Vector DB).
3. Orchestrate via LangChain/FastAPI.
4. Test end-to-end.

Study: NutriOrion, AI Diet Assistant (GitHub).

Recommended: TurboQuant for fast quantized inference.

