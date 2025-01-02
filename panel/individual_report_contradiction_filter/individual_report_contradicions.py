from pdf.models import IndividualReportContradictionFilter, IndividualReportContradictionFilterCategory, Category
from login.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone
from django.core import serializers

from ..views import info_common

from django.utils.dateformat import DateFormat
from django.core.exceptions import ObjectDoesNotExist


@login_required(redirect_field_name=None, login_url='/login/')
def individual_report_contradictions_list(request):
    context = info_common(request)
    filters_inst = IndividualReportContradictionFilter.objects.all()
    filters_categories = IndividualReportContradictionFilterCategory.objects.all()
    context.update(
        {
            'filters': filters_inst,
            'filters_categories': filters_categories
        }
    )

    return render(request, 'individual_report_contradiction_filter/individual_report_contradictions_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_contradictions_filter(request):
    context = info_common(request)
    categories = Category.objects.all()
    context.update({
        'categories': categories
    })

    return render(request, 'individual_report_contradiction_filter/panel_add_individual_report_contradictions_filter.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_individual_report_contradictions_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        categories = json_data['categories']
        name = json_data['name']
        filter_id = json_data['filter_id']
        if filter_id != '':
            filter_id = json_data['filter_id']
            filter_inst = IndividualReportContradictionFilter.objects.get(id=filter_id)
            IndividualReportContradictionFilterCategory.objects.filter(filter=filter_inst).delete()
        else:
            filter_inst = IndividualReportContradictionFilter()
        filter_inst.created_by = request.user
        filter_inst.name = name
        filter_inst.save()
        for category in categories:
            filter_category = IndividualReportContradictionFilterCategory()
            filter_category.category = Category.objects.get(id=category['category_id'])
            filter_category.filter = filter_inst
            filter_category.points_to = category['points_to']
            filter_category.points_from = category['points_from']
            filter_category.created_by = request.user
            filter_category.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_individual_report_contradictions_filter(request, filter_id):
    context = info_common(request)
    filter_inst = IndividualReportContradictionFilter.objects.get(id=filter_id)
    filter_categories = IndividualReportContradictionFilterCategory.objects.filter(filter=filter_inst)
    categories = Category.objects.all()
    context.update({
        'filter': filter_inst,
        'filter_categories': filter_categories,
        'categories': categories,
    })
    return render(request, 'individual_report_contradiction_filter/panel_add_individual_report_contradictions_filter.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_individual_report_contradictions_filter(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        filter_id = json_data['filter_id']
        IndividualReportContradictionFilter.objects.get(id=filter_id).delete()
    return HttpResponse(200)

