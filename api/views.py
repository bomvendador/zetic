import json
from json import JSONDecodeError

from django.http import HttpResponseServerError, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from pdf.single_report import (
    IncomingSingleReportData,
    SingleReportData,
    load_point_mapper_v1,
)
from pdf.single_report_dict import SingleReportV1
from pdf.views import pdf_single_generator
from pdf_group.views import pdf_group_generator


# Create your views here.


def server_response(request):
    return HttpResponse(status=200)


@method_decorator(csrf_exempt, name="dispatch")
def json_request(request):
    try:
        request_json = json.loads(request.body.decode("utf-8"))
        print(
            f'{timezone.localtime(timezone.now()).strftime("%d.%m.%Y %H:%M:%S")} - {request_json}'
        )
    except IOError:
        return HttpResponseServerError("JSON request error")

    # print(request_json['type'])
    if "type" in request_json:
        return pdf_group_generator(request_json)
    else:
        incoming_data = IncomingSingleReportData.from_dict(request_json)
        report_data: SingleReportData = incoming_data.to_single_report_data(
            load_point_mapper_v1
        )
        return pdf_single_generator(report_data, incoming_data, SingleReportV1)


def home(request):
    context = {}
    return HttpResponseRedirect("/login/")
