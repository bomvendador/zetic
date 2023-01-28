#!/usr/bin/env bash

#region Configuration
DOCKER_IMAGE=zetic/questionnaire-webapp
DOCKER_TAG=$1 #$(git symbolic-ref --short HEAD)
#endregion
HOST=node2.zetic.ru
FILE=zetic-panel.tar.gz

docker build \
        --tag ${DOCKER_IMAGE}:${DOCKER_TAG} \
        --platform linux/amd64 \
        --file Dockerfile .

docker save ${DOCKER_IMAGE}:${DOCKER_TAG} | gzip > $FILE

scp ${FILE} ${HOST}:~/
rm ${FILE}

ssh ${HOST} "docker load < $FILE"
ssh ${HOST} "rm $FILE"

exit 0

####
docker load < zetic-panel.tar.gz

/usr/local/bin/celery -A reports beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach;
/usr/local/bin/celery -A reports worker -l info --logfile=celery.log --detach;


docker stop zetic-panel && docker rm zetic-panel
docker run --name zetic-panel \
        -e DB_USER="zetic" \
        -e DB_PASSWORD="iegh5vieRah7joJ7ohng" \
        -e DB_HOST="zetic-mysql" \
        -e DB_NAME="zetic" \
        -e DB_PORT="3306" \
        -e CELERY_HOST="redis://zetic-redis:6379" \
        --link zetic-mysql:zetic-mysql \
        --link zetic-redis:zetic-redis \
        --health-cmd="curl --fail http://localhost:8000/ || exit 1" \
        --health-interval=2s \
        --health-timeout=1s \
        --health-retries=3 \
        -p 8000:8000 \
        -d zetic/questionnaire-webapp:v2.1.3 \
        /bin/bash -c "
        /usr/local/bin/celery -A reports beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach;
        /usr/local/bin/celery -A reports worker -l info --logfile=celery.log --detach;
        /usr/local/bin/python manage.py runserver 0.0.0.0:8000
        "
