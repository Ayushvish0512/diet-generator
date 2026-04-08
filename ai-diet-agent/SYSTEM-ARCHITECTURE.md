# System Architecture & Pipeline Design

This document outlines the end-to-end technical architecture of the AI Diet Agent, focusing on how data moves from raw sources to personalized SLM-generated meal suggestions.

---

## 🧱 1. ETL Pipeline (India Nutrition Data)

A production-grade pipeline that ensures ground-truth accuracy.

### 🔄 High-Level Flow
`Sources` → `Raw Storage` → `Cleaning` → `Normalization` → `DB Insert`

1.  **Ingestion Layer:**
    - **Structured (Priority):** ICMR-NIN, IFCT.
    - **Semi-structured:** HealthifyMe, Open Food Facts.
    - **Unstructured (RAG):** Dietary Guidelines for Indians.
2.  **Raw Storage:** Store data in its original form before cleaning (e.g., `raw_food_data` table in Postgres).
3.  **Cleaning Layer:** Unit normalization (mg to g), null removal, and deduplication.
4.  **Canonical Mapping:** Map raw names (e.g., "Milk, cow, whole") to canonical names ("milk").
5.  **Validation Layer:** Reject anomalies (e.g., Protein > 100g/100g or Calories > 900kcal/100g).

---

## 🧠 2. Food Normalization System (The Hardest Part)

Converts messy user input into structured, canonical food entities.

### 🔹 Architecture
`User Input` → `Preprocessing` → `Entity Detection` → `Canonical Mapping` → `Portion Conversion`

-   **Preprocessing:** Lowercasing, stopword removal (e.g., "and", "with").
-   **Entity Detection:** Hybrid approach using a dictionary of Indian foods (Paneer, Roti, Dal) and fine-tuned NLP.
-   **Canonical Mapping Table (`food_aliases`):**
    - `roti` → `wheat_roti`
    - `paneer butter masala` → `paneer_curry`
-   **Fuzzy Matching:** Using Levenshtein distance or `sentence-transformers` for "panner" → "paneer".
-   **Portion Normalization:** Converting "1 katori" or "2 roti" into grams (e.g., 1 roti = 30g).

---

## ⚙️ 3. Computation Engines

### 🔹 Meal → Nutrient Engine (Deterministic)
Calculates the total nutrient profile of a logged meal using SQL or Python.
```sql
SELECT 
  n.name,
  SUM(fn.value_per_100g * mi.quantity_g / 100) as total
FROM meal_items mi
JOIN food_nutrients fn ON mi.food_id = fn.food_id
JOIN nutrients n ON fn.nutrient_id = n.id
WHERE mi.meal_id = :meal_id
GROUP BY n.name;
```

### 🔹 Deficiency Engine
Computes the gap between required and actual nutrients.
```python
def compute_deficiency(required, actual):
    return {
        k: max(required[k] - actual.get(k, 0), 0)
        for k in required
    }
```

---

## 🔎 4. RAG & SLM Integration (MedGemma Edition)

1.  **RAG Pipeline:** Retrieves semantic knowledge (e.g., "Leafy greens are rich in calcium") based on detected deficiencies.
2.  **Prompt Builder:** Constructs a structured JSON prompt containing deficiencies and retrieved context.
3.  **SLM Generation:** Powered by **MedGemma-4b-it** running locally via **Ollama**. This specialized medical model maps `deficiency` → `food suggestions` with clinical-grade accuracy.

---

## 📐 5. Final System Map

```text
                ┌──────────────┐
                │  Data Sources │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ ETL Pipeline │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ PostgreSQL   │ (Truth Layer)
                └──────┬───────┘
                       ↓
User Input → Normalization → Meal Engine → Deficiency Engine
                                      ↓
                                RAG Retrieval (Vector DB)
                                      ↓
                                  SLM (Intelligence Layer)
                                      ↓
                             Meal Suggestions
```

---

## ⚠️ Critical Success Factors
- **Food Alias Mapping:** 70% of the effort goes here.
- **Portion → Grams:** Essential for accurate math.
- **Mixed Dish Decomposition:** Breaking "Paneer Butter Masala" into its core components for nutrient estimation.
