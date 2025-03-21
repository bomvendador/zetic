import datetime

from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, User, Participant, EmployeeGender, \
    Project, ProjectParticipants, Questionnaire, Report, QuestionnaireVisits, QuestionnaireQuestionAnswers, Study, UserCompanies
from login.models import UserProfile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from reports import settings
import json
from django.utils import timezone
import requests

from panel.views import info_common
from api.outcoming import Attributes, sync_add_employee
from panel.custom_funcs import update_attributes, string_to_date_format
from django.db.models import Sum, Q

from django.template.loader import render_to_string

import operator
from functools import reduce

from panel.constants import CONSTANT_USER_ROLES


@login_required(redirect_field_name=None, login_url='/login/')
def create_report_1(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        companies_ids = json_data['companies_ids']
        gender_id = json_data['gender_id']
        date_from = json_data['date_from']
        date_to = json_data['date_to']
        age_from = json_data['age_from']
        age_to = json_data['age_to']
        roles_ids = json_data['roles_ids']
        positions_ids = json_data['positions_ids']
        industries_ids = json_data['industries_ids']
        user_role = UserProfile.objects.get(user=request.user).role.name
        response = {}
        reports_data = None
        if user_role != CONSTANT_USER_ROLES['SUPER_ADMIN'] and user_role != CONSTANT_USER_ROLES['ADMIN'] and user_role != CONSTANT_USER_ROLES['PARTNER']:
            response.update({
                'access_error': 'Отчет для роли пользователя недоступен'
            })
        else:
            match user_role:
                case 'Суперадмин':
                    if companies_ids:
                        reports_data = Report.objects.filter(Q(participant__employee__company__in=companies_ids) &
                                                             Q(primary=True))
                    else:
                        reports_data = Report.objects.all()
                case 'Админ' | 'Партнер':
                    if not companies_ids:
                        companies_created_by_user = Company.objects.filter(created_by=request.user)
                        companies_ids = []
                        for user_company in companies_created_by_user:
                            companies_ids.append(user_company.id)
                        user_companies = UserCompanies.objects.filter(user=request.user)
                        for user_company in user_companies:
                            companies_ids.append(user_company.company.id)

                    reports_data = Report.objects.filter(Q(participant__employee__company__in=companies_ids) &
                                                         Q(primary=True))
        if date_from:
            reports_data = reports_data.filter(added__date__gte=string_to_date_format(date_from))
        if date_to:
            reports_data = reports_data.filter(added__date__lte=string_to_date_format(date_to))

        if gender_id:
            gender = EmployeeGender.objects.get(id=gender_id)
            reports_data = reports_data.filter(participant__employee__sex=gender)

        if age_from:
            year_to = datetime.datetime.now().year - int(age_from)
            reports_data = reports_data.filter(participant__employee__birth_year__lte=year_to)
        if age_to:
            year_from = datetime.datetime.now().year - int(age_to)
            reports_data = reports_data.filter(participant__employee__birth_year__gte=year_from)

        if roles_ids:
            reports_data = reports_data.filter(participant__employee__role__in=roles_ids)

        if industries_ids:
            reports_data = reports_data.filter(participant__employee__industry__in=industries_ids)

        if positions_ids:
            reports_data = reports_data.filter(participant__employee__position__in=positions_ids)

        # print(len(reports_data))
        if reports_data:
            rows = render_to_string('statistics_reports/report_1/tr_statistics_report_1.html', {'data': reports_data}).rstrip()
            # print(rows)
            response.update({
                'rows': rows
            })
        # print(response)
        return JsonResponse({'response': response})
