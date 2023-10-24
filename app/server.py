from fastapi import FastAPI
from dotenv import dotenv_values

from mealplanservice.database import SQLMealPlanDB
from mealplanservice import mealPlanService

cfg = dotenv_values(".env")

app = FastAPI()
db = SQLMealPlanDB(cfg)
service = mealPlanService(app, db, cfg)

service.configure_database()
service.configure_routes()