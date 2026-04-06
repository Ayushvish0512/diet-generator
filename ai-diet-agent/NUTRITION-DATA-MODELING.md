# Nutrition Data Modeling & System Design

The difference between a toy RAG system and a production nutrition app is **data modeling**. If your structure is weak, your LLM will give inaccurate or unsafe diet plans. This document outlines the data-engineering view: schemas, data shapes, and how that flows into a Small Language Model (SLM).

---

## 🧠 1. Core Principle: Parallel Representations

Do **NOT** feed raw internet text directly to an SLM. You must build two parallel representations:
1.  **Structured Layer:** Authoritative, numeric, and queryable (PostgreSQL).
2.  **Unstructured Layer:** Text chunks for semantic retrieval (Vector DB/RAG).

---

## 🧱 2. Data Shapes (JSON for Queries & Logic)

### 🔹 Input Meal (from DB)
```json
{
  "meal": [
    { "food": "milk", "qty_g": 250 },
    { "food": "fish", "qty_g": 150 }
  ]
}
```

### 🔹 Aggregated Nutrients (Computed)
```json
{
  "protein_g": 45,
  "calcium_mg": 400,
  "calories_kcal": 500
}
```

### 🔹 Deficiency Object (VERY IMPORTANT)
This is the primary object fed to the SLM.
```json
{
  "deficiencies": {
    "protein_g": 15,
    "calcium_mg": 600
  }
}
```

---

## 🔍 3. RAG Layer (Vector DB Knowledge)

Do **NOT** embed numeric tables. Embed **semantic knowledge** that explains the "why" and "how".

**Example Chunk:**
```json
{
  "text": "Milk is high in calcium but low in iron. Fish is high in protein but does not provide enough calcium to meet daily requirements alone.",
  "metadata": {
    "source": "nutrition_guideline",
    "tags": ["calcium", "protein"]
  }
}
```

---

## 🤖 4. SLM Integration (Prompting & Fine-Tuning)

### 🔹 Prompt Input Format
```json
{
  "user_profile": { "age": 25, "weight": 70, "goal": "muscle_gain" },
  "current_meal": [ { "food": "milk", "qty_g": 250 }, { "food": "fish", "qty_g": 150 } ],
  "nutrient_totals": { "protein_g": 45, "calcium_mg": 400 },
  "deficiencies": { "protein_g": 15, "calcium_mg": 600 },
  "retrieved_knowledge": [
    "Milk is high in calcium but not sufficient alone.",
    "Leafy greens and dairy help meet calcium needs."
  ]
}
```

### 🔹 Fine-Tuning Dataset Format
If you fine-tune, the model should learn to map deficiency objects to structured suggestions.
```json
{
  "input": { "deficiencies": { "protein_g": 20, "calcium_mg": 500 } },
  "output": {
    "suggestions": [
      { "food": "chicken breast", "reason": "high protein" },
      { "food": "milk", "reason": "high calcium" }
    ]
  }
}
```

---

## ⚙️ 5. Pipeline (End-to-End Data Flow)

1.  **Ingest:** Fetch data (USDA API, etc.) and normalize into the Relational DB.
2.  **Log:** User logs a meal; store in `meal_items`.
3.  **Compute:** Backend computes nutrient totals and compares with user requirements.
4.  **Detect:** Identify deficiencies and build a **Deficiency Object**.
5.  **Retrieve:** Query Vector DB for semantic knowledge related to detected deficiencies.
6.  **Prompt:** Build a structured JSON prompt for the SLM.
7.  **Generate:** SLM generates personalized suggestions and explanations.

---

## 🛠️ 6. Minimal Tech Stack

-   **DB:** PostgreSQL (Source of Truth)
-   **Vector DB:** FAISS / Pinecone / Chroma
-   **Backend:** Python (FastAPI)
-   **Embeddings:** `sentence-transformers`
-   **SLM:** LLaMA-3 / Mistral (3B–7B)

---

## 🚨 The Golden Rule
-   ❌ **Math** is deterministic (handled by the DB layer).
-   ✅ **Knowledge** is retrieved (RAG).
-   ✅ **Language** is generated (SLM).
