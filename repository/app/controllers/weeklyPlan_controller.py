from fastapi import HTTPException
from app.models.weeklyPlan import WeeklyPlanRequest
# Importamos los servicios que acabamos de crear
from app.service.weeklyPlan_service import get_plan_by_week_service, update_plan_service

def get_weekly_plan_controller(user_id: str, week_start: str):
    response = get_plan_by_week_service(user_id, week_start)
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response["plan"]

def update_weekly_plan_controller(user_id: str, plan_data: WeeklyPlanRequest):
    print("Updating plan with data:", plan_data)
    data = plan_data.dict()
    data["id_User"] = user_id

    response = update_plan_service(data)

    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    return response