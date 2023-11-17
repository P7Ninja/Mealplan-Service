from pydantic import BaseModel

class BaseMealPlan(BaseModel):
    userID: int
    startDate: str
    endDate: str

class mealPlanRecipe(BaseModel):
    planID: int
    recipeID: int

class mealsPerDay(BaseModel):
    planID: int
    meals: int
    totalCalories: int
    totalProtein: float
    totalCarbohydrates: float
    totalFat: float

class mealplan(BaseMealPlan):
    id: int