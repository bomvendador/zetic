# -*- coding: utf-8 -*-

# Create your views here.

from django.http import HttpResponse, HttpResponseNotFound
import datetime
from pdf.title_page import title_page

from pdf.extract_data import extract_section

import fpdf

from pdf.page2_file import page2
from pdf.page3_file import page3
from pdf.page4_file import page4
from pdf.page5_file import page5
from pdf.page6_file import page6

from pdf.save_data import save_data_to_db
import cyrtranslit
from reports import settings


def pdf_generator(request_json):
    pdf = fpdf.FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_font("RalewayMedium", style="", fname=settings.STATIC_ROOT + "/fonts/Raleway-Medium.ttf", uni=True)
    pdf.add_font("RalewayRegular", style="", fname=settings.STATIC_ROOT + "/fonts/Raleway-Regular.ttf", uni=True)
    pdf.add_font("RalewayLight", style="", fname=settings.STATIC_ROOT + "/fonts/Raleway-Light.ttf", uni=True)
    pdf.add_font("RalewayBold", style="", fname=settings.STATIC_ROOT + "/fonts/Raleway-Bold.ttf", uni=True)
    pdf.add_page()

    participant_name = request_json['participant_info']['name']

    title_page(pdf, participant_name)

    pdf.add_page()
    page2(pdf, request_json['lie_points'])

    pdf.add_page()
    page3(pdf, extract_section(request_json, 'Кеттелл'))

    pdf.add_page()
    page4(pdf, extract_section(request_json, 'Копинги'))

    pdf.add_page()
    page5(pdf, extract_section(request_json, 'Выгорание Бойко'))

    pdf.add_page()
    page6(pdf, extract_section(request_json, 'Ценности'))

    now = datetime.datetime.now()

    file_name = cyrtranslit.to_latin(participant_name, 'ru') + "_" + now.strftime("%d_%m_%Y__%H_%M_%S") + '.pdf'

    pdf.output("media/reportsPDF/" + file_name)

    try:
        with open('media/reportsPDF/' + file_name, 'rb') as f:
            file_data = f.read()
        response = HttpResponse(file_data, content_type='application/pdf')

        print(file_name)
        response['Content-Disposition'] = f"attachment; filename={file_name}"
        save_data_to_db(request_json, file_name)

    except IOError:
        response = HttpResponseNotFound('<h1>File not exist</h1>')

    return response





