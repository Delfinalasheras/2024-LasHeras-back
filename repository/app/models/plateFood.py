from pydantic import BaseModel, Field

class PlateFood(BaseModel):
    id_food : str
    amount: float = Field(..., ge=0)