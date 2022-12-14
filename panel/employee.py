from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone

from .views import info_common


@login_required(redirect_field_name=None, login_url='/login/')
def add_employee(request):
    context = info_common(request)
    context.update({
        'companies': Company.objects.all(),
        'employee_positions': EmployeePosition.objects.all(),
        'employee_roles': EmployeeRole.objects.all(),
        'industries': Industry.objects.all()
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
            employees_arr.append({
                'name': name,
                'id': employee.id,
                'email': employee.email,
                'created_by': employee.created_by.first_name,
                'created_at': timezone.localtime(employee.created_at).strftime("%Y-%m-%d %H:%M:%S"),
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
            'role': employee.role.name_ru,
            'position': employee.position.name_ru,
            'industry': employee.industry.name_ru,
        }
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
                employee_inst.role = EmployeeRole.objects.get(name_ru=employee['Роль'])
                employee_inst.position = EmployeePosition.objects.get(name_ru=employee['Должность'])
                employee_inst.industry = Industry.objects.get(name_ru=employee['Индустрия'])
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
            employee_inst.role = EmployeeRole.objects.get(id=employee_data['role_id'])
            employee_inst.position = EmployeePosition.objects.get(id=employee_data['position_id'])
            employee_inst.industry = Industry.objects.get(id=employee_data['industry_id'])
            employee_inst.sex = employee_data['gender']
            employee_inst.birth_year = employee_data['employee_birth_year']
            employee_inst.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse('email exists')


@login_required(redirect_field_name=None, login_url='/login/')
def employees_list(request):
    context = info_common(request)
    context.update(
        {
            'companies': Company.objects.all(),
            'employees': Employee.objects.all(),
            'employee_positions': EmployeePosition.objects.all(),
            'employee_roles': EmployeeRole.objects.all(),
            'industries': Industry.objects.all()
        }
    )

    return render(request, 'panel_employees_list.html', context)



