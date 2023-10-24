from fastapi import FastAPI, Query
from .database import BaseMealPlanDB
from typing import Annotated

_list = Annotated[list[str] | None, Query()]

class mealPlanService:
    def __init__(self, app: FastAPI, database: BaseMealPlanDB, cfg: dict) -> None:
        self.__app = app
        self.__db = database
        self.__cfg = cfg
        
    def configure_database(self):
        @self.__app.on_event("startup")
        def startup():
            self.__db.startup()
        
        @self.__app.on_event("shutdown")
        def shutdown():
            self.__db.shutdown()

    def configure_routes(self):
        self.__app.add_api_route("/get_current_mealplan/{userID}", self.get_current_mealplan, methods=["GET"])
        # self.__app.add_api_route("/get_all_mealplans/{id}", self.get_mealplan, methods=["GET"])
        # self.__app.add_api_route("/delete_mealplan", self.delete_mealplan, methods=["POST"])
        self.__app.add_api_route("/", lambda: {"message": "Mealplan-Service"}, methods=["GET"])

    async def get_current_mealplan(self, userID: int=0):
        return self.__db.get_current_mealplan(userID=userID)

    # async def get_all_mealplans(self, userID int):
        

    # async def get_current_mealplan(self,
    #                                planID: int=0, 
    #                                userID: int=0, 
    #                                startDate: str='', 
    #                                endDate: str='', 
    #                                totalCalories: int=0, 
    #                                totalProtein: float=0.0,
    #                                totalCarbohydrates: float=0.0,
    #                                totalFat: float=0.0

    async def get_recipe(self, id: int):
        return self.__db.get_recipe(id)
    
    async def get_recipes(self, 
                          calories: float=0.0, 
                          protein: float=0.0, 
                          fat: float=0.0, 
                          carbohydrates: float=0.0, 
                          energy_error: float=0.0, 
                          tags: _list=None,
                          ingredients: _list=None
                          ):
        return self.__db.get_recipes(
            calories=calories, 
            protein=protein,
            fat=fat,
            carbs=carbohydrates,
            energy_error=energy_error,
            tags=tags,
            ingredients=ingredients
            )
    
    async def get_random_recipe(self, 
                          calories: float=0.0, 
                          protein: float=0.0, 
                          fat: float=0.0, 
                          carbohydrates: float=0.0, 
                          energy_error: float=0.0, 
                          tags: _list=None,
                          ingredients: _list=None
                          ):
        return self.__db.get_random_recipe(
            calories=calories, 
            protein=protein,
            fat=fat,
            carbs=carbohydrates,
            energy_error=energy_error,
            tags=tags,
            ingredients=ingredients
            )