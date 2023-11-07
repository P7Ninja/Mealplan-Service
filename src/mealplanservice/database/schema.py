from pydantic import BaseModel

class BaseMealPlan(BaseModel):
    userID: int
    startDate: str
    endDate: str
    totalCalories: int
    totalProtein: float
    totalCarbohydrates: float
    totalFat: float

class mealPlanRecipe(BaseModel):
    planID: int
    recipeID: int

class mealsPerDay(BaseModel):
    planID: int
    meals: int

class mealplan(BaseMealPlan):
    id: int