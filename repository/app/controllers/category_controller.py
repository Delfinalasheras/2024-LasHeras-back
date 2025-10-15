from app.service.category_service import create_category, get_user_categories, update_category, delete_category_service
from app.models.category import Category
from app.controllers.food_controller import get_foods
from app.service.plate_service import get_plates
from app.service.drink_service import drinks
from fastapi import HTTPException
import re

icons = ['Apple', 'Carrot', 'Fish', 'Pizza', 'Ice Cream', 'Bread', 'Egg', 'Cheese', 'Drumstick', 'Hotdog',
         'Hamburger', 'Pepper', 'Cookie', 'Bacon', 'Leaf', 'Seedling', 'Lemon', 'Wine Bottle', 'Mug', "Seedling"]


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


def validate_category_data(user_id: str, category: Category):
    if user_id != category.id_User:
        raise HTTPException(
            status_code=400, detail="id_User is not valid "
        )
    validate_name(category.name, 'Name')
    if category.icon not in icons:
        raise HTTPException(
            status_code=400, detail="Icon not valid "
        )
    foods = get_foods()
    existing_food_ids = [food["id"]
                         for food in foods["message"]['food']]
    for food in category.foods:
        if food not in existing_food_ids:
            raise HTTPException(
                status_code=400, detail=f"Invalid food ID: {food}")

    user_drinks = drinks(user_id)
    existing_drinks_ids = [drink["id"] for drink in user_drinks['Drinks']]
    for drink in category.drinks:
        if drink not in existing_drinks_ids:
            raise HTTPException(
                status_code=400, detail=f"Invalid drink ID: {drink}")

    plates = get_plates()
    existing_plate_ids = [plate["id"] for plate in plates]
    for plate in category.plates:
        if plate not in existing_plate_ids:
            raise HTTPException(
                status_code=400, detail=f"Invalid plate ID: {plate}")

    if not category.foods and not category.plates and not category.drinks:
        raise HTTPException(
            status_code=400,
            detail="At least one of 'foods', 'plates', or 'drinks' must contain data"
        )


def userCategoryLog(user_id: str, category: Category):
    validate_category_data(user_id, category)
    response = create_category(category)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])


def get_category(user_id: str):
    response = get_user_categories(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def update_category_controller(user_id: str, category_id: str, updated_category_data: Category):
    categories = get_category(user_id)[
        'message']['categories'] + get_category("default")['message']['categories']
    print(categories)
    existing_categories_ids = [category["id"] for category in categories]
    if category_id not in [existing_categories_ids]:
        raise HTTPException(
            status_code=400, detail=f"Invalid category ID: {category_id}")
    if updated_category_data.id_User != user_id:
        raise HTTPException(
            status_code=400, detail="The user id must not be changed")
    validate_category_data(user_id, updated_category_data)
    response = update_category(category_id, updated_category_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def delete_category(id_user: str, category_id: str):
    categories = get_category(id_user)
    if not category_id:
        raise HTTPException(
            status_code=400, detail="The category id is empty")
    if not categories:
        raise HTTPException(
            status_code=400, detail="The current user has no categories")
    print(categories['message']['categories'])
    existing_categories_ids = [category["id"]
                               for category in categories['message']['categories']]
    if category_id not in existing_categories_ids:
        raise HTTPException(
            status_code=400, detail=f"Invalid category ID: {category_id}")
    response = delete_category_service(category_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
