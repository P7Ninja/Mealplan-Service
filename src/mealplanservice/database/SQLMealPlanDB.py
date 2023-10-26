from fastapi import FastAPI
import mysql.connector
from mealplanservice.database import schema
from .BaseMealPlanDB import BaseMealPlanDB

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
        self.execute_query("SELECT * FROM mealPlan WHERE userID=%s ORDER BY planID DESC", (userID,))
        meal_plan_result   = self.__cursor.fetchone()
        planID             = meal_plan_result[0]
        userID             = meal_plan_result[1]
        startDate          = meal_plan_result[2]
        endDate            = meal_plan_result[3]
        totalCalories      = meal_plan_result[4]
        totalProtein       = meal_plan_result[5]
        totalCarbohydrates = meal_plan_result[6]
        totalFat           = meal_plan_result[7]

        self.execute_query("SELECT id, recipeID FROM mealplanrecipes WHERE planID=%s ORDER BY id DESC", (planID,))
        meal_plan_recipes_result = self.__cursor.fetchall()
        recipe_id_list = []
        for row in meal_plan_recipes_result:
            recipe_id_list.append(row[1])

        self.execute_query("SELECT id, meals FROM mealsperday WHERE planID=%s ORDER BY id DESC", (planID,))
        meals_per_day_result = self.__cursor.fetchall()
        meals_per_day_list = []
        for row in meals_per_day_result:
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

        return mealplan_json
    
    def get_all_meal_plans(self, userID: int):
        self.execute_query("SELECT * FROM mealPlan WHERE userID=%s ORDER BY planID DESC", (userID,))
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

            self.execute_query("SELECT id, recipeID FROM mealplanrecipes WHERE planID=%s ORDER BY id DESC", (planID,))
            meal_plan_recipes_result = self.__cursor.fetchall()
            recipe_id_list = []
            for row in meal_plan_recipes_result:
                recipe_id_list.append(row[1])

            self.execute_query("SELECT id, meals FROM mealsperday WHERE planID=%s ORDER BY id DESC", (planID,))
            meals_per_day_result = self.__cursor.fetchall()
            meals_per_day_list = []
            for row in meals_per_day_result:
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
        
        return mealplan_json

