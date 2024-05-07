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

from pdf_group.title import title_page
from pdf_group.squares import page as squares_page
from pdf_group.section_1 import page as section_1_page
from pdf_group.section_2 import page as section_2_page
from pdf_group.section_3 import page as section_3_page
from pdf_group.section_4 import page as section_4_page
from pdf_group.description import page as description_page
from pdf_group.participants_list import page as participants_page
from pdf.views import save_serve_file
from pdf_group.save_data import save_data_to_db as save_data_group


def pdf_group_generator(request_json):
    pdf = fpdf.FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_font("RalewayMedium", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Medium.ttf", uni=True)
    pdf.add_font("RalewayRegular", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Regular.ttf", uni=True)
    pdf.add_font("RalewayLight", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Light.ttf", uni=True)
    pdf.add_font("RalewayBold", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Bold.ttf", uni=True)
    pdf.add_font("NotoSansDisplayMedium", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/NotoSansDisplay-Medium.ttf", uni=True)

    max_y = 280
    total_participant_qnt = len(request_json['square_results'])
    # line_height = round(pdf.font_size * 2)
    line_height = 5.5
    table_height = round(total_participant_qnt / 2) * line_height
    table_y = max_y - table_height
    # print(f'line_height = {line_height} total_participant_qnt = {total_participant_qnt} table_height = {table_height} table_y = {table_y}')

    pdf.add_page()
    # print(request_json)
    # lang = request_json['lang']
    lang = 'ru'
    client_name = request_json['project']

    title_page(pdf, client_name, lang)

    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    description_page(pdf, lang)

    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    participants_page(pdf, request_json['square_results'], lang)

    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    squares_page(pdf, request_json['square_results'], table_y)

    pdf.set_line_width(0.1)
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    section_1_page(pdf, request_json['square_results'], lang)

    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    section_2_page(pdf, request_json['square_results'], lang)

    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    section_3_page(pdf, request_json['square_results'], lang)

    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    section_4_page(pdf, request_json['square_results'], lang)

    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page4(pdf, request_json['square_results'], lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page5(pdf, request_json['square_results'], lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page6(pdf, request_json['square_results'], lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page7(pdf, request_json['square_results'], lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page8(pdf, request_json['square_results'], lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page9(pdf, request_json['square_results'], lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page10(pdf, request_json['square_results'], lang, table_y)
    #
    # pdf.add_page()
    #
    # pdf.set_text_color(0, 0, 0)
    # page11(pdf, request_json['square_results'], lang, table_y)

    now = datetime.datetime.now()

    file_name = cyrtranslit.to_latin(client_name, 'ru') + "_" + now.strftime("%d_%m_%Y__%H_%M_%S") + "_" + lang.upper() + '_group.pdf'

    path = "media/reportsPDF/group/"

    save_data_group(request_json, file_name)
    # print(request_json['square_results'])
    # response = save_serve_file(pdf, path, file_name, request_json)
    response = save_serve_file(pdf, path, file_name)

    return response


