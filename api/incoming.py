import datetime
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from pdf.models import Participant, Company, Employee
import json
import ast
from pdf.views import pdf_single_generator
from pdf_group.views import pdf_group_generator
from django.utils import timezone
from datetime import datetime

TOKEN = 'b55a461f947c6d315ad67f1d65d2ec592e400679'


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def participant_started(request):
# {"study": {"public_code": "ertrtre"},"participant": {"email": "jhkjk@huihuihjhhiio.dfd"}}
#     print(type(request.body.decode('utf-8')))
#     print(request.body.decode('utf-8'))

    json_request = json.loads(request.body.decode('utf-8'))
    # print(json_request)
    print(f'{timezone.localtime(timezone.now()).strftime("%d.%m.%Y %H:%M:%S")} - participant_started - {json_request}')

    study_public_code = json_request['study']['public_code']
    total_questions_qnt = json_request['study']['total_questions_qnt']
    participant_email = json_request['participant']['email']
    participant_name = json_request['participant']['name']
    employee = Employee.objects.get(email=participant_email)
    if not employee.name == participant_name:
        employee.name = participant_name
        employee.save()
    participant = Participant.objects.get(employee__email=participant_email, study__public_code=study_public_code)
    participant.started_at = datetime.now()
    participant.total_questions_qnt = total_questions_qnt
    participant.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def data_for_report(request):
    if request.method == 'POST':
        try:
            request_json = json.loads(request.body.decode('utf-8'))
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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def questions_answered_qnt(request):
# {"study": {"public_code": "ertrtre"},"participant": {"email": "jhkjk@huihuihjhhiio.dfd"}}
    json_request = json.loads(request.body.decode('utf-8'))
    print(f'{timezone.localtime(timezone.now()).strftime("%d.%m.%Y %H:%M:%S")} - questions_answered_qnt - {json_request}')
    study_public_code = json_request['study']['public_code']
    questions_answered = json_request['questions_answered_qnt']
    participant_email = json_request['participant']['email']
    participant_name = json_request['participant']['name']
    participant = Participant.objects.get(employee__email=participant_email, study__public_code=study_public_code)
    participant.answered_questions_qnt = questions_answered
    participant.employee.name = participant_name
    participant.save()
    return HttpResponse(status=200)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def companies_employees(request):
    data = []
    companies_ = Company.objects.filter(active=True)
    for company in companies_:
        employees_arr = []
        employees = Employee.objects.filter(company=company)
        for employee in employees:
            employees_arr.append({
                'name': employee.name,
                'email': employee.email
            })

        data.append({
                        'company_name': company.name,
                        'company_id': company.id,
                        'employees': employees_arr
                    })
    # return JsonResponse(data, safe=False)
    return Response(data)
