#!/usr/bin/env bash



docker build \
        --tag zetic/zetic-panel:2.1.0 \
        --platform linux/amd64 \
        --file Dockerfile .

docker save zetic/zetic-panel:2.1.0 | gzip > zetic-panel.tar.gz

scp zetic-panel.tar.gz node2.zetic.ru:~/


####
docker load < zetic-panel.tar.gz
docker stop zetic-panel && docker rm zetic-panel

celery -A reports beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach && \
celery -A reports worker -l info --logfile=celery.log --detach && \

docker run --name zetic-panel \
        -e DB_USER="zetic" \
        -e DB_PASSWORD="iegh5vieRah7joJ7ohng" \
        -e DB_HOST="zetic-mysql" \
        -e DB_NAME="zetic" \
        -e DB_PORT="3306" \
        -e CELERY_HOST="redis://zetic-redis:6379" \
        --link zetic-mysql:zetic-mysql \
        --link zetic-redis:zetic-redis \
        -p 8000:8000 \
        -d zetic/zetic-panel:2.1.0 \
        python manage.py runserver 0.0.0.0:8000
