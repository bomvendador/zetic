from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone
from login.models import UserRole, UserProfile, User
from panel.custom_funcs import generate_code
from api.outcoming import sync_add_company

from .views import info_common


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
    context.update(
        {
            'company': company_inst,
            'admins': Employee.objects.filter(company=company_inst, company_admin=True)
        }
    )

    return render(request, 'panel_edit_company.html', context)


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





