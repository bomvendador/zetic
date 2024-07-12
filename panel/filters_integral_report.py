from pdf.models import Category, IntegralReportFilter, IntegralReportFilterCategory
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
def integral_report_filters_list(request):
    context = info_common(request)

    filters_inst = IntegralReportFilter.objects.all()
    filters_categories = IntegralReportFilterCategory.objects.all()
    context.update(
        {
            'filters': filters_inst,
            'filters_categories': filters_categories
        }
    )

    return render(request, 'integral_report_filter/panel_integral_report_filter_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_filter(request):
    context = info_common(request)
    context.update({
        'categories': get_categories_for_filter()
    })

    return render(request, 'integral_report_filter/panel_add_integral_report_filter.html', context)


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


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_integral_report_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        categories = json_data['categories']
        name = json_data['name']
        filter_inst = IntegralReportFilter()
        filter_inst.created_by = request.user
        filter_inst.name = name
        filter_inst.save()
        for category in categories:
            filter_category = IntegralReportFilterCategory()
            filter_category.category = Category.objects.get(id=category['category_id'])
            filter_category.filter = filter_inst
            filter_category.created_by = request.user
            filter_category.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def save_edited_integral_report_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        categories = json_data['categories']
        name = json_data['name']
        filter_id = json_data['filter_id']
        filter_inst = IntegralReportFilter.objects.get(id=filter_id)
        filter_inst.created_by = request.user
        filter_inst.name = name
        filter_inst.save()
        IntegralReportFilterCategory.objects.filter(filter=filter_inst).delete()
        for category in categories:
            filter_category = IntegralReportFilterCategory()
            filter_category.category = Category.objects.get(id=category['category_id'])
            filter_category.filter = filter_inst
            filter_category.created_by = request.user
            filter_category.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_integral_report_filter(request, filter_id):
    context = info_common(request)
    filter_inst = IntegralReportFilter.objects.get(id=filter_id)
    filter_categories = IntegralReportFilterCategory.objects.filter(filter=filter_inst)
    context.update({
        'filter': filter_inst,
        'categories': get_categories_for_filter(),
        'filter_categories': filter_categories,
    })

    return render(request, 'integral_report_filter/panel_edit_integral_report_filter.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_integral_report_filter(request):
    json_data = json.loads(request.body.decode('utf-8'))
    filter_id = json_data['filter_id']
    filter_inst = IntegralReportFilter.objects.get(id=filter_id)
    filter_inst.delete()
    return HttpResponse(200)
