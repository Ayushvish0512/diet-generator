# Database Schema

### 1️⃣ users Table
**Purpose:** Store basic user identity. `email` is the primary key.

| Column Name | Type | Constraints / Notes |
| :--- | :--- | :--- |
| email | TEXT | Primary Key |
| name | TEXT | Optional, user’s name |
| created_at | TIMESTAMP | Default: `now()` |

**Notes:**
- You can generate UUID if needed, but email serves as the unique identifier.
- This table will be referenced by `preferences` and `meal_history`.

---

### 2️⃣ preferences Table
**Purpose:** Store user-specific diet and meal preferences.

| Column Name | Type | Constraints / Notes |
| :--- | :--- | :--- |
| email | TEXT | Foreign Key → `users.email`, Primary Key |
| dietary_restrictions | TEXT[] | E.g., `["lactose intolerant", "gluten-free"]` |
| dislikes | TEXT[] | E.g., `["eggplant", "mushrooms"]` |
| max_prep_time_minutes | INTEGER | Max minutes the user is willing to cook |
| diet_preferences | TEXT[] | E.g., `["low-carb", "high-protein"]` |
| created_at | TIMESTAMP | Default: `now()` |
| updated_at | TIMESTAMP | Auto-update on change |

**Notes:**
- `diet_preferences` allows capturing user’s broader diet style (keto, vegan, Mediterranean, etc.).
- You can upsert this table whenever a user updates their preferences.

---

### 3️⃣ meal_history Table
**Purpose:** Track what meals were suggested, adherence, and feedback.

| Column Name | Type | Constraints / Notes |
| :--- | :--- | :--- |
| id | UUID | Primary Key, generated per meal |
| email | TEXT | Foreign Key → `users.email` |
| meal_name | TEXT | Name of the suggested meal |
| ingredients | JSONB | List of ingredients used in the meal |
| instructions_in_3_steps | JSONB | List of 3-step instructions |
| prep_time | INTEGER | Minutes taken to prepare |
| date_assigned | DATE | When the meal was suggested |
| followed | BOOLEAN | True/False/NULL (if user hasn’t responded yet) |
| feedback_notes | TEXT | Optional user feedback: "Too long", "Tasted bland" |

**Notes:**
- Use UUID for `id` to safely reference meals instead of using `meal_name`.
- Keeps JSON for ingredients and instructions to avoid creating another table.

---

### ✅ Relationships
- `users.email` → Primary key, referenced by:
  - `preferences.email`
  - `meal_history.email`

**Example Query:**
```sql
SELECT *
FROM meal_history mh
JOIN preferences p ON mh.email = p.email
WHERE p.dietary_restrictions @> ARRAY['gluten-free'];
```

---

### ⚡ Key Points for Implementation
- **Insert / Upsert Preferences:** On user creation, generate a default preferences row or upsert whenever they update.
