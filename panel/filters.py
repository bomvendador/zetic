from pdf.models import Category, Section, ResearchTemplate, ResearchTemplateSections, Study, Company, Employee, \
    Industry, EmployeePosition, EmployeeRole, AgeGenderGroup, RawToTPointsType, RawToTPoints
from login.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone
from django.core import serializers

from .views import info_common
from api import outcoming

from django.utils.dateformat import DateFormat
from django.core.exceptions import ObjectDoesNotExist


@login_required(redirect_field_name=None, login_url='/login/')
def filters_list(request):
    context = info_common(request)

    filters_inst = RawToTPointsType.objects.all()
    context.update(
        {
            'filters': filters_inst,
        }
    )

    return render(request, 'panel_filters_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_filter(request):
    context = info_common(request)
    industries = Industry.objects.all()
    positions = EmployeePosition.objects.all()
    roles = EmployeeRole.objects.all()
    ages_genders = AgeGenderGroup.objects.all()
    sections = Section.objects.all()
    categories = Category.objects.all()
    # default_filter_inst = RawToTPointsType.objects.filter(is_default=True)
    numbers = []
    for i in range(1, 36):
        numbers.append(i)
    # numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
    context.update(
        {
            'industries': industries,
            'positions': positions,
            'roles': roles,
            'ages_genders': ages_genders,
            'sections': sections,
            'categories': categories,
            'numbers': numbers,
            # 'default_filters_cnt': len(default_filter_inst),
        }
    )

    return render(request, 'panel_add_filter.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_edited_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        is_default = json_data['is_default']
        name = json_data['name']
        filter_id = json_data['filter_id']
        raw_to_tpoints_type = RawToTPointsType.objects.get(id=filter_id)
        raw_to_tpoints_type.name_ru = name
        raw_to_tpoints_type.created_by = request.user
        age_gender_id = json_data['age_gender_id']
        raw_to_tpoints_type.age_gender_group = AgeGenderGroup.objects.get(id=age_gender_id)

        if is_default:
            raw_to_tpoints_type.is_default = True
        else:
            industry_id = json_data['industry_id']
            position_id = json_data['position_id']
            role_id = json_data['role_id']

            raw_to_tpoints_type.industry = Industry.objects.get(id=industry_id)
            raw_to_tpoints_type.employee_position = EmployeePosition.objects.get(id=position_id)
            raw_to_tpoints_type.employee_role = EmployeeRole.objects.get(id=role_id)
        raw_to_tpoints_type.save()
        filter_data = json_data['filter_data']
        for data in filter_data:
            category_id = data['category_id']
            raw_points = data['raw_points']
            t_points = data['t_points']
            raw_point_id = data['raw_point_id']
            raw_to_tpoints = RawToTPoints.objects.get(id=raw_point_id)
            raw_to_tpoints.category = Category.objects.get(id=category_id)
            raw_to_tpoints.t_point = t_points
            raw_to_tpoints.raw_points = raw_points
            raw_to_tpoints.type = raw_to_tpoints_type
            raw_to_tpoints.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_filter_from_file(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        is_default = json_data['is_default']
        name = json_data['name']
        age_gender_id = json_data['age_gender_id']

        filter_data = json_data['filter_data']
        errors = {}
        wrong_codes = []
        codes_ok = True
        filter_exists = False
        for data in filter_data:
            try:
                category_inst = Category.objects.get(code=data['Код'])
            except ObjectDoesNotExist:
                codes_ok = False
                wrong_codes.append(data['Код'])
        if not codes_ok:
            errors.update({
                'wrong_codes': wrong_codes
            })
        if RawToTPointsType.objects.filter(age_gender_group_id=age_gender_id, is_default=is_default):
            if is_default:
                filter_exists = True
                errors.update({
                    'filter_exists': True
                })
            else:
                if RawToTPointsType.objects.filter(industry_id=json_data['industry_id'],
                                                   employee_role_id=json_data['role_id'],
                                                   employee_position=json_data['position_id']):
                    filter_exists = True
                    errors.update({
                        'filter_exists': True
                    })

        if codes_ok and not filter_exists:
            raw_to_tpoints_type = RawToTPointsType()
            raw_to_tpoints_type.name_ru = name
            raw_to_tpoints_type.created_by = request.user
            raw_to_tpoints_type.age_gender_group = AgeGenderGroup.objects.get(id=age_gender_id)
            if is_default:
                raw_to_tpoints_type.is_default = True
            else:
                industry_id = json_data['industry_id']
                position_id = json_data['position_id']
                role_id = json_data['role_id']

                raw_to_tpoints_type.industry = Industry.objects.get(id=industry_id)
                raw_to_tpoints_type.employee_position = EmployeePosition.objects.get(id=position_id)
                raw_to_tpoints_type.employee_role = EmployeeRole.objects.get(id=role_id)
            raw_to_tpoints_type.save()

            for data in filter_data:
                category_inst = Category.objects.get(code=data['Код'])
                for key in data:
                    if not key == 'Код' and not key == 'Шкала':
                        print(f'{key} - {data[key]}')
                        raw_to_tpoints = RawToTPoints()
                        raw_to_tpoints.category = category_inst
                        raw_to_tpoints.t_point = data[key]
                        raw_to_tpoints.raw_points = key
                        raw_to_tpoints.type = raw_to_tpoints_type
                        raw_to_tpoints.save()
        else:
            return JsonResponse({'error': errors})

            # category_id = data['category_id']
            # raw_points = data['raw_points']
            # t_points = data['t_points']
            # raw_to_tpoints = RawToTPoints()
            # raw_to_tpoints.category = Category.objects.get(id=category_id)
            # raw_to_tpoints.t_point = t_points
            # raw_to_tpoints.raw_points = raw_points
            # raw_to_tpoints.type = raw_to_tpoints_type
            # raw_to_tpoints.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        filter_id = json_data['filter_id']

        try:
            RawToTPointsType.objects.get(id=filter_id).delete()
            return HttpResponse(status=200)
        except Exception:
            return JsonResponse({"error": "Фильтр связан с одним из объектов и не может быть удален"})


@login_required(redirect_field_name=None, login_url='/login/')
def edit_filter(request, filter_id):
    context = info_common(request)
    filter_inst = RawToTPointsType.objects.get(id=filter_id)
    raw_to_tpoint_inst = RawToTPoints.objects.filter(type=filter_inst)
    industries = Industry.objects.all()
    positions = EmployeePosition.objects.all()
    roles = EmployeeRole.objects.all()
    ages_genders = AgeGenderGroup.objects.all()
    sections = Section.objects.all()
    categories = Category.objects.all()
    raw_points = []
    for raw_point in raw_to_tpoint_inst:
        raw_points.append({
            'category_id': raw_point.category.id,
            'raw_point': raw_point.raw_points,
            't_point': raw_point.t_point,
            'raw_point_id': raw_point.id,
        })
    numbers = []
    for i in range(0, 36):
        numbers.append(i)

    context.update(
        {
            'filter': filter_inst,
            'raw_to_tpoint': raw_to_tpoint_inst,
            'numbers': numbers,
            'industries': industries,
            'positions': positions,
            'roles': roles,
            'ages_genders': ages_genders,
            'sections': sections,
            'categories': categories,
            'raw_points': raw_points,

        }
    )
    return render(request, 'panel_edit_filter.html', context)

#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def get_company_employees(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         company_id = json_data['company_id']
#         employees_inst = Employee.objects.filter(company_id=company_id)
#         employees = []
#         for employee in employees_inst:
#             employees.append({
#                 'id': employee.id,
#                 'name': employee.name,
#                 'sex': employee.sex.name_ru,
#                 'birth_year': employee.birth_year,
#                 'email': employee.email,
#                 'position': employee.position.name_ru,
#                 'industry': employee.industry.name_ru,
#                 'role': employee.role.name_ru,
#             })
#         response = {
#             'employees': employees,
#         }
#         print(response)
#         return JsonResponse({'response': response})
#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def add_new_study(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         template_id = json_data['template_id']
#         employees_ids = json_data['employees_ids']
#         input_study_name = json_data['input_study_name']
#         company_id = json_data['company_id']
#         study_inst = Study()
#         study_inst.created_by = request.user
#         study_inst.name = input_study_name
#         study_inst.company = Company.objects.get(id=company_id)
#         study_inst.research_template = ResearchTemplate.objects.get(id=template_id)
#         study_inst.save()
#         for employees_id in employees_ids:
#             participant_inst = Participant()
#             participant_inst.created_by = request.user
#             participant_inst.employee = Employee.objects.get(id=employees_id)
#             participant_inst.study = study_inst
#             participant_inst.save()
#         response = {
#             'status': 200,
#         }
#         return JsonResponse({'response': response})
#
