# from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, Study
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import requests
from reports import settings
import json
from celery import shared_task



@login_required(redirect_field_name=None, login_url='/login/')
def get_code_for_invitation(request, json_request):

    return 'josipfjsdof'


@login_required(redirect_field_name=None, login_url='/login/')
def get_study_question_groups(request, public_code):
    response = [
        {'code': 1,
         'name': 'ЧЕРТЫ ХАРАКТЕРА'
         },
        {'code': 2,
         'name': 'ПОВЕДЕНИЕ В СТРЕССЕ'
         },
        {'code': 3,
         'name': 'ВЫГОРАНИЕ'
         },
        {'code': 4,
         'name': 'ЦЕННОСТИ'
         },

    ]
    return response


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
                            headers={'Authorization': 'Bearer ' + settings.API_BEARER}, data=data)
    print(f'sync response - {response}')
    return response



