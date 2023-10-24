from fastapi import FastAPI
import json
import mysql.connector

from mealplanservice.database import schema
from .BaseMealPlanDB import BaseMealPlanDB

class SQLMealPlanDB(BaseMealPlanDB):
    def __init__(self, cfg: dict) -> None:
        super().__init__(cfg)
        self.__database = None
        self.__cursor = None

    def startup(self, connect_args: dict=dict()):
        self.__database = mysql.connector.connect(
            host=self.cfg["HOST"],
            user=self.cfg["USER"],
            password=self.cfg["PASSWORD"],
            database=self.cfg["DATABASE"]
        )

        self.__cursor = self.__database.cursor(dictionary=True)

    def execute_query(self, query, parameters):
        self.__cursor.execute(query, parameters)
        self.__database.commit()

    def create_meal_plan(self, userID: int, startDate: str, endDate: str, mealsPerDay: int, totalCalories: int, totalProtein: int, totalCarbohydrates: int, totalFat: int):
        if any (x is None for x in [userID, startDate, endDate, mealsPerDay, totalCalories, totalProtein, totalCarbohydrates, totalFat]):
            return
        self.execute_query("INSERT INTO mealPlan VALUES(0, %s, %s, %s, %s, %s, %s, %s, %s)", (userID, startDate, endDate, mealsPerDay, totalCalories, totalProtein, totalCarbohydrates, totalFat))

    def create_meal_recipes(self, planID: int, recipeID: int):
        if(planID != None and recipeID != None):
            self.execute_query("INSERT INTO mealPlanRecipes VALUES(%s, %s)", (planID, recipeID))

    def create_meals_per_day(self, planID: int, meals: int):
        if(planID != None and meals != None):
            self.execute_query("INSERT INTO mealsPerDay VALUES(%s, %s)", (planID, meals))

    def delete_meal_plan(self, planID: int):
        if(planID == None):
            return
        self.execute_query("DELETE FROM mealPlan WHERE planID=%s", (planID,))


    def get_current_mealplan(self, userID: int):
        self.execute_query("SELECT planID, userID, startDate, endDate, totalCalories, totalProtein, totalCarbohydrates, totalFat FROM mealPlan WHERE userID=%s ORDER BY planID DESC", (userID,))
        mealPlanResult = cursor.fetchone()
        planID = mealPlanResult[0]
        userID = mealPlanResult[1]
        startDate = mealPlanResult[2]
        endDate = mealPlanResult[3]
        totalCalories = mealPlanResult[4]
        totalProtein = mealPlanResult[5]
        totalCarbohydrates = mealPlanResult[6]
        totalFat = mealPlanResult[7]

    # CreateMealPlan(1, "202s3-10-12 23:05:00", "2023-10-13 23:10:00", 6, 2)
    # CreateMeal(1, 2, 34)
    # CreatePlanNutrition(1, 3000, 300, 160, 100)

    # DeleteMealPlan(3)

    def update_meal(self, planID: int, mealNum: int, recipeID: int, calories: int, carbohydrates: int, protein: int, fat: int):
        if(planID == None or mealNum == None or recipeID == None):
            return
        self.execute_query("UPDATE meal SET recipeID=%s WHERE planID=%s AND mealNum=%s", (recipeID, planID, mealNum))
        self.execute_query("UPDATE totalPlanNutrition SET calories=%s, carbohydrates=%s, protein=%s, fat=%s WHERE planID=%s",
                    (calories, carbohydrates, protein, fat, planID))
        
    def fetch_meal_plan(self, planID: int):
        data = {
            "mealPlan": [],
            "meal": [],
            "totalPlanNutrition": []
        }

        self.execute_query("SELECT userID, startDate, endDate, totalMeals, mealsPerDay FROM mealPlan WHERE planID=%s", (planID,))
        mealPlanResult = cursor.fetchone()
        userID = mealPlanResult[0]
        startDate = mealPlanResult[1]
        endDate = mealPlanResult[2]
        totalMeals = mealPlanResult[3]
        mealsPerDay = mealPlanResult[4]

        data["mealPlan"].append({"planID": planID, "userID": userID, "startDate":f"{startDate}", "endDate": f"{endDate}",
        "totalMeals": totalMeals, "mealsPerDay": mealsPerDay})
        
        self.execute_query("SELECT mealNum, recipeID FROM meal WHERE planID=%s", (planID,))
        meals = cursor.fetchall()
        
        
        for meal in meals:
            mealNum = meal[0]
            recipeID = meal[1]
            data["meal"].append({f"meal{mealNum}": {"recipeID": recipeID}})

        self.execute_query("SELECT calories, carbohydrates, protein, fat FROM totalPlanNutrition WHERE planID=%s", (planID,))
        totalPlanNutritionResult = cursor.fetchone()
        calories = totalPlanNutritionResult[0]
        carbohydrates = totalPlanNutritionResult[1]
        protein = totalPlanNutritionResult[2]
        fat = totalPlanNutritionResult[3]
        data["totalPlanNutrition"].append({"planID": planID, "calories": calories, "carbohydrates": carbohydrates, "protein": protein, "fat": fat})

        return data



    # UpdateMeal(1, 1, 3678, 3000, 280, 180, 100)

    # FetchMealPlan(1)
