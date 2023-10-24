from fastapi import FastAPI
from dotenv import dotenv_values

from mealplanservice import mealPlanManager, simpleMealPlanDB

cfg = dotenv_values(".env")

app = FastAPI()
db = simpleMealPlanDB(cfg)
service = mealPlanManager(app, db, cfg)

service.configure_database()
service.configure_routes()