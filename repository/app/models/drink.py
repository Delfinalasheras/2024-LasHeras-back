from pydantic import BaseModel, Field
from typing import List

class Drink(BaseModel):
    name : str
    sugar_portion: int
    caffeine_portion: int 
    calories_portion: int
    measure_portion: int
    measure: str
    typeOfDrink: str
    id_User: str
