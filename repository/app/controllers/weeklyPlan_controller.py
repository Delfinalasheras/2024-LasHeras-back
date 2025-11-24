from app.models.weeklyPlan import WeeklyPlanRequest, DayPlan, MealItem
# Importamos los servicios que acabamos de crear
from app.service.weeklyPlan_service import get_plan_by_week_service, save_or_update_plan_service
from app.service.plate_service import getPlateByID
from app.service.food_service import food_by_id
from fastapi import HTTPException
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import re

def validate_string_id(campo: str, label: str):
    if not isinstance(campo, str):
        raise HTTPException(
            status_code=400, detail=f"{label} debe ser una cadena de texto."
        )
    if not campo.strip():
        raise HTTPException(
            status_code=400, detail=f"{label} no puede estar vacío o en blanco."
        )

def validate_positive_float(campo: float, label: str):
    if not isinstance(campo, (float, int)):
        raise HTTPException(
            status_code=400, detail=f"{label} debe ser un número."
        )
    if campo <= 0:
        raise HTTPException(
            status_code=400, detail=f"{label} debe ser mayor que cero."
        )
def validate_meal_item(item: MealItem, meal_type: str, day_name: str):
    validate_string_id(item.plate_id, f"ID de Plato ({day_name} - {meal_type})")
    validate_string_id(item.name, f"Nombre de Plato ({day_name} - {meal_type})")
    if item.amount_eaten is not None:
        if not isinstance(item.amount_eaten, (float, int)):
            raise HTTPException(
                status_code=400, detail=f"Cantidad consumida debe ser un número en {day_name} - {meal_type}."
            )
        if item.amount_eaten < 0:
            raise HTTPException(
                status_code=400, detail=f"Cantidad consumida debe ser mayor o igual a cero en {day_name} - {meal_type}."
            )


def validate_day_plan(day_data: DayPlan, day_name: str, expected_date: str):
    
    if day_data.date != expected_date:
        raise HTTPException(
            status_code=400, 
            detail=f"Error en fecha para '{day_name}'. Se esperaba {expected_date} pero se recibió {day_data.date}."
        )
    meals = {
        'breakfast': day_data.breakfast,
        'lunch': day_data.lunch,
        'snack': day_data.snack,
        'dinner': day_data.dinner
    }
    
    for meal_type, items in meals.items():
        if not isinstance(items, list):
             raise HTTPException(
                status_code=400, detail=f"'{meal_type}' de {day_name} debe ser una lista."
            )
        for item in items:
            validate_meal_item(item, meal_type, day_name)
def get_weekly_plan_controller(user_id: str, week_start: str):
    response = get_plan_by_week_service(user_id, week_start)
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response["plan"]

def update_weekly_plan_controller(user_id: str, plan_data: WeeklyPlanRequest):
    print("Updating plan with data:", plan_data)
    REQUIRED_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    validate_string_id(user_id, "ID de Usuario")
    try:
        start_date = datetime.strptime(plan_data.week_start, '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(
            status_code=400, detail="El formato de 'week_start' es inválido. Use YYYY-MM-DD."
        )

    if start_date.weekday() != 0: 
        raise HTTPException(
            status_code=400, detail="'week_start' debe ser un Lunes."
        )

    if not isinstance(plan_data.days, dict):
        raise HTTPException(status_code=400, detail="'days' debe ser un objeto/diccionario.")
        
    if set(plan_data.days.keys()) != set(REQUIRED_DAYS):
        raise HTTPException(
            status_code=400, detail="El plan debe contener exactamente los 7 días (monday a sunday)."
        )

    for i, day_name in enumerate(REQUIRED_DAYS):
        day_data = plan_data.days[day_name]
        expected_date = (start_date + timedelta(days=i)).isoformat()
        
        validate_day_plan(day_data, day_name, expected_date)
    data = plan_data.dict()
    data["id_User"] = user_id

    response = save_or_update_plan_service(data)

    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    return response
def get_shoppingList(user_id: str, week_start: str):
    response = get_plan_by_week_service(user_id, week_start)
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    group_plates = group_plates_from_weekly_plan(response["plan"])
    plan=generate_shopping_list(group_plates)
    shopping_list = {}


    return plan
def group_plates_from_weekly_plan(weekly_plan):
    """
    Devuelve: { plate_id: total_amount_eaten }
    """
    grouped = {}
    for day_name, day_data in weekly_plan["days"].items():
        for meal in ["breakfast", "lunch", "snack", "dinner"]:
            items = day_data.get(meal, [])

            for item in items:
                plate_id = item["plate_id"]
                eaten = item["amount_eaten"]

                if plate_id not in grouped:
                    grouped[plate_id] = eaten
                else:
                    grouped[plate_id] += eaten

    return grouped

def generate_shopping_list(grouped_plates):
    shopping = {}

    for plate_id, total_eaten in grouped_plates.items():

        plate = getPlateByID(plate_id)['plate']
        # --- Caso PLATE ---
        if plate and "ingredients" in plate:
            for pf in plate["ingredients"]:
                print(pf)
                food = food_by_id(pf["ingredientId"])["food"]
                if not food:
                    continue

                food_id = pf["ingredientId"]
                name = food["name"]
                measure = food.get("measure")
                base_amount = pf["quantity"]  # cantidad por porción de plate

                total_amount = base_amount * total_eaten

                if food_id not in shopping:
                    shopping[food_id] = {
                        "name": name,
                        "measure": measure,
                        "total_amount": total_amount
                    }
                else:
                    shopping[food_id]["total_amount"] += total_amount

        # --- Caso FOOD DIRECTO ---
        else:
            food = food_by_id(plate_id)["food"]
            if not food:
                continue

            food_id = plate_id
            name = food["name"]
            measure = food.get("measure")
            base_amount = 1

            total_amount = base_amount * total_eaten

            if food_id not in shopping:
                shopping[food_id] = {
                    "name": name,
                    "measure": measure,
                    "total_amount": total_amount
                }
            else:
                shopping[food_id]["total_amount"] += total_amount

    return shopping

