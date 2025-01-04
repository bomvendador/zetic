import time

from pdf.models import Category, Section, ResearchTemplate, ResearchTemplateSections, Study, Company, Employee, \
    Participant, IndividualReportAllowedOptions, GroupReportAllowedOptions, CompanyIndividualReportAllowedOptions, \
    CompanyGroupReportAllowedOptions, ParticipantIndividualReportAllowedOptions, StudyIndividualReportAllowedOptions
from login.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone
from django.core import serializers

from .views import info_common
from api import outcoming

from django.utils.dateformat import DateFormat


@login_required(redirect_field_name=None, login_url='/login/')
def companies_studies_list(request):
    context = info_common(request)

    cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
    studies_arr = []
    if cur_user_role_name == 'Админ заказчика':
        employee = Employee.objects.get(user=request.user)
        companies = Company.objects.filter(id=employee.company.id)
    if cur_user_role_name == 'Менеджер' or cur_user_role_name == 'Партнер':
        companies = Company.objects.filter(created_by=request.user)

    if cur_user_role_name == 'Админ' or cur_user_role_name == 'Суперадмин':
        companies = Company.objects.all()

    for company in companies:
        studies = Study.objects.filter(company=company)
        for study in studies:
            created_at = timezone.localtime(study.created_at).strftime("%d.%m.%Y %H:%M:%S")
            if study.created_by:
                created_by = study.created_by.first_name
            else:
                created_by = ''
            name = study.name
            company_name = company.name
            if study.research_template:
                research_template_name = study.research_template.name
            else:
                research_template_name = ''
            studies_arr.append({
                'name': name,
                'created_at': created_at,
                'created_by': created_by,
                'company_name': company_name,
                'research_template_name': research_template_name,
            })
    # if cur_user_role_name == 'Админ заказчика':
    #     company = Employee.objects.get(user=request.user).company
    #     companies = Company.objects.filter(id=company.id)
    if cur_user_role_name == 'Админ' or cur_user_role_name == 'Суперадмин':
        studies_inst = Study.objects.all()
    context.update(
        {
            'studies': studies_arr,
        }
    )

    return render(request, 'panel_companies_studies_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_study(request):
    context = info_common(request)
    cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
    if cur_user_role_name == 'Админ заказчика':
        employee = Employee.objects.get(user=request.user)
        companies = Company.objects.filter(id=employee.company.id)
        research_templates = ResearchTemplate.objects.all()

    if cur_user_role_name == 'Менеджер' or cur_user_role_name == 'Партнер':
        companies = Company.objects.filter(created_by=request.user)
        research_templates = ResearchTemplate.objects.filter(by_default=True)

    if cur_user_role_name == 'Админ' or cur_user_role_name == 'Суперадмин':
        companies = Company.objects.all()
        research_templates = ResearchTemplate.objects.all()
    individual_report_allowed_options = IndividualReportAllowedOptions.objects.all()
    context.update(
        {
            'individual_report_allowed_options': individual_report_allowed_options,
            'companies': companies,
            'research_templates': research_templates,
            'user_role': cur_user_role_name,
        }
    )

    return render(request, 'panel_add_study.html', context)


# @login_required(redirect_field_name=None, login_url='/login/')
# def add_new_research_template(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         print(json_data)
#         sections = json_data['sections']
#         template_name = json_data['template_name']
#         template_inst = ResearchTemplate()
#         template_inst.name = template_name
#         template_inst.created_by = request.user
#         template_inst.save()
#         position = 0
#         for section in sections:
#             position = position + 1
#             section_inst = Section.objects.get(id=section['section_id'])
#             template_section_inst = ResearchTemplateSections()
#             template_section_inst.section = section_inst
#             template_section_inst.research_template = template_inst
#             template_section_inst.position = position
#             template_section_inst.save()
#         return HttpResponse(status=200)
#
#

@login_required(redirect_field_name=None, login_url='/login/')
def get_company_options_allowed(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        company_individual_report_allowed_options = CompanyIndividualReportAllowedOptions.objects.filter(company_id=company_id)
        company_group_report_allowed_options = CompanyGroupReportAllowedOptions.objects.filter(company_id=company_id)
        company_individual_report_options = []
        company_group_report_options = []
        for option in company_individual_report_allowed_options:
            company_individual_report_options.append({
                'id': option.option.id,
                'name': option.option.name,
                'value': option.value,
            })
        for option in company_group_report_allowed_options:
            company_group_report_options.append({
                'id': option.option.id,
                'name': option.option.name,
                'value': option.value,
            })
        response = {
            'company_individual_report_options': company_individual_report_options,
            'company_group_report_options': company_group_report_options,

        }
        return JsonResponse({'response': response})


@login_required(redirect_field_name=None, login_url='/login/')
def get_company_employees(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        employees_inst = Employee.objects.filter(company_id=company_id)
        employees = []

        for employee in employees_inst:

            if employee.name:
                name = employee.name
            else:
                name = ''
            if employee.created_by:
                created_by = employee.created_by.first_name
                created_by_email = employee.created_by.email
            else:
                created_by = ''
                created_by_email = ''

            if employee.industry:
                employee_industry = employee.industry.name_ru
            else:
                employee_industry = ''
            if employee.role:
                employee_role = employee.role.name_ru
            else:
                employee_role = ''
            if employee.position:
                employee_position = employee.position.name_ru
            else:
                employee_position = ''
            if employee.sex:
                employee_sex = employee.sex.name_ru
            else:
                employee_sex = ''
            if employee.birth_year:
                employee_birth_year = employee.birth_year
            else:
                employee_birth_year = ''

            employees.append({
                'name': name,
                'id': employee.id,
                'email': employee.email,
                'industry': employee_industry,
                'role': employee_role,
                'position': employee_position,
                'birth_year': employee_birth_year,
                'sex': employee_sex,

                'created_by': created_by,
                'active': employee.company_admin_active,
                'created_at': timezone.localtime(employee.created_at).strftime("%d.%m.%Y %H:%M:%S"),
                'created_by_email': created_by_email
            })

            # employees.append({
            #     'id': employee.id,
            #     'name': employee.name,
            #     'sex': employee.sex.name_ru,
            #     'birth_year': employee.birth_year,
            #     'email': employee.email,
            #     'position': employee.position.name_ru,
            #     'industry': employee.industry.name_ru,
            #     'role': employee.role.name_ru,
            # })

        response = {
            'employees': employees,

        }
        return JsonResponse({'response': response})


@login_required(redirect_field_name=None, login_url='/login/')
def add_new_study(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        template_id = json_data['template_id']
        employees_ids = json_data['employees_ids']
        input_study_name = json_data['input_study_name']
        company_id = json_data['company_id']
        individual_report_allowed_options = json_data['individual_report_allowed_options']
        study_inst = Study()
        study_inst.created_by = request.user
        study_inst.name = input_study_name
        study_inst.company = Company.objects.get(id=company_id)
        study_inst.research_template = ResearchTemplate.objects.get(id=template_id)
        study_inst.save()
        for employees_id in employees_ids:
            participant_inst = Participant()
            participant_inst.created_by = request.user
            participant_inst.employee = Employee.objects.get(id=employees_id)
            participant_inst.study = study_inst
            participant_inst.save()
            for option in individual_report_allowed_options:
                participant_individual_report_allowed_options = ParticipantIndividualReportAllowedOptions()
                participant_individual_report_allowed_options.created_by = request.user
                participant_individual_report_allowed_options.participant = participant_inst
                participant_individual_report_allowed_options.option = IndividualReportAllowedOptions.objects.get(id=option['id'])
                participant_individual_report_allowed_options.value = option['value']
                participant_individual_report_allowed_options.save()
        for option in individual_report_allowed_options:
            study_individual_report_allowed_options = StudyIndividualReportAllowedOptions()
            study_individual_report_allowed_options.created_by = request.user
            study_individual_report_allowed_options.study = study_inst
            study_individual_report_allowed_options.option = IndividualReportAllowedOptions.objects.get(id=option['id'])
            study_individual_report_allowed_options.value = option['value']
            study_individual_report_allowed_options.save()

        response = {
            'status': 200,
        }
        return JsonResponse({'response': response})

