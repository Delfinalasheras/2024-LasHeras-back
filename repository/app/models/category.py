from pydantic import BaseModel, Field
from typing import List


class Category(BaseModel):
    name: str
    icon: str
    id_User: str
    foods: List[str]
    plates: List[str]
    drinks: List[str]

    class Config:
        # Esto facilita la conversión entre ORM (SQLAlchemy) y Pydantic.
        orm_mode = True
