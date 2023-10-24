from pydantic import BaseModel

class BasemealPlan(BaseModel):
    userID: int
    startDate: str
    endDate: str
    mealsPerDay: list[int]
    recipes: list[int]
    totalCalories: int
    totalProtein: float
    totalCarbohydrates: float
    totalFat: float

class mealplan(BasemealPlan):
    id: int


