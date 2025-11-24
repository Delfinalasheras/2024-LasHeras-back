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
    print("Remaining nutrients for user:", remaining)

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

    if not totals:
        return get_default_recommendations(user_id,goals, meal_type)

    totals = totals[0]

    return get_dynamic_recommendations(user_id,goals, totals, meal_type)







# def build_daily_menu(user_id: str):
#     goals = get_user_goals(user_id)
#     if not goals:
#         return {}

#     total_daily_goal = goals["calories"]
#     min_required = total_daily_goal * 0.90

#     foods_p = foods()
#     public_plates = get_public_plates()
#     user_plates = get_user_plates(user_id)

#     foods_only = foods_p["food"]
#     foods_by_id = {f["id"]: f for f in foods_only}

#     plates_only = public_plates + user_plates["Plates"]
#     plates_only = [enrich_plate_ingredients(p, foods_by_id) for p in plates_only]

#     default_cate = get_user_categories("default")["categories"]
#     grouped = group_foods_by_default_categories(foods_only, default_cate)

#     meat_foods = grouped.get("Meat", [])
#     veg_foods = grouped.get("Vegetables", [])

#     used_ids = set()

#     # --- Result ---
#     menu = {}
#     total = 0

#     for meal_type, pct in MEAL_CAL_SPLIT.items():
#         limit = total_daily_goal * pct
#         current_meal_cal = 0 # Contador para las calorías de la comida actual

#         foods_for_meal = filter_meal(foods_only, meal_type)
#         plates_for_meal = filter_meal(plates_only, meal_type)

#         foods_for_meal = [f for f in foods_for_meal if get_item_id(f) not in used_ids]
#         plates_for_meal = [p for p in plates_for_meal if get_item_id(p) not in used_ids]

#         menu[meal_type] = []
#         if plates_for_meal:
#             plates_sorted = sorted(plates_for_meal, key=lambda x: x["calories_portion"])
#             choice = None
#             valid_plates = [p for p in plates_sorted if p["calories_portion"] <= limit]
            
#             if valid_plates:
#                 choice = valid_plates[-1]
#             elif plates_sorted:
#                 choice = plates_sorted[0] 
            
#             if choice:
#                 menu[meal_type].append({"item": choice, "amount_eaten": 1})
#                 used_ids.add(get_item_id(choice))
#                 total += choice["calories_portion"]
#                 current_meal_cal += choice["calories_portion"]
#                 continue
        
#         candidates = foods_for_meal
        
#         if meal_type in (2, 4):
#             foods_ids_for_meal = {f["id_food"] for f in foods_for_meal}
#             meat_list = [f for f in meat_foods if f["id_food"] in foods_ids_for_meal]
#             veg_list = [f for f in veg_foods if f["id_food"] in foods_ids_for_meal]

#             if meat_list and veg_list:
#                 meat_list.sort(key=lambda x: x["calories_portion"], reverse=True)
#                 veg_list.sort(key=lambda x: x["calories_portion"], reverse=True)

#                 best_meat = meat_list[0]
#                 best_veg = veg_list[0]
#                 combined_cal = best_meat["calories_portion"] + best_veg["calories_portion"]

#                 if current_meal_cal + combined_cal <= limit * 1.05: 
#                     menu[meal_type] = [
#                         {"item": best_meat, "amount_eaten": 1},
#                         {"item": best_veg, "amount_eaten": 1}
#                     ]
#                     used_ids.add(get_item_id(best_meat))
#                     used_ids.add(get_item_id(best_veg))
#                     total += combined_cal
#                     current_meal_cal += combined_cal
                    
                    
#                     candidates = [f for f in candidates if get_item_id(f) not in used_ids]
#         candidates_sorted = sorted(candidates, key=lambda x: x["calories_portion"], reverse=True) 
#         for candidate in candidates_sorted:
#             cal_portion = candidate["calories_portion"]
#             if current_meal_cal + cal_portion <= limit * 1.10: 
#                 menu[meal_type].append({"item": candidate, "amount_eaten": 1})
#                 used_ids.add(get_item_id(candidate))
#                 total += cal_portion
#                 current_meal_cal += cal_portion
#         if current_meal_cal < limit * 0.90:
#             scale_factor = limit / current_meal_cal if current_meal_cal > 0 else 0
#             new_meal_cal = 0
#             for item_dict in menu[meal_type]:
#                 item = item_dict["item"]
#                 current_amount = item_dict["amount_eaten"]
#                 cal_per_portion = item["calories_portion"]
                
#                 scaled_amount = round(scale_factor * current_amount)
#                 new_amount = max(1, min(scaled_amount, 3))
#                 total -= item_dict["amount_eaten"] * cal_per_portion
#                 item_dict["amount_eaten"] = new_amount
#                 total += new_amount * cal_per_portion
#                 new_meal_cal += new_amount * cal_per_portion

#     menu["total_estimado"] = total
#     menu["objetivo"] = total_daily_goal
#     menu["cumple_90_por_ciento"] = total >= min_required

#     return menu


