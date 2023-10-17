from pydantic import BaseModel

class mealPlan(BaseModel):
    id: int
    userID: int
    startDate: str
    endDate: str
    totalMeals: int
    mealsPerDay: int
    

class meal(BaseModel):
    planid: int
    recipeid: int
    mealNum: int

class planNutrition(BaseModel):
    