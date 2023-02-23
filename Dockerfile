FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=5s \
            --timeout=3s \
            --start-period=30s \
            --retries=3 \
            CMD curl -f http://localhost:8000/ || exit 1

#RUN apt update \
#    && apt install -y libmysqlclient-dev gcc python3-dev musl-dev
RUN apt-get -y install default-libmysqlclient-dev gcc

WORKDIR /reports
COPY requirements.txt /reports/reqs-min.txt
RUN pip install --no-cache-dir -r /reports/reqs-min.txt

COPY . /reports/

RUN python manage.py collectstatic --noinput

CMD ["./entrypoint.sh"]

