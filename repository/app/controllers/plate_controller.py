from app.service.plate_service import update_user_platestoverified,get_public_plates_notUser, create_plate,get_user_plates,delete_Plate_service,update_Plate,getPlateByID, get_public_plates
from app.models.plate import Plate
from fastapi import HTTPException
from datetime import datetime


def plateLog(plate: Plate):
    response = create_plate(plate)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"id": response}
def get_plate_user(user_id: str):
    response = get_user_plates(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def delete_plate(userPlate_id: str):
    response = delete_Plate_service(userPlate_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return  response


def update_plate_controller(userPlate_id: str, Plate_data: Plate):
    response = update_Plate(userPlate_id, Plate_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
def get_platebyID(plate_id: str):
    response = getPlateByID(plate_id)
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
def get_publicPlates_notUser(user_id:str):
    response= get_public_plates_notUser(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"Plates": response}