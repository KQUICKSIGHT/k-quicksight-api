
# syntax=docker/dockerfile:1
FROM python:3.10.6-slim-buster

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "manage.py", "runserver  --settings=k_qicksight_app.settings", "0.0.0.0:8000", "--noreload"]