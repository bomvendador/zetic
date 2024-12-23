from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
import datetime

import os

from pdf.extract_data import extract_section

import fpdf

# from pdf.save_data import save_data_to_db
import cyrtranslit
from reports import settings
import time
from pdf.models import CompanyGroupReportAllowedOptions, GroupReportAllowedOptions, Company
from pdf_group.title import title_page
from pdf_group.squares import page as squares_page
from pdf_group.section_1 import page as section_1_page
from pdf_group.section_2 import page as section_2_page
from pdf_group.section_3 import page as section_3_page
from pdf_group.section_4 import page as section_4_page
from pdf_group.description import page as description_page
from pdf_group.participants_list import page as participants_page
from pdf_group.integral_report_page import page as integral_report_page
from pdf_group.traffic_light_report.traffic_light_report_page import page as traffic_light_report_page
from pdf.views import save_serve_file
from pdf_group.save_data import save_data_to_db as save_data_group
from django.db.models import Sum, Q


def pdf_group_generator(request_json):
    static_url = 'static/'
    pdf = fpdf.FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_font("cambria", style="",
                 fname=os.path.join(settings.BASE_DIR, static_url) + "/fonts/Cambria.ttf", uni=True)
    pdf.add_font("CambriaBold", style="",
                 fname=os.path.join(settings.BASE_DIR, static_url) + "/fonts/Cambria-Bold.ttf", uni=True)

    pdf.add_font("RalewayMedium", style="", fname=os.path.join(settings.BASE_DIR, static_url) + "/fonts/Raleway-Medium.ttf", uni=True)
    pdf.add_font("RalewayRegular", style="", fname=os.path.join(settings.BASE_DIR, static_url) + "/fonts/Raleway-Regular.ttf", uni=True)
    pdf.add_font("RalewayLight", style="", fname=os.path.join(settings.BASE_DIR, static_url) + "/fonts/Raleway-Light.ttf", uni=True)
    pdf.add_font("RalewayBold", style="", fname=os.path.join(settings.BASE_DIR, static_url) + "/fonts/Raleway-Bold.ttf", uni=True)
    pdf.add_font("NotoSansDisplayMedium", style="", fname=os.path.join(settings.BASE_DIR, static_url) + "/fonts/NotoSansDisplay-Medium.ttf", uni=True)

    company_id = request_json['company_id']
    square_results = request_json['square_results']
    max_y = 280
    total_participant_qnt = len(square_results)
    # line_height = round(pdf.font_size * 2)
    line_height = 5.5
    table_height = round(total_participant_qnt / 2) * line_height
    table_y = max_y - table_height
    # print(f'line_height = {line_height} total_participant_qnt = {total_participant_qnt} table_height = {table_height} table_y = {table_y}')

    pdf.add_page()
    print(square_results)
    # lang = request_json['lang']
    lang = 'ru'
    # client_name = request_json['project']

    title_page(pdf, request_json, lang)

    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    participants_page(pdf, square_results, lang)

    # интегральный отчет
    pdf.set_line_width(0.1)

    # integral_group_report_allowed = True
    integral_group_report_allowed_options = GroupReportAllowedOptions.objects.get(name='Интегральный отчет')
    company_integral_group_report_options = CompanyGroupReportAllowedOptions.objects.get(Q(option=integral_group_report_allowed_options) &
                                                                                     Q(company=Company.objects.get(id=company_id))).value
    # if not company_integral_group_report_options:
    #     integral_group_report_allowed = False

    # print(f'company_integral_group_report_options id = {len(company_integral_group_report_options)}')
    # print(f'integral_group_report_allowed = {integral_group_report_allowed}')
    if company_integral_group_report_options:
        groups = []
        for participant_data in square_results:
            group_name = participant_data[4]
            if group_name != '':
                if not any(group_name in key for key in groups):
                    groups.append({
                        group_name: [participant_data]
                    })
                else:
                    for group in groups:
                        if group_name in group:
                            group[group_name].append(participant_data)

        # print('----groups-----')
        # print(groups)
        # print('--------------')
        if len(groups) > 0:
            groups_for_integral_report = []
            # print('====groups_for_integral_report====')
            for group in groups:
                key_vals = next(iter(group.values()))
                if len(key_vals) >= 3:
                    # print(key_vals)
                    groups_for_integral_report.append(key_vals)
                    group_name_for_report = key_vals[0][4]
                    pdf.add_page()
                    integral_report_page(pdf, 'ru', square_results, f'Интегральный отчет (группа - "{group_name_for_report}")')

            # print('-------------------')
        pdf.add_page()
        pdf.set_text_color(0, 0, 0)
        integral_report_page(pdf, 'ru', square_results, 'Интегральный отчет (все участники)')

    # ---------------------

    # светофор
    traffic_light_group_report_allowed_options = GroupReportAllowedOptions.objects.get(name='Светофор')
    company_traffic_light_group_report_options = CompanyGroupReportAllowedOptions.objects.get(Q(option=traffic_light_group_report_allowed_options) &
                                                                                     Q(company=Company.objects.get(id=company_id))).value

    if company_traffic_light_group_report_options:
        pdf.add_page()
        pdf.set_text_color(0, 0, 0)
        traffic_light_report_page(pdf, 'ru', request_json)
    # -------------

    # страница квадратов
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    squares_page(pdf, square_results, table_y)

    # ---------------

    # страница описания
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    description_page(pdf, lang)
    #-----------------

    # if 'group_report_id' in request_json:
    #     group_report_id = request_json['group_report_id']
    # else:
    #     group_report_id = ''

    pdf.set_line_width(0.1)
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    section_1_page(pdf, square_results, lang)

    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    section_2_page(pdf, square_results, lang)

    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    section_3_page(pdf, square_results, lang)

    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    section_4_page(pdf, square_results, lang)

    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page4(pdf, square_results, lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page5(pdf, square_results, lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page6(pdf, square_results, lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page7(pdf, square_results, lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page8(pdf, square_results, lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page9(pdf, square_results, lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page10(pdf, square_results, lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page11(pdf, square_results, lang, table_y)

    now = datetime.datetime.now()

    file_name = cyrtranslit.to_latin(request_json['company_name'], 'ru') + '_' + cyrtranslit.to_latin(request_json['project_name'], 'ru') + "___" + now.strftime("%d_%m_%Y__%H_%M_%S") + "_" + lang.upper() + '_group.pdf'

    path = "media/reportsPDF/group/"

    report_id = save_data_group(request_json, file_name)
    # print(square_results)
    # response = save_serve_file(pdf, path, file_name, request_json)
    response = save_serve_file(pdf, path, file_name)
    response.update({
        'report_id': report_id
    })
    return response


