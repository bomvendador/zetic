# -*- coding: utf-8 -*-

# Create your views here.
from pdf.models import Questionnaire, QuestionnaireQuestionAnswers, QuestionAnswers, Category, CategoryQuestions, Report
from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse, JsonResponse, FileResponse
from django.db.models import Sum
from . import raw_to_t_point

from django.views.decorators.csrf import csrf_exempt
import datetime
from pdf.title_page import title_page
from pdf.page_conclusions import page as page_short_conclusions

import os

from pdf.extract_data import extract_section

import fpdf

from pdf.page2_file import page2
from pdf.page3_file import page3
from pdf.page4_file import page4
from pdf.page5_file import page5
from pdf.page6_file import page6

from pdf.save_data import save_data_to_db_and_send_report
import cyrtranslit
from reports import settings
import time
import fitz
import json


def pdf_single_generator(questionnaire_id, report_id):
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
    sum_lie_point = 0
    for answer in questionnaire_questions_answers_for_validity_inst:
        sum_lie_point = sum_lie_point + answer.answer.raw_point

    # appraisal_data = request_json['appraisal_data']
    # appraisal_data_in_request = []
    # for item in appraisal_data:
    #     appraisal_data_in_request.append(item['code'])

    # participant_info = request_json['participant_info']
    # participant_info = {
    #         "name": "Дваркович Владимир",
    #         "sex": "женский",
    #         "birth_year": "1987",
    #         "email": "dvarkovich@email.com"
    #       }
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
    lie_points = round(sum_lie_point / 40 * 10)

    title_page(pdf, employee.name, lang)

    # questionnaire_questions_answers_code_1 = QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire_inst,
    #                                                                                      question__category__code__startswith='1_')
    # if questionnaire_questions_answers_code_1.exists():
    #     answers_category_code_1 = questionnaire_questions_answers_code_1.first().question.category
    # categories = Category.objects.filter(code__startswith='1_')
    # answers_code_1 = []
    #
    # for category in categories:
    #     code2 = category.code.split('_')[1]
    #     print(f'cpde2 = {code2}')
    #     if not int(code2) == 100:
    #         print('pass')
    #         raw_points = 0
    #         for answer in questionnaire_questions_answers_code_1:
    #             if answer.question.category == category:
    #                 raw_points = raw_points + answer.answer.raw_point
    #             # print(f'raw_point - {answer.answer.raw_point} categoryname - {answer.question.category.name} answer - {answer.question.text}')
    #         if not raw_points == 0:
    #             answers_code_1.append({
    #                 "category": category.name,
    #                 "code": category.code,
    #                 "points": raw_to_t_point.filter_raw_points_to_t_points(raw_points, employee.id, category.id)
    #
    #             })
    # print(answers_code_1)

    pdf.add_page()
    page2(pdf, lie_points, lang)

    pdf.add_page()
    page_short_conclusions(pdf, questionnaire_id, 'ru')

    # if '1' in appraisal_data_in_request:
    #     pdf.add_page()
    #     # page3(pdf, extract_section(request_json, 'Кеттелл'), lang)
    #     page3(pdf, extract_section(request_json, '1'), lang, participant_info)

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



    #
    # if '2' in appraisal_data_in_request:
    #     pdf.add_page()
    #     # page4(pdf, extract_section(request_json, 'Копинги'), lang)
    #     page4(pdf, extract_section(request_json, '2'), lang, participant_info)
    #
    # if '3' in appraisal_data_in_request:
    #     pdf.add_page()
    #     page5(pdf, extract_section(request_json, '3'), lang, participant_info)
    #     # page5(pdf, extract_section(request_json, 'Выгорание Бойко'), lang)
    #
    # if '4' in appraisal_data_in_request:
    #     pdf.add_page()
    #     page6(pdf, extract_section(request_json, '4'), lang, participant_info)
    #     # page6(pdf, extract_section(request_json, 'Ценности'), lang)
    #
    now = datetime.datetime.now()

    file_name = cyrtranslit.to_latin(questionnaire_inst.participant.employee.name.strip(), 'ru') + "_" + now.strftime(
        "%d_%m_%Y__%H_%M_%S") + "_" + lang.upper() + '_single.pdf'

    path = "media/reportsPDF/single/"

    # save_data_to_db(request_json, file_name)
    response = save_serve_file(pdf, path, file_name)

    save_data_to_db_and_send_report(questionnaire_inst.id, file_name, questionnaire_inst.participant.study.id, lie_points, lang, report_id)


    time_finish = time.perf_counter()
    # print(round(time_finish-time_start, 2))
    return response


def regenerate_report(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        report_id = json_data['report_id']
        report = Report.objects.get(id=report_id)
        questionnaire = Questionnaire.objects.get(participant=report.participant)
        pdf_single_generator(questionnaire.id, report_id)
        return HttpResponse(report.participant.employee.company.name)


def category_data(code_prefix, questionnaire_id, employee_id):
    questionnaire_inst = Questionnaire.objects.get(id=questionnaire_id)

    questionnaire_questions_answers = QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire_inst,
                                                                                         question__category__code__startswith=code_prefix)
    if questionnaire_questions_answers.exists():
        answers_category_code_1 = questionnaire_questions_answers.first().question.category
    categories = Category.objects.filter(code__startswith=code_prefix)
    answers = []

    for category in categories:
        code2 = category.code.split('_')[1]
        # print(f'cpde2 = {code2}')
        if not int(code2) == 100:
            # print('pass')
            raw_points = 0
            for answer in questionnaire_questions_answers:
                if answer.question.category == category:
                    raw_points = raw_points + answer.answer.raw_point
                # print(f'raw_point - {answer.answer.raw_point} categoryname - {answer.question.category.name} answer - {answer.question.text}')
            # if not raw_points == 0:
            answers.append({
                "category": category.name,
                "code": category.code,
                "points": raw_to_t_point.filter_raw_points_to_t_points(raw_points, employee_id, category.id)

            })
                # print('=== answers_code_1 ===')
                # print(answers_code_1)
                # print('======================')
    return answers


def save_serve_file(pdf, path, file_name):
    if not os.path.exists(path):
        os.makedirs(path)
    pdf.output(path + file_name)

    response = {
        'file_name': file_name
    }
    print(response)
    return JsonResponse(response, safe=False)


@csrf_exempt
def download_single_report(request, filename):
    reportsPDF_folder = os.path.join(settings.MEDIA_ROOT, 'reportsPDF')
    group_reports_folder = os.path.join(reportsPDF_folder, 'single')
    full_path = os.path.join(group_reports_folder, filename)
    print(full_path)
    with open(full_path, 'rb') as f:
        file_data = f.read()
        response = HttpResponse(file_data, content_type='application/pdf')
        response['Content-Disposition'] = f"attachment; filename={filename}"
    return response


@csrf_exempt
def download_file(request, filename):
    files_folder = os.path.join(settings.MEDIA_ROOT, 'files')
    # group_reports_folder = os.path.join(files_folder, 'single')
    full_path = os.path.join(files_folder, filename)
    print(full_path)
    response = FileResponse(open(full_path, 'rb'))
    return response


@csrf_exempt
def download_group_report(request, filename):
    reportsPDF_folder = os.path.join(settings.MEDIA_ROOT, 'reportsPDF')
    group_reports_folder = os.path.join(reportsPDF_folder, 'group')
    full_path = os.path.join(group_reports_folder, filename)
    print(full_path)
    response = FileResponse(open(full_path, 'rb'))

    # with open(full_path, 'rb') as f:
    #     file_data = f.read()
    #     response = HttpResponse(file_data, content_type='application/pdf')
    #     response['Content-Disposition'] = f"attachment; filename={filename}"
    return response
