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
class CommentCreate(BaseModel):
    comment: str = Field(..., min_length=1, description="El texto no puede estar vacío")
    score: int = Field(..., ge=1, le=5, description="Puntuación entre 1 y 5")

