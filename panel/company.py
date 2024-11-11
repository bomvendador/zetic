from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, ResearchTemplate, \
    CompanySelfQuestionnaireLink, EmployeeGender, Questionnaire, Study, Participant, CommonBooleanSettings, \
    CompanyReportMadeNotificationReceivers, ConsultantCompany, ConsultantStudy, IndividualReportAllowedOptions, \
    CompanyIndividualReportAllowedOptions, GroupReportAllowedOptions, CompanyGroupReportAllowedOptions, \
    StudyIndividualReportAllowedOptions, ParticipantIndividualReportAllowedOptions
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
from django.core.mail import send_mail
from smtplib import SMTPException, SMTPRecipientsRefused
from django.utils.html import strip_tags
from django.template.loader import render_to_string


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
        name = json_data['name'].strip()
        demo_limit = json_data['demo_limit']
        active = json_data['active']
        print(json_data)

        # demo_status = json_data['demo_status']
        companies_existing = Company.objects.filter(name=name)
        if companies_existing.exists():
            response = {
                'error': 'Компания с таким именем уже существует',
            }
            return JsonResponse(response)
        else:
            company_inst = Company()
            company_inst.name = name
            if not demo_limit == '':
                company_inst.demo_status_questionnaires_limit = demo_limit
            company_inst.created_by = request.user
            public_code = generate_code(8)
            company_inst.public_code = public_code
            if active == 1:
                company_inst.active = True
            else:
                company_inst.active = False
            if 'demo_status' in json_data:
                company_inst.demo_status = json_data['demo_status']
            company_inst.save()
            individual_report_options_allowed = IndividualReportAllowedOptions.objects.all()
            for option in individual_report_options_allowed:
                company_individual_report_options_allowed = CompanyIndividualReportAllowedOptions()
                company_individual_report_options_allowed.company = company_inst
                company_individual_report_options_allowed.option = option
                company_individual_report_options_allowed.created_by = request.user
                company_individual_report_options_allowed.save()
            group_report_options_allowed = GroupReportAllowedOptions.objects.all()
            for option in group_report_options_allowed:
                company_group_report_options_allowed = CompanyGroupReportAllowedOptions()
                company_group_report_options_allowed.company = company_inst
                company_group_report_options_allowed.option = option
                company_group_report_options_allowed.created_by = request.user
                company_group_report_options_allowed.save()

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
def add_report_made_notification_receiver(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        employee_id = json_data['employee_id']
        employee_inst = Employee.objects.get(id=employee_id)
        receiver_inst = CompanyReportMadeNotificationReceivers()
        receiver_inst.created_by = request.user
        receiver_inst.employee = employee_inst
        receiver_inst.company = employee_inst.company
        receiver_inst.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_report_made_notification_receiver(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        receiver_id = json_data['receiver_id']
        CompanyReportMadeNotificationReceivers.objects.get(id=receiver_id).delete()
        return HttpResponse(status=200)


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
    employees_available_report_made_notification_receivers = []
    employees = Employee.objects.filter(company=company_inst)
    for employee in employees:
        receiver = CompanyReportMadeNotificationReceivers.objects.filter(employee=employee)
        if not receiver.exists():
            employees_available_report_made_notification_receivers.append({
                'id': employee.id,
                'name': employee.name,
                'email': employee.email,
            })
    consultants = ConsultantCompany.objects.filter(company=company_inst)
    consultants_studies = ConsultantStudy.objects.filter(consultant_company__company=company_inst)
    company_individual_report_options_allowed = CompanyIndividualReportAllowedOptions.objects.filter(company=company_inst)
    individual_report_options_allowed = IndividualReportAllowedOptions.objects.all()
    if individual_report_options_allowed.exists() and not company_individual_report_options_allowed.exists():
        for option in individual_report_options_allowed:
            company_individual_report_options_allowed = CompanyIndividualReportAllowedOptions()
            company_individual_report_options_allowed.company = company_inst
            company_individual_report_options_allowed.option = option
            company_individual_report_options_allowed.created_by = request.user
            company_individual_report_options_allowed.save()

    company_group_report_options_allowed = CompanyGroupReportAllowedOptions.objects.filter(company=company_inst)
    group_report_options_allowed = GroupReportAllowedOptions.objects.all()
    if group_report_options_allowed.exists() and not company_group_report_options_allowed.exists():
        for option in group_report_options_allowed:
            company_group_report_options_allowed = CompanyGroupReportAllowedOptions()
            company_group_report_options_allowed.company = company_inst
            company_group_report_options_allowed.option = option
            company_group_report_options_allowed.created_by = request.user
            company_group_report_options_allowed.save()
    context.update(
        {
            'company_group_report_options_allowed': CompanyGroupReportAllowedOptions.objects.filter(company=company_inst),
            'company_individual_report_options_allowed': CompanyIndividualReportAllowedOptions.objects.filter(company=company_inst),
            'company': company_inst,
            'employees': Employee.objects.filter(company=company_inst),
            'admins': Employee.objects.filter(company=company_inst, company_admin=True),
            'templates': templates,
            'links': company_self_questionnaire_links_inst,
            'report_made_notification_receivers': CompanyReportMadeNotificationReceivers.objects.filter(company=company_inst),
            'employees_available_report_made_notification_receivers': employees_available_report_made_notification_receivers,
            'consultants': consultants,
            'consultants_studies': consultants_studies
        }
    )

    return render(request, 'panel_edit_company.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def get_available_consultants(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        consultants_all = UserProfile.objects.filter(role__name='Консультант')
        consultants_available = ConsultantCompany.objects.filter(~Q(company_id=company_id))

        consultants = []
        for consultant in consultants_all:
            if not ConsultantCompany.objects.filter(Q(user=consultant.user) & Q(company_id=company_id)).exists():
                consultants.append({
                    'user_id': consultant.user.id,
                    'name': consultant.user.first_name,
                    'email': consultant.user.email
                })
        print(consultants)
        result = {
            'consultants': consultants
        }
        return JsonResponse(result)


@login_required(redirect_field_name=None, login_url='/login/')
def get_available_consultant_company_studies(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        consultant_company_id = json_data['consultant_company_id']
        consultant_company_inst = ConsultantCompany.objects.get(id=consultant_company_id)
        company_studies = Study.objects.filter(company=consultant_company_inst.company)
        studies = []
        for company_study in company_studies:
            if not ConsultantStudy.objects.filter(Q(study=company_study) & Q(consultant_company=consultant_company_inst)).exists():
                studies.append({
                    'id': company_study.id,
                    'name': company_study.name,
                })
        result = {
            'studies': studies,
            'consultant_company_id': consultant_company_id
        }
        return JsonResponse(result)


@login_required(redirect_field_name=None, login_url='/login/')
def add_consultant_study_for_company(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        study_id = json_data['study_id']
        consultant_company_id = json_data['consultant_company_id']
        consultant_study = ConsultantStudy()
        consultant_study.created_by = request.user
        consultant_study.study = Study.objects.get(id=study_id)
        consultant_study.consultant_company = ConsultantCompany.objects.get(id=consultant_company_id)
        consultant_study.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_consultant_study_from_company(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        consultant_study_id = json_data['consultant_study_id']
        ConsultantStudy.objects.get(id=consultant_study_id).delete()
        return HttpResponse(status=200)



@login_required(redirect_field_name=None, login_url='/login/')
def add_consultant_for_company(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        user_id = json_data['user_id']
        consultant_company = ConsultantCompany()
        consultant_company.created_by = request.user
        consultant_company.user = User.objects.get(id=user_id)
        consultant_company.company = Company.objects.get(id=company_id)
        consultant_company.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_consultant_fromm_company(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        consultant_company_id = json_data['consultant_company_id']
        ConsultantCompany.objects.get(id=consultant_company_id).delete()
        return HttpResponse(status=200)


# @login_required(redirect_field_name=None, login_url='/login/')
# def add_consultant_study_for_company(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         company_id = json_data['company_id']
#         user_id = json_data['user_id']
#         consultant_company = ConsultantCompany()
#         consultant_company.created_by = request.user
#         consultant_company.user = User.objects.get(id=user_id)
#         consultant_company.company = Company.objects.get(id=company_id)
#         consultant_company.save()
#         return HttpResponse(status=200)


def company_questionnaire(request, code):
    company_self_questionnaire_link_inst = CompanySelfQuestionnaireLink.objects.get(code=code)
    company_inst = company_self_questionnaire_link_inst.company
    company_questionnaires_qnt = len(Questionnaire.objects.filter(participant__employee__company=company_inst))
    demo_status_for_companies_setting = CommonBooleanSettings.objects.get(name='Демо-режимы для компаний').value
    if company_inst.demo_status_questionnaires_limit <= company_questionnaires_qnt:
        questionnaires_left = 0
    else:
        questionnaires_left = company_inst.demo_status_questionnaires_limit - company_questionnaires_qnt
    if questionnaires_left == 0 and company_inst.demo_status and demo_status_for_companies_setting:
        if not request.user.is_authenticated:
            subject = f'Превышение лимита для ссылки (компания - {company_inst.id}. {company_inst.name}'
            context = {
                'company': company_inst,
                'company_questionnaires_qnt': company_questionnaires_qnt,
            }
            html_message = render_to_string('notification_company_questionnaire_limit_error_.html', context)
            # print(f'company_questionnaires_qnt = {company_questionnaires_qnt}')
            plain_text = strip_tags(html_message)
            from_email = 'ZETIC <info@zetic.ru>'
            to_email = 'info@zetic.ru'

            try:
                send_mail(
                    subject,
                    plain_text,
                    from_email,
                    [to_email],
                    html_message=html_message
                )
            except SMTPRecipientsRefused as e:
                print(e)
        return render(request, 'panel_company_questionnaire_participant_data_limit_error.html')
    else:
        years = []
        current_year = datetime.now().year
        for i in range(1960, current_year - 18 + 1):
            years.append(i)
        context = {
            'gender': EmployeeGender.objects.all(),
            'roles': EmployeeRole.objects.all(),
            'industries': Industry.objects.all(),
            'positions': EmployeePosition.objects.all(),
            'years': years,
            'company': company_self_questionnaire_link_inst.company,
            'code': code,
        }
        return render(request, 'panel_company_questionnaire_participant_data.html', context)


def create_self_questionnaire(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        data = json_data['data']
        email = data['email']
        company_id = data['company_id']
        hostname = data['hostname']
        protocol = data['protocol']
        company = Company.objects.get(id=company_id)
        employees_inst = Employee.objects.filter(Q(email=email))
        # print(json_data)
        if employees_inst.exists():
            response = {
                'error': 'Сотрудник с таким Email уже существует',
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

            individual_report_allowed_options = IndividualReportAllowedOptions.objects.all()
            for option in individual_report_allowed_options:
                study_individual_report_allowed_options = StudyIndividualReportAllowedOptions()
                study_individual_report_allowed_options.study = new_study
                study_individual_report_allowed_options.option = option
                study_individual_report_allowed_options.save()

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

            for option in individual_report_allowed_options:
                participant_individual_report_allowed_options = ParticipantIndividualReportAllowedOptions()
                participant_individual_report_allowed_options.participant = new_participant
                participant_individual_report_allowed_options.option = option
                participant_individual_report_allowed_options.save()

            new_questionnaire_inst = Questionnaire()
            new_questionnaire_inst.data_filled_up_by_participant = True
            new_questionnaire_inst.participant = new_participant
            new_questionnaire_inst.save()
            send_email_by_email_type_var = send_email_by_email_type(new_study.id, [{'id': new_participant.id}], 'self_questionnaire', 1, protocol, hostname)
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
        demo_limit = json_data['demo_limit']
        company_inst = Company.objects.get(id=company_id)
        company_inst.name = company_name
        if active == 1:
            company_inst.active = True
        else:
            company_inst.active = False
        if 'demo_status' in json_data:
            company_inst.demo_status = json_data['demo_status']
        if not demo_limit == '':
            company_inst.demo_status_questionnaires_limit = demo_limit
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


@login_required(redirect_field_name=None, login_url='/login/')
def update_company_report_options_allowed(request):
    if request.method == 'PUT':
        json_data = json.loads(request.body.decode('utf-8'))
        options_vals = json_data['options_vals']
        change_participants_individual_report_options = json_data['change_participants_individual_report_options']
        company_id = json_data['company_id']
        company_ist = Company.objects.get(id=company_id)
        print(json_data)
        for option in options_vals:
            option_type = option['type']
            option_id = option['id']
            option_val = option['value']
            if option_type == 'individual':
                # company_option = CompanyIndividualReportAllowedOptions.objects.get(Q(company_id=company_id) &
                #                                                                    Q(option_id=option_id))
                company_option = CompanyIndividualReportAllowedOptions.objects.get(id=option_id)
            else:
                company_option = CompanyGroupReportAllowedOptions.objects.get(id=option_id)
                # company_option = CompanyGroupReportAllowedOptions.objects.get(Q(company_id=company_id) &
                #                                                                    Q(option_id=option_id))
            company_option.value = option_val
            company_option.save()
            if change_participants_individual_report_options:
                study_individual_report_allowed_options = StudyIndividualReportAllowedOptions.objects.filter(Q(study__company=company_ist) &
                                                                                                             Q(option=company_option.option))
                if study_individual_report_allowed_options.exists():
                    for study_individual_option in study_individual_report_allowed_options:
                        study_individual_option.value = option_val
                        study_individual_option.save()
                participants = Participant.objects.filter(Q(employee__company=company_ist) &
                                                          Q(completed_at__isnull=True))
                if participants.exists():
                    for participant in participants:
                        print(f'part id = {participant.id}')
                        participant_individual_report_allowed_options = ParticipantIndividualReportAllowedOptions.objects.filter(Q(participant=participant) &
                                                                                                                                 Q(option=company_option.option))
                        for participant_individual_option in participant_individual_report_allowed_options:
                            participant_individual_option.value = option_val
                            participant_individual_option.save()

        return HttpResponse(status=200)





