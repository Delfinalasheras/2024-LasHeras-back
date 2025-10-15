from pydantic import BaseModel, Field
from typing import List
class Goals(BaseModel):
    id_User: str
    protein_goal: int
    carbs_goal: int
    sodium_goal: int
    fats_goal: int
    calorie_goal: int