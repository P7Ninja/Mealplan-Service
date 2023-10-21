from fastapi import FastAPI
from dotenv import dotenv_values

from recipeservice import RecipeService, SQLRecipeDB

cfg = dotenv_values(".env")

app = FastAPI()
db = SQLRecipeDB(cfg)
service = RecipeService(app, db, cfg)

service.configure_database()
service.configure_routes()