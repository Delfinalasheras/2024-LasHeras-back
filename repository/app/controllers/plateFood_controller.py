from app.service.plateFood_service import create_plateFood,delete_plateFood_service,update_plateFood,get_user_plateFood
from app.models.plateFood import PlateFood
from fastapi import HTTPException
from datetime import datetime


def PlateFoodLog(PlateFood: PlateFood):
    response = create_plateFood(PlateFood)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}

def get_plateFood(plate_id: str):
    response = get_user_plateFood(plate_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
def delete_PlateFood(userPlateFood_id: str):
    response = delete_plateFood_service(userPlateFood_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])


def update_PlateFood_controller(userPlateFood_id: str, PlateFood_data: PlateFood):
    response = update_plateFood(userPlateFood_id, PlateFood_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}