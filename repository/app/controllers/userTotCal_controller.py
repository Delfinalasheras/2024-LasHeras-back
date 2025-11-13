from app.service.userTotCal_service import (
    updateDailyCalories,
    createUserTotCal_service,
    get_totalCAL,
    count_recent_consecutive_days_with_calories
)
from app.models.userTotCal import CalUpdateModel, UserTotCal
from fastapi import HTTPException
from datetime import datetime
from app.config import db


def updateDailyCalories_controller(user_id: str, calPerDay_id: str, calUpdate: CalUpdateModel):
    try:
        # Buscar el documento
        Totocal_ref = db.collection('UserTotalCal').document(calPerDay_id)
        Totocal_doc = Totocal_ref.get()

        if not Totocal_doc.exists:
            raise HTTPException(status_code=404, detail=f"Record with ID {calPerDay_id} not found")

        data = Totocal_doc.to_dict()
        if data.get('id_user') != user_id:
            raise HTTPException(status_code=403, detail="You can only update your own calorie record")
        validate_totcal_data(calUpdate)
        response = updateDailyCalories(calPerDay_id, calUpdate.dict())

        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])

        return {"message": "Calories updated successfully!"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating record: {str(e)}")


def validate_totcal_data(userTotCal):
    # Aseguramos que los valores no sean negativos
    for field in ["totCal", "totCarbs", "totFats", "totProt", "totSodium"]:
        value = getattr(userTotCal, field, None)
        if value is not None and value < 0:
            raise HTTPException(status_code=400, detail=f"{field} cannot be negative")

    # Validar tipo de día
    if hasattr(userTotCal, "day") and not isinstance(userTotCal.day, datetime):
        raise HTTPException(status_code=400, detail="Day must be a valid datetime object")


def createUserTotCal(user_id: str, userTotCal: UserTotCal):
    validate_totcal_data(userTotCal)

    totcal_data = userTotCal.dict()
    totcal_data["id_user"] = user_id

    response = createUserTotCal_service(totcal_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    return {"message": "Total calories created successfully!"}


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
