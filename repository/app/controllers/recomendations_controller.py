from datetime import datetime
from app.models.goals import Goals as UserGoals
from app.models.userTotCal import UserTotCal as UserDailyTotals
from app.service.category_service import get_user_categories
from app.service.food_service import foods
from app.service.user_service import get_user_goals
from app.service.userTotCal_service import get_total
from app.service.plate_service import get_public_plates, get_user_plates


def calculate_remaining(goals: UserGoals, totals: UserDailyTotals):
    """Devuelve cuánto le queda al usuario consumir en el día."""
    return {
        "calories": max(goals["calories"] - totals["totCal"], 0),
        "carbs": max(goals["carbohydrates"] - totals["totCarbs"], 0),
        "fat": max(goals["fats"] - totals["totFats"], 0),
        "sodium": max(goals["sodium"] - totals["totSodium"], 0),
    }


def filter_food_by_mealType(all_foods, meal_type):
    foods = all_foods["food"]
    fixed_foods = []
    for f in foods:
        # Si existe ' timeDay' la renombramos a 'timeDay'
        if " timeDay" in f:
            f["timeDay"] = f.pop(" timeDay")
        fixed_foods.append(f)

    return [f for f in fixed_foods if meal_type in f.get("timeDay", [])]


def get_default_recommendations(user_id:str,goals: UserGoals, meal_type: int):
    """Recomendaciones básicas para cuando NO comió nada en el día."""

    calories_limit = {
        1: goals["calories"] * 0.25,  # desayuno
        2: goals["calories"] * 0.40,  # almuerzo
        3: goals["calories"] * 0.10,  # snack
        4: goals["calories"] * 0.35   # cena
    }.get(meal_type, goals["calories"] * 0.25)

    foods_p = foods()
    public_plates = get_public_plates()
    user_plates = get_user_plates(user_id)
    # Combine all foods from foods, public plates, and user plates
    all_foods = {
        "food": foods_p["food"] + public_plates + user_plates["Plates"]
    }
    meal_foods = filter_food_by_mealType(all_foods, meal_type)

    candidates = [
        f for f in meal_foods
        if f["calories_portion"] <= calories_limit
    ]

    candidates.sort(key=lambda f: f["calories_portion"])

    return candidates[:5]


def get_dynamic_recommendations(user_id:str,goals: UserGoals, totals: UserDailyTotals, meal_type: int):
    """Recomendaciones basadas en lo que le queda por consumir."""
    remaining = calculate_remaining(goals, totals)

    foods_p = foods()
    public_plates = get_public_plates()
    user_plates = get_user_plates(user_id)
    # Combine all foods from foods, public plates, and user plates
    all_foods = {
        "food": foods_p["food"] + public_plates + user_plates["Plates"]
    }
    meal_foods = filter_food_by_mealType(all_foods, meal_type)

    valid = []

    for f in meal_foods:
        if (
            f["calories_portion"] <= remaining["calories"] and
            f["carbohydrates_portion"] <= remaining["carbs"] and
            f["fats_portion"] <= remaining["fat"] and
            f["sodium_portion"] <= remaining["sodium"]
        ):
            valid.append(f)

    valid.sort(key=lambda f: remaining["calories"] - f["calories_portion"])

    return valid[:5]

def get_recommendations(user_id: str, meal_type: int):
    goals = get_user_goals(user_id)



    if not goals:
        return []

    today = datetime.now()
    totals = get_total(user_id, today)

    # No comió nada → default recommendations
    if not totals:
        return get_default_recommendations(user_id,goals, meal_type)

    totals = totals[0]

    return get_dynamic_recommendations(user_id,goals, totals, meal_type)

