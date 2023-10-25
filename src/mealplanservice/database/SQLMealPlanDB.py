from fastapi import FastAPI
import json
import mysql.connector

from mealplanservice.database import schema
from .BaseMealPlanDB import BaseMealPlanDB
from pprint import pprint

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
        self.__cursor = self.__database.cursor(buffered=True)

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
        self.execute_query("SELECT * FROM mealPlan WHERE userID=%s ORDER BY planID ASC", (userID,))
        meal_plan_result   = self.__cursor.fetchone()
        planID             = meal_plan_result[0]
        userID             = meal_plan_result[1]
        startDate          = meal_plan_result[2]
        endDate            = meal_plan_result[3]
        totalCalories      = meal_plan_result[4]
        totalProtein       = meal_plan_result[5]
        totalCarbohydrates = meal_plan_result[6]
        totalFat           = meal_plan_result[7]

        self.execute_query("SELECT id, recipeID FROM mealplanrecipes WHERE planID=%s ORDER BY id ASC", (planID,))
        meal_plan_recipes_result = self.__cursor.fetchall()
        recipe_id_list = []
        for row in meal_plan_recipes_result:
            recipe_id_list.append(row[1])

        self.execute_query("SELECT id, meals FROM mealsperday WHERE planID=%s ORDER BY id ASC", (planID,))
        meals_per_day_result = self.__cursor.fetchall()
        meals_per_day_list = []
        for row in meals_per_day_result:
            print(row)
            meals_per_day_list.append(row[1])

        mealplan_json = {
            "planID": planID,
            "userID": userID,
            "startDate": str(startDate),
            "endDate": str(endDate),
            "totalCalories": totalCalories,
            "totalProtein": totalProtein,
            "totalCarbohydrates": totalCarbohydrates,
            "totalFat": totalFat
        }

        latest_recipe_index = 0
        for day in range(0, len(meals_per_day_list)):
            mealplan_json[f"day{day+1}"] = {}
            for meal in range(meals_per_day_list[day]):
                mealplan_json[f"day{day+1}"][f"meal{meal+1}"] = {
                    "recipeID": recipe_id_list[latest_recipe_index + meal]
                }
            latest_recipe_index += meal + 1


        mealplan_json_str = json.dumps(mealplan_json, indent=4)

        with open('src/mealplanservice/database/visualisering.json', 'w') as f:
            f.write(mealplan_json_str)
        return mealplan_json_str
    
    def get_all_mealplans(self, userID: int):
        self.execute_query("SELECT * FROM mealPlan WHERE userID=%s ORDER BY planID ASC", (userID,))
        meal_plan_result1   = self.__cursor.fetchall()
        plan_num = 1
        mealplan_json = {}
        for meal_plan_result in meal_plan_result1:
            planID             = meal_plan_result[0]
            userID             = meal_plan_result[1]
            startDate          = meal_plan_result[2]
            endDate            = meal_plan_result[3]
            totalCalories      = meal_plan_result[4]
            totalProtein       = meal_plan_result[5]
            totalCarbohydrates = meal_plan_result[6]
            totalFat           = meal_plan_result[7]

            self.execute_query("SELECT id, recipeID FROM mealplanrecipes WHERE planID=%s ORDER BY id ASC", (planID,))
            meal_plan_recipes_result = self.__cursor.fetchall()
            recipe_id_list = []
            for row in meal_plan_recipes_result:
                recipe_id_list.append(row[1])

            self.execute_query("SELECT id, meals FROM mealsperday WHERE planID=%s ORDER BY id ASC", (planID,))
            meals_per_day_result = self.__cursor.fetchall()
            meals_per_day_list = []
            for row in meals_per_day_result:
                print(row)
                meals_per_day_list.append(row[1])
        
            mealplan_json[f"plan{plan_num}"] = {
                "planID": planID,
                "userID": userID,
                "startDate": str(startDate),
                "endDate": str(endDate),
                "totalCalories": totalCalories,
                "totalProtein": totalProtein,
                "totalCarbohydrates": totalCarbohydrates,
                "totalFat": totalFat
                }
                

            latest_recipe_index = 0
            for day in range(0, len(meals_per_day_list)):
                mealplan_json[f"plan{plan_num}"][f"day{day+1}"] = {}
                for meal in range(meals_per_day_list[day]):
                    mealplan_json[f"plan{plan_num}"][f"day{day+1}"][f"meal{meal+1}"] = {
                        "recipeID": recipe_id_list[latest_recipe_index + meal]
                    }
                latest_recipe_index += meal + 1
            plan_num += 1
        
        
        mealplan_json_str = json.dumps(mealplan_json, indent=5)
        with open('src/mealplanservice/database/visualisering.json', 'w') as f:
            f.write(mealplan_json_str)
        return mealplan_json_str
        
    # def update_meal(self, planID: int, mealNum: int, recipeID: int, calories: int, carbohydrates: int, protein: int, fat: int):
    #     if(planID == None or mealNum == None or recipeID == None):
    #         return
    #     self.execute_query("UPDATE meal SET recipeID=%s WHERE planID=%s AND mealNum=%s", (recipeID, planID, mealNum))
    #     self.execute_query("UPDATE totalPlanNutrition SET calories=%s, carbohydrates=%s, protein=%s, fat=%s WHERE planID=%s",
    #                 (calories, carbohydrates, protein, fat, planID))
        
