from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, Study, Participant, ParticipantQuestionGroups
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import requests
from reports import settings
import json
from celery import shared_task
from django.utils import timezone



@login_required(redirect_field_name=None, login_url='/login/')
def get_code_for_invitation(request, json_request):
    study_id = json_request['study_id']
    study_public_code = Study.objects.get(id=study_id).public_code
    participant_id = json_request['participant_id']
    participant = Participant.objects.get(id=participant_id)
    participant_question_groups = ParticipantQuestionGroups.objects.filter(participant=participant)
    sections = []
    for participant_question_group in participant_question_groups:
        sections.append(str(participant_question_group.question_group_code))
    employee = participant.employee
    data = {
        "email": employee.email,
        "study_code": study_public_code,
        "sections": sections,
        "employee": {
                "name": employee.name,
                "sex": employee.sex.public_code,
                "role_id": employee.role.public_code,
                "position_id": employee.position.public_code,
                "industry_id": employee.industry.public_code,
                "birth_year": employee.birth_year
            }
        }
    print(data)
    url = settings.API_LINK + 'participant/'
    response = requests.post(url,
                            headers={'Authorization': 'Bearer ' + settings.API_BEARER, 'Content-type': 'application/json'}, json=data)
    print(f'{timezone.localtime(timezone.now()).strftime("%d.%m.%Y %H:%M:%S")} - sync response - {response}')
    print(f'sync json - {response.json()}')

    return response.json()


# @login_required(redirect_field_name=None, login_url='/login/')
# def get_study_question_groups(request, public_code):
#     response = [
#         {'code': 1,
#          'name': 'ЧЕРТЫ ХАРАКТЕРА'
#          },
#         {'code': 2,
#          'name': 'ПОВЕДЕНИЕ В СТРЕССЕ'
#          },
#         {'code': 3,
#          'name': 'ВЫГОРАНИЕ'
#          },
#         {'code': 4,
#          'name': 'ЦЕННОСТИ'
#          },
#
#     ]
#     return response


class Attributes:


    def get_sex():
        try:
            response = requests.get(settings.API_LINK + 'attributes', headers={'Authorization': 'Bearer ' + settings.API_BEARER}).json()
            return response['sex']
        except ValueError:
            return 'Server error'

    def get_roles():
        try:
            response = requests.get(settings.API_LINK + 'attributes', headers={'Authorization': 'Bearer ' + settings.API_BEARER}).json()
            return response['role']
        except ValueError:
            return 'Server error'

    def get_positions():
        try:
            response = requests.get(settings.API_LINK + 'attributes', headers={'Authorization': 'Bearer ' + settings.API_BEARER}).json()
            return response['position']
        except ValueError:
            return 'Server error'

    def get_industries():
        try:
            response = requests.get(settings.API_LINK + 'attributes', headers={'Authorization': 'Bearer ' + settings.API_BEARER}).json()
            return response['industry']
        except ValueError:
            return 'Server error'


def get_research():
    headers = {'Authorization': 'Bearer sinoh8kien7eiv3mooyie4AeWoh5ohd6xo6u'}
    result = requests.get('https://demo-admin.zetic.borsky.dev/api/research', headers=headers).json()
    print(f'res = {result}')
    return result

 # [{'publicCode': 'QgJA6E', 'name': 'Zetic', 'sections':
 #     [{'publicCode': '46Pygl', 'name': 'Секция 1. Черты характера'},
 #      {'publicCode': 'z6w1LA', 'name': 'Секция 2. Работа в неопределенности'},
 #      {'publicCode': 'o6jEX4', 'name': 'Секция 3. Выгорание '},
 #      {'publicCode': '1gzM6B', 'name': 'Секция 4. Ценности'}
 #      ]}
 #  ]


def get_company():
    result = requests.get('https://demo-admin.zetic.borsky.dev/api/company', headers=headers).json()
    print(f'res = {result}')
    return result


@shared_task
def sync_add_company(name, public_code):
    data = {
        "name": name,
        "public_code": public_code
    }
    response = requests.post(settings.API_LINK + 'company',
                            headers={'Authorization': 'Bearer ' + settings.API_BEARER, 'Content-type': 'application/json'}, json=data)
    # print(f'sync response - {response}')
    # return response


@shared_task
def sync_add_employee(employee_id):
    employee = Employee.objects.get(id=employee_id)
    company_id = employee.company.public_code
    data = {
        "name": employee.name,
        "email": employee.email,
        "role_id": employee.role.public_code,
        "position_id": employee.position.public_code,
        "industry_id": employee.industry.public_code,
        "sex_id": employee.sex.public_code,
        "birth_year": employee.birth_year
    }
    url = settings.API_LINK + 'company/' + company_id + '/employee'
    response = requests.post(url,
                            headers={'Authorization': 'Bearer ' + settings.API_BEARER, 'Content-type': 'application/json'}, json=data)
    print(f'{timezone.localtime(timezone.now()).strftime("%d.%m.%Y %H:%M:%S")} - sync response - {response}')
    # return response


def get_company_studies(company_public_code):
    url = settings.API_LINK + 'company/' + company_public_code + '/study'
    response = requests.get(url, headers={'Authorization': 'Bearer ' + settings.API_BEARER})
    print('---')
    print(response.json())
    return response.json()
