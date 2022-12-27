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
from pdf_group.page2 import page2
from pdf_group.page3 import page3
from pdf_group.page4 import page4
from pdf_group.page5 import page5
from pdf_group.page6 import page6
from pdf_group.page7 import page7
from pdf_group.page8 import page8
from pdf_group.page9 import page9
from pdf_group.page10 import page10
from pdf_group.page11 import page11
from pdf.views import save_serve_file
from pdf_group.save_data import save_data_to_db as save_data_group


def pdf_group_generator(request_json):
    pdf = fpdf.FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_font("RalewayMedium", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Medium.ttf", uni=True)
    pdf.add_font("RalewayRegular", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Regular.ttf", uni=True)
    pdf.add_font("RalewayLight", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Light.ttf", uni=True)
    pdf.add_font("RalewayBold", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Bold.ttf", uni=True)
    pdf.add_font("NotoSansDisplayMedium", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/NotoSansDisplay-Medium.ttf", uni=True)

    pdf.add_page()
    print(request_json)
    # lang = request_json['lang']
    lang = 'ru'
    client_name = request_json['project']

    title_page(pdf, client_name, lang)

    pdf.add_page()

    pdf.set_text_color(0, 0, 0)
    page2(pdf, request_json['square_results'])

    pdf.add_page()

    pdf.set_text_color(0, 0, 0)
    page3(pdf, request_json['square_results'], lang)

    pdf.add_page()

    pdf.set_text_color(0, 0, 0)
    page4(pdf, request_json['square_results'], lang)

    pdf.add_page()

    pdf.set_text_color(0, 0, 0)
    page5(pdf, request_json['square_results'], lang)

    pdf.add_page()

    pdf.set_text_color(0, 0, 0)
    page6(pdf, request_json['square_results'], lang)

    pdf.add_page()

    pdf.set_text_color(0, 0, 0)
    page7(pdf, request_json['square_results'], lang)

    pdf.add_page()

    pdf.set_text_color(0, 0, 0)
    page8(pdf, request_json['square_results'], lang)

    pdf.add_page()

    pdf.set_text_color(0, 0, 0)
    page9(pdf, request_json['square_results'], lang)

    pdf.add_page()

    pdf.set_text_color(0, 0, 0)
    page10(pdf, request_json['square_results'], lang)

    pdf.add_page()

    pdf.set_text_color(0, 0, 0)
    page11(pdf, request_json['square_results'], lang)

    now = datetime.datetime.now()

    file_name = cyrtranslit.to_latin(client_name, 'ru') + "_" + now.strftime("%d_%m_%Y__%H_%M_%S") + "_" + lang.upper() + '_group.pdf'

    path = "media/reportsPDF/group/"

    save_data_group(request_json, file_name)
    # print(request_json['square_results'])
    response = save_serve_file(pdf, path, file_name, request_json)

    return response


