# Mealplan-service

## Running the service

Make a `.env` file in the root directory and create a variable write the following:
```python
DB_CONN="mysql+mysqlconnector://<YOUR_SQLALCHEMY_STRING>"
```
the mysql prefix is only if youre using a mysql server, else look up different sqlalchemy supported sql databases

### Running in docker

Creating docker container and running the app:
```sh
docker build -t mealplanservice .
docker run -p 8443:8443 recipeservice
```

### Development

run this in powershell:

```sh
python -m venv .venv
.venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
```

on macOS/Linux you might need to do `source .venv\Scripts\activate` and `.venv/Scripts/activate.bat` in windows CMD

#### Start Micro Service
```sh
uvicorn app.server:app --reload
```

#### Test
```sh
pytest tests
```
