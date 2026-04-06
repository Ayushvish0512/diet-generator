# Diet Generator Schema Updates TODO

## Remaining Steps:
1. [x] Update app/utils/prompt_builder.py - Add build_prompt with failed_meals & feedback
2. [x] Update app/services/ai_service.py - Add sync generate_meal_from_ai(prompt)
3. [x] Update app/services/meal_service.py - Implement task's generate_meal(user_id)
4. [x] Update app/routes/preferences.py - Use preferences table
5. [x] Update app/services/adherence_service.py - Implement log_adherence(meal_name, followed, feedback)
6. [x] Update app/routes/adherence.py - Adjust to new service params
7. [x] Update app/routes/meals.py - Use new sync generate_meal
8. [ ] Verify models & test endpoints manually

Progress tracked here.
