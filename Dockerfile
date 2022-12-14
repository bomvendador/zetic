FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update \
    && apt install -y postgresql gcc python3-dev musl-dev


WORKDIR /reports
COPY requirements.txt /reports/requirements.txt
RUN apt-get update -y &&  \
    apt-get -y install libpq-dev gcc && \
    pip install --no-cache-dir -r /reports/requirements.txt

COPY . /reports/

