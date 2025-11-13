from pydantic import BaseModel, Field
from typing import List

class Category(BaseModel):
    name: str = Field(..., min_length=1)
    icon: str = Field(..., min_length=1)
    foods: List[str] = Field(..., min_items=1)

    class Config:
        # Esto facilita la conversión entre ORM (SQLAlchemy) y Pydantic.
        orm_mode = True
