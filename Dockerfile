FROM python:3.10

WORKDIR /application

COPY requirements.txt /application/

RUN pip install --no-cache-dir -r requirements.txt

COPY /src/mealplanservice /application/mealplanservice
COPY /app/server.py /application/server.py
COPY /.env /application/.env

EXPOSE 8755

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8755", "--root-path", "/mealplanservice"]