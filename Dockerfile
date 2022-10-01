FROM python:3-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

ENV SERVER_PORT=8000

EXPOSE ${SERVER_PORT}

ENTRYPOINT python manage.py runserver 0.0.0.0:${SERVER_PORT}
