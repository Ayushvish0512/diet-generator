# Automated Dish Decomposition Engine

A production-grade nutrition system must go beyond simple food logging. It requires a sophisticated engine to decompose complex Indian dishes into their constituent ingredients to provide accurate nutrient estimates.

---

## 🧠 0. The Core Concept: Inference Engine
The goal is to move from a single dish name to a granular nutrient profile:
**Dish** → **Ingredients** → **Nutrients**

**Example:**
`"paneer butter masala"`
↓
- `paneer`: 120g
- `butter`: 20g
- `tomato_gravy`: 100g
- `cream`: 30g
- `oil`: 10g

---

## ⚙️ 1. AI-First System Architecture
`User Input` → `Dish Detection` → `Decomposition Model (AI)` → `Ingredient Normalization` → `Gram Estimation Model` → `Nutrient Engine`

---

## 🧩 2. Core Components

### 🔹 A. Dish Decomposition Model (Local SLM)
Using local models like **LLaMA-3** or **Mistral-7B** via Ollama to identify ingredients.

**Prompt Strategy:**
```json
{
  "task": "decompose_indian_dish",
  "input": "paneer butter masala",
  "output_format": {
    "ingredients": [
      { "name": "paneer", "role": "primary" },
      { "name": "butter", "role": "fat" },
      { "name": "tomato", "role": "base" },
      { "name": "cream", "role": "fat" },
      { "name": "oil", "role": "cooking" }
    ]
  }
}
```

### 🔹 B. Quantity Estimation Model (Priors + AI)
Estimating ratios is harder than identifying ingredients.
1.  **Template Priors:** Use a default distribution for common dishes (e.g., 40% protein, 40% gravy, 20% fat for curries).
2.  **AI Refinement:** The SLM adjusts grams based on the specific dish and portion size (e.g., "Estimate grams for 1 serving (250g) of Paneer Butter Masala").

---

## 🔁 3. The Full Pipeline Flow
1.  **Split:** "2 roti + paneer butter masala" → `["roti", "paneer butter masala"]`.
2.  **Decompose:** Identify the 5-7 core ingredients of the curry.
3.  **Estimate:** Assign grams to each ingredient based on a standard 250g serving.
4.  **Normalize:** Map identified ingredients to the `food_id` in your PostgreSQL database.
5.  **Compute:** Run the SQL nutrient engine to get final totals.

---

## 🤖 4. Fully Automated Feedback Loop
To avoid redundant AI calls and improve accuracy over time:
1.  **Store:** Save every unique AI decomposition in a `dish_decompositions` table.
2.  **Review:** Flag decompositions for human or expert-agent approval.
3.  **Reuse:** Check the DB first; only use the AI if the dish is new.
*Result: The AI becomes a fallback as your ground-truth database grows.*

---

## ⚠️ 5. Real-World Challenges & Solutions

| Problem | Solution |
| :--- | :--- |
| **Context Variance** | Add context tags: `"restaurant"` (high fat) vs `"home"` (low fat). |
| **Ingredient Explosion** | Group minor items: use `"spices_mix"` instead of listing 10 individual spices. |
| **Portion Ambiguity** | Use standard priors: `"1 plate"` = 300g–400g. |

---

## 🚀 6. The Hybrid Winning Strategy
The most robust system is neither fully AI nor fully rules-based. It is a **Hybrid Model**:
- **SLM** for structure and logic.
- **Embeddings** for matching and mapping.
- **Historical Data** for memory and correction.
- **Priors** for mathematical boundaries.
