from pdf.models import Category, Section, ResearchTemplate, ResearchTemplateSections, Study, Company, Employee, \
    Industry, EmployeePosition, EmployeeRole, AgeGenderGroup, RawToTPointsType, RawToTPoints, MatrixFilter, \
    MatrixFilterCategory, MatrixFilterInclusiveEmployeePosition, MatrixFilterParticipantNotDistributed, \
    MatrixFilterParticipantNotDistributedEmployeePosition
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

from .custom_funcs import squares_data

def get_available_squares():
    matrix_filters = MatrixFilter.objects.all()
    squares_available = []
    for square in squares_data:
        square_is_in_filter = False
        if matrix_filters:
            for matrix_filter in matrix_filters:
                if matrix_filter.square_code == square['code']:
                    square_is_in_filter = True
        if not square_is_in_filter:
            squares_available.append(square)
    return squares_available


def get_available_squares_for_participant_not_distributed_filter():
    matrix_filters = MatrixFilterParticipantNotDistributed.objects.all()
    squares_available = []
    for square in squares_data:
        square_is_in_filter = False
        if matrix_filters:
            for matrix_filter in matrix_filters:
                if matrix_filter.square_code == square['code']:
                    square_is_in_filter = True
        if not square_is_in_filter:
            squares_available.append(square)
    return squares_available


def get_available_positions_for_participant_not_distributed_filter():
    matrix_filter_positions = MatrixFilterParticipantNotDistributedEmployeePosition.objects.all()
    positions = EmployeePosition.objects.all()
    positions_available = []
    for position in positions:
        position_is_in_filter = False
        for filter_position in matrix_filter_positions:
            if position == filter_position.employee_position:
                position_is_in_filter = True
        if not position_is_in_filter:
            positions_available.append({
                'id': position.id,
                'name': position.name_ru
            })
    return positions_available


@login_required(redirect_field_name=None, login_url='/login/')
def filters_list(request):
    context = info_common(request)

    filters_inst = MatrixFilter.objects.all()
    squares_available = get_available_squares()
    if len(squares_available) > 0:
        no_available_squares = 0
    else:
        no_available_squares = 1

    filters_participant_not_distributed_inst = MatrixFilterParticipantNotDistributed.objects.all()
    positions_available = get_available_positions_for_participant_not_distributed_filter()
    if len(positions_available) > 0:
        no_available_positions = 0
    else:
        no_available_positions = 1



    context.update(
        {
            'filters': filters_inst,
            'no_available_squares': no_available_squares,
            'filters_participant_not_distributed': filters_participant_not_distributed_inst,
            'no_available_positions': no_available_positions,
        }
    )

    return render(request, 'panel_filters_matrix_list.html', context)


# squares_data = [
#     {
#         'code': '1_1',
#         'square_name': 'ИНТЕГРАТОРЫ',
#         'square_role_name': 'Магнит'
#     },
#     {
#         'code': '1_2',
#         'square_name': 'ИНТЕГРАТОРЫ',
#         'square_role_name': 'Фасилитатор'
#     },
#     {
#         'code': '1_3',
#         'square_name': 'ИНТЕГРАТОРЫ',
#         'square_role_name': 'Переговорщик'
#     },
#     {
#         'code': '1_4',
#         'square_name': 'ИНТЕГРАТОРЫ',
#         'square_role_name': 'Коннектор'
#     },
#     {
#         'code': '2_1',
#         'square_name': 'ПРЕДПРИНИМАТЕЛИ',
#         'square_role_name': 'Визионер'
#     },
#     {
#         'code': '2_2',
#         'square_name': 'ПРЕДПРИНИМАТЕЛИ',
#         'square_role_name': 'Авантюрист'
#     },
#     {
#         'code': '2_3',
#         'square_name': 'ПРЕДПРИНИМАТЕЛИ',
#         'square_role_name': 'Искатель ресурсов'
#     },
#     {
#         'code': '2_4',
#         'square_name': 'ПРЕДПРИНИМАТЕЛИ',
#         'square_role_name': 'Изобретатель'
#     },
#     {
#         'code': '3_1',
#         'square_name': 'АДМИНИСТРАТОРЫ',
#         'square_role_name': 'Хранитель'
#     },
#     {
#         'code': '3_2',
#         'square_name': 'АДМИНИСТРАТОРЫ',
#         'square_role_name': 'Вдохновитель'
#     },
#     {
#         'code': '3_3',
#         'square_name': 'АДМИНИСТРАТОРЫ',
#         'square_role_name': 'Контролер'
#     },
#     {
#         'code': '3_4',
#         'square_name': 'АДМИНИСТРАТОРЫ',
#         'square_role_name': 'Благородный служитель'
#     },
#     {
#         'code': '4_1',
#         'square_name': 'ПРОИЗВОДИТЕЛИ',
#         'square_role_name': 'Организатор'
#     },
#     {
#         'code': '4_2',
#         'square_name': 'ПРОИЗВОДИТЕЛИ',
#         'square_role_name': 'Любитель улучшений'
#     },
#     {
#         'code': '4_3',
#         'square_name': 'ПРОИЗВОДИТЕЛИ',
#         'square_role_name': 'Реализатор'
#     },
#     {
#         'code': '4_4',
#         'square_name': 'ПРОИЗВОДИТЕЛИ',
#         'square_role_name': 'Решатель проблем'
#     },
# ]


@login_required(redirect_field_name=None, login_url='/login/')
def add_filter(request):
    context = info_common(request)
    categories_arr = []
    categories = Category.objects.all()
    for category in categories:
        if not category.for_validity:
            categories_arr.append({
                'id': category.id,
                'code': category.code,
                'category_name': category.name,
                'section_name': category.section.name
            })
    positions_arr = []
    positions = EmployeePosition.objects.all()
    for position in positions:
        positions_arr.append({
            'name': position.name_ru,
            'id': position.id,
        })

    # default_filter_inst = RawToTPointsType.objects.filter(is_default=True)
    squares_available = get_available_squares()
    if len(squares_available) > 0:
        context.update(
            {
                'squares_available': squares_available,
                'positions': positions_arr,
                'categories': categories_arr,
            }
        )

        return render(request, 'panel_add_filter_matrix.html', context)
    else:
        filters_inst = MatrixFilter.objects.all()
        context.update(
            {
                'filters': filters_inst,
                'no_available_squares': 1
            }
        )

        return render(request, 'panel_filters_matrix_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_filter_participant_not_distributed(request):
    context = info_common(request)
    # positions_arr = []
    positions = get_available_positions_for_participant_not_distributed_filter()
    # for position in positions:
    #     positions_arr.append({
    #         'name': position.name_ru,
    #         'id': position.id,
    #     })

    # default_filter_inst = RawToTPointsType.objects.filter(is_default=True)
    squares_available = get_available_squares_for_participant_not_distributed_filter()
    context.update(
        {
            'squares_available': squares_available,
            'positions': positions,
        }
    )

    return render(request, 'panel_add_filter_matrix_for_participants_not_distributed.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_matrix_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        categories = json_data['categories']
        positions = json_data['positions']
        square = json_data['square']
        matrix_filter_inst = MatrixFilter()
        matrix_filter_inst.square_name = square['name']
        matrix_filter_inst.square_code = square['code']
        matrix_filter_inst.created_by = request.user
        matrix_filter_inst.save()
        for category in categories:
            category_inst = Category.objects.get(id=category['category_id'])
            matrix_category_inst = MatrixFilterCategory()
            matrix_category_inst.created_by = request.user
            matrix_category_inst.category = category_inst
            matrix_category_inst.matrix_filter = matrix_filter_inst
            matrix_category_inst.points_from = category['points_from']
            matrix_category_inst.points_to = category['points_to']
            matrix_category_inst.save()
        for position in positions:
            position_inst = EmployeePosition.objects.get(id=position)
            matrix_position_inst = MatrixFilterInclusiveEmployeePosition()
            matrix_position_inst.created_by = request.user
            matrix_position_inst.matrix_filter = matrix_filter_inst
            matrix_position_inst.employee_position = position_inst
            matrix_position_inst.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_matrix_filter(request, filter_id):
    context = info_common(request)
    matrix_filter = MatrixFilter.objects.get(id=filter_id)
    filter_categories = MatrixFilterCategory.objects.filter(matrix_filter=matrix_filter)
    filter_positions = MatrixFilterInclusiveEmployeePosition.objects.filter(matrix_filter=matrix_filter)

    categories_arr = []
    categories = Category.objects.all()
    for category in categories:
        if not category.for_validity:
            categories_arr.append({
                'id': category.id,
                'code': category.code,
                'category_name': category.name,
                'section_name': category.section.name
            })
    positions_arr = []
    positions = EmployeePosition.objects.all()
    for position in positions:
        positions_arr.append({
            'name': position.name_ru,
            'id': position.id,
        })

    all_matrix_filters = MatrixFilter.objects.all()
    squares_available = []
    for square in squares_data:
        square_is_in_filter = False
        if all_matrix_filters:
            for matrix_filter_from_all in all_matrix_filters:
                if matrix_filter_from_all.square_code == square['code']:
                    square_is_in_filter = True
        if square_is_in_filter is False or matrix_filter.square_code == square['code']:
            squares_available.append(square)
    if len(squares_available) > 0:
        context.update(
            {
                'squares_available': squares_available,
                'positions': positions_arr,
                'categories': categories_arr,
            }
        )

    context.update(
        {
            'matrix_filter': matrix_filter,
            'filter_categories': filter_categories,
            'filter_positions': filter_positions,
        }
    )
    return render(request, 'panel_edit_filter_matrix.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_edited_matrix_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        filter_id = json_data['filter_id']
        categories = json_data['categories']
        positions = json_data['positions']
        square = json_data['square']
        matrix_filter_inst = MatrixFilter.objects.get(id=filter_id)
        matrix_filter_inst.square_name = square['name']
        matrix_filter_inst.square_code = square['code']
        matrix_filter_inst.created_by = request.user
        matrix_filter_inst.save()
        MatrixFilterCategory.objects.filter(matrix_filter=matrix_filter_inst).delete()
        for category in categories:
            category_inst = Category.objects.get(id=category['category_id'])
            matrix_category_inst = MatrixFilterCategory()
            matrix_category_inst.created_by = request.user
            matrix_category_inst.category = category_inst
            matrix_category_inst.matrix_filter = matrix_filter_inst
            matrix_category_inst.points_from = category['points_from']
            matrix_category_inst.points_to = category['points_to']
            matrix_category_inst.save()

        MatrixFilterInclusiveEmployeePosition.objects.filter(matrix_filter=matrix_filter_inst).delete()
        for position in positions:
            position_inst = EmployeePosition.objects.get(id=position)
            matrix_position_inst = MatrixFilterInclusiveEmployeePosition()
            matrix_position_inst.created_by = request.user
            matrix_position_inst.matrix_filter = matrix_filter_inst
            matrix_position_inst.employee_position = position_inst
            matrix_position_inst.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_matrix_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        filter_id = json_data['filter_id']
        MatrixFilter.objects.get(id=filter_id).delete()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_matrix_filter_for_participants_not_distributed(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        positions = json_data['positions']
        square = json_data['square']
        matrix_filter_inst = MatrixFilterParticipantNotDistributed()
        matrix_filter_inst.square_name = square['name']
        matrix_filter_inst.square_code = square['code']
        matrix_filter_inst.created_by = request.user
        matrix_filter_inst.save()
        for position in positions:
            position_inst = EmployeePosition.objects.get(id=position)
            matrix_position_inst = MatrixFilterParticipantNotDistributedEmployeePosition()
            matrix_position_inst.created_by = request.user
            matrix_position_inst.matrix_filter = matrix_filter_inst
            matrix_position_inst.employee_position = position_inst
            matrix_position_inst.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_matrix_filter_for_participants_not_distributed(request, filter_id):
    context = info_common(request)
    matrix_filter = MatrixFilterParticipantNotDistributed.objects.get(id=filter_id)
    filter_positions = MatrixFilterParticipantNotDistributedEmployeePosition.objects.filter(matrix_filter=matrix_filter)
    positions_arr = []
    positions = EmployeePosition.objects.all()
    for position in positions:
        positions_arr.append({
            'name': position.name_ru,
            'id': position.id,
        })

    all_matrix_filters = MatrixFilterParticipantNotDistributed.objects.all()
    squares_available = []
    for square in squares_data:
        square_is_in_filter = False
        if all_matrix_filters:
            for matrix_filter_from_all in all_matrix_filters:
                if matrix_filter_from_all.square_code == square['code']:
                    square_is_in_filter = True
        if square_is_in_filter is False or matrix_filter.square_code == square['code']:
            squares_available.append(square)
    if len(squares_available) > 0:
        context.update(
            {
                'squares_available': squares_available,
                'positions': positions_arr,
            }
        )

    context.update(
        {
            'matrix_filter': matrix_filter,
            'filter_positions': filter_positions,
        }
    )
    return render(request, 'panel_edit_filter_matrix_for_participants_not_distributed.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_edited_matrix_filter_for_participants_not_distributed(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        filter_id = json_data['filter_id']
        positions = json_data['positions']
        square = json_data['square']
        matrix_filter_inst = MatrixFilterParticipantNotDistributed.objects.get(id=filter_id)
        matrix_filter_inst.square_name = square['name']
        matrix_filter_inst.square_code = square['code']
        matrix_filter_inst.created_by = request.user
        matrix_filter_inst.save()
        MatrixFilterParticipantNotDistributedEmployeePosition.objects.filter(matrix_filter=matrix_filter_inst).delete()
        for position in positions:
            position_inst = EmployeePosition.objects.get(id=position)
            matrix_position_inst = MatrixFilterParticipantNotDistributedEmployeePosition()
            matrix_position_inst.created_by = request.user
            matrix_position_inst.matrix_filter = matrix_filter_inst
            matrix_position_inst.employee_position = position_inst
            matrix_position_inst.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_matrix_filter_for_participants_not_distributed(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        filter_id = json_data['filter_id']
        MatrixFilterParticipantNotDistributed.objects.get(id=filter_id).delete()
        return HttpResponse(200)



# @login_required(redirect_field_name=None, login_url='/login/')
# def get_available_squares(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         squares_data = json_data['squares_data']
#         print(squares_data)
#         matrix_filter = MatrixFilter.objects.all()
#         squares_available = []
#         #
#         # for category in categories:
#         #     category_is_in_matrix = False
#         #     if matrix_filter:
#         #         for filter in matrix_filter:
#         #
#         #
#         # for employee in employees_inst:
#         #     employees.append({
#         #         'id': employee.id,
#         #         'name': employee.name,
#         #         'sex': employee.sex.name_ru,
#         #         'birth_year': employee.birth_year,
#         #         'email': employee.email,
#         #         'position': employee.position.name_ru,
#         #         'industry': employee.industry.name_ru,
#         #         'role': employee.role.name_ru,
#         #     })
#         # response = {
#         #     'employees': employees,
#         # }
#         # print(response)
#         # return JsonResponse({'response': response})
#
#         return HttpResponse(200)

#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def save_edited_filter(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         print(json_data)
#         is_default = json_data['is_default']
#         name = json_data['name']
#         filter_id = json_data['filter_id']
#         raw_to_tpoints_type = RawToTPointsType.objects.get(id=filter_id)
#         raw_to_tpoints_type.name_ru = name
#         raw_to_tpoints_type.created_by = request.user
#         age_gender_id = json_data['age_gender_id']
#         raw_to_tpoints_type.age_gender_group = AgeGenderGroup.objects.get(id=age_gender_id)
#
#         if is_default:
#             raw_to_tpoints_type.is_default = True
#         else:
#             industry_id = json_data['industry_id']
#             position_id = json_data['position_id']
#             role_id = json_data['role_id']
#
#             raw_to_tpoints_type.industry = Industry.objects.get(id=industry_id)
#             raw_to_tpoints_type.employee_position = EmployeePosition.objects.get(id=position_id)
#             raw_to_tpoints_type.employee_role = EmployeeRole.objects.get(id=role_id)
#         raw_to_tpoints_type.save()
#         filter_data = json_data['filter_data']
#         for data in filter_data:
#             category_id = data['category_id']
#             raw_points = data['raw_points']
#             t_points = data['t_points']
#             raw_point_id = data['raw_point_id']
#             raw_to_tpoints = RawToTPoints.objects.get(id=raw_point_id)
#             raw_to_tpoints.category = Category.objects.get(id=category_id)
#             raw_to_tpoints.t_point = t_points
#             raw_to_tpoints.raw_points = raw_points
#             raw_to_tpoints.type = raw_to_tpoints_type
#             raw_to_tpoints.save()
#         return HttpResponse(status=200)
#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def save_new_filter_from_file(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         print(json_data)
#         is_default = json_data['is_default']
#         name = json_data['name']
#         age_gender_id = json_data['age_gender_id']
#
#         filter_data = json_data['filter_data']
#         errors = {}
#         wrong_codes = []
#         codes_ok = True
#         filter_exists = False
#         for data in filter_data:
#             try:
#                 category_inst = Category.objects.get(code=data['Код'])
#             except ObjectDoesNotExist:
#                 codes_ok = False
#                 wrong_codes.append(data['Код'])
#         if not codes_ok:
#             errors.update({
#                 'wrong_codes': wrong_codes
#             })
#         if RawToTPointsType.objects.filter(age_gender_group_id=age_gender_id, is_default=is_default):
#             if is_default:
#                 filter_exists = True
#                 errors.update({
#                     'filter_exists': True
#                 })
#             else:
#                 if RawToTPointsType.objects.filter(industry_id=json_data['industry_id'],
#                                                    employee_role_id=json_data['role_id'],
#                                                    employee_position=json_data['position_id']):
#                     filter_exists = True
#                     errors.update({
#                         'filter_exists': True
#                     })
#
#         if codes_ok and not filter_exists:
#             raw_to_tpoints_type = RawToTPointsType()
#             raw_to_tpoints_type.name_ru = name
#             raw_to_tpoints_type.created_by = request.user
#             raw_to_tpoints_type.age_gender_group = AgeGenderGroup.objects.get(id=age_gender_id)
#             if is_default:
#                 raw_to_tpoints_type.is_default = True
#             else:
#                 industry_id = json_data['industry_id']
#                 position_id = json_data['position_id']
#                 role_id = json_data['role_id']
#
#                 raw_to_tpoints_type.industry = Industry.objects.get(id=industry_id)
#                 raw_to_tpoints_type.employee_position = EmployeePosition.objects.get(id=position_id)
#                 raw_to_tpoints_type.employee_role = EmployeeRole.objects.get(id=role_id)
#             raw_to_tpoints_type.save()
#
#             for data in filter_data:
#                 category_inst = Category.objects.get(code=data['Код'])
#                 for key in data:
#                     if not key == 'Код' and not key == 'Шкала':
#                         print(f'{key} - {data[key]}')
#                         raw_to_tpoints = RawToTPoints()
#                         raw_to_tpoints.category = category_inst
#                         raw_to_tpoints.t_point = data[key]
#                         raw_to_tpoints.raw_points = key
#                         raw_to_tpoints.type = raw_to_tpoints_type
#                         raw_to_tpoints.save()
#         else:
#             return JsonResponse({'error': errors})
#
#             # category_id = data['category_id']
#             # raw_points = data['raw_points']
#             # t_points = data['t_points']
#             # raw_to_tpoints = RawToTPoints()
#             # raw_to_tpoints.category = Category.objects.get(id=category_id)
#             # raw_to_tpoints.t_point = t_points
#             # raw_to_tpoints.raw_points = raw_points
#             # raw_to_tpoints.type = raw_to_tpoints_type
#             # raw_to_tpoints.save()
#         return HttpResponse(status=200)
#
#
#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def edit_filter(request, filter_id):
#     context = info_common(request)
#     filter_inst = RawToTPointsType.objects.get(id=filter_id)
#     raw_to_tpoint_inst = RawToTPoints.objects.filter(type=filter_inst)
#     industries = Industry.objects.all()
#     positions = EmployeePosition.objects.all()
#     roles = EmployeeRole.objects.all()
#     ages_genders = AgeGenderGroup.objects.all()
#     sections = Section.objects.all()
#     categories = Category.objects.all()
#     raw_points = []
#     for raw_point in raw_to_tpoint_inst:
#         raw_points.append({
#             'category_id': raw_point.category.id,
#             'raw_point': raw_point.raw_points,
#             't_point': raw_point.t_point,
#             'raw_point_id': raw_point.id,
#         })
#     numbers = []
#     for i in range(0, 36):
#         numbers.append(i)
#
#     context.update(
#         {
#             'filter': filter_inst,
#             'raw_to_tpoint': raw_to_tpoint_inst,
#             'numbers': numbers,
#             'industries': industries,
#             'positions': positions,
#             'roles': roles,
#             'ages_genders': ages_genders,
#             'sections': sections,
#             'categories': categories,
#             'raw_points': raw_points,
#
#         }
#     )
#     return render(request, 'panel_edit_filter.html', context)
#
#
