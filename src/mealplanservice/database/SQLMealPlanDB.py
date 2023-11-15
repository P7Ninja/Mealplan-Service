import pprint
from fastapi import FastAPI, HTTPException
import mysql.connector
import requests
from mealplanservice.database import schema
from .BaseMealPlanDB import BaseMealPlanDB
import os
import httpx
from enum import Enum
from typing import TypeVar, Type
import asyncio

# app = FastAPI()

class SQLMealPlanDB(BaseMealPlanDB):
    def __init__(self, cfg: dict) -> None:
        super().__init__(cfg)
        self.__database = None
        self.__cursor = None

    def startup(self):
        self.__database = mysql.connector.connect(
            host=self.cfg["HOST"],
            user=self.cfg["USER"],
            password=self.cfg["PASSWORD"],
            database=self.cfg["DATABASE"]
        )

        self.__cursor = self.__database.cursor(dictionary=True)
        self.__cursor = self.__database.cursor(buffered=True)

    def execute_query(self, query, parameters):
        self.__cursor.execute(query, parameters)
        self.__database.commit()

    def create_meal_plan(self, baseMealPlan: schema.BaseMealPlan):
        parameters = (0, baseMealPlan.userID, baseMealPlan.startDate, baseMealPlan.endDate, baseMealPlan.totalCalories, 
                      baseMealPlan.totalProtein, baseMealPlan.totalCarbohydrates, baseMealPlan.totalFat)
        self.execute_query("INSERT INTO mealPlan VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", parameters)
        return {"message": "Success"}

    def create_meal_recipe(self, mealPlanRecipe: schema.mealPlanRecipe):
        self.execute_query("INSERT INTO mealPlanRecipes VALUES(0, %s, %s)", (mealPlanRecipe.planID, mealPlanRecipe.recipeID))
        return {"message": "Success", "planID": mealPlanRecipe.planID, "recipeID": mealPlanRecipe.recipeID}

    def create_meals_per_day(self, mealsPerDay: schema.mealsPerDay):
        self.execute_query("INSERT INTO mealsPerDay VALUES(0, %s, %s)", (mealsPerDay.planID, mealsPerDay.meals))
        return {"message": "Success", "planID": mealsPerDay.planID, "recipeID": mealsPerDay.meals}

    def delete_meal_plan(self, planID: int):
        if(planID == None):
            return
        self.execute_query("DELETE FROM mealPlan WHERE planID=%s", (planID,))
        return {"Message": "Success", "planID": planID}

    def get_current_meal_plan(self, userID: int):
        self.execute_query("""
            SELECT mp.*, mpr.recipeID, mpd.meals
            FROM mealPlan mp
            LEFT JOIN mealplanrecipes mpr ON mp.planID = mpr.planID
            LEFT JOIN mealsperday mpd ON mp.planID = mpd.planID
            WHERE mp.userID=%s
            ORDER BY mp.planID DESC
        """, (userID,))

        meal_plan_results = self.__cursor.fetchall()

        if not meal_plan_results:
            return None

        meal_plan_json = {
            "planID": meal_plan_results[0][0],
            "userID": meal_plan_results[0][1],
            "startDate": str(meal_plan_results[0][2]),
            "endDate": str(meal_plan_results[0][3]),
            "totalCalories": meal_plan_results[0][4],
            "totalProtein": meal_plan_results[0][5],
            "totalCarbohydrates": meal_plan_results[0][6],
            "totalFat": meal_plan_results[0][7],
            "days": []
        }

        days = []
        day_content = {}
        latest_recipe_index = 0

        for row in meal_plan_results:
            if row[8] is not None:  # Check if there is a recipeID
                day_content[f"recipeID{len(day_content) + 1}"] = row[8]

            if len(day_content) == row[9]:  # Check if we have added all meals for the day
                days.append(day_content)
                day_content = {}
                latest_recipe_index += row[9]

        days.reverse()
        meal_plan_json["days"] = days

        return meal_plan_json

    
    def get_all_meal_plans(self, userID: int):
        self.execute_query("SELECT * FROM mealPlan WHERE userID=%s ORDER BY planID DESC", (userID,))
        meal_plan_results   = self.__cursor.fetchall()
        plan_num = 1
        meal_plan_json = {}
        for meal_plan_result in meal_plan_results:
            meal_plan_json[f"plan{plan_num}"] = {
                "planID": meal_plan_result[0],
                "userID": meal_plan_result[1],
                "startDate": str(meal_plan_result[2]),
                "endDate": str(meal_plan_result[3]),
                "totalCalories": meal_plan_result[4],
                "totalProtein": meal_plan_result[5],
                "totalCarbohydrates": meal_plan_result[6],
                "totalFat": meal_plan_result[7]
                }

            self.execute_query("SELECT id, recipeID FROM mealplanrecipes WHERE planID=%s ORDER BY id DESC", (meal_plan_json[f"plan{plan_num}"]["planID"],))
            meal_plan_recipes_result = self.__cursor.fetchall()
            recipe_id_list = []
            for row in meal_plan_recipes_result:
                recipe_id_list.append(row[1])

            self.execute_query("SELECT id, meals FROM mealsperday WHERE planID=%s ORDER BY id DESC", (meal_plan_json[f"plan{plan_num}"]["planID"],))
            meals_per_day_result = self.__cursor.fetchall()
            meals_per_day_list = []
            for row in meals_per_day_result:
                meals_per_day_list.append(row[1])            

            days = []
            latest_recipe_index = 0
            for day in range(0, len(meals_per_day_list)):
                day_content = {}
                meal_plan_json[f"plan{plan_num}"]["days"] = {}
                for meal in range(meals_per_day_list[day]):
                    day_content[f"recipeID{meal+1}"] = recipe_id_list[latest_recipe_index + meal]
                latest_recipe_index += meal + 1
                days.append(day_content)
            days.reverse()
            meal_plan_json[f"plan{plan_num}"]["days"] = days
            plan_num += 1
        
        return meal_plan_json

