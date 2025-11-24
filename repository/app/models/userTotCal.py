from pydantic import BaseModel, Field
from datetime import datetime
# Modelo para registrar un nuevo Food
class UserTotCal(BaseModel):
    day: datetime # Ensure Food_price is non-negative
    totCal: float = Field(..., ge=0)
    totProt: float = Field(..., ge=0)
    totSodium: float = Field(..., ge=0)
    totCarbs: float = Field(..., ge=0)
    totFats:float = Field(..., ge=0)

class CalUpdateModel(BaseModel):
    calUpdate: int