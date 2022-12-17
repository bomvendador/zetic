from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime
from django.utils import timezone
from django.db.models.functions import ExtractDay
from panel.mail_handler import send_invitation_email, send_reminder
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
        now_aware = timezone.now()
        delta = now_aware - participant.invitation_sent_datetime
        if delta >= 7:
            data = {
                'participant_id': participant.id,
                'type': 'reminder',
            }
            send_reminder(data)

            print(f'{participant.employee.name} delta - {delta.days}')
        # return total

