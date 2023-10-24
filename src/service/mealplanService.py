from fastapi import FastAPI, Query
from .database import baseMealplanDB
from typing import Annotated

_list = Annotated[list[str] | None, Query()]

class mealplanService:
    def __init__(self, app: FastAPI, database: baseMealplanDB, cfg: dict) -> None:
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
        self.__app.add_api_route("/recipe/random", self.get_random_recipe, methods=["GET"])
        self.__app.add_api_route("/mealplan/{id}", self.get_mealplan, methods=["GET"])
        self.__app.add_api_route("/recipe", self.get_recipes, methods=["GET"])
        self.__app.add_api_route("/", lambda: {"message": "Recipe-Service"}, methods=["GET"])

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