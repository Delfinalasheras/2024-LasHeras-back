from app.service.notifications_service import get_user_notifications,changeNotificationToRead
from fastapi import HTTPException, Request

def getNotis(user_id: str):
    try:
        response = get_user_notifications(user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
def NotificationRead(noti_id: str):
    try:
        response = changeNotificationToRead(noti_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))