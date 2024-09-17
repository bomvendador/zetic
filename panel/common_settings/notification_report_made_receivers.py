from pdf.models import Category, Section, CategoryQuestions, CommonBooleanSettings, UsersReportMadeNotificationReceivers
from login.models import UserRole, UserProfile, User

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone
from django.core import serializers

from panel.views import info_common

from django.db.models import Sum, Q


@login_required(redirect_field_name=None, login_url='/login/')
def notification_report_made_receivers_home(request):
    context = info_common(request)
    users = User.objects.all()
    available_receivers = []
    for user in users:
        receiver_inst = UsersReportMadeNotificationReceivers.objects.filter(user=user)
        if not receiver_inst.exists():
            available_receivers.append({
                'id': user.id,
                'name': user.first_name,
                'email': user.email,
            })
    context.update({
        'common_report_made_notification_receivers': UsersReportMadeNotificationReceivers.objects.all(),
        'available_receivers': available_receivers
    })

    return render(request, 'settings/panel_notification_report_made_receivers.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_common_report_made_notification_receiver(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        user_id = json_data['user_id']
        user_inst = User.objects.get(id=user_id)
        receiver_inst = UsersReportMadeNotificationReceivers()
        receiver_inst.user = user_inst
        receiver_inst.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_common_report_made_notification_receiver(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        receiver_id = json_data['receiver_id']
        UsersReportMadeNotificationReceivers.objects.get(id=receiver_id).delete()
        return HttpResponse(status=200)
