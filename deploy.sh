#!/usr/bin/env bash

#region Configuration
DOCKER_IMAGE=zetic/zetic-panel
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

echo "Load image"
ssh ${HOST} "docker load < $FILE"
ssh ${HOST} "rm $FILE"

echo "Restart panel"
ssh ${HOST} "./panel-start.sh ${DOCKER_TAG}"

echo "Prune images"
ssh ${HOST} -C "docker image prune -a -f"
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
        -v /var/lib/zetic/panel/media/reportsPDF:/reports/media/reportsPDF \
        -p 8000:8000 \
        -d zetic/zetic-panel:v2.2.0

sudo rm -rf /var/lib/zetic/panel/static/*
sudo docker cp zetic-panel:/reports/static_root/. /var/lib/zetic/panel/static/
