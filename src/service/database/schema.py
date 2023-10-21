from pydantic import BaseModel

class mealPlan(BaseModel):
    id: int
    userID: int
    startDate: str
    endDate: str
    mealsPerDay: list[int]
    recipes: list[int]


class planNutrition(BaseModel):
    planid: int
    totalCalories: int
    totalProtein: float
    totalCarbs: float
    totalFat: float
