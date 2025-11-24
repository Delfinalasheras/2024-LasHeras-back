from app.service.food_service import foods
from app.service.user_service import get_user_goals
from app.service.userTotCal_service import get_total
from app.service.plate_service import get_public_plates, get_user_plates
from app.controllers.recomendations_controller import filter_food_by_mealType
from app.service.category_service import get_user_categories
import random
from ..config import db # Asumo que importas tu instancia 'db' de algun lado

MEAL_CAL_SPLIT = {
    1: 0.30,
    2: 0.50, 
    3: 0.20, 
    4: 0.45   
}
def load_menu_from_db(user_id: str, date: str):
    """Carga el menú diario guardado en la base de datos."""
    try:
        user_wp_query = db.collection('DailyMenu').where('id_User', '==', user_id)
        matches = user_wp_query.stream()

        for wp in matches:
            wp_dict = wp.to_dict()
            if wp_dict.get('dia') == date:
                return wp_dict

        return None

    except Exception as e:
        return {"error": str(e)}
    return None
def save_menu_to_db(user_id: str, date: str):
    try:
        menu_data= build_daily_menu(user_id)
        print("Generated menu data:", menu_data)
        new_doc = db.collection('DailyMenu').document()
        menu_data['id_User'] = user_id
        menu_data['dia'] = date
        new_doc.set(menu_data)
        return menu_data

    except Exception as e:
        return {"error": str(e)}



#DATOS INICIALES
def load_user_daily_data(user_id):
    goals = get_user_goals(user_id)
    if not goals:
        return None, None

    total_daily_goal = goals["calories"]
    min_required = total_daily_goal * 0.90

    foods_p = foods()
    public_plates = get_public_plates()
    user_plates = get_user_plates(user_id)

    foods_only = [
        {**f, "calories_portion": float(f.get("calories_portion", 0))}
        for f in foods_p["food"]
    ]

    foods_by_id = {f["id"]: f for f in foods_only}

    plates_only = public_plates + user_plates["Plates"]
    plates_only = [
        {**p, "calories_portion": float(p.get("calories_portion", 0))}
        for p in plates_only
    ]
    plates_only = [enrich_plate_ingredients(p, foods_by_id) for p in plates_only]

    return (
        total_daily_goal,
        min_required,
        foods_only,
        plates_only,
        foods_by_id
    )



# CATEGORIAS
def load_default_categories(foods_only):
    default_cate = get_user_categories("default")["categories"]
    grouped = group_foods_by_default_categories(foods_only, default_cate)
    meat_foods = grouped.get("Meat", [])
    veg_foods = grouped.get("Vegetables", [])
    return meat_foods, veg_foods
# SELECCIÓN DE PLATOs
def pick_best_plate(plates_for_meal, limit):
    if not plates_for_meal:
        return None
    
    plates_sorted = sorted(plates_for_meal, key=lambda x: x["calories_portion"])
    valid = [p for p in plates_sorted if p["calories_portion"] <= limit]

    if valid:
        return valid[-1]    # El mayor dentro del límite
    return plates_sorted[0] # El de menor caloría
# SELECCIÓN CARNE + VEGETAL (ALMUERZO/CENA)
def pick_meat_veg_combo(meat_foods, veg_foods, foods_for_meal, current_meal_cal, limit):
    foods_ids_for_meal = {f["id_food"] for f in foods_for_meal}

    meat_list = [f for f in meat_foods if f["id_food"] in foods_ids_for_meal]
    veg_list = [f for f in veg_foods if f["id_food"] in foods_ids_for_meal]

    if not meat_list or not veg_list:
        return None

    meat_list.sort(key=lambda x: x["calories_portion"], reverse=True)
    veg_list.sort(key=lambda x: x["calories_portion"], reverse=True)

    best_meat = random.choice(meat_list[:min(3, len(meat_list))])
    best_veg = random.choice(veg_list[:min(3, len(veg_list))])

    combined_cal = best_meat["calories_portion"] + best_veg["calories_portion"]

    if current_meal_cal + combined_cal <= limit * 1.05:
        return best_meat, best_veg, combined_cal

    return None
# LLENAR COMIDA CON ALIMENTOS
def fill_meal_with_foods(menu_list, candidates, limit, current_meal_cal, used_ids, total):
    candidates_sorted = sorted(candidates, key=lambda x: x["calories_portion"], reverse=True)

    for c in candidates_sorted:
        cal = c["calories_portion"]
        if current_meal_cal + cal <= limit * 1.10:
            menu_list.append({"item": c, "amount_eaten": 1})
            used_ids.add(get_item_id(c))
            current_meal_cal += cal
            total += cal

    return current_meal_cal, total
def scale_meal(menu_list, limit, current_meal_cal, total):
    if current_meal_cal >= limit * 0.90:
        return current_meal_cal, total

    scale_factor = limit / current_meal_cal if current_meal_cal > 0 else 0
    new_total = total
    new_meal_cal = 0

    for item_dict in menu_list:
        item = item_dict["item"]
        cal_per_portion = item["calories_portion"]
        current_amount = item_dict["amount_eaten"]

        scaled_amount = round(scale_factor * current_amount)
        new_amount = max(1, min(scaled_amount, 3))

        new_total -= current_amount * cal_per_portion
        new_total += new_amount * cal_per_portion
        new_meal_cal += new_amount * cal_per_portion

        item_dict["amount_eaten"] = new_amount

    return new_meal_cal, new_total

def build_daily_menu(user_id: str):
    data = load_user_daily_data(user_id)
    if data[0] is None:
        return {}

    total_daily_goal, min_required, foods_only, plates_only, foods_by_id = data
    meat_foods, veg_foods = load_default_categories(foods_only)

    used_ids = set()
    menu = {}
    total = 0

    for meal_type, pct in MEAL_CAL_SPLIT.items():
        limit = total_daily_goal * pct
        current_meal_cal = 0
        meal_key = str(meal_type)

        foods_for_meal = [f for f in filter_meal(foods_only, meal_type) if get_item_id(f) not in used_ids]
        plates_for_meal = [p for p in filter_meal(plates_only, meal_type) if get_item_id(p) not in used_ids]

        menu[meal_key] = []

        # --- 1) Platos primero
        choice = pick_best_plate(plates_for_meal, limit)
        if choice:
            menu[meal_key].append({"item": choice, "amount_eaten": 1})
            used_ids.add(get_item_id(choice))
            current_meal_cal += choice["calories_portion"]
            total += choice["calories_portion"]
            continue

        # --- 2) Carne + vegetal
        if meal_type in (2, 4):
            combo = pick_meat_veg_combo(meat_foods, veg_foods, foods_for_meal, current_meal_cal, limit)
            if combo:
                m, v, combined = combo
                menu[meal_key] = [
                    {"item": m, "amount_eaten": 1},
                    {"item": v, "amount_eaten": 1},
                ]
                used_ids.add(get_item_id(m))
                used_ids.add(get_item_id(v))
                current_meal_cal += combined
                total += combined

                # quitar usados
                foods_for_meal = [f for f in foods_for_meal if get_item_id(f) not in used_ids]

        # --- 3) Agregar alimentos hasta llegar al rango
        current_meal_cal, total = fill_meal_with_foods(
            menu[meal_key], foods_for_meal, limit, current_meal_cal, used_ids, total
        )

        # --- 4) Ajustar cantidades si quedó muy bajo
        current_meal_cal, total = scale_meal(menu[meal_key], limit, current_meal_cal, total)

    # Datos finales
    menu["total_estimado"] = total
    menu["objetivo"] = total_daily_goal
    menu["cumple_90_por_ciento"] = total >= min_required

    return menu


def get_item_id(item):
    return item.get("id_food") or item.get("id") or item.get("plateID")
def group_foods_by_default_categories(all_foods, default_categories):
    cat_map = {c["name"]: [] for c in default_categories}

    for c in default_categories:
        cat_name = c["name"]
        food_ids = c["foods"] 

        for f in all_foods:
            if f.get("id_food") in food_ids:
                cat_map[cat_name].append(f)

    return cat_map
def filter_meal(items, meal_type):
    return filter_food_by_mealType({"food": items}, meal_type)

def enrich_plate_ingredients(plate, foods_by_id):
    """Agrega los datos del Food real dentro de cada ingrediente del Plate."""
    enriched_ingredients = []

    for ing in plate.get("ingredients", []):
        food = foods_by_id.get(ing["ingredientId"])

        if food:
            enriched = {
                **ing,         
                **food        
            }
        else:
            enriched = ing 

        enriched_ingredients.append(enriched)

    plate["ingredients"] = enriched_ingredients
    return plate