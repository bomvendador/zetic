from django.http import HttpResponseServerError, HttpResponse
import json
from pdf.views import pdf_generator


# Create your views here.


def server_response(request):
    return HttpResponse(status=200)


def json_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)['code']
        except KeyError:
            HttpResponseServerError('JSON request error')
        request_json = json.loads(request.POST)
    else:
        file = 'media/json/single-report-example.json'
        with open(file, encoding="utf8") as f:
            request_json = json.load(f)

    return pdf_generator(request_json)

