from pydantic import BaseModel
from typing import List

class BaseMealPlan(BaseModel):
    userID: int
    startDate: str
    endDate: str

class MealPlanRecipe(BaseModel):
    planID: int
    recipeID: int

class MealsPerDay(BaseModel):
    planID: int
    meals: int
    totalCalories: int
    totalProtein: float
    totalCarbohydrates: float
    totalFat: float

class GenerateMealPlan(BaseModel):
    userID: int
    targets: List[float]
    split_days: List[float]

class Mealplan(BaseMealPlan):
    id: int