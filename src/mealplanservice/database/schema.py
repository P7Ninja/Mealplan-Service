from pydantic import BaseModel

class BasemealPlan(BaseModel):
    userID: int
    startDate: str
    endDate: str
    totalCalories: int
    totalProtein: float
    totalCarbohydrates: float
    totalFat: float

class mealPlanRecipes(BaseModel):
    id: int
    planID: int
    recipeID: int

class mealsPerDay(BaseModel):
    id: int
    planID: int
    meals: int

class mealplan(BasemealPlan):
    id: int