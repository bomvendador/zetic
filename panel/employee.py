from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, User, Participant, EmployeeGender, \
    Project, ProjectParticipants, Questionnaire, Report
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
    # try:
    #     response = requests.get(settings.API_LINK + 'attributes',
    #                             headers={'Authorization': 'Bearer ' + settings.API_BEARER}).json()
    #     update_attributes(request, response)
    #     sex = response['sex']
    #     positions = response['position']
    #     industries = response['industry']
    #     roles = response['role']
    #
    # except ValueError:
    #     sex = []
    #     positions = []
    #     industries = []
    #     roles = []
    #     for item in EmployeeGender.objects.all():
    #         sex.append({
    #             'id': item.public_code,
    #             'name_ru': item.name_ru
    #         })
    #     for item in EmployeeRole.objects.all():
    #         roles.append({
    #             'id': item.public_code,
    #             'name_ru': item.name_ru
    #         })
    #     for item in EmployeePosition.objects.all():
    #         positions.append({
    #             'id': item.public_code,
    #             'name_ru': item.name_ru
    #         })
    #     for item in Industry.objects.all():
    #         industries.append({
    #             'id': item.public_code,
    #             'name_ru': item.name_ru
    #         })

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

    print(positions)
    print(industries)
    print(roles)
    # for role in roles:

    context.update({
        'companies': companies,
        'employee_positions': positions,
        'employee_roles': roles,
        'industries': industries,
        'genders': sex
    })

    return render(request, 'employee/panel_add_employee.html', context)


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

        response = {
            'name': name,
            'email': employee.email,
            'gender': {
                'name_ru': employee.sex.name_ru,
                'id': 'gender_id_' + str(employee.sex.id),
                       },
            'birth_year': employee.birth_year,
            'role': {
                'name_ru': employee.role.name_ru,
                'id': 'role_id_' + str(employee.role.id),
                       },
            'position': {
                'name_ru': employee.position.name_ru,
                'id': 'position_id_' + str(employee.position.id),
                       },
            'industry': {
                'name_ru': employee.industry.name_ru,
                'id': 'industry_id_' + str(employee.industry.id),
                       }
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_employee(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        employee_id = json_data['employee_id']
        employee = Employee.objects.get(id=employee_id)
        print(json_data)
        employee_created_participant = False
        employee_is_participant = Participant.objects.filter(employee=employee).exists()
        if employee.user is not None:
            employee_created_participant = Participant.objects.filter(created_by=employee.user).exists()
            print(Participant.objects.filter(created_by=employee.user).count())
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
            email = employee['E-mail для приглашений']
            if not is_employee_already_exists(email):
                cnt = cnt + 1
                employee_inst = Employee()
                employee_inst.email = email
                employee_inst.birth_year = employee['Год рождения']
                employee_inst.role = employee['Роль']
                employee_inst.position = employee['Должность']
                employee_inst.industry = employee['Индустрия']
                employee_inst.sex = employee['Пол']
                try:
                    employee_inst.name = employee['Фамилия Имя (или псевдоним по выбору участника)']
                except KeyError:
                    pass
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
        print('-----employee data------')
        print(json_data)
        print(employee_data)
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
    # try:
    #     response = requests.get(settings.API_LINK + 'attributes',
    #                             headers={'Authorization': 'Bearer ' + settings.API_BEARER}).json()
    #     update_attributes(request, response)
    #     sex = response['sex']
    #     positions = response['position']
    #     industries = response['industry']
    #     roles = response['role']
    #
    # except ValueError:
    #     sex = []
    #     positions = []
    #     industries = []
    #     roles = []
    #     for item in EmployeeGender.objects.all():
    #         sex.append({
    #             'id': item.public_code,
    #             'name_ru': item.name_ru
    #         })
    #     for item in EmployeeRole.objects.all():
    #         roles.append({
    #             'id': item.public_code,
    #             'name_ru': item.name_ru
    #         })
    #     for item in EmployeePosition.objects.all():
    #         positions.append({
    #             'id': item.public_code,
    #             'name_ru': item.name_ru
    #         })
    #     for item in Industry.objects.all():
    #         industries.append({
    #             'id': item.public_code,
    #             'name_ru': item.name_ru
    #         })

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
            'employees': Employee.objects.all(),
            'employee_positions': positions,
            'employee_roles': roles,
            'industries': industries,
            'genders': sex
        }
    )

    return render(request, 'employee/panel_employees_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def employees_search(request):
    context = info_common(request)

    context.update(
        {
        }
    )

    return render(request, 'employee/panel_employees_search.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def search_for_employees(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        fio = json_data['fio']
        email = json_data['email']
        if not fio == '' and not email == '':
            employees_inst = Employee.objects.filter(Q(name=fio) & Q(email=email))
        elif not fio == '':
            employees_inst = Employee.objects.filter(Q(name=fio))
        else:
            employees_inst = Employee.objects.filter(Q(email=email))
        data = []
        for employee in employees_inst:
            employee_data = {
                'name': employee.name,
                'email': employee.email,
                'company_name': employee.company.name,
            }
            participants = Participant.objects.filter(employee=employee)
            projects = []
            questionnaires = []
            reports_dates = []
            reports_files = []
            for participant in participants:
                project_participants_inst = ProjectParticipants.objects.filter(participant=participant)
                for project_participant in project_participants_inst:
                    projects.append(project_participant.project.name)
                questionnaires_inst = Questionnaire.objects.filter(participant=participant)
                for questionnaire in questionnaires_inst:
                    questionnaires.append(timezone.localtime(questionnaire.created_at).strftime("%d.%m.%Y %H:%M:%S"))
                reports_inst = Report.objects.filter(participant=participant)
                for report in reports_inst:
                    reports_dates.append(timezone.localtime(report.added).strftime("%d.%m.%Y %H:%M:%S"))
                    reports_files.append(report.file.name)

            employee_data.update({
                'projects': projects,
                'questionnaires': questionnaires,
                'reports_dates': reports_dates,
                'reports_files': reports_files
            })
            data.append(employee_data)
        rows = render_to_string('employee/tr_employee_search.html', {'data': data}).rstrip()
        return JsonResponse({'rows': rows})


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


