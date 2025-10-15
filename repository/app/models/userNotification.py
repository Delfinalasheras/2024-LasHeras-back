from pydantic import BaseModel, Field
from datetime import datetime

class UserNotification(BaseModel):
    is_read: bool
    message: str
    timestamp: datetime
    user_id: str