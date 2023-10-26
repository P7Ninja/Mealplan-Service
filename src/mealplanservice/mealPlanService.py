from fastapi import FastAPI, Query
from .database import BaseMealPlanDB
from typing import Annotated
from .database import schema

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
        self.__app.add_api_route("/mealPlan", self.create_meal_plan, methods=["POST"])
        self.__app.add_api_route("/mealPlanRecipe", self.create_meal_plan_recipe, methods=["POST"])
        self.__app.add_api_route("/mealsPerDay", self.create_meals_per_day, methods=["POST"])
        self.__app.add_api_route("/mealPlan/{userID}", self.get_current_meal_plan, methods=["GET"])
        self.__app.add_api_route("/mealPlans/{userID}", self.get_all_meal_plans, methods=["GET"])
        self.__app.add_api_route("/mealPlan/{planID}", self.delete_meal_plan, methods=["DELETE"])
        self.__app.add_api_route("/", lambda: {"message": "Mealplan-Service"}, methods=["GET"])

    async def create_meal_plan(self, baseMealPlan: schema.BaseMealPlan):
        return self.__db.create_meal_plan(baseMealPlan)

    async def create_meal_plan_recipe(self, mealPlanRecipe: schema.mealPlanRecipe):
        return self.__db.create_meal_recipe(mealPlanRecipe)
    
    async def create_meals_per_day(self, mealsPerDay: schema.mealsPerDay):
        return self.__db.create_meals_per_day(mealsPerDay)

    async def get_current_meal_plan(self, userID: int=0):
        return self.__db.get_current_meal_plan(userID)

    async def get_all_meal_plans(self, userID: int=0):
        return self.__db.get_all_meal_plans(userID)
    
    async def delete_meal_plan(self, planID: int=0):
        return self.__db.delete_meal_plan(planID)