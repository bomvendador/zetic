# -*- coding: utf-8 -*-

# Create your views here.

import datetime
import os
import time
from dataclasses import dataclass

import cyrtranslit
import fpdf
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    JsonResponse,
    FileResponse,
)
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from pdf.extract_data import extract_section
from pdf.models import PointDescription
from pdf.page2_file import page2
from pdf.page3_file import page3
from pdf.page4_file import page4
from pdf.page5_file import page5
from pdf.page6_file import page6
from pdf.save_data import save_data_to_db
from pdf.single_report import (
    IncomingSingleReportData,
    SingleReportData,
    load_point_mapper_v1,
)
from pdf.single_report_dict import SingleReportDict
from pdf.title_page import title_page
from reports import settings


def pdf_single_generator(report_data: SingleReportData):
    q_filter = Q()
    if not report_data.cattell_data.is_empty():
        q_filter |= report_data.cattell_data.to_query()

    if not report_data.coping_data.is_empty():
        q_filter |= report_data.coping_data.to_query()

    if not report_data.boyko_data.is_empty():
        q_filter |= report_data.boyko_data.to_query()

    if not report_data.values_data.is_empty():
        q_filter |= report_data.values_data.to_query()

    time_start = time.perf_counter()
    # load all points descriptions
    points_description = PointDescription.objects.filter(q_filter)
    time_end = time.perf_counter()
    print(
        f"load all points ({len(report_data.cattell_data)} + {len(report_data.coping_data)} + {len(report_data.boyko_data)} + {len(report_data.values_data)}) descriptions: {time_end - time_start}"
    )
    print(f"QueryFilter: {q_filter}")
    if report_data.lang == "en":
        points_description_dict = {
            item["category__code"]: item["text_en"]
            for item in points_description.values("category__code", "text_en")
        }
    else:
        points_description_dict = {
            item["category__code"]: item["text"]
            for item in points_description.values("category__code", "text")
        }

    time_start = time.perf_counter()
    report_generator = SingleReportDict(points_description_dict)
    pdf = report_generator.generate_pdf(report_data)
    time_end = time.perf_counter()
    print(f"generate pdf: {time_end - time_start}")

    now = datetime.datetime.now()

    if report_data.lang == "ru":
        name_eng = cyrtranslit.to_latin(report_data.participant_name.strip(), "ru")
    else:
        name_eng = report_data.participant_name.strip()

    file_name = "{0}_{1}_{2}_single.pdf".format(
        name_eng, now.strftime("%d_%m_%Y__%H_%M_%S"), report_data.lang.upper()
    )

    path = os.path.join(settings.BASE_DIR, "media", "reportsPDF", "single")

    save_data_to_db(request_json, file_name, pdf)

    response = save_serve_file(pdf, path, file_name, request_json)

    time_finish = time.perf_counter()
    # print(round(time_finish-time_start, 2))
    return response


def save_serve_file(pdf, path, file_name, request_json):
    if not os.path.exists(path):
        os.makedirs(path)
    pdf.output(path + file_name)

    response = {"file_name": file_name}
    print(response)
    return JsonResponse(response, safe=False)


@csrf_exempt
@login_required(redirect_field_name=None, login_url="/login/")
def download_single_report(request, filename):
    full_path = os.path.join(settings.MEDIA_ROOT, "reportsPDF", "single", filename)
    print(full_path)
    with open(full_path, "rb") as f:
        file_data = f.read()
        response = HttpResponse(file_data, content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename={filename}"
    return response


@csrf_exempt
@login_required(redirect_field_name=None, login_url="/login/")
def download_file(request, filename):
    files_folder = os.path.join(settings.MEDIA_ROOT, "files")
    # group_reports_folder = os.path.join(files_folder, 'single')
    full_path = os.path.join(files_folder, filename)
    print(full_path)
    response = FileResponse(open(full_path, "rb"))
    return response


@csrf_exempt
@login_required(redirect_field_name=None, login_url="/login/")
def download_group_report(request, filename):
    reportsPDF_folder = os.path.join(settings.MEDIA_ROOT, "reportsPDF")
    group_reports_folder = os.path.join(reportsPDF_folder, "group")
    full_path = os.path.join(group_reports_folder, filename)
    print(full_path)
    with open(full_path, "rb") as f:
        file_data = f.read()
        response = HttpResponse(file_data, content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
