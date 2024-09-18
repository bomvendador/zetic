# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from celery import shared_task
from datetime import datetime
from django.utils import timezone
from django.db.models.functions import ExtractDay
from panel.mail_handler import send_invitation_email, send_reminder, send_month_report
from pdf.models import Participant, EmailSentToParticipant, Company, Questionnaire, QuestionnaireVisits, Participant, \
    QuestionnaireQuestionAnswers, Report, Category, ReportDataByCategories
from calendar import monthrange, isleap
from django.db.models import Sum, Q


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
from pdf.views import save_serve_file, category_data

import cyrtranslit


@shared_task(name='pdf_single_generator')
def pdf_single_generator_task(questionnaire_id, report_id):
    time_start = time.perf_counter()
    pdf = fpdf.FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_font("Cambria", style="",
                 fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Cambria.ttf", uni=True)
    pdf.add_font("Cambria-Bold", style="",
                 fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Cambria-Bold.ttf", uni=True)
    pdf.add_font("RalewayMedium", style="",
                 fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Medium.ttf", uni=True)
    pdf.add_font("RalewayRegular", style="",
                 fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Regular.ttf", uni=True)
    pdf.add_font("RalewayLight", style="",
                 fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Light.ttf", uni=True)
    pdf.add_font("RalewayBold", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Bold.ttf",
                 uni=True)
    pdf.add_font("NotoSansDisplayMedium", style="",
                 fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/NotoSansDisplay-Medium.ttf", uni=True)
    pdf.add_page()

    questionnaire_inst = Questionnaire.objects.get(id=questionnaire_id)
    questionnaire_questions_answers_for_validity_inst = QuestionnaireQuestionAnswers.objects.filter(
        questionnaire=questionnaire_inst,
        question__category__for_validity=True)
    employee = questionnaire_inst.participant.employee
    if not report_id == '':
        report_inst = Report.objects.get(id=report_id)
        lie_points = report_inst.lie_points
    else:
        sum_lie_point = 0
        for answer in questionnaire_questions_answers_for_validity_inst:
            sum_lie_point = sum_lie_point + answer.answer.raw_point
        lie_points = round(sum_lie_point / 40 * 10)
    participant_info = {
        "name": employee.name,
        "sex": employee.sex.name_ru,
        "birth_year": employee.birth_year,
        "email": employee.email
    }
    # participant_name = participant_info['name']
    lang = 'ru'
    # lang = request_json['lang']
    # lie_points = round(request_json['lie_points']/40 * 10)

    title_page(pdf, employee.name, lang)

    pdf.add_page()
    page2(pdf, lie_points, lang)

    pdf.add_page()
    page_short_conclusions(pdf, questionnaire_id, 'ru', report_id)

    answer_code_1 = category_data('1_', questionnaire_id, employee.id)
    if answer_code_1:
        pdf.add_page()
        # page3(pdf, extract_section(request_json, 'Кеттелл'), lang)
        page3(pdf, answer_code_1, lang, participant_info)

    answer_code_2 = category_data('2_', questionnaire_id, employee.id)
    if answer_code_2:
        pdf.add_page()
        # page3(pdf, extract_section(request_json, 'Кеттелл'), lang)
        page4(pdf, answer_code_2, lang, participant_info)

    answer_code_3 = category_data('3_', questionnaire_id, employee.id)
    if answer_code_3:
        pdf.add_page()
        # page3(pdf, extract_section(request_json, 'Кеттелл'), lang)
        page5(pdf, answer_code_3, lang, participant_info)

    answer_code_4 = category_data('4_', questionnaire_id, employee.id)
    if answer_code_4:
        pdf.add_page()
        # page3(pdf, extract_section(request_json, 'Кеттелл'), lang)
        page6(pdf, answer_code_4, lang, participant_info)
    now = datetime.now()

    file_name = cyrtranslit.to_latin(questionnaire_inst.participant.employee.name.strip(), 'ru') + "_" + now.strftime(
        "%d_%m_%Y__%H_%M_%S") + "_" + lang.upper() + '_single.pdf'

    path = "media/reportsPDF/single/"

    # save_data_to_db(request_json, file_name)
    response = save_serve_file(pdf, path, file_name)

    send_email_result = save_data_to_db_and_send_report(questionnaire_inst.id, file_name, questionnaire_inst.participant.study.id, lie_points, lang, report_id)

    time_finish = time.perf_counter()
    # print(round(time_finish-time_start, 2))
    return response


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


