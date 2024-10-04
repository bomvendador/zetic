from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, User, Participant, EmployeeGender, \
    Project, Study, ProjectStudy, TrafficLightReportFilter, TrafficLightReportFilterCategory
from login.models import UserProfile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from reports import settings
import json
from django.utils import timezone
import requests
from django.template.loader import render_to_string

from .views import info_common
from api.outcoming import Attributes, sync_add_employee
from .custom_funcs import update_attributes


@login_required(redirect_field_name=None, login_url='/login/')
def get_company_projects(request):
    if request.method == 'POST':
        context = info_common(request)
        json_data = json.loads(request.body.decode('utf-8'))

        company_id = json_data['company_id']
        company_projects_inst = Project.objects.filter(company_id=company_id)
        if company_projects_inst.exists():
            projects = company_projects_inst
            context.update(
                {
                    'projects': projects,
                }
            )
            response = render_to_string('projects/panel_company_projects_rows.html', context)
        else:
            response = 'no_projects'
        print(response)
        return HttpResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def get_company_studies(request):
    if request.method == 'POST':
        context = info_common(request)
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        studies_inst = Study.objects.filter(company_id=company_id)
        if studies_inst.exists():
            # studies = studies_inst
            context.update(
                {
                    'studies': studies_inst,
                }
            )
            response = render_to_string('projects/panel_company_studies_rows.html', context)
        else:
            response = 'no_studies'
        return HttpResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_project(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        study_ids = json_data['study_ids']
        name = json_data['name']
        company_id = json_data['company_id']
        project_inst = Project()
        project_inst.created_by = request.user
        project_inst.name = name
        project_inst.company = Company.objects.get(id=company_id)
        project_inst.save()
        for study_id in study_ids:
            project_study = ProjectStudy()
            project_study.created_by = request.user
            project_study.study = Study.objects.get(id=study_id)
            project_study.project = project_inst
            project_study.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def save_edited_project(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        study_ids = json_data['study_ids']
        name = json_data['name']
        project_id = json_data['project_id']
        project_inst = Project.objects.get(id=project_id)
        project_inst.name = name
        project_inst.save()
        ProjectStudy.objects.filter(project=project_inst).delete()
        for study_id in study_ids:
            project_study = ProjectStudy()
            project_study.created_by = request.user
            project_study.study = Study.objects.get(id=study_id)
            project_study.project = project_inst
            project_study.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def projects_list(request):
    context = info_common(request)
    cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
    if cur_user_role_name == 'Менеджер' or cur_user_role_name == 'Партнер':
        companies_inst = Company.objects.filter(created_by=request.user)
    else:
        companies_inst = Company.objects.all()
    companies = []
    for company in companies_inst:
        projects = Project.objects.filter(company=company)
        if projects.exists():
            companies.append({
                'name': company.name,
                'id': company.id,
                'active': company.active,
            })

    # if cur_user_role_name == 'Менеджер':
    #     companies = Company.objects.filter(created_by=request.user)
    # if cur_user_role_name == 'Админ' or cur_user_role_name == 'Суперадмин':
    #     companies = Company.objects.all()
    context.update(
        {
            'companies': companies,
        }
    )

    return render(request, 'projects/panel_projects_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_new_project(request):
    context = info_common(request)
    cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
    if cur_user_role_name == 'Менеджер' or cur_user_role_name == 'Партнер':
        companies = Company.objects.filter(created_by=request.user)

    if cur_user_role_name == 'Админ' or cur_user_role_name == 'Суперадмин':
        companies = Company.objects.all().order_by('name')
    companies_for_projects = []
    for company in companies:
        studies = Study.objects.filter(company=company)
        if studies.exists():
            companies_for_projects.append({
                'id': company.id,
                'name': company.name,
                'active': company.active,
            })
    context.update(
        {
            'companies': companies_for_projects,
        }
    )
    print(companies)
    return render(request, 'projects/panel_add_project.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_project(request, project_id):
    context = info_common(request)
    # cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
    project = Project.objects.get(id=project_id)
    studies = ProjectStudy.objects.filter(project=project)
    filters_inst = TrafficLightReportFilter.objects.filter(project=project).order_by('position')
    filters_categories = TrafficLightReportFilterCategory.objects.filter(filter__project=project)

    context.update(
        {
            'project': project,
            'studies': studies,
            'filters': filters_inst,
            'filters_categories': filters_categories
        }
    )
    return render(request, 'projects/panel_edit_project.html', context)


