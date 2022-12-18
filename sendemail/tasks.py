from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime
from django.utils import timezone
from django.db.models.functions import ExtractDay
from panel.mail_handler import send_invitation_email, send_reminder
from pdf.models import Participant, EmailSentToParticipant


@shared_task(name='send_participant_reminder')
def participant_reminder():
    participants = Participant.objects.filter(invitation_sent=True, started_at=None)
    for participant in participants:
        now_aware = timezone.now()
        email_sent_to_participant = EmailSentToParticipant.objects.filter(participant=participant).latest('created_at')
        delta = now_aware - email_sent_to_participant.created_at
        if delta.days >= 7:
            data = {
                'participant_id': participant.id,
                'type': 'reminder',
            }
            send_reminder(data)
            print(f'{participant.employee.name} delta - {delta.days}')


        # return total

