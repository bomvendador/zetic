#!/usr/bin/env bash



celery -A reports beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach
celery -A reports worker -l info --logfile=celery.log --detach


python manage.py runserver 0.0.0.0:8000

