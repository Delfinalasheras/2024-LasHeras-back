from app.service.drinkType_service import create_drinkType, drinkType, drinkType_by_id,getUserDrinkTypes,deleteDrinkType
from app.models.drinkType import DrinkType
from fastapi import HTTPException

def validate_drinktype_data(drinkType: DrinkType):
    required_fields = [
        "name",
    ]
    for field in required_fields:
        value = getattr(drinkType, field, None)
        if value is None or (isinstance(value, str) and not value.strip()):
            raise HTTPException(status_code=400, detail=f"Field '{field}' is required and cannot be empty")
def register_new_drinkType(user_id,drinkType: DrinkType):
    validate_drinktype_data(drinkType)
    drink_data = drinkType.dict()
    drink_data["id_user"] = user_id
    response = create_drinkType(drink_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "drinkType registered successfully", "drinkType_id": response["id"]}

def get_drinkTypes():
    response = drinkType()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}

def get_drinkType_by_id(drinkType_id: str):
    response = drinkType_by_id(drinkType_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}

def UserDrinkTypes(user_id: str):
    response = getUserDrinkTypes(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
def delete_DrinkType(drinkType_id):
    response = deleteDrinkType(drinkType_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}