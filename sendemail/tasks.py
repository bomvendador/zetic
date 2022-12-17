from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime
from panel import mail_handler
from pdf.models import Participant

@shared_task(name="print_msg_main")
def print_message(message, *args, **kwargs):
    print(f"Celery is working!! Message is {message}")


@shared_task(name="print_time")
def print_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Current Time is {current_time}")


@shared_task(name='get_calculation')
def calculate(val1, val2):
    total = val1 + val2
    return total


@shared_task(name='send_participant_reminder')
def participant_reminder():
    participants = Participant.objects.filter(invitation_sent=True, started_at=None)
    for participant in participants:
        delta = datetime.now() - participant.invitation_sent_datetime
        print(f'{participant.employee.name} delta - {delta}')
        # return total

