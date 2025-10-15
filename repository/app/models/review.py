from pydantic import BaseModel, Field
from typing import List
class Comment(BaseModel):
    comment: str
    id_User: str
    score: int

class Review(BaseModel):
    plate_Id: str
    comments: List[Comment]
    score: float

