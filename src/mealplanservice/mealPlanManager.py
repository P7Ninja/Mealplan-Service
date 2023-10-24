import requests

# Get inventory items from Inventory Service
# Get Recipe from inventory ingredients from recipe service
# Get discounts from food service
# Get foods from food service
# return to request

def getFoodInventory(userid: int):
    url = "api/inventory/user?userid=%d", (userid)
    inventoryList = requests.get(url)

    url = f"api/food/"
    foodList = requests.post(url, json=inventoryList)
    return foodList


def getRecipeFromInventory(userid: int, calorieTarget: int, proteinTarget: int, carbTarget: int, fatTarget: int, mealTypes: list, mealsPerDay: list):
    food = getFoodInventory(userid)
    
    url = f"api/recipe/"
    recipe = requests.post(url, calorieTarget, proteinTarget, carbTarget, fatTarget, food, mealTypes, mealsPerDay)
    

def splitCaloriesAndMacros(userData[0]):
    if proteinTarget not defined:
        proteinTarget = (targetCalories*0.25)/4
        carbTarget = (targetCalories*0.60)/4
        fatTarget = (targetCalories*0.15)/8

    breakfastTarget = [calorieTarget*0.2, proteinTarget*0.2, carbTarget*0.2, fatTarget*0.2]
    lunchTarget = [calorieTarget*0.3, proteinTarget*0.3, carbTarget*0.3, fatTarget*0.3]
    dinnerTarget = [calorieTarget*0.5, proteinTarget*0.5, carbTarget*0.5, fatTarget*0.5]
    



# {
    # breakfastTarget.CalorieTarget: int
    # proteinTarget: int
    # carbTarget: int
    # fatTarget: int
    # targetList: [calorieTarget: int]
    # foodList: [name, name,..., name]
    # mealTypes: [morgenmad, snack, frokost, aften, snack]
    # mealsPerDay: [2, 3]
# }

# targetCalories = 3000
# proteinTarget = (targetCalories*0.25)/4 =
# carbTarget = (targetCalories*0.60)/4
# fatTarget = (targetCalories*0.15)/8
