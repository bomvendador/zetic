# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from celery import shared_task
from datetime import datetime
from django.utils import timezone
from django.db.models.functions import ExtractDay
from panel.mail_handler import send_invitation_email, send_reminder, send_month_report
from pdf.models import Participant, EmailSentToParticipant, Company, Questionnaire, QuestionnaireVisits, Participant, \
    QuestionnaireQuestionAnswers, Report, Category, ReportDataByCategories, ConsultantForm
from calendar import monthrange, isleap
from django.db.models import Sum, Q

from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from smtplib import SMTPException, SMTPRecipientsRefused


import fpdf
import os
import time
from reports import settings

from pdf.title_page import title_page
from pdf.page2_file import page2
from pdf.page3_file import page3
from pdf.page4_file import page4
from pdf.page5_file import page5
from pdf.page6_file import page6
from pdf.page_conclusions import page as page_short_conclusions
from pdf import raw_to_t_point
from pdf.save_data import save_data_to_db_and_send_report
from pdf.views import save_serve_file, category_data, pdf_single_generator

import cyrtranslit


@shared_task(name='pdf_single_generator')
def pdf_single_generator_task(questionnaire_id, report_id):
    # pdf_single_generator(questionnaire_id, report_id)
    pdf_single_generator({
        'questionnaire_id': questionnaire_id,
        'report_id': report_id
    })


@shared_task(name='send_report_to_participant_with_consultant_text_task')
def send_report_to_participant_with_consultant_text_task(forms_ids):
    email_errors = []
    email_success = []
    for form_id in forms_ids:
        consultant_form = ConsultantForm.objects.get(id=form_id)
        questionnaire = Questionnaire.objects.filter(participant=consultant_form.participant).latest('created_at')
        result = pdf_single_generator({
            'questionnaire_id': questionnaire.id,
            'report_id': '',
            'type': 'consultant_form',
            'consultant_form_id': consultant_form.id
        })
        if 'error' in result:
            email_errors.append({
                'participant_name': consultant_form.participant.employee.name,
                'participant_email': consultant_form.participant.employee.email,
            })
        else:
            email_success.append({
                'participant_name': consultant_form.participant.employee.name,
                'participant_email': consultant_form.participant.employee.email,
            })
    if settings.DEBUG == 0:
        # to_email = ['info@zetic.ru', 'bomvendador@yandex.ru']
        to_email = ['bomvendador@yandex.ru']
        context = {
            'email_errors': email_errors,
            'email_success': email_success,
        }
        subject = 'Отправка дополненного отчета респондентам ZETIC'
        html_message = render_to_string('email_templates/zetic_admin_notification_report_to_participant_made_consultant_text.html', context)

        from_email = 'ZETIC <info@zetic.ru>'

        if settings.DEBUG == 0:
            to_email = ['bomvendador@yandex.ru']
        email = EmailMessage(subject, html_message, from_email, [to_email])
        email.content_subtype = "html"
        try:
            email.send()
            result = {
                'result': 200
            }

        except SMTPRecipientsRefused as e:
            result = {
                'error': 'Указан некорректный Email'
            }

    else:
        return {'email_errors': email_errors, 'email_success': email_success}


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
    questionnaires_inst = Questionnaire.objects.filter(
        Q(participant__completed_at=None) & Q(participant__invitation_sent=True))
    for questionnaire in questionnaires_inst:
        if QuestionnaireVisits.objects.filter(questionnaire=questionnaire).exists():
            questionnaire_visits_inst = QuestionnaireVisits.objects.filter(questionnaire=questionnaire).latest(
                'created_at')
            start_date = questionnaire_visits_inst.created_at
        else:
            start_date = questionnaire.created_at
        diff = diff_month(start_date, now_aware)
        if diff >= 3:
            questionnaire.active = False
            questionnaire.save()
        # print('================')
        # print(f'questionnaire = {questionnaire.id}')
        # print(f'participant = {questionnaire.participant.employee.email}')
        # print(f'{start_date} - {now_aware}')
        # print(f'разница = {diff}')
        # print('================')


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
