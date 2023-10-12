from fastapi import FastAPI
import json
import mysql.connector
from pprint import pprint

app = FastAPI()

database = mysql.connector.connect(
    host='krishusdata.mysql.database.azure.com',
    user='kmg',
    password='krissupersecretpassword0!',
    database='MealPlanService',
)

cursor = database.cursor()
cursor = database.cursor(buffered=True)

def ExecuteQuery(query, parameters):
    cursor.execute(query, parameters)
    database.commit()

@app.post("/createMealPlan/")
def CreateMealPlan(userID, startDate, endDate, totalMeals, mealsPerDay):
    if(userID != None and startDate != None and endDate != None and totalMeals != None and mealsPerDay != None):
        ExecuteQuery("INSERT INTO mealPlan VALUES(0, %s, %s, %s, %s, %s)", (userID, startDate, endDate, totalMeals, mealsPerDay))

@app.post("/createMeal/")
def CreateMeal(planID, mealNum, recipeID):
    if(planID != None and mealNum != None and recipeID != None):
        ExecuteQuery("INSERT INTO meal VALUES(%s, %s, %s)", (planID, mealNum, recipeID))

@app.post("/createPlanNutrition/")
def CreatePlanNutrition(planID, calories, carbohydrates, protein, fat):
    if(planID != None and calories != None and carbohydrates != None and protein != None and fat != None):
        ExecuteQuery("INSERT INTO totalPlanNutrition VALUES(%s, %s, %s, %s, %s)", (planID, calories, carbohydrates, protein, fat))

@app.post("/deleteMealPlan/")
def DeleteMealPlan(planID):
    if(planID == None):
        return
    ExecuteQuery("DELETE FROM mealPlan WHERE planID=%s", (planID,))


# CreateMealPlan(1, "202s3-10-12 23:05:00", "2023-10-13 23:10:00", 6, 2)
# CreateMeal(1, 2, 34)
# CreatePlanNutrition(1, 3000, 300, 160, 100)

# DeleteMealPlan(3)

@app.post("/updateMealPlan/")
def UpdateMeal(planID, mealNum, recipeID, calories, carbohydrates, protein, fat):
    if(planID == None or mealNum == None or recipeID == None):
        return
    ExecuteQuery("UPDATE meal SET recipeID=%s WHERE planID=%s AND mealNum=%s", (recipeID, planID, mealNum))
    ExecuteQuery("UPDATE totalPlanNutrition SET calories=%s, carbohydrates=%s, protein=%s, fat=%s WHERE planID=%s",
                 (calories, carbohydrates, protein, fat, planID))
    
def FetchMealPlan(planID):
    data = {
        "mealPlan": [],
        "meal": [],
        "totalPlanNutrition": []
    }

    ExecuteQuery("SELECT userID, startDate, endDate, totalMeals, mealsPerDay FROM mealPlan WHERE planID=%s", (planID,))
    mealPlanResult = cursor.fetchone()
    userID = mealPlanResult[0]
    startDate = mealPlanResult[1]
    endDate = mealPlanResult[2]
    totalMeals = mealPlanResult[3]
    mealsPerDay = mealPlanResult[4]

    data["mealPlan"].append({"planID": planID, "userID": userID, "startDate":f"{startDate}", "endDate": f"{endDate}",
     "totalMeals": totalMeals, "mealsPerDay": mealsPerDay})
    
    ExecuteQuery("SELECT mealNum, recipeID FROM meal WHERE planID=%s", (planID,))
    meals = cursor.fetchall()
    
    
    for meal in meals:
        mealNum = meal[0]
        recipeID = meal[1]
        data["meal"].append({f"meal{mealNum}": {"recipeID": recipeID}})

    ExecuteQuery("SELECT calories, carbohydrates, protein, fat FROM totalPlanNutrition WHERE planID=%s", (planID,))
    totalPlanNutritionResult = cursor.fetchone()
    calories = totalPlanNutritionResult[0]
    carbohydrates = totalPlanNutritionResult[1]
    protein = totalPlanNutritionResult[2]
    fat = totalPlanNutritionResult[3]
    data["totalPlanNutrition"].append({"planID": planID, "calories": calories, "carbohydrates": carbohydrates, "protein": protein, "fat": fat})

    return data

# UpdateMeal(1, 1, 3678, 3000, 280, 180, 100)

# FetchMealPlan(1)


@app.get("/getHealth/")
def GetUsersLatestHealthEntry(userID):
    
    data = {
        "height": [],
        "weight": [],
        "fatPercentage": [],
        "musclePercentage": [],
        "waterPercentage": []
    }
    
    print("SELECT dateStamp, height FROM heightLog WHERE userID=%s ORDER BY id DESC LIMIT 0, 1", "sadasd")

    cursor.execute("SELECT dateStamp, height FROM heightLog WHERE userID=%s ORDER BY id DESC LIMIT 0, 1", (userID,))
    heightResult = cursor.fetchone()
    dateStamp = heightResult[0]
    height = heightResult[1]
    data["height"].append({"dateStamp": dateStamp, "height": height})

    # WEIGHT
    cursor.execute("SELECT dateStamp, weight FROM weightLog WHERE userID=%s ORDER BY id DESC LIMIT 0, 1", (userID,))
    weightResult = cursor.fetchone()
    dateStamp = weightResult[0]
    weight = weightResult[1]
    data["weight"].append({"dateStamp": dateStamp, "weight": weight})

    # FAT
    cursor.execute("SELECT dateStamp, fatPercentage FROM fatPercentageLog WHERE userID=%s ORDER BY id DESC LIMIT 0, 1", (userID,))
    fatPercentageResult = cursor.fetchone()
    dateStamp = fatPercentageResult[0]
    fatPercentage = fatPercentageResult[1]
    data["fatPercentage"].append({"dateStamp": dateStamp, "fatPercentage": fatPercentage})
    
    # MUSCLE
    cursor.execute("SELECT dateStamp, musclePercentage FROM musclePercentageLog WHERE userID=%s ORDER BY id DESC LIMIT 0, 1", (userID,))
    musclePercentageResult = cursor.fetchone()
    dateStamp = musclePercentageResult[0]
    musclePercentage = musclePercentageResult[1]
    data["musclePercentage"].append({"dateStamp": dateStamp, "musclePercentage": musclePercentage})
    
    # WATER
    cursor.execute("SELECT dateStamp, waterPercentage FROM waterPercentageLog WHERE userID=%s ORDER BY id DESC LIMIT 0, 1", (userID,))
    waterPercentageResult = cursor.fetchone()
    dateStamp = waterPercentageResult[0]
    waterPercentage = waterPercentageResult[1]
    data["waterPercentage"].append({"dateStamp": dateStamp, "waterPercentage": waterPercentage})
    
    return data