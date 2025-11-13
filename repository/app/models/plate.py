from pydantic import BaseModel, Field
from typing import List


class PlateFood(BaseModel):
    ingredientId: str
    quantity: float = Field(..., ge=0)


class Plate(BaseModel):
    name: str
    ingredients: List[PlateFood]
    calories_portion: float
    sodium_portion: float
    carbohydrates_portion: float
    fats_portion: float
    protein_portion: float
    image: str
    public: bool = False
    verified: int = 0
