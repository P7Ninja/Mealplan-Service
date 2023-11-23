from fastapi import FastAPI

from mealplanservice.database import SQLMealPlanDB
from mealplanservice import mealPlanService
import os
from dotenv import dotenv_values

class Config:
    def __init__(self) -> None:
        self.__env = os.environ
        self.__envfile = dict()
        if os.path.exists(".env"):
            self.__envfile = dotenv_values(".env")

    def __getitem__(self, key: str):
        if key in self.__env:
            return self.__env[key]
        return self.__envfile[key]

cfg = Config()

app = FastAPI()
db = SQLMealPlanDB(cfg)
service = mealPlanService(app, db, cfg)

service.configure_database()
service.configure_routes()