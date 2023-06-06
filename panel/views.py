import json
import logging
import os
import time
from datetime import datetime, timedelta

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils import timezone

from login.models import UserRole, UserProfile, User
from panel import mail_handler
from pdf.models import Company, Participant, ReportData, Report, Category, ReportGroup, ReportGroupSquare, Employee, \
    EmployeeGender, Study
from pdf.views import pdf_single_generator
from pdf_group.views import pdf_group_generator
from reports import settings

# Create your views here.
# from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


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


def millisec_to_time(millisec):
    d = datetime(1, 1, 1) + millisec
    if d.day - 1 == 0:
        return "{0}:{1}:{2}".format(d.hour, d.minute, d.second)
    else:
        return "{0}:{1}:{2}:{3}".format(d.day - 1, d.hour, d.minute, d.second)


@login_required(redirect_field_name=None, login_url='/login/')
def home(request):
    context = info_common(request)

    participants = Participant.objects.filter(created_by=request.user)
    cnt = 0
    time_diff_total = 0

    for participant in participants:
        if participant.completed_at is not None and participant.started_at is not None:
            cnt = cnt + 1
            cur_time_diff = participant.completed_at - participant.started_at
            time_diff_total = time_diff_total + cur_time_diff.total_seconds()

    total_completion_time = 0 if cnt == 0 else time_diff_total / cnt

    points_1 = {
        '1_1': 0,
        '1_2': 0,
        '1_3': 0,
        '1_4': 0,
        '1_5': 0,
        '1_6': 0,
        '1_7': 0,
        '1_8': 0,
        '1_9': 0,
        '1_10': 0,
        '1_11': 0,
        '1_12': 0,
        '1_13': 0,
        '1_14': 0,
        '1_15': 0,
    }
    points_2 = {
        '2_1': 0,
        '2_2': 0,
        '2_3': 0,
        '2_4': 0,
        '2_5': 0,
        '2_6': 0,
        '2_7': 0,
        '2_8': 0,
        '2_9': 0,
        '2_10': 0,
        '2_11': 0,
        '2_12': 0,
        '2_13': 0,
        '2_14': 0,
        '2_15': 0,
        '2_16': 0,
    }
    points_3 = {
        '3_1': 0,
        '3_2': 0,
        '3_3': 0,
        '3_4': 0,
        '3_5': 0,
        '3_6': 0,
        '3_7': 0,
        '3_8': 0,
        '3_9': 0,
        '3_10': 0,
        '3_11': 0,
        '3_12': 0,
    }
    points_4 = {
        '4_1': 0,
        '4_2': 0,
        '4_3': 0,
        '4_4': 0,
        '4_5': 0,
        '4_6': 0,
        '4_7': 0,
        '4_8': 0,
        '4_9': 0,
        '4_10': 0,
    }

    individual_reports = ReportData.objects.filter(report__participant__created_by=request.user)
    for report in individual_reports:
        # print(report.report.participant.employee.name)
        if report.section_code == '1':
            points_1[report.category_code] = points_1[report.category_code] + report.points
        if report.section_code == '2':
            points_2[report.category_code] = points_2[report.category_code] + report.points
        if report.section_code == '3':
            points_3[report.category_code] = points_3[report.category_code] + report.points
        if report.section_code == '4':
            points_4[report.category_code] = points_4[report.category_code] + report.points

    points_1_arr = []
    points_2_arr = []
    points_3_arr = []
    points_4_arr = []

    # points_1_copy = points_1.copy()
    # for k_copy, v_copy in points_1_copy:
    #     for k, v in points_1:
    #         if not k_copy == k:

    # for k, v in points_2:
    #     points_2_arr.append(v)
    # for k, v in points_3:
    #     points_3_arr.append(v)
    # for k, v in points_4:
    #     points_4_arr.append(v)

    print(points_1)
    print(points_2)
    print(points_3)
    print(points_4)

    print('-----')
    sorted_dict_1 = sorted(points_1, key=points_1.get, reverse=True)[:5]
    sorted_dict_2 = sorted(points_2, key=points_2.get, reverse=True)[:5]
    sorted_dict_3 = sorted(points_3, key=points_3.get, reverse=True)[:5]
    sorted_dict_4 = sorted(points_4, key=points_4.get, reverse=True)[:5]

    sorted_dict_1_min = [(k, v) for k, v in points_1.items()]
    sorted_dict_1_min.sort(key=lambda s: s[1])
    top_1_min = [i[0] for i in sorted_dict_1_min[:5]]

    categories_names_1 = []
    categories_names_1_min = []
    categories_names_2 = []
    categories_names_3 = []
    categories_names_4 = []

    for sorted_dict in top_1_min:
        category_name = Category.objects.get(code=sorted_dict).name
        categories_names_1_min.append(category_name)
    for sorted_dict in sorted_dict_1:
        category_name = Category.objects.get(code=sorted_dict).name
        categories_names_1.append(category_name)
    for sorted_dict in sorted_dict_2:
        category_name = Category.objects.get(code=sorted_dict).name
        categories_names_2.append(category_name)
    for sorted_dict in sorted_dict_3:
        category_name = Category.objects.get(code=sorted_dict).name
        categories_names_3.append(category_name)
    for sorted_dict in sorted_dict_4:
        category_name = Category.objects.get(code=sorted_dict).name
        categories_names_4.append(category_name)

    print(categories_names_1)
    print(categories_names_2)
    print(categories_names_3)
    print(categories_names_4)

    stats = {
        'total_completion_time': str(timedelta(seconds=total_completion_time)).split('.')[0],
        'top_1': categories_names_1,
        'top_2': categories_names_2,
        'top_3': categories_names_3,
        'top_4': categories_names_4,
        'categories_names_1_min': categories_names_1_min,
    }

    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        userprofile = UserProfile.objects.get(user=request.user)
        if userprofile.role.name == 'Админ заказчика':
            company = Employee.objects.get(user=request.user).company
            stats.update({
                'employees_qnt': Employee.objects.filter(company=company).count(),
                'individual_reports_qnt': Report.objects.filter(study__company=company).count(),
                'group_reports_qnt': ReportGroup.objects.filter(company=company).count()
            })
        if userprofile.role.name == 'Админ' or userprofile.role.name == 'Суперадмин':
            stats.update({
                'companies_qnt': Company.objects.all().count(),
                'employees_qnt': Employee.objects.all().count(),
                'individual_reports_qnt': Report.objects.all().count(),
                'group_reports_qnt': ReportGroup.objects.all().count()
            })
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
            stats.update({
                'companies_qnt': companies.count(),
                'employees_qnt': Employee.objects.filter(created_by=request.user).count(),
                'individual_reports_qnt': individual_reports_qnt,
                'group_reports_qnt': group_reports_qnt
            })

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
                'percentage': participant.current_percentage,
                'completed_at': participant.completed_at,
                'answered': participant.answered_questions_qnt,
                'total': participant.total_questions_qnt,
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
                'lie_points': report.lie_points,
                'role_name': report.participant.employee.role.name_ru,
                'position': report.participant.employee.position.name_ru,
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
        try:
            response = pdf_group_generator(json_data)
            return response
        except Exception as e:
            logger.error('An error occurred: %s', str(e), exc_info=True)
            return HttpResponseBadRequest('Ошибка при создании отчета')


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
                'email': report.participant.employee.email,
                'file_name': report.file.name,
                'comments': comments
            })
        response = {
            'data': list(report_arr)
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def send_individual_report(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        report_id = json_data['report_id']
        report = Report.objects.get(id=report_id)
        full_path = os.path.join(settings.MEDIA_ROOT, 'reportsPDF', 'single', report.file.name)
        print(full_path)
        sent = False
        with open(full_path, 'rb') as f:
            sent = True
            report.participant.report_sent_at = timezone.now()
            report.participant.save()
            mail_handler.send_participant_report(
                to_email=report.participant.employee.email,
                pdf_report=f.read(),
            )

        if sent:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


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
                email = employee['email']
                name = employee['name']

                if not Employee.objects.filter(email=email).exists():
                    employee_inst = Employee()
                    employee_inst.name = name
                    employee_inst.email = email
                    employee_inst.sex = ''
                    employee_inst.birth_year = 0
                    employee_inst.company = company_inst
                    employee_inst.save()

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
                            participant_inst.total_questions_qnt = int(participant['total_questions_qnt'])
                            participant_inst.answered_questions_qnt = int(participant['answered_questions_qnt'])
                            participant_inst.current_percentage = int(participant['total_questions_qnt']) / int(
                                participant['answered_questions_qnt']) * 100
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
