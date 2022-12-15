from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.contrib.auth import authenticate, login, logout

import json
# Create your views here.

from pdf.models import Company, Participant, ReportData, Report, Category, ReportGroup, ReportGroupSquare, Industry, Employee, EmployeeRole, EmployeePosition
# from django.contrib.auth.models import User

from login.models import UserRole, UserProfile, User

from pdf_group.views import pdf_group_generator
from django.contrib.auth.decorators import login_required
from login import urls as login_urls
from django.utils import timezone


@login_required(redirect_field_name=None, login_url='/login/')
def info_common(request):
    context = {
        'cur_userprofile': UserProfile.objects.get(user=request.user)
    }
    return context


@login_required(redirect_field_name=None, login_url='/login/')
def home(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = info_common(request)
    context.update({
        'user_profile': user_profile
    })
    return render(request, 'panel_home.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def panel_logout(request):
    logout(request)
    return HttpResponse('')


@login_required(redirect_field_name=None, login_url='/login/')
def team_distribution(request):
    context = info_common(request)
    context.update({
        'companies': Company.objects.all()
    })

    return render(request, 'panel_distribution.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def get_company_participants(request):

    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company = json_data['company']
        participants = Participant.objects.filter(employee__company__name=company).values()
        response = {
            'participants': list(participants)
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def get_report_participants_data(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        report_participants = json_data['report_participants']
        print(report_participants)
        participants_data = []
        lie_points = []
        # response = {}
        for participant in report_participants:
            report = Report.objects.filter(participant__email=participant).latest('added')
            lie_points.append({
                'fio': report.participant.fio,
                'email': report.participant.email,
                'lie_points': report.lie_points
            })
            report_datas = ReportData.objects.filter(report=report)
            for report_data in report_datas:
                # print(report_data)
                participants_data.append({
                    'fio': report_data.report.participant.fio,
                    'section': report_data.section.name,
                    'category': report_data.category.name,
                    'points': report_data.points,
                })
        response = {
            'data': list(participants_data),
            'lie_points': list(lie_points)
        }
        return JsonResponse(response, safe=False)


@login_required(redirect_field_name=None, login_url='/login/')
def save_group_report_data(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        # print(json_data)
        # for item in json_data['square_results']:
        #     print(item)
        response = pdf_group_generator(json_data)
        return response


# список командных отчетов
@login_required(redirect_field_name=None, login_url='/login/')
def group_reports_list(request):
    context = info_common(request)
    companies = Company.objects.all()
    companies_arr = []
    for company in companies:
        report_group = ReportGroup.objects.filter(company=company)
        if report_group.count() > 0:
            companies_arr.append(company.name)
    context.update(
        {'companies_arr': companies_arr}
    )

    return render(request, 'panel_group_reports_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def get_group_reports_list(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company = json_data['company']
        group_reports = ReportGroup.objects.filter(company__name=company)
        # participants = Participant.objects.filter(Company__name=Company).values()
        report = []
        for group_report in group_reports:
            report_group_square_arr = []
            reports_group_square = ReportGroupSquare.objects.filter(report_group=group_report)
            for report_group_square in reports_group_square:
                report_group_square_arr.append(report_group_square.report.participant.fio)
            report.append({
                'company': group_report.company.name,
                'id': group_report.id,
                'date': group_report.added.strftime('%d.%m.%Y %H:%M:%S'),
                'participants': report_group_square_arr,
                'qnt': len(report_group_square_arr),
                'file_name': group_report.file.name,
                'comments': group_report.comments

            })
        response = {
            'data': list(report)
        }
        return JsonResponse(response)


# список индивидуальных отчетов
@login_required(redirect_field_name=None, login_url='/login/')
def individual_reports_list(request):
    context = info_common(request)
    companies = Company.objects.all()
    companies_arr = []
    for company in companies:
        reports = Report.objects.filter(participant__employee__company=company)
        if reports.count() > 0:
            companies_arr.append(company.name)
    context.update(
        {'companies_arr': companies_arr}
    )

    return render(request, 'panel_individual_reports_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def get_individual_reports_list(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company = json_data['company']
        reports = Report.objects.filter(participant__employee__company__name=company)
        report_arr = []
        for report in reports:
            report_arr.append({
                'company': report.participant.employee.company.name,
                'date': timezone.localtime(report.added).strftime("%d.%m.%Y %H:%M:%S"),
                'name': report.participant.employee.name,
                'file_name': report.file.name
            })
        response = {
            'data': list(report_arr)
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def users_list(request):
    context = info_common(request)
    context.update(
        {'user_profiles': UserProfile.objects.all()}
    )

    return render(request, 'panel_users_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def user_profile(request, user_id):
    context = info_common(request)
    context.update({
        'user_profile': UserProfile.objects.get(user_id=user_id),
        'roles': UserRole.objects.all()
    })

    return render(request, 'panel_user_profile.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_user_pwd(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        user_id = json_data['user_id']
        pwd = json_data['password']
        user_inst = User.objects.get(id=user_id)
        user_inst.set_password(pwd)

        return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/login/')
def save_user_profile(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        user_id = json_data['user_id']
        fio = json_data['user_fio']
        email = json_data['user_email']
        tel = json_data['user_tel']
        role = json_data['user_role']

        user_inst = User.objects.get(id=user_id)
        user_profile_inst = UserProfile.objects.get(user=user_inst)

        user_inst.email = email
        user_profile_inst.fio = fio
        user_profile_inst.tel = tel
        user_profile_inst.role = UserRole.objects.get(name=role)

        user_inst.save()
        user_profile_inst.save()

        return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/login/')
def add_user(request):
    context = info_common(request)
    context.update({
        'roles': UserRole.objects.all()
    })

    return render(request, 'panel_add_user.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_user(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        fio = json_data['user_fio']
        email = json_data['user_email']
        tel = json_data['user_tel']
        role = json_data['user_role']
        pwd = json_data['password']

        user_inst = User()
        user_inst.email = email
        user_inst.username = email
        user_inst.first_name = fio
        user_inst.set_password(pwd)

        user_inst.save()

        user_profile_inst = UserProfile()

        user_profile_inst.user = user_inst
        user_profile_inst.fio = fio
        user_profile_inst.tel = tel
        user_profile_inst.role = UserRole.objects.get(name=role)
        user_profile_inst.save()

        return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/login/')
def delete_user(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        user_id = json_data['user_id']
        user = User.objects.get(id=user_id)
        user.delete()
        return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/login/')
def delete_group_report(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        group_report_inst = ReportGroup.objects.get(id=json_data['report_id'])
        group_report_inst.delete()

        return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/login/')
def add_company_init(request):
    context = info_common(request)
    context.update({
        'roles': UserRole.objects.all()
    })

    return render(request, 'panel_add_company.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_new_company(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name = json_data['name']
        active = json_data['active']
        print(json_data)
        company_inst = Company()
        company_inst.name = name
        company_inst.created_by = request.user
        if active == 1:
            company_inst.active = True
        else:
            company_inst.active = False

        company_inst.save()

        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def companies_list(request):
    context = info_common(request)
    context.update(
        {
            'companies': Company.objects.all(),
         }
    )

    return render(request, 'panel_companies_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_company(request, company_id):
    context = info_common(request)
    company_inst = Company.objects.get(id=company_id)
    context.update(
        {
            'company': company_inst,
            'admins': Employee.objects.filter(company=company_inst, company_admin=True)
        }
    )

    return render(request, 'panel_edit_company.html', context)



