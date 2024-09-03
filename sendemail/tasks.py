from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from celery import shared_task
from datetime import datetime
from django.utils import timezone
from django.db.models.functions import ExtractDay
from panel.mail_handler import send_invitation_email, send_reminder, send_month_report
from pdf.models import Participant, EmailSentToParticipant, Company
from calendar import monthrange, isleap


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


@shared_task(name='send_monthly_report')
def monthly_report():
    companies = Company.objects.all()
    now_aware = timezone.now()
    today = datetime.today()
    print(f'y - {today.year} m - {today.month} d - {today.day}')
    month_days_qnt = monthrange(today.year, today.month)[1]
    year_days_qnt = isleap(today.year) + 365
    print(year_days_qnt)
    monthly_report_arr = []
    for company in companies:
        week_qnt = 0
        month_qnt = 0
        year_qnt = 0

        participants = Participant.objects.filter(employee__company=company, completed_at__isnull=False)
        if len(participants) > 0:
            for participant in participants:
                print(participant.employee.name)
                delta = now_aware - participant.completed_at
                if delta.days <= 7:
                    week_qnt = week_qnt + 1
                if delta.days <= month_days_qnt:
                    month_qnt = month_qnt + 1
                if delta.days <= year_days_qnt:
                    year_qnt = year_qnt + 1
            company_dict = {
                'company': company.name,
                'week_qnt': week_qnt,
                'month_qnt': month_qnt,
                'year_qnt': year_qnt,
            }
            monthly_report_arr.append(company_dict)
    send_month_report(monthly_report_arr)
    return HttpResponse(status=200)
