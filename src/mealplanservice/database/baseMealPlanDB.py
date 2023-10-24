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
    
    def create_mealplan(self, mealplan: schema.BasemealPlan) -> schema.mealplan:
         return
    
    def get_all_mealplans(self, userID: int) -> schema.mealplan:
         return
    
    def get_current_mealplan(self, userID: int) -> schema.mealplan:
         return
    
    def delete_mealplan(self, planID: int) -> schema.mealplan:
         return
    
    # def update_mealplan_item(self, id: int) -> schema.mealplan:
    #     raise NotImplementedError("Not Implemented!")
