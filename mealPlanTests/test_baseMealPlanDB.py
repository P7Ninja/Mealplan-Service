import pytest
import shutil
from pytest import FixtureRequest
from pathlib import Path

from recipeservice import SQLRecipeDB
from recipeservice.database.schema import BaseRecipe, Ingredient, Energy

@pytest.fixture
def db(request: FixtureRequest, tmp_path: Path):
    db_path = tmp_path / "db"
    db_path.mkdir()
    db_file = db_path / "db.sql"
    shutil.copyfile("./tests/test.db", db_file)
    db = SQLRecipeDB({"DB_CONN": f"sqlite:///{db_file}"})
    db.startup()
    def tearddown():
        db.shutdown()

    request.addfinalizer(tearddown)
    return db