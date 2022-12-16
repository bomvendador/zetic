from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone
from login.models import UserRole, UserProfile, User

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
        print(json_data)
        company_inst = Company()
        company_inst.name = name
        company_inst.created_by = request.user
        if active == 1:
            company_inst.active = True
        else:
            company_inst.active = False

        company_inst.save()

        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def companies_list(request):
    context = info_common(request)
    context.update(
        {
            'companies': Company.objects.all(),
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
        print(json_data)
        employee_id = json_data['employee_id']
        employee = Employee.objects.get(id=employee_id)
        employee.company_admin = True
        employee.company_admin_active = True
        employee.save()

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
