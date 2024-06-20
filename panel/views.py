from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

import json
# Create your views here.

from pdf.models import Company, Participant, ReportData, Report, Category, ReportGroup, ReportGroupSquare, Industry, \
    Employee, EmployeeRole, EmployeePosition, EmployeeGender, Study, ResearchTemplate, ResearchTemplateSections, \
    Section, \
    MatrixFilter, MatrixFilterParticipantNotDistributed, MatrixFilterInclusiveEmployeePosition, MatrixFilterCategory, \
    MatrixFilterParticipantNotDistributedEmployeePosition
# from django.contrib.auth.models import User

from login.models import UserRole, UserProfile, User
from login.views import home as login_home

from pdf_group.views import pdf_group_generator
from django.contrib.auth.decorators import login_required, wraps
from login import urls as login_urls
from django.utils import timezone
import time
from pdf.views import pdf_single_generator
from datetime import datetime, timedelta
from django.db.models import ProtectedError

from django.db.models import Q

from .custom_funcs import squares_data

from django.db.models import Sum


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

    if cnt > 0:
        total_completion_time = time_diff_total / cnt
    else:
        total_completion_time = 0
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
        '2_2': 0,
        '2_8': 0,
        '2_10': 0,
        '2_12': 0,
        '2_14': 0,
        '2_15': 0,
        '2_16': 0,
        '2_17': 0,
        '2_18': 0,
        '2_19': 0,
        '2_20': 0,
    }
    points_3 = {
        '3_13': 0,
        '3_14': 0,
        '3_15': 0,
        '3_16': 0,
        '3_17': 0,
        '3_18': 0,
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
        # if report.section_code == '2':
        #     points_2[report.category_code] = points_2[report.category_code] + report.points
        if report.section_code == '3':
            points_3[report.category_code] = points_3[report.category_code] + report.points
        if report.section_code == '4':
            points_4[report.category_code] = points_4[report.category_code] + report.points

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
                'id': participant.id,
                'study_name': participant.study.name,
                'employee_id': participant.employee.id,
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
        participants_data = get_participants_data_for_group_report(report_participants)
        response = {}


        # matrix_filters = MatrixFilter.objects.all()
        # for participant in report_participants:
        #     participant_position_is_in_filter = False
        #     print(f'participant - {participant}')
        #     employee_inst = Employee.objects.get(email=participant)
        #     employee_position_inst = EmployeePosition.objects.get(employee=employee_inst)
        #     report = Report.objects.filter(participant__employee__email=participant).latest('added')
        #     participant_squares = []
        #     for matrix_filter in matrix_filters:
        #         filter_has_positions = False
        #         filter_positions_inst = MatrixFilterInclusiveEmployeePosition.objects.filter(
        #             matrix_filter=matrix_filter)
        #         if filter_positions_inst:
        #             filter_has_positions = True
        #             for filter_position in filter_positions_inst:
        #                 if filter_position.employee_position == employee_position_inst:
        #                     participant_position_is_in_filter = True
        #         if (filter_has_positions and participant_position_is_in_filter) or not filter_has_positions:
        #             filter_categories = MatrixFilterCategory.objects.filter(matrix_filter=matrix_filter)
        #             report_data_inst = ReportData.objects.filter(report=report)
        #             total_filter_categories = len(filter_categories)
        #             categories_fits_cnt = 0
        #             for filter_category in filter_categories:
        #                 for data in report_data_inst:
        #                     if data.category_code == filter_category.category.code and \
        #                             (filter_category.points_from <= data.points <= filter_category.points_to):
        #                         categories_fits_cnt = categories_fits_cnt + 1
        #             if categories_fits_cnt > 0:
        #                 participant_squares.append({
        #                     'square_name': matrix_filter.square_name,
        #                     'square_code': matrix_filter.square_code,
        #                     'percentage': categories_fits_cnt * 100 / total_filter_categories
        #                 })
        #     if len(participant_squares) == 0:
        #         matrix_filters_participant_not_distributed_inst = MatrixFilterParticipantNotDistributed.objects.all()
        #         for matrix_filter_participant_not_distributed in matrix_filters_participant_not_distributed_inst:
        #             matrix_filters_participant_not_distributed_employee_position = MatrixFilterParticipantNotDistributedEmployeePosition.objects.filter(matrix_filter=matrix_filter_participant_not_distributed)
        #             for matrix_filter_participant_not_distributed_employee_position in matrix_filters_participant_not_distributed_employee_position:
        #                 if matrix_filter_participant_not_distributed_employee_position.employee_position == employee_position_inst:
        #                     participant_squares.append({
        #                         'square_name': matrix_filter_participant_not_distributed.square_name,
        #                         'square_code': matrix_filter_participant_not_distributed.square_code,
        #                         'percentage': 0
        #                     })
        #
        #     participants_data.append({
        #         'fio': report.participant.employee.name,
        #         'email': report.participant.employee.email,
        #         'lie_points': report.lie_points,
        #         'role_name': report.participant.employee.role.name_ru,
        #         'position': report.participant.employee.position.name_ru,
        #         'participant_squares': participant_squares,
        #     })

        # report_datas = ReportData.objects.filter(report=report)
        # for report_data in report_datas:
        #     # print(report_data)
        #     participants_data.append({
        #         'fio': report_data.report.participant.employee.name,
        #         'section_code': report_data.section_code,
        #         'category_code': report_data.category_code,
        #         'points': report_data.points,
        #     })
        response = {
            'squares_data': squares_data,
            # 'data': list(participants_data),
            'participants_data': list(participants_data)
        }
        return JsonResponse(response, safe=False)


def get_participants_data_for_group_report(participants_ids):
    participants_data = []
    matrix_filters = MatrixFilter.objects.all()
    for participant_id in participants_ids:
        participant_position_is_in_filter = False
        print(f'participant_id - {participant_id}')
        participant_inst = Participant.objects.get(id=participant_id)
        employee_inst = Employee.objects.get(id=participant_inst.employee.id)
        employee_position_inst = EmployeePosition.objects.get(employee=employee_inst)
        report = Report.objects.get(participant_id=participant_id)
        report_data_inst = ReportData.objects.filter(report=report)

        print(f'report id - {report.id}')
        participant_squares = []
        participant_squares_ordered = []
        for matrix_filter in matrix_filters:
            filter_has_positions = False
            filter_positions_inst = MatrixFilterInclusiveEmployeePosition.objects.filter(
                matrix_filter=matrix_filter)
            if filter_positions_inst:
                filter_has_positions = True
                for filter_position in filter_positions_inst:
                    if filter_position.employee_position == employee_position_inst:
                        participant_position_is_in_filter = True
            if (filter_has_positions and participant_position_is_in_filter) or not filter_has_positions:
                print(f'---начало---')

                filter_categories = MatrixFilterCategory.objects.filter(matrix_filter=matrix_filter)

                total_filter_categories = len(filter_categories)
                # print(f'report_data_inst = {len(report_data_inst)}')
                categories_fits_cnt = 0
                for filter_category in filter_categories:
                    report_data_categories_points_sum = ReportData.objects.filter(Q(report=report) & Q(category_code=filter_category.category.code)).aggregate(Sum('points'))
                    if filter_category.points_from <= len(report_data_categories_points_sum) <= filter_category.points_to:
                        categories_fits_cnt = categories_fits_cnt + 1

                    # for data in report_data_inst:
                    #     # print(f'фильтры {data.category_code} - {filter_category.category.code}')
                    #     # if data.category_code == filter_category.category.code:
                    #     #     print(f'фильтр {data.category_code}')
                    #     #     print(f'{filter_category.points_from} <= {data.points} <= {filter_category.points_to}')
                    #
                    #
                    #     if data.category_code == filter_category.category.code and \
                    #             (filter_category.points_from <= data.points <= filter_category.points_to):
                    #         print(f'фильтр {filter_category.category.code} сработал')
                    #         print(f'{filter_category.points_from} <= {data.points} <= {filter_category.points_to}')
                    #         print(f'categories_fits_cnt = {categories_fits_cnt}')
                    #         categories_fits_cnt = categories_fits_cnt + 1
                # print(f'Категория - {}')
                print(f'categories_fits_cnt = {categories_fits_cnt}')
                print('---конец---')
                if categories_fits_cnt > 0:
                    participant_squares.append({
                        'square_name': matrix_filter.square_name,
                        'square_code': matrix_filter.square_code,
                        'percentage': int(categories_fits_cnt * 100 / total_filter_categories)
                    })
                    # if len(participant_squares) > 1:
                    #     for i in range(len(participant_squares) - 1, 0, -1):
                    #         # print(f'i = {i}')
                    #         # print(f"{participant_squares[i]['percentage']} > {participant_squares[i - 1]['percentage']}")
                    #         if participant_squares[i]['percentage'] > participant_squares[i - 1]['percentage']:
                    #             cur_val = participant_squares[i]['percentage']
                    #             prev_val = participant_squares[i - 1]['percentage']
                    #             participant_squares[i - 1]['percentage'] = cur_val
                    #             participant_squares[i]['percentage'] = prev_val
        if len(participant_squares) == 0:
            matrix_filters_participant_not_distributed_inst = MatrixFilterParticipantNotDistributed.objects.all()
            for matrix_filter_participant_not_distributed in matrix_filters_participant_not_distributed_inst:
                matrix_filters_participant_not_distributed_employee_position = MatrixFilterParticipantNotDistributedEmployeePosition.objects.filter(
                    matrix_filter=matrix_filter_participant_not_distributed)
                for matrix_filter_participant_not_distributed_employee_position in matrix_filters_participant_not_distributed_employee_position:
                    if matrix_filter_participant_not_distributed_employee_position.employee_position == employee_position_inst:
                        participant_squares.append({
                            'square_name': matrix_filter_participant_not_distributed.square_name,
                            'square_code': matrix_filter_participant_not_distributed.square_code,
                            'percentage': 0
                        })

        participants_data.append({
            'fio': report.participant.employee.name,
            'email': report.participant.employee.email,
            'lie_points': report.lie_points,
            'role_name': report.participant.employee.role.name_ru,
            'position': report.participant.employee.position.name_ru,
            'participant_squares': participant_squares,
            'employee_id': report.participant.employee.id,
            'participant_id': report.participant.id,
        })
        print(participant_squares)
    return participants_data


@login_required(redirect_field_name=None, login_url='/login/')
def save_group_report_data(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print('--- 421 ---')
        print(json_data)
        print('===421===')

        operation = json_data['operation']
        square_results = json_data['square_results']

        if operation == 'edit':
            group_report_inst = ReportGroup.objects.get(id=json_data['group_report_id'])
            # report_group_square = ReportGroupSquare.objects.filter(report_group=group_report_inst).delete()
            # ReportGroupSquare.objects.filter(report_group=group_report_inst).delete()
            for square_result in square_results:
                participant_number = square_result[7]
                if participant_number == '':
                    report_group_square_inst = ReportGroupSquare.objects.filter(report_group=group_report_inst)
                    biggest_number = 0
                    if report_group_square_inst:
                        for report_group_square in report_group_square_inst:
                            if int(report_group_square.participant_number) > int(biggest_number):
                                biggest_number = report_group_square.participant_number
                    else:
                        biggest_number = 1
                    new_report_group_square = ReportGroupSquare()
                    new_report_group_square.report_group = group_report_inst
                    new_report_group_square.participant_number = biggest_number + 1
                    new_report_group_square.save()
                    square_result[7] = biggest_number + 1
            json_data['square_results'] = square_results
            ReportGroupSquare.objects.filter(report_group=group_report_inst).delete()
        else:
            cnt = 0
            for square_result in square_results:
                cnt = cnt + 1
                square_result.append(cnt)

        print('--- 449 ---')
        print(json_data)
        print('===449===')


        # for item in json_data['square_results']:
        #     print(item)
        response = pdf_group_generator(json_data)
        return response


@login_required(redirect_field_name=None, login_url='/login/')
def delete_participant_from_group_report(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        employee_id = json_data['employee_id']
        group_report_id = json_data['group_report_id']
        group_report_squares = ReportGroupSquare.objects.filter(Q(report_group=ReportGroup.objects.get(id=group_report_id)) & Q(report__participant__employee_id=employee_id))[0]
        group_report_squares.delete()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def get_available_participants_for_group_report(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        group_report_id = json_data['group_report_id']
        group_report_inst = ReportGroup.objects.get(id=group_report_id)
        group_report_squares_inst = ReportGroupSquare.objects.filter(report_group=group_report_inst)
        company_inst = Company.objects.get(id=company_id)
        reports_inst = Report.objects.filter(participant__employee__company=company_inst)
        employees_inst = Employee.objects.filter(company_id=company_id)
        employees = []
        for report in reports_inst:
            # print(employee.name)
            employee_is_in_group_report = False
            for group_report_participant in group_report_squares_inst:
                if group_report_participant.report.participant.employee == report.participant.employee:
                    employee_is_in_group_report = True
            if not employee_is_in_group_report:
                # print(employee.email)
                employees.append({
                    'participant_data': get_participants_data_for_group_report([report.participant.id]),
                    'squares_data': squares_data
                })
        print(employees)
        return JsonResponse(employees, safe=False)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_group_report_data(request, report_id):
    context = info_common(request)
    group_report_inst = ReportGroup.objects.get(id=report_id)
    group_report_squares_inst = ReportGroupSquare.objects.filter(report_group=group_report_inst)
    participants_emails = []
    group_reports = []
    for group_report in group_report_squares_inst:

        # participants_emails.append(group_report.report.participant.employee.email)
        participant_data = get_participants_data_for_group_report([group_report.report.participant.id])
        print(participant_data)
        group_reports.append({
            'participant_data': participant_data[0],
            'report': {
                'group_name': group_report.participant_group,
                'group_color': group_report.participant_group_color,
                'bold': group_report.bold,
                'square_code': group_report.square_code,
                'participant_number': group_report.participant_number,
                'employee_id': group_report.report.participant.employee.id
            },

        })

    context.update({
        'group_reports': group_reports,
        'squares_data': squares_data,
        'company_id': group_report_inst.company.id,
        'group_report_id': report_id,
        'company_name': group_report_inst.company.name,
    })
    print(group_reports)

    return render(request, 'panel_edit_group_report.html', context)


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
                # print(f'report_group_square - {report_group_square.id}')
                report_group_square_arr.append(report_group_square.report.participant.employee.name)
            report.append({
                'company': group_report.company.name,
                'id': group_report.id,
                'date': timezone.localtime(group_report.added).strftime("%d.%m.%Y %H:%M:%S"),
                'timestamp': group_report.added,
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
        try:
            user.delete()
            return HttpResponse('ok')
        except ProtectedError:
            user_profile_inst = UserProfile.objects.get(user=user)
            user_profile_inst.active = False
            user_profile_inst.save()
            return HttpResponse('error')


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
