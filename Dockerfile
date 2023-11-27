FROM python:3.10-alpine

WORKDIR /application

COPY requirements.txt /application/

RUN pip install --no-cache-dir -r requirements.txt

COPY /src/mealplanservice /application/mealplanservice
COPY /app/server.py /application/server.py
COPY /.env /application/.env


CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7004", "--root-path", "/mealplanservice"]