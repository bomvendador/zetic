from __future__ import absolute_import, unicode_literals
import os
from celery import Celery as CeleryReports
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reports.settings')

app = CeleryReports('reports')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))



# app.conf.beat_schedule = {
#     # Execute the Speed Test every 10 minutes
#     'network-speedtest-10min': {
#         'task': 'print_msg_main',
#         'schedule': crontab(minute='*/2'),
#         'args': ("Hello",)
#     },
# }
# app.conf.beat_schedule = {
#     # Scheduler Name
#     'print-message-ten-seconds': {
#         # Task Name (Name Specified in Decorator)
#         'task': 'print_msg_main',
#         # Schedule
#         'schedule': 10.0,
#         # Function Arguments
#         'args': ("Hello",)
#     },
#     # Scheduler Name
#     'print-time-twenty-seconds': {
#         # Task Name (Name Specified in Decorator)
#         'task': 'print_time',
#         # Schedule
#         'schedule': 20.0,
#     },
#     # Scheduler Name
#     'calculate-forty-seconds': {
#         # Task Name (Name Specified in Decorator)
#         'task': 'get_calculation',
#         # Schedule
#         'schedule': 40.0,
#         # Function Arguments
#         'args': (10, 20)
#     },
# }