from pdf.models import Category, TrafficLightReportFilter, TrafficLightReportFilterCategory, Project
from django.db.models import Avg, Max, Min, Sum
from login.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
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
def traffic_light_report_filters_list(request):
    context = info_common(request)
    filters_inst = TrafficLightReportFilter.objects.filter(project=None).order_by('position')
    filters_categories = TrafficLightReportFilterCategory.objects.filter(filter__project=None)
    context.update(
        {
            'filters': filters_inst,
            'filters_categories': filters_categories
        }
    )

    return render(request, 'traffic_light_report/panel_traffic_light_report_filter_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_filter(request):
    context = info_common(request)
    positions = get_traffic_light_filters_positions('')
    max_position = TrafficLightReportFilter.objects.filter(project=None).aggregate(Max('position'))['position__max']
    if not max_position:
        max_position = 0
    context.update({
        'categories': get_categories_for_filter(),
        'positions': positions,
        'new_position': int(max_position) + 1,

    })
    return render(request, 'traffic_light_report/panel_add_traffic_light_report_filter.html', context)


def add_traffic_light_report_filter_to_project(request, project_id):
    context = info_common(request)
    project_inst = Project.objects.get(id=project_id)
    positions = get_traffic_light_filters_positions(project_id)
    max_position = TrafficLightReportFilter.objects.filter(project_id=project_id).aggregate(Max('position'))['position__max']
    print(f'max pos = {max_position}')
    if max_position:
        new_position = int(max_position) + 1
    else:
        new_position = 1
    print(new_position)
    print(positions)
    context.update({
        'categories': get_categories_for_filter(),
        # 'positions': positions[:-1],
        'positions': positions,
        'project': project_inst,
        'new_position': new_position
    })
    print(context)

    return render(request, 'traffic_light_report/panel_add_traffic_light_report_filter.html', context)


def get_traffic_light_filters_positions(project_id):
    positions = []
    if not project_id == '':
        traffic_light_report_inst = TrafficLightReportFilter.objects.filter(project_id=project_id).order_by('position')
        max_position = TrafficLightReportFilter.objects.filter(project_id=project_id).aggregate(Max('position'))['position__max']
    else:
        traffic_light_report_inst = TrafficLightReportFilter.objects.filter(project=None).order_by('position')
        max_position = TrafficLightReportFilter.objects.filter(project=None).aggregate(Max('position'))['position__max']
    for filter_item in traffic_light_report_inst:
        positions.append(filter_item.position)
    if max_position is not None:
        positions.append(int(max_position) + 1)
    return positions


def get_categories_for_filter():
    categories_arr = []
    categories = Category.objects.all().order_by('code')
    for category in categories:
        if not category.for_validity:
            categories_arr.append({
                'id': category.id,
                'code': category.code,
                'category_name': category.name,
                'section_name': category.section.name
            })
    return categories_arr


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_traffic_light_report_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        categories = json_data['categories']
        name = json_data['name']
        red = json_data['red']
        yellow = json_data['yellow']
        green = json_data['green']
        project_id = json_data['project_id']
        green_from_left = json_data['green_from_left']
        position = json_data['position']
        description = json_data['description']
        filter_inst = TrafficLightReportFilter()

        if not project_id == '':
            # max_position = TrafficLightReportFilter.objects.filter(project_id=project_id).aggregate(Max('position'))['position__max']
            update_traffic_light_filters_positions(position, json_data['project_id'])
            filter_inst.project_id = project_id
        else:
            # max_position = TrafficLightReportFilter.objects.filter(project=None).aggregate(Max('position'))['position__max']
            update_traffic_light_filters_positions(position, '')


        # position_gap_for_existing_filter = 0
        # all_existing_filters_inst = TrafficLightReportFilter.objects.all().order_by('position')
        # cnt = 0
        # for existing_filter in all_existing_filters_inst:
        #     cnt = cnt + 1
        #     if int(existing_filter.position) == int(position):
        #         position_gap_for_existing_filter = 1
        #     existing_filter.position = cnt + position_gap_for_existing_filter
        #     existing_filter.save()
        #     print(f'{existing_filter.name} - {existing_filter.position} - {cnt} - {position_gap_for_existing_filter}')

        filter_inst.position = position
        filter_inst.created_by = request.user
        filter_inst.name = name
        filter_inst.points_from_green = green['points_from']
        filter_inst.points_to_green = green['points_to']
        filter_inst.points_from_yellow = yellow['points_from']
        filter_inst.points_to_yellow = yellow['points_to']
        filter_inst.points_from_red = red['points_from']
        filter_inst.points_to_red = red['points_to']
        filter_inst.description = description
        if green_from_left:
            filter_inst.direction = 'green_from_left'
        else:
            filter_inst.direction = 'red_from_left'
        filter_inst.save()
        for category in categories:
            filter_category = TrafficLightReportFilterCategory()
            filter_category.category = Category.objects.get(id=category['category_id'])
            filter_category.filter = filter_inst
            filter_category.created_by = request.user
            filter_category.save()
        return HttpResponse(200)


def update_traffic_light_filters_positions(position, project_id):
    position_gap_for_existing_filter = 0
    if project_id == '':
        all_existing_filters_inst = TrafficLightReportFilter.objects.all().order_by('position')
    else:
        all_existing_filters_inst = TrafficLightReportFilter.objects.filter(project_id=project_id).order_by('position')
    cnt = 0
    for existing_filter in all_existing_filters_inst:
        cnt = cnt + 1
        if int(existing_filter.position) == int(position):
            position_gap_for_existing_filter = 1
        existing_filter.position = cnt + position_gap_for_existing_filter
        existing_filter.save()
        print(f'{existing_filter.name} - {existing_filter.position} - {cnt} - {position_gap_for_existing_filter}')


@login_required(redirect_field_name=None, login_url='/login/')
def save_edited_traffic_light_report_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        categories = json_data['categories']
        name = json_data['name']
        red = json_data['red']
        yellow = json_data['yellow']
        green = json_data['green']
        filter_id = json_data['filter_id']
        green_from_left = json_data['green_from_left']
        position = json_data['position']
        description = json_data['description']
        for_circle_diagram = json_data['for_circle_diagram']
        filter_inst = TrafficLightReportFilter.objects.get(id=filter_id)
        if filter_inst.project:
            max_position = TrafficLightReportFilter.objects.filter(project=filter_inst.project).aggregate(Max('position'))['position__max']
            all_existing_filters_inst = TrafficLightReportFilter.objects.filter(project=filter_inst.project).order_by('position')
        else:
            max_position = TrafficLightReportFilter.objects.filter(project=None).aggregate(Max('position'))['position__max']
            all_existing_filters_inst = TrafficLightReportFilter.objects.filter(project=None).order_by('position')
        print(max_position)

        for existing_filter in all_existing_filters_inst:
            if int(existing_filter.position) >= int(position) and existing_filter.position < filter_inst.position and not existing_filter == filter_inst:
                existing_filter.position = existing_filter.position + 1
                existing_filter.save()
        filter_inst.created_by = request.user
        filter_inst.name = name
        filter_inst.points_from_green = green['points_from']
        filter_inst.points_to_green = green['points_to']
        filter_inst.points_from_yellow = yellow['points_from']
        filter_inst.points_to_yellow = yellow['points_to']
        filter_inst.points_from_red = red['points_from']
        filter_inst.points_to_red = red['points_to']
        filter_inst.position = position
        filter_inst.description = description
        if green_from_left:
            filter_inst.direction = 'green_from_left'
        else:
            filter_inst.direction = 'red_from_left'
        if for_circle_diagram:
            filter_inst.for_circle_diagram = True
            filter_inst.circle_diagram_description_red = red['circle_diagram_description']
            filter_inst.circle_diagram_description_yellow = yellow['circle_diagram_description']
            filter_inst.circle_diagram_description_green = green['circle_diagram_description']
        else:
            filter_inst.for_circle_diagram = False
            filter_inst.circle_diagram_description_red = None
            filter_inst.circle_diagram_description_yellow = None
            filter_inst.circle_diagram_description_green = None
        filter_inst.save()
        TrafficLightReportFilterCategory.objects.filter(filter=filter_inst).delete()
        for category in categories:
            filter_category = TrafficLightReportFilterCategory()
            filter_category.category = Category.objects.get(id=category['category_id'])
            filter_category.filter = filter_inst
            filter_category.created_by = request.user
            filter_category.save()
        if filter_inst.project:
            project_id = filter_inst.project_id
        else:
            project_id = ''
        return JsonResponse({"project_id": project_id})

        # return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_traffic_light_report_filter(request, filter_id):
    context = info_common(request)
    filter_inst = TrafficLightReportFilter.objects.get(id=filter_id)
    filter_categories = TrafficLightReportFilterCategory.objects.filter(filter=filter_inst)
    for_circle_diagram_allowed = True
    if not filter_inst.for_circle_diagram:
        for_circle_diagram_inst = TrafficLightReportFilter.objects.filter(for_circle_diagram=True)
        if for_circle_diagram_inst.exists():
            for_circle_diagram_allowed = False
    if filter_inst.project:
        positions = get_traffic_light_filters_positions(filter_inst.project.id)
    else:
        positions = get_traffic_light_filters_positions('')
    context.update({
        'filter': filter_inst,
        'categories': get_categories_for_filter(),
        'filter_categories': filter_categories,
        'positions': positions[:-1],
        'for_circle_diagram_allowed': for_circle_diagram_allowed
    })
    print(context)

    return render(request, 'traffic_light_report/panel_edit_traffic_light_report_filter.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_traffic_light_report_filter(request):
    json_data = json.loads(request.body.decode('utf-8'))
    filter_id = json_data['filter_id']
    filter_inst = TrafficLightReportFilter.objects.get(id=filter_id)
    if filter_inst.project:
        project_id = filter_inst.project.id
    else:
        project_id = ''
    filter_inst.delete()
    update_filters_positions(project_id)
    return HttpResponse(200)


def update_filters_positions(project_id):
    if project_id == '':
        filters_inst = TrafficLightReportFilter.objects.all().order_by('position')
    else:
        filters_inst = TrafficLightReportFilter.objects.filter(project_id=project_id).order_by('position')
    cnt = 0
    for traffic_light_filter in filters_inst:
        cnt = cnt + 1
        traffic_light_filter.position = cnt
        traffic_light_filter.save()
