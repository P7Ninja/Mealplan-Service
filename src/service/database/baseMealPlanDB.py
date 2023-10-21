from . import schema

class BaseMealplanDB:
    def __init__(self, cfg: dict) -> None:
            self.cfg = cfg
                
    def startup(self):
        return
    
    def shutdown(self):
        return
    
    def create(self):
        return
    
    def create_mealplan(self):
         return
    
    def get_mealplan(self):
         return
    
    def delete_mealplan(self):
         return
    
    def update_mealplan_item(self):
        raise NotImplementedError("Not Implemented!")
    
    def create_plan_nutrition(self):
         return
    
    def create_daily_nutrition(self):
         return
    
