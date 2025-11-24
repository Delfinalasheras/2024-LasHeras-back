from datetime import datetime
from app.models.goals import Goals as UserGoals
from app.models.userTotCal import UserTotCal as UserDailyTotals
from app.service.category_service import get_user_categories
from app.service.food_service import foods
from app.service.user_service import get_user_goals
from app.service.userTotCal_service import get_total
from app.service.plate_service import get_public_plates, get_user_plates



def calculate_remaining(goals: UserGoals, totals: UserDailyTotals) :
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


def get_default_recommendations(goals: UserGoals, meal_foods):
    calories_limit = {
        1: goals["calories"] * 0.25,
        2: goals["calories"] * 0.40,
        3: goals["calories"] * 0.10,
        4: goals["calories"] * 0.35
    }

    limit = calories_limit.get(meal_foods["meal_type"], goals["calories"] * 0.25)

    candidates = [
        f for f in meal_foods["foods"]
        if f.get("calories_portion", 0) <= limit
    ]

    candidates.sort(key=lambda f: f["calories_portion"])
    return candidates[:5]



def get_dynamic_recommendations(goals, totals, meal_foods):
    remaining = calculate_remaining(goals, totals)
    tolerance = 1.10
    valid = []

    for f in meal_foods["foods"]:

        f_cal = f.get("calories_portion", 0)
        f_carb = f.get("carbohydrates_portion", 0)
        f_fat = f.get("fats_portion", 0)
        f_sod = f.get("sodium_portion", 0)

        max_cal_allowed = remaining["calories"] if remaining["calories"] > 0 else 200

        if f_cal > max_cal_allowed * tolerance:
            continue
        
        fits = (
            (remaining["carbs"] < 0 or f_carb <= remaining["carbs"] * tolerance) and
            (remaining["fat"] < 0 or f_fat <= remaining["fat"] * tolerance) and
            (remaining["sodium"] < 0 or f_sod <= remaining["sodium"] * tolerance)
        )

        if fits:
            valid.append(f)

    valid.sort(key=lambda f: abs(remaining["calories"] - f.get("calories_portion", 0)))

    if not valid:
        meal_foods["foods"].sort(key=lambda f: f.get("calories_portion", 0))
        return meal_foods["foods"][:5]

    return valid[:5]

def get_recommendations(user_id: str):
    goals = get_user_goals(user_id)
    if not goals:
        return {}

    foods_p = foods()
    public_plates = get_public_plates()
    user_plates = get_user_plates(user_id)

    all_foods = {
        "food": foods_p["food"] + public_plates + user_plates["Plates"]
    }
    grouped = group_foods_by_mealtype(all_foods)

    today = datetime.now()
    totals = get_total(user_id, today)
    totals = totals[0] if totals else None
    result = {}

    for meal_type in [1, 2, 3, 4]:
        meal_foods = {
            "meal_type": meal_type,
            "foods": grouped.get(meal_type, [])
        }

        if not totals:
            recs = get_default_recommendations(goals, meal_foods)
        else:
            recs = get_dynamic_recommendations(goals, totals, meal_foods)

        result[meal_type] = recs

    return result

def group_foods_by_mealtype(all_foods):
    grouped = {1: [], 2: [], 3: [], 4: []}

    for f in all_foods["food"]:
        for mt in f.get("timeDay", []):
            if mt in grouped:
                grouped[mt].append(f)

    return grouped