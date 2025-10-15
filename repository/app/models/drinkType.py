from pydantic import BaseModel
class DrinkType(BaseModel):
    name: str
    id_user: str