from fastapi import FastAPI, Query
from .database import BaseMealPlanDB
from .database import schema
import httpx
from typing import List
from datetime import date, timedelta
from fastapi import HTTPException, status

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
        self.__app.add_api_route("/generate", self.generate_meal_plan, methods=["POST"])
        self.__app.add_api_route("/mealPlan/{userID}", self.get_current_meal_plan, methods=["GET"])
        self.__app.add_api_route("/mealPlans/{userID}", self.get_all_meal_plans, methods=["GET"])
        self.__app.add_api_route("/", lambda: {"message": "Mealplan-Service"}, methods=["GET"])
        self.__app.add_api_route("/mealPlan/{planID}/{userID}", self.delete_meal_plan, methods=["DELETE"])
   
    async def create_meal_plan(self, baseMealPlan: schema.BaseMealPlan):
        return self.__db.create_meal_plan(baseMealPlan)

    async def create_meal_plan_recipe(self, mealPlanRecipe: schema.MealPlanRecipe):
        return self.__db.create_meal_recipe(mealPlanRecipe)
    
    async def create_meals_per_day(self, mealsPerDay: schema.MealsPerDay):
        return self.__db.create_meals_per_day(mealsPerDay)

    async def get_current_meal_plan(self, userID: int=0):
        return self.__db.get_current_meal_plan(userID)

    async def get_all_meal_plans(self, userID: int=0):
        return self.__db.get_all_meal_plans(userID)
    
    async def delete_meal_plan(self, userID: int=0, planID: int=0):
        return self.__db.delete_meal_plan(userID, planID)

    async def get_recipe_from_recipeservice(self, recipe_split_parameters):
        try:
            async with httpx.AsyncClient() as client:
                return await client.get(self.__cfg["RECIPESERVICE"]+"/recipe/random", params=recipe_split_parameters)
        except httpx.ConnectError as err:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to communicate with the recipe service: {err}"
            )

    async def generate_meal_plan(self, generate_meal_plan: schema.GenerateMealPlan):
        async with httpx.AsyncClient() as client:
            energy_error = 1
            # inventory = getinventory(user_id)
            all_recipes = {}
            aggregated_daily_recipes = {}
            for day in range(0, (len(generate_meal_plan.split_days)//3)):
                breakfast_index = 3 * day
                lunch_index = 3 * day + 1
                dinner_index = 3 * day + 2
                breakfast_split = generate_meal_plan.split_days[breakfast_index]
                lunch_split = generate_meal_plan.split_days[lunch_index]
                dinner_split = generate_meal_plan.split_days[dinner_index]
                recipe_num = 0

                if breakfast_split:
                    recipe_num += 1
                    split_breakfast = {
                    "calories": generate_meal_plan.targets[0] * breakfast_split,
                    "fat": generate_meal_plan.targets[1] * breakfast_split,
                    "carbohydrates": generate_meal_plan.targets[2] * breakfast_split,
                    "protein": generate_meal_plan.targets [3] * breakfast_split,
                    'energy_error': energy_error, 
                    'tags': ["Morgenmad"], 
                    'ingredients': []
                    }

                    breakfast_response = await self.get_recipe_from_recipeservice(split_breakfast)

                    breakfast_recipe = breakfast_response.json()
                    all_recipes[f"recipe{recipe_num}"] = breakfast_recipe
                if lunch_split:
                    recipe_num += 1
                    split_lunch = {
                    "calories": generate_meal_plan.targets[0] * lunch_split,
                    "fat": generate_meal_plan.targets[1] * lunch_split,
                    "carbohydrates": generate_meal_plan.targets[2] * lunch_split,
                    "protein": generate_meal_plan.targets [3] * lunch_split,
                    'energy_error': energy_error, 
                    'tags': ["Middagsmad"], 
                    'ingredients': []
                    }
                    lunch_response = await self.get_recipe_from_recipeservice(split_lunch)
                    lunch_recipe = lunch_response.json()
                    all_recipes[f"recipe{recipe_num}"] = lunch_recipe
                if dinner_split:
                    recipe_num += 1
                    split_dinner = {
                    "calories": generate_meal_plan.targets[0] * dinner_split,
                    "fat": generate_meal_plan.targets[1] * dinner_split,
                    "carbohydrates": generate_meal_plan.targets[2] * dinner_split,
                    "protein": generate_meal_plan.targets [3] * dinner_split,
                    'energy_error': energy_error, 
                    'tags': ["Aftensmad"], 
                    'ingredients': []
                    }
                    dinner_response = await self.get_recipe_from_recipeservice(split_dinner)
                    dinner_recipe = dinner_response.json()
                    all_recipes[f"recipe{recipe_num}"] = dinner_recipe

                if all_recipes == {}:
                    return "ERROR! The split_days values are all 0!"
                aggregated_daily_recipes[f"day{day+1}"] = await self.aggregate_daily_recipes(all_recipes)
            print(aggregated_daily_recipes)
            await self.insert_generated_mealplan(generate_meal_plan.userID, aggregated_daily_recipes)
            print("Returning...")
            return aggregated_daily_recipes


        
    async def aggregate_daily_recipes(self, all_recipes):
        totalCalories = 0
        totalProtein = 0
        totalCarbohydrates = 0
        totalFat = 0
        aggregated_daily_recipes = {}
        aggregated_daily_recipes["recipes"] = {}
        for recipe in range(1, len(all_recipes) + 1):
            totalCalories += all_recipes[f"recipe{recipe}"]["energy"]["calories"]
            totalProtein += all_recipes[f"recipe{recipe}"]["energy"]["protein"]
            totalCarbohydrates += all_recipes[f"recipe{recipe}"]["energy"]["carbohydrates"]
            totalFat += all_recipes[f"recipe{recipe}"]["energy"]["fat"]
            aggregated_daily_recipes["recipes"][f"recipe{recipe}"] = all_recipes[f"recipe{recipe}"]["id"]

        aggregated_daily_recipes["totalCalories"] = totalCalories
        aggregated_daily_recipes["totalProtein"] = totalProtein
        aggregated_daily_recipes["totalCarbohydrates"] = totalCarbohydrates
        aggregated_daily_recipes["totalFat"] = totalFat

        return aggregated_daily_recipes

    async def insert_generated_mealplan(self, userid, aggregated_daily_recipes):
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=len(aggregated_daily_recipes))
        meal_plan = schema.BaseMealPlan(userID=userid, startDate=str(start_date), endDate=str(end_date))
        planID = await self.create_meal_plan(meal_plan)
        for day in range(1, len(aggregated_daily_recipes) + 1):
            meals = len(aggregated_daily_recipes[f"day{day}"]["recipes"])
            totalCalories = aggregated_daily_recipes[f"day{day}"]["totalCalories"]
            totalProtein = aggregated_daily_recipes[f"day{day}"]["totalProtein"]
            totalCarbohydrates = aggregated_daily_recipes[f"day{day}"]["totalCarbohydrates"]
            totalFat = aggregated_daily_recipes[f"day{day}"]["totalFat"]
            meals_per_day = schema.mealsPerDay(planID=planID, meals=meals, totalCalories=totalCalories, 
                                               totalProtein=totalProtein, totalCarbohydrates=totalCarbohydrates, totalFat=totalFat)
            await self.create_meals_per_day(meals_per_day)
            for recipe_num in range(1, len(aggregated_daily_recipes[f"day{day}"]["recipes"]) + 1):
                meal_plan_recipe = schema.mealPlanRecipe(planID=planID, recipeID=aggregated_daily_recipes[f"day{day}"]["recipes"][f"recipe{recipe_num}"])
                await self.create_meal_plan_recipe(meal_plan_recipe)
            

