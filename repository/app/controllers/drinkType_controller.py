from app.service.drinkType_service import create_drinkType, drinkType, drinkType_by_id,getUserDrinkTypes,deleteDrinkType
from app.models.drinkType import DrinkType
from fastapi import HTTPException


def register_new_drinkType(drinkType: DrinkType):
    response = create_drinkType(drinkType.dict())
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