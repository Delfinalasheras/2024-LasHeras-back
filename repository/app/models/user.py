from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# Modelo para registrar un nuevo Food


class UserGoals(BaseModel):
    calories: int
    sodium: int
    fats: int
    carbohydrates: int
    protein: int
    sugar: int
    caffeine: int


class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    surname: str
    weight: float = Field(..., ge=0)
    height: float = Field(..., ge=0)
    birthDate: datetime
    goals: Optional[UserGoals]
    validation: int
    achievements: List[int]


class UserForgotPassword(BaseModel):
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class ResetPassword(BaseModel):
    token: str
    new_password: str


class UpdateUserData(BaseModel):
    id_user: str
    name: str
    surname: str
    weight: float
    height: float
    birthDate: datetime
    goals: UserGoals
    validation: int
    achievements: List[int]
class GoalRequest(BaseModel):
    achivement_id: int 
