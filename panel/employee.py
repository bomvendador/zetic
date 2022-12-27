from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, User, Participant
from login.models import UserProfile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone

from .views import info_common
from api.outcoming import Attributes


@login_required(redirect_field_name=None, login_url='/login/')
def add_employee(request):
    context = info_common(request)
    cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
    if cur_user_role_name == 'Менеджер':
        companies = Company.objects.filter(created_by=request.user)
    else:
        companies = Company.objects.all()

    context.update({
        'companies': companies,
        'employee_positions': Attributes.get_positions(),
        'employee_roles': Attributes.get_roles(),
        'industries': Attributes.get_industries(),
        'genders': Attributes.get_sex()
    })

    return render(request, 'panel_add_employee.html', context)


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
            employees_arr.append({
                'name': name,
                'id': employee.id,
                'email': employee.email,
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
            'gender': employee.sex,
            'birth_year': employee.birth_year,
            'role': employee.role,
            'position': employee.position,
            'industry': employee.industry,
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
            employee_inst.role = employee_data['role_id']
            employee_inst.position = employee_data['position_id']
            employee_inst.industry = employee_data['industry_id']
            employee_inst.sex = employee_data['gender']
            employee_inst.birth_year = employee_data['employee_birth_year']
            employee_inst.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse('email exists')


@login_required(redirect_field_name=None, login_url='/login/')
def employees_list(request):
    context = info_common(request)
    cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
    if cur_user_role_name == 'Менеджер':
        companies = Company.objects.filter(created_by=request.user)
    else:
        companies = Company.objects.all()

    context.update(
        {
            'companies': companies,
            'employees': Employee.objects.all(),
            'employee_positions': Attributes.get_positions(),
            'employee_roles': Attributes.get_roles(),
            'industries': Attributes.get_industries(),
            'genders': Attributes.get_sex()
        }
    )

    return render(request, 'panel_employees_list.html', context)


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


