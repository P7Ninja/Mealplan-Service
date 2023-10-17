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
    

# {
    # CalorieTarget: int
    # proteinTarget: int
    # carbTarget: int
    # fatTarget: int
    # foodList: [name, name,..., name]
    # mealTypes: [morgenmad, snack, frokost, aften, snack]
    # mealsPerDay: [2, 3]
# }
