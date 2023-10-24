from fastapi import FastAPI
from dotenv import dotenv_values



cfg = dotenv_values(".env")

app = FastAPI()
db = SQLMealPlanDB(cfg)
service = MealPlanService(app, db, cfg)

service.configure_database()
service.configure_routes()
