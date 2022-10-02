FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update &&  \
    apt-get -y install libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt

COPY . /code/

ENV SERVER_PORT=8000

ENTRYPOINT python manage.py runserver 0.0.0.0:${SERVER_PORT}
