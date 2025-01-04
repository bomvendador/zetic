# -*- coding: utf-8 -*-

# Create your views here.
from pdf.models import Questionnaire, QuestionnaireQuestionAnswers, QuestionAnswers, Category, CategoryQuestions, \
    Report, ReportDataByCategories, ParticipantIndividualReportAllowedOptions, IndividualReportAllowedOptions, \
    CompanyIndividualReportAllowedOptions, IndividualReportContradictionFilter, IndividualReportContradictionFilterCategory
from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse, JsonResponse, FileResponse
from django.db.models import Sum, Q
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
from pdf.consultant_text_page import page as consultant_page
from .circle_diagram import page_circle_diagram

from pdf.save_data import save_data_to_db_and_send_report
import cyrtranslit
from reports import settings
import time
import fitz
import json


def pdf_single_generator(data):
# def pdf_single_generator(questionnaire_id, report_id):
    print('------data-----')
    print(data)
    print('-----------')
    questionnaire_id = data['questionnaire_id']
    report_id = data['report_id']
    time_start = time.perf_counter()
    static_dir = 'static/'
    pdf = fpdf.FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_font("Cambria", style="",
                 fname=os.path.join(settings.BASE_DIR, static_dir) + "/fonts/Cambria.ttf", uni=True)
    pdf.add_font("Cambria-Bold", style="",
                 fname=os.path.join(settings.BASE_DIR, static_dir) + "/fonts/Cambria-Bold.ttf", uni=True)
    pdf.add_font("RalewayMedium", style="",
                 fname=os.path.join(settings.BASE_DIR, static_dir) + "/fonts/Raleway-Medium.ttf", uni=True)
    pdf.add_font("RalewayRegular", style="",
                 fname=os.path.join(settings.BASE_DIR, static_dir) + "/fonts/Raleway-Regular.ttf", uni=True)
    pdf.add_font("RalewayLight", style="",
                 fname=os.path.join(settings.BASE_DIR, static_dir) + "/fonts/Raleway-Light.ttf", uni=True)
    pdf.add_font("RalewayBold", style="", fname=os.path.join(settings.BASE_DIR, static_dir) + "/fonts/Raleway-Bold.ttf",
                 uni=True)
    pdf.add_font("NotoSansDisplayMedium", style="",
                 fname=os.path.join(settings.BASE_DIR, static_dir) + "/fonts/NotoSansDisplay-Medium.ttf", uni=True)
    pdf.add_page()

    questionnaire_inst = Questionnaire.objects.get(id=questionnaire_id)
    questionnaire_questions_answers_for_validity_inst = QuestionnaireQuestionAnswers.objects.filter(
        questionnaire=questionnaire_inst,
        question__category__for_validity=True)
    employee = questionnaire_inst.participant.employee
    if report_id != '':
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
        "email": employee.email,
        "company_name": employee.company.name,
    }
    # participant_name = participant_info['name']
    lang = 'ru'
    # lang = request_json['lang']
    # lie_points = round(request_json['lie_points']/40 * 10)

    title_page(pdf, employee.name, lang, employee.company.name)

    pdf.add_page()
    page2(pdf, lie_points, lang)

    individual_report_allowed_options_short_conclusions = IndividualReportAllowedOptions.objects.get(name='Краткие выводы')

    show_short_conclusions = True
    participant_short_conclusions_options_filter = ParticipantIndividualReportAllowedOptions.objects.filter(Q(participant=questionnaire_inst.participant) &
                                                                                                  Q(option=individual_report_allowed_options_short_conclusions))
    if participant_short_conclusions_options_filter.exists():
        participant_short_conclusions_options = ParticipantIndividualReportAllowedOptions.objects.get(Q(participant=questionnaire_inst.participant) &
                                                                                                  Q(option=individual_report_allowed_options_short_conclusions))
        if not participant_short_conclusions_options.value:
            show_short_conclusions = False
    else:
        company_short_conclusions_options_filter = CompanyIndividualReportAllowedOptions.objects.filter(Q(option=individual_report_allowed_options_short_conclusions) &
                                                                                                 Q(company=questionnaire_inst.participant.employee.company))
        if company_short_conclusions_options_filter.exists():
            company_short_conclusions_options = CompanyIndividualReportAllowedOptions.objects.get(Q(option=individual_report_allowed_options_short_conclusions) &
                                                                                                  Q(company=questionnaire_inst.participant.employee.company))

            if not company_short_conclusions_options.value:
                show_short_conclusions = False
    if show_short_conclusions:
        pdf.add_page()
        page_short_conclusions(pdf, questionnaire_id, lang, report_id)

    # if '1' in appraisal_data_in_request:
    #     pdf.add_page()
    #     # page3(pdf, extract_section(request_json, 'Кеттелл'), lang)

    #     page3(pdf, extract_section(request_json, '1'), lang, participant_info)

    study_inst = questionnaire_inst.participant.study
    individual_report_allowed_options_circle_diagram = IndividualReportAllowedOptions.objects.get(name='Круговая диаграмма')
    if 'Создано сотрудником' in study_inst.name:
        participant_circle_diagram_options_filter_circle_diagram = CompanyIndividualReportAllowedOptions.objects.get(Q(option=individual_report_allowed_options_circle_diagram) &
                                                                                                                        Q(company=questionnaire_inst.participant.employee.company)).value
    else:
        participant_circle_diagram_options_filter_circle_diagram = ParticipantIndividualReportAllowedOptions.objects.get(Q(participant=questionnaire_inst.participant) &
                                                                                                                            Q(option=individual_report_allowed_options_circle_diagram)).value
    # print(f'circle_diagram = {}')
    if participant_circle_diagram_options_filter_circle_diagram:
        pdf.add_page()
        page_circle_diagram(pdf, questionnaire_id, report_id, lang)

    response_code_1 = category_data('1_', questionnaire_id, employee.id)
    response_code_2 = category_data('2_', questionnaire_id, employee.id)
    response_code_3 = category_data('3_', questionnaire_id, employee.id)
    response_code_4 = category_data('4_', questionnaire_id, employee.id)

    print('----response_code_1-----')
    print(response_code_1)
    print('---------')
    responses_codes = {
        '1': response_code_1,
        '2': response_code_2,
        '3': response_code_3,
        '4': response_code_4,
    }

    contradiction_filters_data = []
    contradiction_filters = IndividualReportContradictionFilter.objects.all()
    for contradiction_filter in contradiction_filters:
        contradiction_filter_to_show = True
        contradiction_filter_data = []
        contradiction_filter_categories = IndividualReportContradictionFilterCategory.objects.filter(filter=contradiction_filter)
        for contradiction_filter_category in contradiction_filter_categories:
            category_code = contradiction_filter_category.category.code
            points_from = contradiction_filter_category.points_from
            points_to = contradiction_filter_category.points_to
            category_prefix = category_code.split('_')[0]
            if responses_codes[category_prefix]:
                response_code_answers = responses_codes[category_prefix]['answers']
                for answer in response_code_answers:
                    if answer['code'] == category_code:
                        if points_from <= answer['points'] <= points_to:
                            contradiction_filter_data.append(category_code)
                        else:
                            contradiction_filter_to_show = False
        if contradiction_filter_to_show:
            contradiction_filters_data.append(contradiction_filter_data)
    print(contradiction_filters_data)
    pages_data = {
        'pdf': pdf,
        'lang': lang,
        'participant_info': participant_info,
        'contradiction_filters_data': contradiction_filters_data,
    }

    if response_code_1['category_is_not_empty']:
        answer_code_1 = response_code_1['answers']
        pages_data.update({
            'answer_code': answer_code_1
        })
        pdf.add_page()
        # page3(pdf, extract_section(request_json, 'Кеттелл'), lang)
        # page3(pdf, answer_code_1, lang, participant_info)
        page3(pages_data)

    # answer_code_2 = category_data('2_', questionnaire_id, employee.id)
    # if len(answer_code_2) > 0:
    if response_code_2['category_is_not_empty']:
        answer_code_2 = response_code_2['answers']
        pages_data.update({
            'answer_code': answer_code_2
        })

        pdf.add_page()
        # page3(pdf, extract_section(request_json, 'Кеттелл'), lang)
        # page4(pdf, answer_code_2, lang, participant_info, contradiction_filters_data)
        page4(pages_data)

    # answer_code_3 = category_data('3_', questionnaire_id, employee.id)
    # if len(answer_code_3) > 0:
    if response_code_3['category_is_not_empty']:
        answer_code_3 = response_code_3['answers']
        pages_data.update({
            'answer_code': answer_code_3
        })
        pdf.add_page()
        # page3(pdf, extract_section(request_json, 'Кеттелл'), lang)
        # page5(pdf, answer_code_3, lang, participant_info)
        page5(pages_data)

    # answer_code_4 = category_data('4_', questionnaire_id, employee.id)
    # if len(answer_code_4) > 0:
    if response_code_4['category_is_not_empty']:
        answer_code_4 = response_code_4['answers']
        pages_data.update({
            'answer_code': answer_code_4
        })
        pdf.add_page()
        # page3(pdf, extract_section(request_json, 'Кеттелл'), lang)
        # page6(pdf, answer_code_4, lang, participant_info)
        page6(pages_data)

    individual_report_allowed_options = IndividualReportAllowedOptions.objects.get(name='Выводы эксперта')
    show_consultant_page = True
    participant_consultant_page_options_filter = ParticipantIndividualReportAllowedOptions.objects.filter(Q(participant=questionnaire_inst.participant) &
                                                                                                  Q(option=individual_report_allowed_options))
    if participant_consultant_page_options_filter.exists():
        participant_consultant_page_options = ParticipantIndividualReportAllowedOptions.objects.get(Q(participant=questionnaire_inst.participant) &
                                                                                                    Q(option=individual_report_allowed_options))
        if not participant_consultant_page_options.value:
            show_consultant_page = False
    else:
        company_consultant_page_options_filter = CompanyIndividualReportAllowedOptions.objects.filter(Q(option=individual_report_allowed_options) &
                                                                                                      Q(company=questionnaire_inst.participant.employee.company))
        if company_consultant_page_options_filter:
            company_consultant_page_options = CompanyIndividualReportAllowedOptions.objects.get(Q(option=individual_report_allowed_options) &
                                                                                                Q(company=questionnaire_inst.participant.employee.company))

            if not company_consultant_page_options.value:
                show_consultant_page = False

    if 'consultant_form_id' in data and show_consultant_page:
        pdf.add_page()
        consultant_page(pdf, lang, data['consultant_form_id'])

    now = datetime.datetime.now()
    request_type = ''
    if 'type' in data:
        if data['type'] == 'consultant_form':
            request_type = 'consultant_form'

    if request_type == 'consultant_form':
        file_name = cyrtranslit.to_latin(questionnaire_inst.participant.employee.name.strip(), 'ru') + "_" + now.strftime(
            "%d_%m_%Y__%H_%M_%S") + "_" + lang.upper() + '_single_expert_conclusions.pdf'
    else:
        file_name = cyrtranslit.to_latin(questionnaire_inst.participant.employee.name.strip(), 'ru') + "_" + now.strftime(
            "%d_%m_%Y__%H_%M_%S") + "_" + lang.upper() + '_single.pdf'

    path = "media/reportsPDF/single/"

    # save_data_to_db(request_json, file_name)

    response_file_name = save_serve_file(pdf, path, file_name)
    # send_email_result = save_data_to_db_and_send_report(questionnaire_inst.id, file_name, questionnaire_inst.participant.study.id, lie_points, lang, report_id)

    save_data_to_db_and_send_report_context = {
        'questionnaire_id': questionnaire_inst.id,
        'file_name': file_name,
        'study_id': questionnaire_inst.participant.study.id,
        'lie_points': lie_points,
        'lang': lang,
        'report_id': report_id,
        'request_type': request_type,
    }
    if 'consultant_form_id' in data:
        save_data_to_db_and_send_report_context.update({
            'consultant_form_id': data['consultant_form_id']
        })
    send_email_result = save_data_to_db_and_send_report(save_data_to_db_and_send_report_context)

    if request_type == 'consultant_form':
        response = send_email_result
    else:
        response = response_file_name

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

        pdf_single_generator({'questionnaire_id': questionnaire.id, 'report_id': report_id})
        return HttpResponse(report.participant.employee.company.name)


def category_data(code_prefix, questionnaire_id, employee_id):
    questionnaire_inst = Questionnaire.objects.get(id=questionnaire_id)

    questionnaire_questions_answers = QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire_inst,
                                                                                         question__category__code__startswith=code_prefix)
    if questionnaire_questions_answers.exists():
        answers_category_code_1 = questionnaire_questions_answers.first().question.category
    categories = Category.objects.filter(code__startswith=code_prefix)
    answers = []
    category_is_not_empty = False
    report_by_categories_exists = False
    for category in categories:
        code2 = category.code.split('_')[1]
        if int(code2) != 100:
            report_by_categories_inst = ReportDataByCategories.objects.filter(Q(category_code=category.code) & Q(report__participant__employee_id=employee_id))
            if report_by_categories_inst.exists():
                points = report_by_categories_inst.latest('created_at').t_points
                report_by_categories_exists = True
            else:
                raw_points = 0
                for answer in questionnaire_questions_answers:
                    if answer.question.category == category:
                        raw_points = raw_points + answer.answer.raw_point
                points = raw_to_t_point.filter_raw_points_to_t_points(raw_points, employee_id, category.id)
                    # print(f'raw_point - {answer.answer.raw_point} categoryname - {answer.question.category.name} answer - {answer.question.text}')
                # if not raw_points == 0:
            answers.append({
                "category": category.name,
                "code": category.code,
                "points": points
                # "points": raw_to_t_point.filter_raw_points_to_t_points(raw_points, employee_id, category.id)

            })
                # print('=== answers_code_1 ===')
                # print(answers_code_1)
                # print('======================')
    if len(questionnaire_questions_answers) > 0 or report_by_categories_exists:
        category_is_not_empty = True
    response = {
        'answers': answers,
        'category_is_not_empty': category_is_not_empty
    }
    return response


def save_serve_file(pdf, path, file_name):
    if not os.path.exists(path):
        os.makedirs(path)
    pdf.output(path + file_name)

    response = {
        'file_name': file_name
    }

    # return JsonResponse(response, safe=False)
    return response


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
    full_path = os.path.join(files_folder, filename)
    response = FileResponse(open(full_path, 'rb'))
    return response


@csrf_exempt
def download_tmp_file(request, filename):
    files_folder = os.path.join(settings.MEDIA_ROOT, 'files', 'tmp')
    full_path = os.path.join(files_folder, filename)
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
