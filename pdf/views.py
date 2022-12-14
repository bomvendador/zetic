# -*- coding: utf-8 -*-

# Create your views here.

from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from pdf.title_page import title_page

import os

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
import time
import fitz


def pdf_single_generator(request_json):
    time_start = time.perf_counter()
    pdf = fpdf.FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_font("RalewayMedium", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Medium.ttf", uni=True)
    pdf.add_font("RalewayRegular", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Regular.ttf", uni=True)
    pdf.add_font("RalewayLight", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Light.ttf", uni=True)
    pdf.add_font("RalewayBold", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/Raleway-Bold.ttf", uni=True)
    pdf.add_font("NotoSansDisplayMedium", style="", fname=os.path.join(settings.BASE_DIR, 'static/') + "/fonts/NotoSansDisplay-Medium.ttf", uni=True)
    pdf.add_page()

    participant_name = request_json['participant_info']['name']
    lang = request_json['lang']

    title_page(pdf, participant_name, lang)

    pdf.add_page()
    page2(pdf, request_json['lie_points'], lang)

    pdf.add_page()
    page3(pdf, extract_section(request_json, 'Кеттелл'), lang)

    pdf.add_page()
    page4(pdf, extract_section(request_json, 'Копинги'), lang)

    pdf.add_page()
    page5(pdf, extract_section(request_json, 'Выгорание Бойко'), lang)

    pdf.add_page()
    page6(pdf, extract_section(request_json, 'Ценности'), lang)

    now = datetime.datetime.now()

    file_name = cyrtranslit.to_latin(participant_name.strip(), 'ru') + "_" + now.strftime("%d_%m_%Y__%H_%M_%S") + "_" + lang.upper() + '_single.pdf'

    path = "media/reportsPDF/single/"

    save_data_to_db(request_json, file_name)

    response = save_serve_file(pdf, path, file_name, request_json)

    time_finish = time.perf_counter()
    # print(round(time_finish-time_start, 2))
    return response


def save_serve_file(pdf, path, file_name, request_json):
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
def download_group_report(request, filename):
    reportsPDF_folder = os.path.join(settings.MEDIA_ROOT, 'reportsPDF')
    group_reports_folder = os.path.join(reportsPDF_folder, 'group')
    full_path = os.path.join(group_reports_folder, filename)
    print(full_path)
    with open(full_path, 'rb') as f:
        file_data = f.read()
        response = HttpResponse(file_data, content_type='application/pdf')
        response['Content-Disposition'] = f"attachment; filename={filename}"
    return response

