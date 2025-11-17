from app.service.plate_service import get_plates, update_user_platestoverified, get_public_plates_notUser, create_plate, get_user_plates, delete_Plate_service, update_Plate, getPlateByID, get_public_plates
from app.models.plate import Plate
from fastapi import HTTPException
from datetime import datetime
from app.controllers.food_controller import get_foods
import re


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


def validate_limit(campo, minimo, label):
    if type(campo) is not float:
        raise HTTPException(
            status_code=400, detail=f"{label} must be a float")
    if not (minimo <= campo):
        raise HTTPException(
            status_code=400, detail=f"{label} must be grater than {minimo}")


def validate_verified(campo, minimo, label):
    if type(campo) is not int:
        raise HTTPException(
            status_code=400, detail=f"{label} must be an intenger")
    if not (minimo <= campo):
        raise HTTPException(
            status_code=400, detail=f"{label} must be grater than {minimo}")
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

def validate_plate_data(plate: Plate):
    validate_name(plate.name, "name")
    validate_limit(plate.calories_portion, 0, "calories_portion")
    validate_limit(plate.sodium_portion, 0, "sodium_portion")
    validate_limit(plate.carbohydrates_portion, 0, "carbohydrates_portion")
    validate_limit(plate.fats_portion, 0, "fats_portion")
    validate_limit(plate.protein_portion, 0, "protein_portion")
    validate_verified(plate.verified, 0, "verified")
    validate_timeDay(plate.timeDay)
    if not plate.ingredients:
        raise HTTPException(
            status_code=400, detail=f"The plate must to have at least one ingredient")

    foods = get_foods()
    existing_food_ids = [food["id"]
                         for food in foods["message"]['food']]

    for ing in plate.ingredients:
        validate_limit(ing.quantity, 0, f"quantity of {ing.ingredientId}")
        if ing.ingredientId not in existing_food_ids:
            raise HTTPException(
                status_code=400, detail=f"Invalid food ID: {ing.ingredientId} ")


def plateLog(user_id:str,plate: Plate):
    validate_plate_data(plate)
    plate_data = plate.dict()
    plate_data["id_User"] = user_id
    
    response = create_plate(plate_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"id": response}


def get_plate_user(user_id: str):
    response = get_user_plates(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def delete_plate(user_id: str, userPlate_id: str):
    user_plates = get_plate_user(user_id)
    existing_plates_ids = [plate["id"]
                           for plate in user_plates["message"]['Plates']]
    if userPlate_id not in existing_plates_ids:
        raise HTTPException(
            status_code=400, detail=f"The plate Id is not valid")
    response = delete_Plate_service(userPlate_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response


def update_plate_controller(id_user: str, userPlate_id: str, Plate_data: Plate):
    user_plates = get_plate_user(id_user)
    existing_plates_ids = [plate["id"]
                           for plate in user_plates["message"]['Plates']]
    if userPlate_id not in existing_plates_ids:
        raise HTTPException(
            status_code=400, detail=f"The plate Id is not valid")

    if id_user != Plate_data.id_User:
        raise HTTPException(
            status_code=400, detail=f"You can not change id_User")

    validate_plate_data(Plate_data)

    response = update_Plate(userPlate_id, Plate_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def get_platebyID(plate_id: str):
    plates = get_plates()
    existing_plate_ids = [plate["id"] for plate in plates]
    if plate_id not in existing_plate_ids:
        raise HTTPException(
            status_code=400, detail=f"Invalid plate ID: {plate_id}")
    response = getPlateByID(plate_id)
    if response['plate'] is None:
        raise HTTPException(
            status_code=400, detail=f"The plate ID: {plate_id} is not in our data base")
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def get_publicPlates():
    response = get_public_plates()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"Plates": response}


def update_user_plates_to_verified(user_id: str):
    response = update_user_platestoverified(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"Plates": response}


def get_publicPlates_notUser(user_id: str):
    response = get_public_plates_notUser(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"Plates": response}