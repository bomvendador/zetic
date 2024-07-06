from pdf.models import Category, Section, ResearchTemplate, ResearchTemplateSections, Study, Company, Employee, \
    Industry, EmployeePosition, EmployeeRole, AgeGenderGroup, RawToTPointsType, RawToTPoints, \
    IndividualReportPointsDescriptionFilter, IndividualReportPointsDescriptionFilterCategory, IndividualReportPointsDescriptionFilterText
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


@login_required(redirect_field_name=None, login_url='/login/')
def individual_report_points_description_filters_list(request):
    context = info_common(request)

    filters_inst = IndividualReportPointsDescriptionFilter.objects.all()
    filters_categories = IndividualReportPointsDescriptionFilterCategory.objects.all()
    context.update(
        {
            'filters': filters_inst,
            'filters_categories': filters_categories
        }
    )

    return render(request, 'individual_report_points_descriptions/panel_individual_report_filter_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_filter(request):
    context = info_common(request)
    # categories_arr = []
    # categories = Category.objects.all()
    # for category in categories:
    #     if not category.for_validity:
    #         categories_arr.append({
    #             'id': category.id,
    #             'code': category.code,
    #             'category_name': category.name,
    #             'section_name': category.section.name
    #         })
    context.update({
        'categories': get_categories_for_filter()
    })

    return render(request, 'individual_report_points_descriptions/panel_add_individual_report_filter.html', context)


def get_categories_for_filter():
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
    return categories_arr
#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def add_filter_participant_not_distributed(request):
#     context = info_common(request)
#     # positions_arr = []
#     positions = get_available_positions_for_participant_not_distributed_filter()
#     # for position in positions:
#     #     positions_arr.append({
#     #         'name': position.name_ru,
#     #         'id': position.id,
#     #     })
#
#     # default_filter_inst = RawToTPointsType.objects.filter(is_default=True)
#     squares_available = get_available_squares_for_participant_not_distributed_filter()
#     context.update(
#         {
#             'squares_available': squares_available,
#             'positions': positions,
#         }
#     )
#
#     return render(request, 'panel_add_filter_matrix_for_participants_not_distributed.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_individual_report_points_description_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        categories = json_data['categories']
        name = json_data['name']
        description_texts = json_data['description_text']
        filter_inst = IndividualReportPointsDescriptionFilter()
        filter_inst.created_by = request.user
        filter_inst.name = name
        filter_inst.save()
        for category in categories:
            filter_category = IndividualReportPointsDescriptionFilterCategory()
            filter_category.category = Category.objects.get(id=category['category_id'])
            filter_category.filter = filter_inst
            filter_category.points_to = category['points_to']
            filter_category.points_from = category['points_from']
            filter_category.created_by = request.user
            filter_category.save()
        for text in description_texts:
            text_inst = IndividualReportPointsDescriptionFilterText()
            text_inst.filter = filter_inst
            text_inst.text = text
            text_inst.created_by = request.user
            text_inst.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def save_edited_individual_report_points_description_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        categories = json_data['categories']
        name = json_data['name']
        filter_id = json_data['filter_id']
        description_texts = json_data['description_text']
        filter_inst = IndividualReportPointsDescriptionFilter.objects.get(id=filter_id)
        filter_inst.created_by = request.user
        filter_inst.name = name
        filter_inst.save()
        IndividualReportPointsDescriptionFilterCategory.objects.filter(filter=filter_inst).delete()
        for category in categories:
            filter_category = IndividualReportPointsDescriptionFilterCategory()
            filter_category.category = Category.objects.get(id=category['category_id'])
            filter_category.filter = filter_inst
            filter_category.points_to = category['points_to']
            filter_category.points_from = category['points_from']
            filter_category.created_by = request.user
            filter_category.save()
        IndividualReportPointsDescriptionFilterText.objects.filter(filter=filter_inst).delete()
        for text in description_texts:
            text_inst = IndividualReportPointsDescriptionFilterText()
            text_inst.filter = filter_inst
            text_inst.text = text
            text_inst.created_by = request.user
            text_inst.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_individual_report_points_description_filter(request, filter_id):
    context = info_common(request)
    filter_inst = IndividualReportPointsDescriptionFilter.objects.get(id=filter_id)
    filter_categories = IndividualReportPointsDescriptionFilterCategory.objects.filter(filter=filter_inst)
    filter_description_texts = IndividualReportPointsDescriptionFilterText.objects.filter(filter=filter_inst)
    context.update({
        'filter': filter_inst,
        'categories': get_categories_for_filter(),
        'filter_categories': filter_categories,
        'filter_description_texts': filter_description_texts
    })

    # filter_categories = MatrixFilterCategory.objects.filter(matrix_filter=matrix_filter)
    # filter_positions = MatrixFilterInclusiveEmployeePosition.objects.filter(matrix_filter=matrix_filter)
    #
    # categories_arr = []
    # categories = Category.objects.all()
    # for category in categories:
    #     if not category.for_validity:
    #         categories_arr.append({
    #             'id': category.id,
    #             'code': category.code,
    #             'category_name': category.name,
    #             'section_name': category.section.name
    #         })
    # positions_arr = []
    # positions = EmployeePosition.objects.all()
    # for position in positions:
    #     positions_arr.append({
    #         'name': position.name_ru,
    #         'id': position.id,
    #     })
    #
    # all_matrix_filters = MatrixFilter.objects.all()
    # squares_available = []
    # for square in squares_data:
    #     square_is_in_filter = False
    #     if all_matrix_filters:
    #         for matrix_filter_from_all in all_matrix_filters:
    #             if matrix_filter_from_all.square_code == square['code']:
    #                 square_is_in_filter = True
    #     if square_is_in_filter is False or matrix_filter.square_code == square['code']:
    #         squares_available.append(square)
    # if len(squares_available) > 0:
    #     context.update(
    #         {
    #             'squares_available': squares_available,
    #             'positions': positions_arr,
    #             'categories': categories_arr,
    #         }
    #     )
    #
    # context.update(
    #     {
    #         'matrix_filter': matrix_filter,
    #         'filter_categories': filter_categories,
    #         'filter_positions': filter_positions,
    #     }
    # )
    return render(request, 'individual_report_points_descriptions/panel_edit_individual_report_filter.html', context)
#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def save_edited_matrix_filter(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         print(json_data)
#         filter_id = json_data['filter_id']
#         categories = json_data['categories']
#         positions = json_data['positions']
#         square = json_data['square']
#         matrix_filter_inst = MatrixFilter.objects.get(id=filter_id)
#         matrix_filter_inst.square_name = square['name']
#         matrix_filter_inst.square_code = square['code']
#         matrix_filter_inst.created_by = request.user
#         matrix_filter_inst.save()
#         MatrixFilterCategory.objects.filter(matrix_filter=matrix_filter_inst).delete()
#         for category in categories:
#             category_inst = Category.objects.get(id=category['category_id'])
#             matrix_category_inst = MatrixFilterCategory()
#             matrix_category_inst.created_by = request.user
#             matrix_category_inst.category = category_inst
#             matrix_category_inst.matrix_filter = matrix_filter_inst
#             matrix_category_inst.points_from = category['points_from']
#             matrix_category_inst.points_to = category['points_to']
#             matrix_category_inst.save()
#
#         MatrixFilterInclusiveEmployeePosition.objects.filter(matrix_filter=matrix_filter_inst).delete()
#         for position in positions:
#             position_inst = EmployeePosition.objects.get(id=position)
#             matrix_position_inst = MatrixFilterInclusiveEmployeePosition()
#             matrix_position_inst.created_by = request.user
#             matrix_position_inst.matrix_filter = matrix_filter_inst
#             matrix_position_inst.employee_position = position_inst
#             matrix_position_inst.save()
#         return HttpResponse(200)
#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def delete_matrix_filter(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         print(json_data)
#         filter_id = json_data['filter_id']
#         MatrixFilter.objects.get(id=filter_id).delete()
#         return HttpResponse(200)
#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def save_new_matrix_filter_for_participants_not_distributed(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         print(json_data)
#         positions = json_data['positions']
#         square = json_data['square']
#         matrix_filter_inst = MatrixFilterParticipantNotDistributed()
#         matrix_filter_inst.square_name = square['name']
#         matrix_filter_inst.square_code = square['code']
#         matrix_filter_inst.created_by = request.user
#         matrix_filter_inst.save()
#         for position in positions:
#             position_inst = EmployeePosition.objects.get(id=position)
#             matrix_position_inst = MatrixFilterParticipantNotDistributedEmployeePosition()
#             matrix_position_inst.created_by = request.user
#             matrix_position_inst.matrix_filter = matrix_filter_inst
#             matrix_position_inst.employee_position = position_inst
#             matrix_position_inst.save()
#         return HttpResponse(200)
#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def edit_matrix_filter_for_participants_not_distributed(request, filter_id):
#     context = info_common(request)
#     matrix_filter = MatrixFilterParticipantNotDistributed.objects.get(id=filter_id)
#     filter_positions = MatrixFilterParticipantNotDistributedEmployeePosition.objects.filter(matrix_filter=matrix_filter)
#     positions_arr = []
#     positions = EmployeePosition.objects.all()
#     for position in positions:
#         positions_arr.append({
#             'name': position.name_ru,
#             'id': position.id,
#         })
#
#     all_matrix_filters = MatrixFilterParticipantNotDistributed.objects.all()
#     squares_available = []
#     for square in squares_data:
#         square_is_in_filter = False
#         if all_matrix_filters:
#             for matrix_filter_from_all in all_matrix_filters:
#                 if matrix_filter_from_all.square_code == square['code']:
#                     square_is_in_filter = True
#         if square_is_in_filter is False or matrix_filter.square_code == square['code']:
#             squares_available.append(square)
#     if len(squares_available) > 0:
#         context.update(
#             {
#                 'squares_available': squares_available,
#                 'positions': positions_arr,
#             }
#         )
#
#     context.update(
#         {
#             'matrix_filter': matrix_filter,
#             'filter_positions': filter_positions,
#         }
#     )
#     return render(request, 'panel_edit_filter_matrix_for_participants_not_distributed.html', context)
#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def save_edited_matrix_filter_for_participants_not_distributed(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         print(json_data)
#         filter_id = json_data['filter_id']
#         positions = json_data['positions']
#         square = json_data['square']
#         matrix_filter_inst = MatrixFilterParticipantNotDistributed.objects.get(id=filter_id)
#         matrix_filter_inst.square_name = square['name']
#         matrix_filter_inst.square_code = square['code']
#         matrix_filter_inst.created_by = request.user
#         matrix_filter_inst.save()
#         MatrixFilterParticipantNotDistributedEmployeePosition.objects.filter(matrix_filter=matrix_filter_inst).delete()
#         for position in positions:
#             position_inst = EmployeePosition.objects.get(id=position)
#             matrix_position_inst = MatrixFilterParticipantNotDistributedEmployeePosition()
#             matrix_position_inst.created_by = request.user
#             matrix_position_inst.matrix_filter = matrix_filter_inst
#             matrix_position_inst.employee_position = position_inst
#             matrix_position_inst.save()
#         return HttpResponse(200)
#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def delete_matrix_filter_for_participants_not_distributed(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         print(json_data)
#         filter_id = json_data['filter_id']
#         MatrixFilterParticipantNotDistributed.objects.get(id=filter_id).delete()
#         return HttpResponse(200)


