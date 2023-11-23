import pytest
from pytest import FixtureRequest
from unittest.mock import call


from mealplanservice.database import SQLMealPlanDB
from mealplanservice.database.schema import BaseMealPlan, mealPlanRecipe, mealsPerDay, mealplan

@pytest.fixture
def db(request: FixtureRequest):
    db = SQLMealPlanDB({'HOST': 'krishusdata.mysql.database.azure.com', 'USER': 'kmg', 'PASSWORD': ']q#GSgNHw}Ynb?9', 'DATABASE': 'mealplanservicetest'})
    db.startup()
    def tearddown():
        db.shutdown()  
    request.addfinalizer(tearddown)
    return db

@pytest.fixture
def mock_mysql_connection(mocker):
    return mocker.patch("mysql.connector.connect")

@pytest.fixture
def mock_database(mock_mysql_connection, request: FixtureRequest):
    mock_database = SQLMealPlanDB({"HOST": "mock_host", "USER": "mock_user", "PASSWORD": "mock_password", "DATABASE": "mock_database"})
    mock_database.startup()
    mock_database.connection = mock_mysql_connection.return_value
    def tearddown():
        mock_database.shutdown()  
    request.addfinalizer(tearddown)
    return mock_database

def test_db_get_current_mealplan(mock_database):
    userID = 1
    mock_database.get_current_meal_plan(userID)
    mock_database.connection.cursor.return_value.execute.assert_has_calls([
        call("""
            SELECT mp.*, mpr.recipeID, mpd.meals
            FROM mealPlan mp
            LEFT JOIN mealplanrecipes mpr ON mp.planID = mpr.planID
            LEFT JOIN mealsperday mpd ON mp.planID = mpd.planID
            WHERE mp.userID=%s
            ORDER BY mp.planID DESC
        """, (1,))
    ])
    
def test_db_get_all_mealplan(mock_database):
    userID = 1
    mock_database.get_all_meal_plans(userID)
    mock_database.connection.cursor.return_value.execute.assert_has_calls([
        call("SELECT * FROM mealPlan WHERE userID=%s ORDER BY planID DESC", (userID,))
    ])

def test_db_create_mealplan_success(mock_database):
    new_mealplan = mealplan(
        id=0,
        userID=1,
        startDate="2023-11-21",
        endDate="2023-11-22"
    )   
    mock_database.create_meal_plan(new_mealplan)
    parameters = (0, new_mealplan.userID, new_mealplan.startDate, new_mealplan.endDate)
    mock_database.connection.cursor.return_value.execute.assert_has_calls([
        call("INSERT INTO mealPlan VALUES(%s, %s, %s, %s)", parameters)
    ])

def test_db_create_meal_recipe(mock_database):
    new_recipe = mealPlanRecipe(
        planID=12,
        recipeID=100
    )
    mock_database.create_meal_recipe(new_recipe)
    mock_database.connection.cursor.return_value.execute.assert_has_calls([
        call("INSERT INTO mealPlanRecipes VALUES(0, %s, %s)", (new_recipe.planID, new_recipe.recipeID))
    ])

def test_db_create_meals_per_day(mock_database):
    new_meals_per_day = mealsPerDay(
        planID=12,
        meals=1,
        totalCalories=3000,
        totalProtein=200,
        totalCarbohydrates=300,
        totalFat=60
    )
    mock_database.create_meals_per_day(new_meals_per_day)
    parameters = (0, new_meals_per_day.planID, new_meals_per_day.meals, new_meals_per_day.totalCalories, new_meals_per_day.totalProtein,
                      new_meals_per_day.totalCarbohydrates, new_meals_per_day.totalFat)
    mock_database.connection.cursor.return_value.execute.assert_has_calls([
        call("INSERT INTO mealsPerDay VALUES(%s, %s, %s, %s, %s, %s, %s)", parameters)
    ])

def test_db_delete_mealplan(mock_database):
    mock_database.delete_meal_plan(1, 12)
    mock_database.connection.cursor.return_value.execute.assert_has_calls([
        call("DELETE FROM mealPlan WHERE userID=%s AND planID=%s", (1, 12))
    ])
