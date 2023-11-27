import mysql.connector
from mealplanservice.database import schema
from .BaseMealPlanDB import BaseMealPlanDB
from fastapi import HTTPException, status

class SQLMealPlanDB(BaseMealPlanDB):
    def __init__(self, cfg: dict) -> None:
        super().__init__(cfg)
        self.__database = None
        self.__cursor = None

    def startup(self):
        try:
            self.__database = mysql.connector.connect(
                host=self.cfg["HOST"],
                user=self.cfg["USER"],
                password=self.cfg["PASSWORD"],
                database=self.cfg["DATABASE"]
            )
            self.__cursor = self.__database.cursor(dictionary=True, buffered=True)
            self.__cursor = self.__database.cursor(buffered=True)
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to connect to the database: {err}"
            )

    def execute_query(self, query, parameters):
        self.__cursor = self.__database.cursor(dictionary=True, buffered=True)
        self.__cursor = self.__database.cursor(buffered=True)
        try:
            self.__cursor.execute(query, parameters)
            self.__database.commit()
        except mysql.connector.Error:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Problems while executing query: {query}")
        
    def create_meal_plan(self, baseMealPlan: schema.BaseMealPlan):  
        parameters = (0, baseMealPlan.userID, baseMealPlan.startDate, baseMealPlan.endDate)
        self.execute_query("INSERT INTO mealPlan VALUES(%s, %s, %s, %s)", parameters)
        self.__cursor.close()
        return self.__cursor.lastrowid

    def create_meal_recipe(self, mealPlanRecipe: schema.MealPlanRecipe):
        self.execute_query("INSERT INTO mealPlanRecipes VALUES(0, %s, %s)", (mealPlanRecipe.planID, mealPlanRecipe.recipeID))
        self.__cursor.close()
        return "Success"

    def create_meals_per_day(self, mealsPerDay: schema.MealsPerDay):
        parameters = (0, mealsPerDay.planID, mealsPerDay.meals, mealsPerDay.totalCalories, mealsPerDay.totalProtein,
                      mealsPerDay.totalCarbohydrates, mealsPerDay.totalFat)
        self.execute_query("INSERT INTO mealsPerDay VALUES(%s, %s, %s, %s, %s, %s, %s)", parameters)
        self.__cursor.close()
        return "Success"

    def delete_meal_plan(self, userID: int, planID: int):
        if(userID == None or planID == None):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No plan with id {planID} to delete")
        print("deleting:", userID, planID)
        self.execute_query("DELETE FROM mealPlan WHERE userID=%s AND planID=%s", (userID, planID))
        self.__cursor.close()
        return "Success"

    def get_current_meal_plan(self, userID: int):
        self.execute_query("SELECT planID, startDate, endDate FROM mealPlan WHERE userID=%s ORDER BY planID DESC", (userID,))
        meal_plan_results = self.__cursor.fetchone()
        planID = meal_plan_results[0]

        self.execute_query("SELECT id, recipeID FROM mealplanrecipes WHERE planID=%s ORDER BY id ASC", (planID,))
        meal_plan_recipes_result = self.__cursor.fetchall()
        recipe_id_list = []
        for row in meal_plan_recipes_result:
            recipe_id_list.append(row[1])

        self.execute_query("SELECT * FROM mealsperday WHERE planID=%s ORDER BY id ASC", (planID,))
        meals_per_day_result = self.__cursor.fetchall()
        meals_per_day_list = []
        for row in meals_per_day_result:
            meals_per_day_list.append(row[2])

        if not meal_plan_results:
            return None

        mealplan_json = {
            "planID": meal_plan_results[0],
            "startDate": meal_plan_results[1],
            "endDate": meal_plan_results[2],
            "days": []
        }
            
        current_recipe_index = 0
        for day, meals_per_day in enumerate(meals_per_day_list):
            mealplan_json["days"].append(
                {
                    "totalCalories": meals_per_day_result[day][3],
                    "totalProtein": meals_per_day_result[day][4],
                    "totalCarbohydrates": meals_per_day_result[day][5],
                    "totalFat": meals_per_day_result[day][6],
                    "recipes": [recipe_id_list[current_recipe_index + meal] for meal in range(meals_per_day)]
                }
            )
            current_recipe_index += meals_per_day

        self.__cursor.close()
        return mealplan_json
    
    def get_all_meal_plans(self, userID: int):
        self.execute_query("SELECT planID, startDate, endDate FROM mealPlan WHERE userID=%s ORDER BY planID ASC", (userID,))
        meal_plan_results = self.__cursor.fetchall()

        mealplan_json = {}
        for meal_plan_result in meal_plan_results:
            planID = meal_plan_result[0]

            self.execute_query("SELECT id, recipeID FROM mealplanrecipes WHERE planID=%s ORDER BY id ASC", (planID,))
            meal_plan_recipes_result = self.__cursor.fetchall()
            recipe_id_list = []
            for row in meal_plan_recipes_result:
                recipe_id_list.append(row[1])

            self.execute_query("SELECT * FROM mealsperday WHERE planID=%s ORDER BY id ASC", (planID,))
            meals_per_day_result = self.__cursor.fetchall()
            meals_per_day_list = []
            for row in meals_per_day_result:
                meals_per_day_list.append(row[2])

            if not meal_plan_result:
                return None

            mealplan_json[f"plan{planID}"] = {
                "planID": meal_plan_result[0],
                "startDate": meal_plan_result[1],
                "endDate": meal_plan_result[2],
                "days": []
            }
                
            current_recipe_index = 0
            for day, meals_per_day in enumerate(meals_per_day_list):
                mealplan_json[f"plan{planID}"]["days"].append(
                    {
                        "totalCalories": meals_per_day_result[day][3],
                        "totalProtein": meals_per_day_result[day][4],
                        "totalCarbohydrates": meals_per_day_result[day][5],
                        "totalFat": meals_per_day_result[day][6],
                        "recipes": [recipe_id_list[current_recipe_index + meal] for meal in range(meals_per_day)]
                    }
                )
                current_recipe_index += meals_per_day

        self.__cursor.close()
        return mealplan_json

