from pdf.models import Industry, EmployeeRole, EmployeePosition
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json


from .views import info_common


@login_required(redirect_field_name=None, login_url='/login/')
def industries_list(request):
    context = info_common(request)
    context.update(
        {'industries': Industry.objects.all()}
    )

    return render(request, 'panel_industries_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_industry(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name_ru = json_data['name_ru']
        name_en = json_data['name_en']

        industry_inst = Industry()
        industry_inst.name_ru = name_ru
        industry_inst.name_en = name_en
        industry_inst.created_by = request.user

        industry_inst.save()

        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_industry(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name_ru = json_data['name_ru']
        name_en = json_data['name_en']
        industry_id = json_data['id']

        industry_inst = Industry.objects.get(id=industry_id)
        industry_inst.name_ru = name_ru
        industry_inst.name_en = name_en
        industry_inst.edited_by = request.user

        industry_inst.save()

        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_industry(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        industry_id = json_data['id']
        industry_inst = Industry.objects.get(id=industry_id)
        try:
            industry_inst.delete()
            return HttpResponse(status=200)
        except Exception:
            return JsonResponse({"error": "Индустрия связана с одним из объектов и не может быть удалена"})


@login_required(redirect_field_name=None, login_url='/login/')
def employees_roles_list(request):
    context = info_common(request)
    context.update(
        {'employees_roles': EmployeeRole.objects.all()}
    )

    return render(request, 'panel_employees_roles_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_employee_role(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name_ru = json_data['name_ru']
        name_en = json_data['name_en']

        employee_role_inst = EmployeeRole()
        employee_role_inst.name_ru = name_ru
        employee_role_inst.name_en = name_en
        employee_role_inst.created_by = request.user

        employee_role_inst.save()

        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_employee_role(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name_ru = json_data['name_ru']
        name_en = json_data['name_en']
        role_id = json_data['id']

        role_inst = EmployeeRole.objects.get(id=role_id)
        role_inst.name_ru = name_ru
        role_inst.name_en = name_en
        role_inst.edited_by = request.user

        role_inst.save()

        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_employee_role(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        role_id = json_data['id']
        role_inst = EmployeeRole.objects.get(id=role_id)
        try:
            role_inst.delete()
            return HttpResponse(status=200)
        except Exception:
            return JsonResponse({"error": "Роль/функция связана с одним из объектов и не может быть удалена"})


@login_required(redirect_field_name=None, login_url='/login/')
def employees_positions_list(request):
    context = info_common(request)
    context.update(
        {'employees_positions': EmployeePosition.objects.all()}
    )

    return render(request, 'panel_employees_positions_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_employee_position(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name_ru = json_data['name_ru']
        name_en = json_data['name_en']
        print(json_data)
        employee_position_inst = EmployeePosition()
        employee_position_inst.name_ru = name_ru
        employee_position_inst.name_en = name_en
        employee_position_inst.created_by = request.user

        employee_position_inst.save()

        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_employee_position(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name_ru = json_data['name_ru']
        name_en = json_data['name_en']
        position_id = json_data['id']

        employee_position_inst = EmployeePosition.objects.get(id=position_id)
        employee_position_inst.name_ru = name_ru
        employee_position_inst.name_en = name_en
        employee_position_inst.edited_by = request.user

        employee_position_inst.save()

        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_employee_position(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        position_id = json_data['id']
        employee_position_inst = EmployeePosition.objects.get(id=position_id)
        try:
            employee_position_inst.delete()
            return HttpResponse(status=200)
        except Exception:
            return JsonResponse({"error": "Должность связана с одним из объектов и не может быть удалена"})

