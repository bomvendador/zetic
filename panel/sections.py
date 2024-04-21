from pdf.models import Section
from login.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone

from .views import info_common
from api import outcoming


@login_required(redirect_field_name=None, login_url='/login/')
def sections_list(request):
    context = info_common(request)
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        sections = Section.objects.all()

        context.update({
            'sections': sections,
        })

        return render(request, 'panel_sections_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_section(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name = json_data['name']
        section_id = json_data['section_id']

        section_inst = Section.objects.get(id=section_id)
        section_inst.name = name

        section_inst.save()

        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_section(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        section_id = json_data['section_id']
        section_inst = Section.objects.get(id=section_id)
        try:
            section_inst.delete()
            return HttpResponse(status=200)
        except Exception:
            return JsonResponse({"error": "Секция связана с одним из объектов и не может быть удалена"})


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_section(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name = json_data['name']
        section_inst = Section()
        section_inst.name = name
        section_inst.created_by = request.user

        section_inst.save()

        return HttpResponse(status=200)
