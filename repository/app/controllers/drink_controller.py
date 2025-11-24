from app.service.drink_service import create_drink, drinks, drink_by_id,delete_drink,update_Drink,GroupedDrinks
from app.models.drink import Drink 
from fastapi import HTTPException
def validate_drink_data(drink: Drink):
    """Valida los datos de la bebida antes de crear o actualizar."""
    required_fields = [
        "name",
        "sugar_portion",
        "caffeine_portion",
        "calories_portion",
        "measure_portion",
        "measure",
        "typeOfDrink"
    ]

    # Validar campos requeridos
    for field in required_fields:
        value = getattr(drink, field, None)
        if value is None or (isinstance(value, str) and not value.strip()):
            raise HTTPException(status_code=400, detail=f"Field '{field}' is required and cannot be empty")

    # Validaciones numéricas
    if drink.sugar_portion < 0:
        raise HTTPException(status_code=400, detail="sugar_portion cannot be negative")
    if drink.caffeine_portion < 0:
        raise HTTPException(status_code=400, detail="caffeine_portion cannot be negative")
    if drink.calories_portion < 0:
        raise HTTPException(status_code=400, detail="calories_portion cannot be negative")
    if drink.measure_portion <= 0:
        raise HTTPException(status_code=400, detail="measure_portion must be greater than 0")



def register_new_drink(user_id:str,drink: Drink):
    validate_drink_data(drink)

    drink_data = drink.dict()
    drink_data["id_User"] = user_id
    
    response = create_drink(drink_data)
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
