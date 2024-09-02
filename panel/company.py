from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, ResearchTemplate, \
    CompanySelfQuestionnaireLink, EmployeeGender, Questionnaire, Study, Participant
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone
from login.models import UserRole, UserProfile, User
from panel.custom_funcs import generate_code
from api.outcoming import sync_add_company

from .views import info_common

from .mail_handler import generate_participant_link_code
from django.db.models import Sum, Q

from datetime import datetime

from .mail_handler import generate_participant_link_code, send_email_by_email_type


@login_required(redirect_field_name=None, login_url='/login/')
def add_company_init(request):
    context = info_common(request)
    context.update({
        'roles': UserRole.objects.all()
    })

    return render(request, 'panel_add_company.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_company(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name = json_data['name']
        active = json_data['active']
        # print(json_data)
        companies_existing = Company.objects.filter(name=name)
        if companies_existing.exists():
            response = {
                'error': 'Компания с таким именем уже существует',
            }
            return JsonResponse(response)
        else:
            company_inst = Company()
            company_inst.name = name
            company_inst.created_by = request.user
            public_code = generate_code(8)
            company_inst.public_code = public_code
            if active == 1:
                company_inst.active = True
            else:
                company_inst.active = False

            company_inst.save()

            # response = sync_add_company.delay(name, public_code)

            return HttpResponse(status=200)
            # return HttpResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def generate_new_self_questionnaire_link(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        template_id = json_data['template_id']
        # print(json_data)
        company_self_questionnaire_link = CompanySelfQuestionnaireLink()
        company_self_questionnaire_link.created_by = request.user
        company_self_questionnaire_link.company = Company.objects.get(id=company_id)
        company_self_questionnaire_link.research_template = ResearchTemplate.objects.get(id=template_id)
        code = generate_participant_link_code(20)
        company_self_questionnaire_link.code = code
        company_self_questionnaire_link.save()
        response = {
            'code': code,
        }
        return JsonResponse(response)
        # return HttpResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def companies_list(request):
    context = info_common(request)
    cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
    if cur_user_role_name == 'Менеджер' or cur_user_role_name == 'Партнер':
        companies = Company.objects.filter(created_by=request.user)
    else:
        companies = Company.objects.all()
    context.update(
        {
            'companies': companies,
         }
    )

    return render(request, 'panel_companies_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_company(request, company_id):
    context = info_common(request)
    company_inst = Company.objects.get(id=company_id)
    company_self_questionnaire_links_inst = CompanySelfQuestionnaireLink.objects.filter(company=company_inst)
    templates = []
    templates_inst = ResearchTemplate.objects.all()
    for template in templates_inst:
        link_is_used = False
        for link in company_self_questionnaire_links_inst:
            if link.research_template == template:
                link_is_used = True
        if not link_is_used:
            templates.append({
                'id': template.id,
                'name': template.name,
            })

    context.update(
        {
            'company': company_inst,
            'admins': Employee.objects.filter(company=company_inst, company_admin=True),
            'templates': templates,
            'links': company_self_questionnaire_links_inst,
        }
    )

    return render(request, 'panel_edit_company.html', context)


def company_questionnaire(request, code):
    context = info_common(request)
    company_self_questionnaire_link_inst = CompanySelfQuestionnaireLink.objects.get(code=code)
    years = []
    current_year = datetime.now().year
    for i in range(1960, current_year - 18 + 1):
        years.append(i)
    context.update({
        'gender': EmployeeGender.objects.all(),
        'roles': EmployeeRole.objects.all(),
        'industries': Industry.objects.all(),
        'positions': EmployeePosition.objects.all(),
        'years': years,
        'company': company_self_questionnaire_link_inst.company,
        'code': code,
    })
    return render(request, 'panel_company_questionnaire_participant_data.html', context)


def create_self_questionnaire(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        data = json_data['data']
        email = data['email']
        company_id = data['company_id']
        company = Company.objects.get(id=company_id)
        employees_inst = Employee.objects.filter(Q(email=email))
        if employees_inst.exists():
            response = {
                'error': 'Сотрудник с таким Email  уже существует',
            }
            return JsonResponse(response)
        else:
            year = data['year']
            code = data['code']
            gender = data['gender']
            name = data['name']
            role_id = data['role_id']
            position_id = data['position_id']
            industry_id = data['industry_id']

            company_self_questionnaire_link_inst = CompanySelfQuestionnaireLink.objects.get(code=code)

            new_employee_inst = Employee()
            new_employee_inst.email = email
            new_employee_inst.name = name
            new_employee_inst.birth_year = year
            new_employee_inst.role = EmployeeRole.objects.get(id=role_id)
            new_employee_inst.position = EmployeePosition.objects.get(id=position_id)
            new_employee_inst.industry = Industry.objects.get(id=industry_id)
            new_employee_inst.role = EmployeeRole.objects.get(id=role_id)
            new_employee_inst.sex = EmployeeGender.objects.get(name_en=gender)
            new_employee_inst.company = company
            new_employee_inst.save()

            new_study = Study()
            new_study.company = company
            new_study.research_template = company_self_questionnaire_link_inst.research_template
            new_study.name = f'Создано сотрудником {name} ({email})'
            new_study.save()

            new_participant = Participant()
            new_participant.employee = new_employee_inst
            new_participant.tos_accepted = True
            new_participant.study = new_study
            new_participant.invitation_sent = True
            new_participant.invitation_sent_datetime = datetime.now()
            new_participant.send_report_to_participant_after_filling_up = True
            new_participant.send_admin_notification_after_filling_up = True
            # new_participant.total_questions_qnt =
            participant_code = generate_participant_link_code(20)
            new_participant.invitation_code = participant_code
            new_participant.save()

            new_questionnaire_inst = Questionnaire()
            new_questionnaire_inst.data_filled_up_by_participant = True
            new_questionnaire_inst.participant = new_participant
            new_questionnaire_inst.save()

            # print(data)
            send_email_by_email_type_var = send_email_by_email_type(new_study.id, [{'id': new_participant.id}], 'self_questionnaire', 1, 1)
            print(send_email_by_email_type_var)

            new_participant.total_questions_qnt = send_email_by_email_type_var['participant_total_questions']
            new_participant.save()

            response = {
                'code': participant_code,
            }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def appoint_company_admin(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        employee_id = json_data['employee_id']
        password = json_data['password']
        employee = Employee.objects.get(id=employee_id)
        employee.company_admin = True
        employee.company_admin_active = True

        new_user = User()
        new_user.first_name = employee.name
        new_user.email = employee.email
        new_user.set_password(password)
        new_user.username = employee.email
        new_user.save()

        employee.user = new_user
        employee.save()

        new_user_profile = UserProfile()
        new_user_profile.created_by = request.user
        new_user_profile.user = new_user
        new_user_profile.role = UserRole.objects.get(name='Админ заказчика')
        new_user_profile.fio = employee.name
        new_user_profile.save()


        if employee.name:
            name = employee.name
        else:
            name = ''
        response = {
            'name': name,
            'email': employee.email,
            'id': employee.id,
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def update_company(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        company_name = json_data['company_name']
        active = json_data['active']
        company_inst = Company(id=company_id)
        company_inst.name = company_name
        if active == 1:
            company_inst.active = True
        else:
            company_inst.active = False

        company_inst.save()

        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_company(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        company_inst = Company(id=company_id)
        company_inst.delete()
        return HttpResponse(status=200)





