from fastapi import FastAPI, Query
from .database import BaseMealPlanDB
from typing import Annotated
from .database import schema
import httpx
from enum import Enum
from typing import TypeVar, Type, List
import asyncio

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
        self.__app.add_api_route("/generate/", self.generate_meal_plan, methods=["GET"])
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
    
    # async def generate_meal_plan(self, userID: int=0):
    #     return self.__db.generate_meal_plan(userID)

    async def generate_meal_plan(self, user_id: int=0, targets: List[int] = Query([]), split_days: List[float] = Query([])):
        print("funk")
        # print(s_r)
        async with httpx.AsyncClient() as client:
            energy_error = 1
            mealplan_json = {}
            recipe_nr = 0
                # inventory = getinventory(user_id)
            for day in range(0, (len(split_days)//3)):
                breakfast_index = 3 * day
                lunch_index = 3 * day + 1
                dinner_index = 3 * day + 2
                breakfast_split = split_days[breakfast_index]
                lunch_split = split_days[lunch_index]
                dinner_split = split_days[dinner_index]
                
                if breakfast_split:
                    split_breakfast = {
                    "calories": targets[0] * breakfast_split,
                    "fat": targets[1] * breakfast_split,
                    "carbohydrates": targets[2] * breakfast_split,
                    "protein": targets [3] * breakfast_split,
                    'energy_error': energy_error, 
                    'tags': ["Morgenmad"], 
                    'ingredients': []
                    }
                    breakfast_response = await client.get(self.__cfg["RECIPESERVICE"]+"/recipe/random", params=split_breakfast)
                    breakfast_recipe = breakfast_response.json()
                    mealplan_json[f"recipe{recipe_nr}"] = breakfast_recipe
                    recipe_nr += 1
                if lunch_split:
                    split_lunch = {
                    "calories": targets[0] * lunch_split,
                    "fat": targets[1] * lunch_split,
                    "carbohydrates": targets[2] * lunch_split,
                    "protein": targets [3] * lunch_split,
                    'energy_error': energy_error, 
                    'tags': ["Middagsmad"], 
                    'ingredients': []
                    }
                    lunch_response = await client.get(self.__cfg["RECIPESERVICE"]+"/recipe/random", params=split_lunch)
                    lunch_recipe = lunch_response.json()
                    mealplan_json[f"recipe{recipe_nr}"] = lunch_recipe
                    recipe_nr += 1
                if dinner_split:
                    split_dinner = {
                    "calories": targets[0] * dinner_split,
                    "fat": targets[1] * dinner_split,
                    "carbohydrates": targets[2] * dinner_split,
                    "protein": targets [3] * dinner_split,
                    'energy_error': energy_error, 
                    'tags': ["Aftensmad"], 
                    'ingredients': []
                    }
                    dinner_response = await client.get(self.__cfg["RECIPESERVICE"]+"/recipe/random", params=split_dinner)
                    dinner_recipe = dinner_response.json()
                    mealplan_json[f"recipe{recipe_nr}"] = dinner_recipe
                    recipe_nr += 1
            return mealplan_json