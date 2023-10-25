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
        self.__app.add_api_route("/get_all_mealplans/{userID}", self.get_all_mealplans, methods=["GET"])
        # self.__app.add_api_route("/delete_mealplan", self.delete_mealplan, methods=["POST"])
        self.__app.add_api_route("/", lambda: {"message": "Mealplan-Service"}, methods=["GET"])

    async def get_current_mealplan(self, userID: int=0):
        return self.__db.get_current_mealplan(userID=userID)

    async def get_all_mealplans(self, userID: int=0):
        return self.__db.get_all_mealplans(userID=userID)