from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from celery import shared_task
from datetime import datetime
from django.utils import timezone
from django.db.models.functions import ExtractDay
from panel.mail_handler import send_invitation_email, send_reminder, send_month_report
from pdf.models import Participant, EmailSentToParticipant, Company, Questionnaire, QuestionnaireVisits, Participant
from calendar import monthrange, isleap
from django.db.models import Sum, Q


def diff_month(start_date, end_date):
    qty_month = ((end_date.year - start_date.year) * 12) + (end_date.month - start_date.month)
    d_days = end_date.day - start_date.day
    if d_days >= 0:
        adjust = 0
    else:
        adjust = -1
    qty_month += adjust
    return qty_month


@shared_task(name='auto_block_questionnaire')
def auto_block_questionnaire():
    now_aware = timezone.now()
    participants_inst = Participant.objects.filter(completed_at=None)
    questionnaires_inst = Questionnaire.objects.filter(Q(participant__completed_at=None) & Q(participant__invitation_sent=True))
    for questionnaire in questionnaires_inst:
        if QuestionnaireVisits.objects.filter(questionnaire=questionnaire).exists():
            questionnaire_visits_inst = QuestionnaireVisits.objects.filter(questionnaire=questionnaire).latest('created_at')
            start_date = questionnaire_visits_inst.created_at
        else:
            start_date = questionnaire.created_at
        diff = diff_month(start_date, now_aware)
        # if diff >= 1:
            # questionnaire.active = False
            # questionnaire.save()
        print('================')
        print(f'questionnaire = {questionnaire.id}')
        print(f'participant = {questionnaire.participant.employee.email}')
        print(f'{start_date} - {now_aware}')
        print(f'разница = {diff}')
        print('================')


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
def monthly_report(request):
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
