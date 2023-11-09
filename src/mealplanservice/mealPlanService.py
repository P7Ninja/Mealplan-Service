from fastapi import FastAPI, Query
from .database import BaseMealPlanDB
from typing import Annotated
from .database import schema
import httpx
from enum import Enum
from typing import TypeVar, Type
import asyncio

_list = Annotated[list[str] | None, Query()]

T = TypeVar('T')

class ResponseType(Enum):
    DICT = 0
    LIST = 1
    PRIM = 2


class Service:
    def __init__(self, dest: str):
        self.__dest = dest
        self.__types = {
            ResponseType.DICT: lambda m, x: m(**x),
            ResponseType.LIST: lambda m, x: m(*x),
            ResponseType.PRIM: lambda m, x: m(x)
        }

    async def request(self, 
                      method: str,
                      endpoint: str,
                      res_model: Type[T],
                      res_type: ResponseType=ResponseType.DICT,
                      data: str = None,
                      ) -> T:
        async with httpx.AsyncClient() as client:
            req = client.build_request(method, self.__dest + endpoint, data=data)
            res = (await asyncio.gather(client.send(req)))[0]
            
            if res.status_code in range(400, 599):
                err: dict = res.json()
                detail = err.get("detail", None)
                if detail is None:
                    detail = err.get("title", "Error")
                raise HTTPException(
                    status_code=res.status_code, 
                    detail=detail
                    )
            return self.__types[res_type](res_model, res.json())

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
    
    async def generate_meal_plan(self, user_id):
        params = {'calories': 428.0, 
                'protein': 29.0207, 
                'fat': 43.7259, 
                'carbohydrates': 25.5363, 
                'energy_error': 1, 
                'tags': [], 
                'ingredients': []}
        service_recipe = Service("http://localhost:8443")
        r = await service_recipe.request("get", "/recipe/random", dict, dict, params)
        
        response_content = await r.text()
        print("Response Content:", response_content)  # Debugging line
        
        response_json = await r.json()
        return response_json

    # targets: list=[], split_days: list=[]