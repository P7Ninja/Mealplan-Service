from . import schema

class BaseMealPlanDB:
    def __init__(self, cfg: dict) -> None:
            self.cfg = cfg
                
    def startup(self):
        return
    
    def shutdown(self):
        return
    
    def create(self):
        return
    
    def create_meal_plan(self, baseMealPlan: schema.BaseMealPlan) -> schema.mealplan:
         return
    
    def get_all_meal_plans(self, userID: int) -> schema.mealplan:
         return
    
    def get_current_meal_plan(self, userID: int) -> schema.mealplan:
         return
    
    def delete_meal_plan(self, planID: int) -> schema.mealplan:
         return
    