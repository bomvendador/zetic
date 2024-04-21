from pdf.models import Category, Section, ResearchTemplate, ResearchTemplateSections, Study, Company, Employee, Participant
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

    studies_inst = Study.objects.all()
    context.update(
        {
            'studies': studies_inst,
        }
    )

    return render(request, 'panel_companies_studies_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_study(request):
    context = info_common(request)
    companies = Company.objects.all()
    research_templates = ResearchTemplate.objects.all()
    context.update(
        {
            'companies': companies,
            'research_templates': research_templates,
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
def get_company_employees(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        employees_inst = Employee.objects.filter(company_id=company_id)
        employees = []
        for employee in employees_inst:
            employees.append({
                'id': employee.id,
                'name': employee.name,
                'sex': employee.sex.name_ru,
                'birth_year': employee.birth_year,
                'email': employee.email,
                'position': employee.position.name_ru,
                'industry': employee.industry.name_ru,
                'role': employee.role.name_ru,
            })
        response = {
            'employees': employees,
        }
        print(response)
        return JsonResponse({'response': response})


@login_required(redirect_field_name=None, login_url='/login/')
def add_new_study(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        template_id = json_data['template_id']
        employees_ids = json_data['employees_ids']
        input_study_name = json_data['input_study_name']
        company_id = json_data['company_id']
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
        response = {
            'status': 200,
        }
        return JsonResponse({'response': response})

