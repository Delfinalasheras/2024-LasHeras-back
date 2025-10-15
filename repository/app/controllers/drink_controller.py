from app.service.drink_service import create_drink, drinks, drink_by_id,delete_drink,update_Drink,GroupedDrinks
from app.models.drink import Drink 
from fastapi import HTTPException


def register_new_drink(drink: Drink):
    response = create_drink(drink.dict())
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "drink registered successfully", "drink_id": response["id"]}

def get_drinks(user_id: str):
    response = drinks(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}

def get_drink_by_id(drink_id: str):
    response = drink_by_id(drink_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
def deletedrink(drink_id: str):
    response= delete_drink(drink_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
def Updatedrink(drink_id: str, UpdatedData:Drink):
    response= update_Drink(drink_id, UpdatedData)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response
def Grouped_Drinks(drink_id: str):
    response= GroupedDrinks(drink_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response
