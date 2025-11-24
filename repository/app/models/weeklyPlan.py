from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# Modelo para un item individual de comida (lo que hay dentro del array)
class MealItem(BaseModel):
    plate_id: str
    name: str
    amount_eaten: Optional[float] = Field(default=1, ge=0)

# Modelo para un día completo (Lunes, Martes, etc.)
class DayPlan(BaseModel):
    date: str  # Ej: "2025-11-17"
    breakfast: List[MealItem] = Field(default_factory=list)
    lunch: List[MealItem] = Field(default_factory=list)
    snack: List[MealItem] = Field(default_factory=list)
    dinner: List[MealItem] = Field(default_factory=list)

# Modelo principal que recibe el Controller (el payload del frontend)
class WeeklyPlanRequest(BaseModel):
    week_start: str  # Ej: "2025-11-17"
    days: Dict[str, DayPlan]
