from app.service.foodUser_service import get_meal_by_id, update_food_user, create_food_user_service, get_user_meals, delete_food_user_service
from app.models.userFood import UserFood
from fastapi import HTTPException
from datetime import datetime
from app.controllers.food_controller import get_food_by_id, get_foods
from app.service.drink_service import drinks
from app.service.plate_service import get_plates


def validate_date(date, label):
    if date.date() > datetime.now().date():
        raise HTTPException(
            status_code=400, detail=f"{label} must be a date in the past.")


def validate_limit(campo, minimo, label):
    if type(campo) is not float:
        raise HTTPException(
            status_code=400, detail=f"{label} must be a float")
    if not (minimo < campo):
        raise HTTPException(
            status_code=400, detail=f"{label} must be grater than {minimo} ")


def validate_foodLog(userFood: UserFood):
    validate_date(userFood.date_ingested, 'Ingested date')
    validate_limit(userFood.amount_eaten, 0, 'amount eaten')


def userFoodLog(userFood: UserFood):
    foods = get_foods()
    existing_food_ids = [food["id"]
                         for food in foods["message"]['food']]

    user_drinks = drinks(userFood.id_User)
    existing_drinks_ids = [drink["id"] for drink in user_drinks['Drinks']]

    plates = get_plates()
    existing_plate_ids = [plate["id"] for plate in plates]

    existing_ids = existing_food_ids+existing_drinks_ids+existing_plate_ids
    if userFood.id_Food not in existing_ids:
        raise HTTPException(
            status_code=400, detail=f" Invalid Food_ID  ")
    validate_foodLog(userFood)
    response = create_food_user_service(userFood)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "User registered successfully"}


def get_meals_user(user_id: str):
    response = get_user_meals(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def delete_meal(user_id: str, userFood_id: str):
    meals = get_meals_user(user_id)
    meal_ids = [meal["id"] for meal in meals['message']['foods']]
    if userFood_id not in meal_ids:
        raise HTTPException(
            status_code=404, detail="The provided userFood_id does not exist in user's meals"
        )
    response = delete_food_user_service(userFood_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response


def update_userFood_controller(user_id: str, userFood_id: str, userFood_data: UserFood):
    meals = get_meals_user(user_id)
    meal_ids = [meal["id"] for meal in meals['message']['foods']]
    if userFood_id not in meal_ids:
        raise HTTPException(
            status_code=404, detail="The provided userFood_id does not exist in user's meals"
        )
    if user_id != userFood_data.id_User:
        raise HTTPException(
            status_code=404, detail="You can not change the id_User "
        )
    meal = get_meal_by_id(userFood_id)
    if not meal:
        raise HTTPException(
            status_code=404, detail="The id_meal does not exist"
        )
    if user_id != userFood_data.id_User or userFood_data.id_User != meal['id_User'] or user_id != meal['id_User']:
        raise HTTPException(
            status_code=404, detail="You can not change the id_User "
        )
    if meal['id_Food'] != userFood_data.id_Food:
        raise HTTPException(
            status_code=404, detail="You can not change the id_Food "
        )
    validate_limit(userFood_data.amount_eaten, 0, 'Amount eaten')
    validate_date(userFood_data.date_ingested, 'Date ingested')
    response = update_food_user(userFood_id, userFood_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}