from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

import json
# Create your views here.

from pdf.models import Company, Participant, ReportData, Report, Category, ReportGroup, ReportGroupSquare, Industry, \
    Employee, EmployeeRole, EmployeePosition, EmployeeGender, Study, StudyQuestionGroup, Section
# from django.contrib.auth.models import User

from login.models import UserRole, UserProfile, User
from login.views import home as login_home

from pdf_group.views import pdf_group_generator
from django.contrib.auth.decorators import login_required, wraps
from login import urls as login_urls
from django.utils import timezone
import time
from pdf.views import pdf_single_generator


@login_required(redirect_field_name=None, login_url='/login/')
def info_common(request):
    userprofile = UserProfile.objects.get(user=request.user)
    context = {
        'cur_userprofile': userprofile
    }
    if userprofile.role.name == 'Админ заказчика':

        employee = Employee.objects.get(user=request.user)

        if not employee.company_admin_active:
            logout(request)
            return 'logout'
        else:
            return context
    else:
        return context


@login_required(redirect_field_name=None, login_url='/login/')
def home(request):

    context = info_common(request)
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        userprofile = UserProfile.objects.get(user=request.user)
        if userprofile.role.name == 'Админ заказчика':
            company = Employee.objects.get(user=request.user).company
            stats = {
                'employees_qnt': Employee.objects.filter(company=company).count(),
                'individual_reports_qnt': Report.objects.filter(study__company=company).count(),
                'group_reports_qnt': ReportGroup.objects.filter(company=company).count()
            }
        if userprofile.role.name == 'Админ' or userprofile.role.name == 'Суперадмин':
            stats = {
                'companies_qnt': Company.objects.all().count(),
                'employees_qnt': Employee.objects.all().count(),
                'individual_reports_qnt': Report.objects.all().count(),
                'group_reports_qnt': ReportGroup.objects.all().count()
            }
        if userprofile.role.name == 'Менеджер':
            companies = Company.objects.filter(created_by=request.user)
            individual_reports = Report.objects.all()
            group_reports = ReportGroup.objects.all()
            individual_reports_qnt = 0
            group_reports_qnt = 0

            for company in companies:
                for individual_report in individual_reports:
                    if individual_report.study:
                        if individual_report.study.company == company:
                            individual_reports_qnt = individual_reports_qnt + 1
                for group_report in group_reports:
                    if group_report.company == company:
                        group_reports_qnt = group_reports_qnt + 1
            stats = {
                'companies_qnt': companies.count(),
                'employees_qnt': Employee.objects.filter(created_by=request.user).count(),
                'individual_reports_qnt': individual_reports_qnt,
                'group_reports_qnt': group_reports_qnt
            }

        context.update({
            'stats': stats
        })
    return render(request, 'panel_home.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def panel_logout(request):
    logout(request)
    return HttpResponse('')


@login_required(redirect_field_name=None, login_url='/login/')
def team_distribution(request):
    context = info_common(request)
    cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
    if cur_user_role_name == 'Менеджер':
        companies = Company.objects.filter(created_by=request.user)
    else:
        companies = Company.objects.all()

    context.update({
        'companies': companies
    })

    return render(request, 'panel_distribution.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def get_company_participants(request):

    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company = json_data['company']
        participants_inst = Participant.objects.filter(employee__company__name=company, completed_at__isnull=False)
        participants = []
        for participant in participants_inst:
            data = {
                'name': participant.employee.name,
                'email': participant.employee.email,
                'id': participant.id,
            }
            participants.append(data)
        response = {
            'participants': participants
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
            print(f'participant - {participant}')
            report = Report.objects.filter(participant__employee__email=participant).latest('added')
            lie_points.append({
                'fio': report.participant.employee.name,
                'email': report.participant.employee.email,
                'lie_points': report.lie_points
            })
            report_datas = ReportData.objects.filter(report=report)
            for report_data in report_datas:
                # print(report_data)
                participants_data.append({
                    'fio': report_data.report.participant.employee.name,
                    'section_code': report_data.section_code,
                    'category_code': report_data.category_code,
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
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
        if cur_user_role_name == 'Менеджер':
            companies = Company.objects.filter(created_by=request.user)
        if cur_user_role_name == 'Админ заказчика':
            companies = Company.objects.filter(id=Employee.objects.get(user=request.user).company.id)
        if cur_user_role_name == 'Админ' or cur_user_role_name == 'Суперадмин':
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
                report_group_square_arr.append(report_group_square.report.participant.employee.name)
            report.append({
                'company': group_report.company.name,
                'id': group_report.id,
                'date': timezone.localtime(group_report.added).strftime("%d.%m.%Y %H:%M:%S"),
                'participants': report_group_square_arr,
                'qnt': len(report_group_square_arr),
                'file_name': group_report.file.name,
                'comments': group_report.comments

            })
        response = {
            'data': list(report)
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def save_individual_report_comments(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        report_tr_id = json_data['report_tr_id']
        comments = json_data['comments']
        report = Report.objects.get(id=report_tr_id)
        report.comments = comments
        report.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def save_group_report_comments(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        report_tr_id = json_data['report_tr_id']
        comments = json_data['comments']
        report = ReportGroup.objects.get(id=report_tr_id)
        report.comments = comments
        report.save()
        return HttpResponse(status=200)


# список индивидуальных отчетов
@login_required(redirect_field_name=None, login_url='/login/')
def individual_reports_list(request):
    context = info_common(request)
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
        if cur_user_role_name == 'Менеджер':
            companies = Company.objects.filter(created_by=request.user)
        if cur_user_role_name == 'Админ заказчика':
            companies = Company.objects.filter(id=Employee.objects.get(user=request.user).company.id)
        if cur_user_role_name == 'Админ' or cur_user_role_name == 'Суперадмин':
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
            if report.comments:
                comments = report.comments
            else:
                comments = ''
            report_arr.append({
                'id': report.id,
                'company': report.participant.employee.company.name,
                'date': timezone.localtime(report.added).strftime("%d.%m.%Y %H:%M:%S"),
                'name': report.participant.employee.name,
                'file_name': report.file.name,
                'comments': comments
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
def migration(request):
    context = info_common(request)
    context.update(
        {'user_profiles': UserProfile.objects.all()}
    )

    return render(request, 'panel_migration.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_migration(request):
    if request.method == 'POST':
        start_time = time.perf_counter()
        json_data = json.loads(request.body.decode('utf-8'))
        # print(request)
        # print(json_data)
        # print(type(json.loads(json_data)))
        companies = json.loads(json_data)['companies']
        # print(type(companies))
        reports_qnt = 0
        employee_qnt = 0
        final_dict = {"lang": "ru"}
        for company in companies:
            if Company.objects.filter(public_code=company['public_code']).exists():
                company_inst = Company.objects.get(public_code=company['public_code'])
            else:
                company_inst = Company()
                company_inst.name = company['name']
                company_inst.public_code = company['public_code']
                company_inst.save()
            # print('--------')
            # print(f'Компания {company["name"]}')
            # print('===========')
            employees = company['employees']
            # studies = company['studies']
            for employee in employees:
                employee_qnt = employee_qnt + 1
                # if employee['name'] == '':
                #     print('Нет имени')
                # else:
                #     print(employee['name'])
                # if employee['email'] == '':
                #     print('Нет имейла')
                # else:
                #     print(employee['email'])
                participants = employee['participants']
                for participant in participants:
                    if 'report' in participant:
                        report_data = participant['report']
                        participant_info = participant['report']['participant_info']
                        study = participant['report']['study']
                        if Employee.objects.filter(email=participant_info['email']).exists():
                            employee_inst = Employee.objects.get(email=participant_info['email'])
                        else:
                            employee_inst = Employee()
                            employee_inst.name = participant_info['name']
                            employee_inst.email = participant_info['email']
                            employee_inst.sex = EmployeeGender.objects.get(public_code=participant_info['sex'])
                            employee_inst.birth_year = participant_info['year']
                            employee_inst.company = company_inst
                            employee_inst.save()

                        if Study.objects.filter(public_code=study['id']).exists():
                            study_inst = Study.objects.get(public_code=study['id'])
                        else:
                            study_inst = Study()
                            study_inst.name = study['name']
                            study_inst.public_code = study['id']
                            study_inst.company = company_inst
                            study_inst.save()

                        if not Participant.objects.filter(employee__email=participant_info['email'],
                                                      study=study_inst).exists():
                            participant_inst = Participant()
                            participant_inst.employee = employee_inst
                            participant_inst.started_at = timezone.now()
                            participant_inst.completed_at = timezone.now()
                            participant_inst.invitation_sent_datetime = timezone.now()
                            participant_inst.study = study_inst
                            participant_inst.invitation_sent = True
                            participant_inst.total_questions_qnt = 441
                            participant_inst.answered_questions_qnt = 441
                            participant_inst.current_percentage = 100
                            participant_inst.save()

                        pdf_single_generator(report_data)
                    # report_code = participant['report']['code']
                    # participant_info = participant['report']['participant_info']

                    # reports_qnt = reports_qnt + 1
                    # appraisal_data = participant['report']['appraisal_data']
                    # for data in appraisal_data:
                    #     point = data['point']
                    #     for points in point:
                    #         if points['points'] < 0:
                    #             print(f'{company["name"]} - {employee["name"]} - {points["category"]} - {points["points"]}')
        finished_time = time.perf_counter()
        print(f'time - {finished_time - start_time}')
        # print(f'reports_qnt - {reports_qnt} employee_qnt - {employee_qnt}')
        return HttpResponse('ok')

