# Nutrition-Focused Database Schema (PostgreSQL)

This schema represents the "Truth Layer" of the application, where all numeric calculations and authoritative food data are stored.

---

### 🔹 1. Foods Table
Basic food metadata.
```sql
CREATE TABLE foods (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    is_vegetarian BOOLEAN DEFAULT FALSE,
    is_vegan BOOLEAN DEFAULT FALSE
);
```

### 🔹 2. Nutrients Table
Standardized list of nutrients.
```sql
CREATE TABLE nutrients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL, -- e.g., "protein", "calcium", "iron"
    unit TEXT NOT NULL  -- e.g., "g", "mg", "kcal"
);
```

### 🔹 3. Food Nutrients Table (CRITICAL)
Mapping nutrients to foods (values per 100g).
```sql
CREATE TABLE food_nutrients (
    food_id INT REFERENCES foods(id),
    nutrient_id INT REFERENCES nutrients(id),
    value_per_100g FLOAT NOT NULL,
    PRIMARY KEY (food_id, nutrient_id)
);
```

### 🔹 4. User Profiles
Static user data for requirement calculation.
```sql
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_email TEXT REFERENCES users(email),
    age INT,
    gender TEXT,
    weight_kg FLOAT,
    height_cm FLOAT,
    activity_level TEXT -- e.g., "sedentary", "active"
);
```

### 🔹 5. Nutrient Requirements
Calculated goals for the user based on health standards (e.g., WHO/USDA).
```sql
CREATE TABLE nutrient_requirements (
    user_profile_id INT REFERENCES user_profiles(id),
    nutrient_id INT REFERENCES nutrients(id),
    required_value FLOAT NOT NULL,
    PRIMARY KEY (user_profile_id, nutrient_id)
);
```

### 🔹 6. Meals & Meal Items
Logging user consumption.
```sql
CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    user_email TEXT REFERENCES users(email),
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE meal_items (
    id SERIAL PRIMARY KEY,
    meal_id INT REFERENCES meals(id),
    food_id INT REFERENCES foods(id),
    quantity_g FLOAT NOT NULL
);
```
