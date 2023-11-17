from fastapi import FastAPI

from mealplanservice.database import SQLMealPlanDB
from mealplanservice import mealPlanService
import os


cfg = os.environ

app = FastAPI()
db = SQLMealPlanDB(cfg)
service = mealPlanService(app, db, cfg)

service.configure_database()
service.configure_routes()