# Daily User Workflow: From Plan to Pantry

This document defines the daily interaction cycle between the AI Agent and the User.

---

## 📅 Phase 1: Diet Generation (The "Plan")
**Trigger:** User request or scheduled weekly event.
1.  **User Profile Check:** Fetch user stats (weight, goal) and preferences (dislikes, diet type).
2.  **Nutrient Target:** Calculate RDA (Recommended Dietary Allowance) using the `Truth Layer` (PostgreSQL).
3.  **Meal Suggestion:** SLM generates a 3-meal plan that hits the nutrient targets.
4.  **Storage:** Meals are saved to `meal_history` for the next day.

---

## 🌙 Phase 2: Evening Kitchen Audit (The "Check")
**Trigger:** 8:00 PM Notification or User Check-in.
1.  **Fetch Tomorrow:** Retrieve tomorrow's meals from `meal_history`.
2.  **Decompose:** Pass the dishes through the **Dish Decomposition Engine**.
3.  **Inventory Query:**
    - **Agent:** "For tomorrow's Breakfast (Poha) and Lunch (Paneer Bhurji), you need: *Flattened Rice, Paneer, Onions, Tomatoes, and Green Chillies*. Do you have these?"
4.  **User Response:**
    - **Scenario A (All present):** "Yes." -> Agent: "Great, you're set for tomorrow!"
    - **Scenario B (Missing item):** "I don't have Paneer."
5.  **Real-Time Pivot:**
    - Agent detects "Paneer" is missing.
    - Queries `Truth Layer` for a substitute (e.g., Tofu or Eggs) or a different dish with similar nutrients.
    - Updates `meal_history` with the new meal.

---

## 🛠️ Implementation Plan

### 1. New Table: `kitchen_inventory` (Optional)
To remember what the user *usually* has, reducing the number of questions.

### 2. Route: `GET /meals/tomorrow/ingredients`
- Fetches tomorrow's meals.
- Uses `ai_service` to decompose them.
- Returns a clean list of ingredients for the UI to show as checkboxes.

### 3. Route: `POST /meals/pivot`
- Triggered if a user unchecks an ingredient.
- Re-runs the SLM to find a replacement meal using only "Available Ingredients."
