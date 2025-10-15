from app.service.userTotCal_service import updateDailyCalories,createUserTotCal_service,get_totalCAL, count_recent_consecutive_days_with_calories
from app.models.userTotCal import CalUpdateModel, UserTotCal
from fastapi import HTTPException
from datetime import datetime

def updateDailyCalories_controller(calPerDay_id, calUpdate: UserTotCal):
    response = updateDailyCalories(calPerDay_id, calUpdate)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}

def createUserTotCal(userTotCal: UserTotCal):
    response = createUserTotCal_service(userTotCal)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
def get_TotCal(user_id: str):
    response = get_totalCAL(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
def get_streak(user_id: str):
    response = count_recent_consecutive_days_with_calories(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}