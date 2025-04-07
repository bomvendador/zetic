from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, User, Participant, EmployeeGender, \
    Project, ProjectParticipants, Questionnaire, Report, QuestionnaireVisits, UserCompanies,\
    CompanyReportMadeNotificationReceivers, ReportGroup, ReportGroupSquare, ConsultantForm, ProjectStudy,\
    EmployeeCompanyChangeEvent, Study
from login.models import UserProfile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from reports import settings
import json
from django.utils import timezone
import requests

from .views import info_common
from api.outcoming import Attributes, sync_add_employee
from .custom_funcs import update_attributes
from django.db.models import Sum, Q

from django.template.loader import render_to_string

import xlsxwriter
from datetime import date, time


@login_required(redirect_field_name=None, login_url='/login/')
def add_employee(request):
    context = info_common(request)
    cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
    if cur_user_role_name == 'Менеджер' or cur_user_role_name == 'Партнер':
        companies = Company.objects.filter(created_by=request.user)
    else:
        if cur_user_role_name == 'Админ' or cur_user_role_name == 'Суперадмин':
            companies = Company.objects.all()
        else:
            if cur_user_role_name == 'Админ заказчика':
                employee = Employee.objects.get(user=request.user)
                companies = Company.objects.filter(id=employee.company.id)
    user_companies = UserCompanies.objects.filter(user=request.user)

    sex = []
    positions = []
    industries = []
    roles = []
    for item in EmployeeGender.objects.all():
        sex.append({
            'id': item.id,
            'name_ru': item.name_ru
        })
    for item in EmployeeRole.objects.all():
        roles.append({
            'id': item.id,
            'name_ru': item.name_ru
        })
    for item in EmployeePosition.objects.all():
        positions.append({
            'id': item.id,
            'name_ru': item.name_ru
        })
    for item in Industry.objects.all():
        industries.append({
            'id': item.id,
            'name_ru': item.name_ru
        })

    # for role in roles:

    context.update({
        'companies': companies,
        'employee_positions': positions,
        'employee_roles': roles,
        'industries': industries,
        'genders': sex,
        'user_companies': user_companies
    })

    response = render(request, 'employee/panel_add_employee.html', context)
    response['Cache-Control'] = 'no-cache'
    return response


@login_required(redirect_field_name=None, login_url='/login/')
def get_company_employees(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        company_id = json_data['company_id']
        employees = Employee.objects.filter(company_id=company_id)
        employees_arr = []
        for employee in employees:
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

            employees_arr.append({
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
        response = {
            'data': list(employees_arr)
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def get_employee_data(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        employee_id = json_data['employee_id']
        employee = Employee.objects.get(id=employee_id)
        if employee.name:
            name = employee.name
        else:
            name = ''
        if employee.sex:
            gender = {
                'name_ru': employee.sex.name_ru,
                'id': 'gender_id_' + str(employee.sex.id),
            }
        else:
            gender = ''
        if not employee.birth_year is None:
            birth_year = employee.birth_year
        else:
            birth_year = ''

        if employee.role:
            role = {
                'name_ru': employee.role.name_ru,
                'id': 'role_id_' + str(employee.role.id),
            }
        else:
            role = ''
        if employee.position:
            position = {
                'name_ru': employee.position.name_ru,
                'id': 'position_id_' + str(employee.position.id),
            }
        else:
            position = ''
        if employee.industry:
            industry = {
                'name_ru': employee.industry.name_ru,
                'id': 'industry_id_' + str(employee.industry.id),
            }
        else:
            industry = ''

        response = {
            'name': name,
            'email': employee.email,
            'gender': gender,
            'birth_year': birth_year,
            'role': role,
            'position': position,
            'industry': industry
        }
        print(response)
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_employee(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        employee_id = json_data['employee_id']
        employee = Employee.objects.get(id=employee_id)
        employee_created_participant = False
        employee_is_participant = Participant.objects.filter(employee=employee).exists()
        if employee.user is not None:
            employee_created_participant = Participant.objects.filter(created_by=employee.user).exists()
        response = {}
        errors = []
        if employee_is_participant:
            errors.append('Сотрудник является участником опросника')
        if employee_created_participant:
            errors.append('Сотрудником были созданы участники опросника')
        if len(errors) > 0:
            response.update({
                'errors': errors
            })
        else:
            if employee.user:
                employee.user.delete()
            employee.delete()
            response.update({
                'result': 'ok',
            })
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_employee_xls(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        employees = json_data['employees']
        company_id = json_data['company_id']
        existing_employees = []
        cnt = 0
        for employee in employees:
            email = employee['E-mail']
            if not is_employee_already_exists(email):
                cnt = cnt + 1
                employee_inst = Employee()
                employee_inst.email = email
                employee_inst.name = employee['ФИО/псевдоним']
                if 'Год рождения' in employee:
                    employee_inst.birth_year = employee['Год рождения']
                if 'Роль' in employee:
                    employee_inst.role = EmployeeRole.objects.filter(name_ru=employee['Роль'])[0]
                if 'Должность' in employee:
                    employee_inst.position = EmployeePosition.objects.filter(name_ru=employee['Должность'])[0]
                if 'Индустрия' in employee:
                    employee_inst.industry = Industry.objects.filter(name_ru=employee['Индустрия'])[0]
                if 'Пол' in employee:
                    employee_inst.sex = EmployeeGender.objects.get(name_ru=employee['Пол'])
                # try:
                #     employee_inst.name = employee['Фамилия Имя (или псевдоним по выбору участника)']
                # except KeyError:
                #     pass
                employee_inst.company = Company.objects.get(id=company_id)
                employee_inst.created_by = request.user
                employee_inst.save()
            else:
                existing_employees.append(email)

        if len(existing_employees) > 0:
            emails = list(existing_employees)
        else:
            emails = 'None'
        response = {
            'emails': emails,
            'cnt': cnt
        }
        return JsonResponse(response)


def is_employee_already_exists(email):
    if Employee.objects.filter(email=email).exists():
        return True
    else:
        return False


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_employee_html(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        employee_data = json_data['employee_data']
        # print('-----employee data------')
        # print(json_data)
        # print(employee_data)
        email = employee_data['email']
        check_passed = True
        if 'employee_id' in employee_data:
            employee_inst = Employee.objects.get(id=employee_data['employee_id'])
            request_type = 'edit'
        else:
            employee_inst = Employee()
            request_type = 'add'
            if is_employee_already_exists(email):
                check_passed = False

        if check_passed:
            if 'company_id' in json_data:
                company_id = json_data['company_id']
                employee_inst.company = Company.objects.get(id=company_id)
                employee_inst.created_by = request.user
            employee_inst.name = employee_data['name']
            employee_inst.email = employee_data['email']
            if 'role_id' in employee_data:
                employee_inst.role = EmployeeRole.objects.get(id=employee_data['role_id'])
            if 'position_id' in employee_data:
                employee_inst.position = EmployeePosition.objects.get(id=employee_data['position_id'])
            if 'industry_id' in employee_data:
                employee_inst.industry = Industry.objects.get(id=employee_data['industry_id'])
            if 'gender_id' in employee_data:
                employee_inst.sex = EmployeeGender.objects.get(id=employee_data['gender_id'])
            if not employee_data['employee_birth_year'] == '':
                employee_inst.birth_year = employee_data['employee_birth_year']
            employee_inst.save()

            # sync_add_employee.delay(employee_inst.id)
            return HttpResponse(status=200)
        else:
            return HttpResponse('email exists')


@login_required(redirect_field_name=None, login_url='/login/')
def employees_list(request):
    context = info_common(request)
    cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
    if cur_user_role_name == 'Менеджер' or cur_user_role_name == 'Партнер':
        companies = Company.objects.filter(created_by=request.user)
    if cur_user_role_name == 'Админ заказчика':
        employee = Employee.objects.get(user=request.user)
        companies = Company.objects.filter(id=employee.company.id)
    if cur_user_role_name == 'Админ' or cur_user_role_name == 'Суперадмин':
        companies = Company.objects.all()
    user_companies = UserCompanies.objects.filter(user=request.user)
    sex = []
    positions = []
    industries = []
    roles = []

    for item in EmployeeGender.objects.all():
        sex.append({
            'id': 'gender_id_' + str(item.id),
            'name_ru': item.name_ru
        })
    for item in EmployeeRole.objects.all():
        roles.append({
            'id': 'role_id_' + str(item.id),
            'name_ru': item.name_ru
        })
    for item in EmployeePosition.objects.all():
        positions.append({
            'id': 'position_id_' + str(item.id),
            'name_ru': item.name_ru
        })
    for item in Industry.objects.all():
        industries.append({
            'id': 'industry_id_' + str(item.id),
            'name_ru': item.name_ru
        })

    context.update(
        {
            'companies': companies,
            'user_companies': user_companies,
            'employees': Employee.objects.all(),
            'employee_positions': positions,
            'employee_roles': roles,
            'industries': industries,
            'genders': sex
        }
    )

    return render(request, 'employee/panel_employees_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def get_company_no_admins(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        company_id = json_data['company_id']
        employees = Employee.objects.filter(company_id=company_id, company_admin=False)
        employees_arr = []
        for employee in employees:
            if employee.name:
                name = employee.name
            else:
                name = ''
            if employee.created_by:
                created_by = employee.created_by.first_name
            else:
                created_by = ''
            employees_arr.append({
                'name': name,
                'id': employee.id,
                'email': employee.email,
                'active': employee.company_admin_active,
            })
        response = {
            'data': list(employees_arr)
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def deactivate_company_admin(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        employee_id = json_data['employee_id']
        operation_type = json_data['operation_type']
        employee = Employee.objects.get(id=employee_id)
        if operation_type == 'deactivate':
            employee.company_admin_active = False
        else:
            employee.company_admin_active = True
        employee.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_company_admin(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        employee_id = json_data['employee_id']
        employee = Employee.objects.get(id=employee_id)
        employee.company_admin_active = False
        employee.company_admin = False
        employee.user.delete()
        employee.user = None
        employee.save()

        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def check_employee_before_company_change(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        employee_id = json_data['employee_id']
        company = Employee.objects.get(id=employee_id).company
        employee_instances = []
        if CompanyReportMadeNotificationReceivers.objects.filter(Q(employee_id=employee_id) & Q(company=company)).exists():
            employee_instances.append('Получатель уведомления о созданном отчете')

        if Participant.objects.filter(Q(employee_id=employee_id)).exists():
            if Report.objects.filter(participant__employee_id=employee_id):
                employee_instances.append('Личный отчет')
            if ReportGroupSquare.objects.filter(report__participant__employee_id=employee_id).exists():
                employee_instances.append('Командный отчет')
            if Questionnaire.objects.filter(participant__employee_id=employee_id).exists():
                employee_instances.append('Опросник')
            if ProjectStudy.objects.filter(study__participant__employee_id=employee_id).exists():
                employee_instances.append('Проект')
            if ConsultantForm.objects.filter(user__participant__employee_id=employee_id).exists():
                employee_instances.append('Анкета консультанта')
        print(employee_instances)
        response = {
            'employee_instances': employee_instances
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def get_available_employee_companies(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        employee_id = json_data['employee_id']
        available_companies = []
        companies = []
        cur_employee_company = Employee.objects.get(id=employee_id).company
        cur_user_role_name = UserProfile.objects.get(user=request.user).role.name

        user_companies = UserCompanies.objects.filter(Q(user=request.user) &
                                                      ~Q(company=cur_employee_company))
        user_companies_ids = []
        for user_company in user_companies:
            user_companies_ids.append(user_company.company.id)
            available_companies.append({
                'id': user_company.company.id,
                'name': user_company.company.name
            })

        if cur_user_role_name == 'Менеджер' or cur_user_role_name == 'Партнер':
            if len(user_companies_ids) > 0:
                companies = Company.objects.filter(Q(created_by=request.user) &
                                                   ~Q(id=cur_employee_company.id) &
                                                   ~Q(id__in=user_companies_ids))
            else:
                companies = Company.objects.filter(Q(created_by=request.user) &
                                                   ~Q(id=cur_employee_company.id))

        if cur_user_role_name == 'Админ' or cur_user_role_name == 'Суперадмин':
            if len(user_companies_ids) > 0:
                companies = Company.objects.filter(~Q(id=cur_employee_company.id) &
                                                   ~Q(id__in=user_companies_ids))
            else:
                companies = Company.objects.filter(~Q(id=cur_employee_company.id))

        for company in companies:
            available_companies.append({
                'id': company.id,
                'name': company.name
            })
        response = {
            'available_companies': available_companies
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def set_new_employee_company(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        employee_id = json_data['employee_id']
        company_id = json_data['company_id']
        company = Company.objects.get(id=company_id)
        employee = Employee.objects.get(id=employee_id)
        employee_previous_company = employee.company
        employee.company = company
        employee.save()
        if CompanyReportMadeNotificationReceivers.objects.filter(Q(employee_id=employee_id) & Q(company=company)).exists():
            company_report_made_notification_receivers = CompanyReportMadeNotificationReceivers.objects.filter(Q(employee_id=employee_id) & Q(company=company))
            for receiver in company_report_made_notification_receivers:
                receiver.company = company
                receiver.save()
        event = EmployeeCompanyChangeEvent()
        event.created_by = request.user
        event.employee = employee
        event.employee_previous_company = employee_previous_company
        event.employee_mew_company = employee.company
        event.save(0)
        employee_participants = Participant.objects.filter(employee=employee)
        for participant in employee_participants:
            new_study = Study()
            new_study.created_by = request.user
            new_study.company = company
            new_study.research_template = participant.study.research_template
            new_study.name = f'{participant.employee.name} ({participant.employee.email}) перенесен(а) из компании {employee_previous_company.name}'
            new_study.invitation_message_text = participant.study.invitation_message_text
            new_study.reminder_message_text = participant.study.reminder_message_text
            new_study.save()
            if 'Создано сотрудником' in participant.study.name or 'перенесен(а) из компании' in participant.study.name:
                participant.study.delete()
            participant.study = new_study
            participant.save()
            individual_reports = Report.objects.filter(participant=participant)
            for report in individual_reports:
                report.study = new_study
                report.save()
                ReportGroupSquare.objects.filter(report=report).delete()
        return HttpResponse(status=200)


def download_add_employee_template(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        employees_quantity = json_data['employees_quantity']
        file_name = f'Шаблон_для_добавления_сотрудников ({employees_quantity} чел.).xlsx'
        workbook = xlsxwriter.Workbook(f"media/files/{file_name}")
        workbook.set_properties({
            'company': 'Zetic'
        })

        worksheet_data = workbook.add_worksheet('Data')

        header_format = workbook.add_format(
            {
                "border": 1,
                "bg_color": "#0d6efd",
                "font_color": "white",
                "bold": True,
                "text_wrap": True,
                "valign": "vcenter",
                "align": "center",
                "indent": 1,
            }
        )

        # Set up layout of the worksheet.
        worksheet_data.set_column("A:A", 40)
        worksheet_data.set_column("B:B", 20)
        worksheet_data.set_column("C:C", 20)
        worksheet_data.set_column("D:D", 20)
        worksheet_data.set_column("E:E", 20)
        worksheet_data.set_column("F:F", 20)
        worksheet_data.set_column("G:G", 20)
        worksheet_data.set_row(0, 36)

        # Write the header cells and some data that will be used in the examples.
        heading1 = "Роль"
        heading2 = "Должность"
        heading3 = "Индустрия"
        heading4 = "Год рождения"

        worksheet_data.write("A1", heading1, header_format)
        worksheet_data.write("B1", heading2, header_format)
        worksheet_data.write("C1", heading3, header_format)
        worksheet_data.write("D1", heading4, header_format)

        roles = EmployeeRole.objects.all()
        cnt = 1

        for item in roles:
            cnt += 1
            worksheet_data.write("A" + repr(cnt), item.name_ru)
        a_cnt = cnt

        industries = Industry.objects.all()
        cnt = 1
        for item in industries:
            cnt += 1
            worksheet_data.write("C" + repr(cnt), item.name_ru)
        c_cnt = cnt

        positions = EmployeePosition.objects.all()
        cnt = 1
        for item in positions:
            cnt += 1
            worksheet_data.write("B" + repr(cnt), item.name_ru)
        b_cnt = cnt

        cnt = 1
        for i in range(1940, 2010):
            cnt += 1
            worksheet_data.write("D" + repr(cnt), i)
        d_cnt = cnt

        worksheet_data.hide()

        worksheet_employees = workbook.add_worksheet('Сотрудники')

        # Set up layout of the worksheet.
        worksheet_employees.set_column("A:A", 5)
        worksheet_employees.set_column("B:B", 40)
        worksheet_employees.set_column("C:C", 20)
        worksheet_employees.set_column("D:D", 20)
        worksheet_employees.set_column("E:E", 20)
        worksheet_employees.set_column("F:F", 20)
        worksheet_employees.set_column("G:G", 20)
        worksheet_employees.set_column("H:H", 20)
        worksheet_employees.set_row(0, 20)

        # Write the header cells and some data that will be used in the examples.
        heading0 = "#"
        heading1 = "ФИО/псевдоним"
        heading2 = "E-mail"
        heading3 = "Роль"
        heading4 = "Должность"
        heading5 = "Индустрия"
        heading6 = "Пол"
        heading7 = "Год рождения"

        worksheet_employees.write("A1", heading0, header_format)
        worksheet_employees.write("B1", heading1, header_format)
        worksheet_employees.write("C1", heading2, header_format)
        worksheet_employees.write("D1", heading3, header_format)
        worksheet_employees.write("E1", heading4, header_format)
        worksheet_employees.write("F1", heading5, header_format)
        worksheet_employees.write("G1", heading6, header_format)
        worksheet_employees.write("H1", heading7, header_format)

        for row_number in range(2, int(employees_quantity) + 2):
            worksheet_employees.write("A" + repr(row_number), row_number - 1)
            worksheet_employees.data_validation(
                "G" + repr(row_number), {"validate": "list", "source": ['Мужской', 'Женский']}
            )
            worksheet_employees.data_validation("D" + repr(row_number), {"validate": "list", "source": "=Data!$A$2:$A" + repr(a_cnt)})
            worksheet_employees.data_validation("F" + repr(row_number), {"validate": "list", "source": "=Data!$C$2:$C" + repr(c_cnt)})
            worksheet_employees.data_validation("E" + repr(row_number), {"validate": "list", "source": "=Data!$B$2:$B" + repr(b_cnt)})
            worksheet_employees.data_validation("H" + repr(row_number), {"validate": "list", "source": "=Data!$D$2:$D" + repr(d_cnt)})

        worksheet_employees.activate()

        workbook.close()
        response = {
            'file_name': file_name
        }
        return JsonResponse(response)
