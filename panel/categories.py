from pdf.models import Category, Section
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


@login_required(redirect_field_name=None, login_url='/login/')
def categories_list(request):
    context = info_common(request)
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        sections = Section.objects.all()
        context.update({
            'sections': sections,
        })

        return render(request, 'panel_categories_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def get_categories_by_section(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        section_id = json_data['section_id']
        categories = Category.objects.filter(section=section_id)
        response = []
        for category in categories:
            if category.created_by is not None:
                name = category.created_by.first_name
            else:
                name = ""
            response.append({
                'id': category.id,
                'name': category.name,
                'section': category.section.name,
                'created_at': category.created_at.strftime("%d.%m.%Y %H:%M:%S"),
                'created_by': name,
                'code': category.code,
            })
            # response.append()
        # response = {
        #     'categories': json.dumps(categories),
        # }
        # json_data = serializers.serialize('json', response)

        # return HttpResponse(json_data, content_type='application/json')
        return JsonResponse({'response': response})


@login_required(redirect_field_name=None, login_url='/login/')
def edit_category(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name = json_data['name']
        code = json_data['code']
        category_id = json_data['category_id']

        category_inst = Category.objects.get(id=category_id)
        category_inst.name = name
        category_inst.code = code

        category_inst.save()

        return JsonResponse({
            'category_id': category_inst.id,
            'name': category_inst.name,
            'code': category_inst.code
        })


@login_required(redirect_field_name=None, login_url='/login/')
def delete_category(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        category_id = json_data['category_id']
        category_inst = Category.objects.get(id=category_id)
        try:
            category_inst.delete()
            return HttpResponse(status=200)
        except Exception:
            return JsonResponse({"error": "Категория связана с одним из объектов и не может быть удалена"})


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_category(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name = json_data['name']
        code = json_data['code']
        section_id = json_data['section_id']
        section_inst = Section.objects.get(id=section_id)
        category_inst = Category()
        category_inst.name = name
        category_inst.code = code
        category_inst.section = section_inst
        category_inst.created_by = request.user

        category_inst.save()

        return HttpResponse(status=200)
