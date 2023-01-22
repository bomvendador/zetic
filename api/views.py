from django.http import HttpResponseServerError, HttpResponse, HttpResponseRedirect
import json
from pdf.views import pdf_single_generator
from pdf_group.views import pdf_group_generator
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


# Create your views here.


def server_response(request):
    return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')
def json_request(request):
    if request.method == 'POST':
        try:
            request_json = json.loads(request.body.decode('utf-8'))
            print(f'{timezone.localtime(timezone.now()).strftime("%d.%m.%Y %H:%M:%S")} - {request_json}')
        except KeyError:
            HttpResponseServerError('JSON request error')
    else:
        file = 'media/json/single-report-example.json'
        with open(file, encoding="utf8") as f:
            request_json = json.load(f)
    # print(request_json['type'])
    if 'type' in request_json:
        return pdf_group_generator(request_json)
    else:
        return pdf_single_generator(request_json)


def home(request):
    context = {}
    return HttpResponseRedirect('/login/')


