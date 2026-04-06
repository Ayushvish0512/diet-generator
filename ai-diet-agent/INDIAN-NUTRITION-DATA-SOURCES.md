# Indian Nutrition Data Sources & Scaping Targets

To build a production-grade nutrition app for the Indian context, you need high-quality, regional data. This document categorizes ~100 essential sources to populate your structured DB (Truth Layer) and unstructured Vector DB (RAG Layer).

---

## 🇮🇳 1. Government & Official Databases (Ground Truth)
These form the core of your authoritative data.
1.  **ICMR-NIN:** Indian Council of Medical Research - National Institute of Nutrition.
2.  **FSSAI:** Food Safety and Standards Authority of India.
3.  **MoHFW:** Ministry of Health and Family Welfare.
4.  **National Health Portal (NHP) India.**
5.  **Open Government Data (OGD) Platform India** (data.gov.in).
6.  **Ministry of Women and Child Development.**
7.  **POSHAN Abhiyaan:** Prime Minister’s Overarching Scheme for Holistic Nourishment.
8.  **NFHS:** National Family Health Survey.
9.  **Ministry of Ayush:** (Traditional Indian medicine & diet).
10. **National Horticulture Board.**

---

## 🥗 2. Food Composition & Nutrient Databases (CRITICAL)
Use these to populate `food_nutrients` and `nutrients` tables.
11. **IFCT:** Indian Food Composition Tables (The gold standard for Indian ingredients).
12. **NIN Data Portal:** Detailed biochemical analysis of regional foods.
13. **ICMR Nutrient Requirements Guidelines:** (RDA for Indians).
14. **FAO India Food Composition:** Food and Agriculture Organization's regional data.
15. **WHO South-East Asia Nutrition Database.**

---

## 🍛 3. Indian Recipe & Food Platforms (Diversity Mapping)
Useful for expanding the `foods` table and mapping regional dish names to ingredients.
16. **Tarla Dalal Recipes** (Massive database of Indian vegetarian food).
17. **Hebbars Kitchen** (South Indian focus).
18. **Archana's Kitchen** (Healthy & traditional recipes).
19. **Sanjeev Kapoor Khazana.**
20. **Tasty Indian Recipes.**
21. **Cookpad India.**
22. **BetterButter.**
23. **NDTV Food.**
24. **Times Food.**
25. **Zomato / Swiggy Blog:** (For food trends and regional naming).

---

## 🧬 4. Health & Nutrition Apps (User Patterns)
26. **HealthifyMe.**
27. **Fittr.**
28. **MyFitnessPal** (Global but has extensive Indian entries).
29. **Cure.fit / Cult.fit.**
30. **StepSetGo.**

---

## 🛒 5. Grocery & Food Catalog APIs (Taxonomy)
31. **BigBasket.**
32. **Blinkit.**
33. **Amazon India Fresh.**
34. **JioMart.**
35. **Open Food Facts (India):** (Crowdsourced barcode data).

---

## 📊 6. International (India-Compatible) Datasets
Use for fallback or normalization of common global foods.
36. **USDA FoodData Central.**
37. **Global Dietary Database.**
38. **Nutritionix API.**
39. **Edamam API.**
40. **Kaggle:** (Search for "Indian Food" datasets).

---

## 🧠 7. RAG Knowledge Sources (Unstructured Layer)
Perfect for your Vector DB to provide "Why" and "How" explanations.
41. **Harvard T.H. Chan School of Public Health.**
42. **Mayo Clinic / Cleveland Clinic.**
43. **Eat Right India** (FSSAI initiative).
44. **Poshan Tracker Reports.**
45. **Dietary Guidelines for Indians (PDFs from ICMR).**

---

## 🧩 8. Regional & Cultural Food Sources
46-60. **State Nutrition Portals:** (e.g., Kerala Health Services, Tamil Nadu Nutrition).
61-70. **NGO Reports:** (e.g., Akshaya Patra Foundation, CRY).
71-80. **Academic Studies:** Tribal diet studies from PubMed/ResearchGate specifically targeting Indian states.

---

## 🔧 9. Developer-Friendly Tooling
81. **Scrapy / BeautifulSoup:** For web scraping recipe sites.
82. **Selenium:** For dynamic content loading.
83. **PostgreSQL:** Primary relational store.
84. **FAISS:** Vector similarity search.
85. **Sentence-Transformers:** For generating embeddings of Indian food descriptions.
86. **FastAPI:** To serve the data to your agents.

---

## 📝 10. Scraping Strategy
- **Prioritize IFCT/NIN:** These are your "Hard Facts".
- **Map Regional Names:** Use recipe sites to create a synonym mapping (e.g., "Bhindi" -> "Ladyfinger" -> "Okra").
- **Normalize Units:** Ensure all scraped data is converted to a "per 100g" or "per standard serving" format.
- **Validation:** Cross-reference scraped recipe data against the IFCT nutrient database to ensure accuracy.
