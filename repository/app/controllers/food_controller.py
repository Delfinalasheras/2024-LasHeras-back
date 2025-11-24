from app.service.food_service import create_food, foods, food_by_id
from app.models.food import Food
import re
from fastapi import HTTPException


def validate_name(campo, label):
    if not campo.strip():
        raise HTTPException(
            status_code=400, detail=f"{label} cannot be empty or blank")
    if type(campo) is not str:
        raise HTTPException(
            status_code=400, detail=f"{label} must be a string")
    if not re.match(r'^[a-zA-Z\s]+$', campo):
        raise HTTPException(
            status_code=400, detail=f"Invalid format for {label}. Only letters and spaces allowed.")

def validate_timeDay(timeDay):
    if not isinstance(timeDay, list):
        raise HTTPException(
            status_code=400, 
            detail="timeDay must be a list"
        )

    if len(timeDay) == 0:
        raise HTTPException(
            status_code=400, 
            detail="timeDay cannot be empty"
        )

    if any((type(x) is not int) for x in timeDay):
        raise HTTPException(
            status_code=400, 
            detail="All values in timeDay must be integers"
        )

    if any(x < 1 or x > 4 for x in timeDay):
        raise HTTPException(
            status_code=400, 
            detail="timeDay values must be between 1 and 4"
        )
    if len(timeDay) != len(set(timeDay)):
        raise HTTPException(
            status_code=400, 
            detail="timeDay contains duplicated values"
        )

def validate_limit(campo, minimo, label):
    if type(campo) is not float:
        raise HTTPException(
            status_code=400, detail=f"{label} must be a float")
    if not (minimo <= campo):
        raise HTTPException(
            status_code=400, detail=f"{label} must be grater or equal than {minimo} ")


def validate_food(food: Food):
    validate_name(food.name, 'Name')
    validate_name(food.measure, 'Measure')
    validate_limit(food.calories_portion, 0, 'calories_portion')
    validate_limit(food.carbohydrates_portion, 0, 'carbohydrates_portion')
    validate_limit(food.sodium_portion, 0, 'sodium_portion')
    validate_limit(food.fats_portion, 0, 'fats_portion')
    validate_limit(food.protein_portion, 0, 'protein_portion')
    validate_timeDay(food.timeDay)   # <-- NUEVO



def register_new_food(food: Food):
    validate_food(food)
    response = create_food(food.dict())
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "food registered successfully", "food_id": response["id"]}


def get_foods():
    response = foods()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def validate_existance(items, itemSearch, id, label):
    existing_ids = [item[itemSearch]
                    for item in items]
    if id not in existing_ids:
        raise HTTPException(
            status_code=400, detail=f"Invalid {label} ID: {id}")


def get_food_by_id(food_id: str):

    response = food_by_id(food_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
def recomendations_user(user_id: str):
    pass