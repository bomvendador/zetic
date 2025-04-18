from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError, JsonResponse, HttpResponseRedirect, FileResponse
from django.contrib.auth import authenticate, login, logout
from reports.settings import MEDIA_ROOT, BASE_DIR
from django.template.loader import render_to_string

import os
import zipfile
import json
# Create your views here.
from django.db.models import Max

from pdf.models import Company, Participant, ReportData, Report, Category, ReportGroup, ReportGroupSquare, Industry, \
    Employee, EmployeeRole, EmployeePosition, EmployeeGender, Study, ResearchTemplate, ResearchTemplateSections, \
    Section, \
    MatrixFilter, MatrixFilterParticipantNotDistributed, MatrixFilterInclusiveEmployeePosition, MatrixFilterCategory, \
    MatrixFilterParticipantNotDistributedEmployeePosition, QuestionnaireQuestionAnswers, QuestionAnswers, \
    ReportDataByCategories, Questionnaire, Project, ProjectStudy, ProjectParticipants, ConsultantCompany, \
    CommonBooleanSettings, StudyIndividualReportAllowedOptions, CompanyIndividualReportAllowedOptions, \
    IndividualReportAllowedOptions, ParticipantIndividualReportAllowedOptions, UserCompanies
# from django.contrib.auth.models import User

from login.models import UserRole, UserProfile, User
from login.views import home as login_home

from pdf_group.views import pdf_group_generator
from django.contrib.auth.decorators import login_required, wraps
from login import urls as login_urls
from django.utils import timezone
import time
# from pdf.views import pdf_single_generator
from datetime import datetime, timedelta
from django.db.models import ProtectedError

from django.db.models import Q

from .custom_funcs import squares_data

from sendemail.tasks import pdf_single_generator_task as pdf_single_generator

from django.db.models import Sum

from pdf import raw_to_t_point

from panel.constants import CONSTANT_USER_ROLES, CONSTANT_SQUARE_NAMES


def tech_works(request):
    userprofile = UserProfile.objects.get(user=request.user)
    # print(userprofile.role.name)
    tech_works_mode = CommonBooleanSettings.objects.get(name='Технические работы').value
    context = {
        'cur_userprofile': userprofile,
        'timestamp': time.time(),
        'tech_works': tech_works_mode,
    }

    return render(request, 'tech_works/tech_works_page.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def info_common(request):
    userprofile = UserProfile.objects.get(user=request.user)
    tech_works_mode = CommonBooleanSettings.objects.get(name='Технические работы').value

    context = {
        'cur_userprofile': userprofile,
        'timestamp': time.time(),
        'tech_works': tech_works_mode,
        'CONSTANT_USER_ROLES': CONSTANT_USER_ROLES
    }
    if userprofile.role.name == CONSTANT_USER_ROLES['CLIENT_ADMIN']:

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
        if userprofile.role.name == CONSTANT_USER_ROLES['CLIENT_ADMIN']:
            company = Employee.objects.get(user=request.user).company
            stats.update({
                'employees_qnt': Employee.objects.filter(company=company).count(),
                'individual_reports_qnt': Report.objects.filter(study__company=company).count(),
                'group_reports_qnt': ReportGroup.objects.filter(company=company).count()
            })
        if userprofile.role.name == CONSTANT_USER_ROLES['ADMIN'] or userprofile.role.name == CONSTANT_USER_ROLES['SUPER_ADMIN']:
            stats.update({
                'companies_qnt': Company.objects.all().count(),
                'employees_qnt': Employee.objects.all().count(),
                'individual_reports_qnt': Report.objects.all().count(),
                'group_reports_qnt': ReportGroup.objects.all().count()
            })
        if userprofile.role.name == CONSTANT_USER_ROLES['MANAGER']:
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
            'stats': stats,
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
    response = []
    match cur_user_role_name:
        case role if role == CONSTANT_USER_ROLES['MANAGER'] or cur_user_role_name == CONSTANT_USER_ROLES['PARTNER']:
            companies = Company.objects.filter(created_by=request.user)
        case role if role == CONSTANT_USER_ROLES['ADMIN'] or cur_user_role_name == CONSTANT_USER_ROLES['SUPER_ADMIN']:
            companies = Company.objects.all()
        case role if role == CONSTANT_USER_ROLES['CLIENT_ADMIN']:
            companies = Company.objects.filter(id=Employee.objects.get(user=request.user).company.id)
        #
        # case _:
        #     employees_inst = Employee.objects.filter(Q(email=email))

    # if cur_user_role_name == CONSTANT_USER_ROLES['MANAGER'] or cur_user_role_name == CONSTANT_USER_ROLES['PARTNER']:
    #     companies = Company.objects.filter(created_by=request.user)
    #
    # if cur_user_role_name == CONSTANT_USER_ROLES['ADMIN'] or cur_user_role_name == CONSTANT_USER_ROLES['SUPER_ADMIN']:
    #     companies = Company.objects.all()
    for company in companies:
        projects = Project.objects.filter(company=company)
        if projects.exists():
            response.append({
                'name': company.name,
                'id': company.id,
            })
    user_companies = UserCompanies.objects.filter(user=request.user)
    for user_company in user_companies:
        projects = Project.objects.filter(company=user_company.company)
        if projects.exists():
            response.append({
                'name': user_company.company.name,
                'id': user_company.company.id,
            })
    context.update({
        'companies': response,
        'CONSTANT_SQUARE_NAMES': CONSTANT_SQUARE_NAMES
    })

    # print(response)
    return render(request, 'panel_distribution.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def get_company_projects_for_group_report(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        projects_inst = Project.objects.filter(company_id=company_id)
        projects = []
        for project in projects_inst:
            data = {
                'id': project.id,
                'project_name': project.name,
                'company_name': project.company.name,
                'created_by': project.created_by.first_name,
                'created_at': timezone.localtime(project.created_at).strftime("%d.%m.%Y %H:%M:%S")
            }
            projects.append(data)
        response = {
            'projects': projects
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def get_company_projects_with_group_report(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        projects_inst = Project.objects.filter(company_id=company_id)
        projects = []
        for project in projects_inst:
            project_participants = ProjectParticipants.objects.filter(project=project)
            if project_participants.exists():
                data = {
                    'id': project.id,
                    'project_name': project.name,
                    'company_name': project.company.name,
                    'created_by': project.created_by.first_name,
                    'created_at': timezone.localtime(project.created_at).strftime("%d.%m.%Y %H:%M:%S")
                }
                projects.append(data)
        response = {
            'projects': projects
        }
        return JsonResponse(response)


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
def get_participants_by_project_studies(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        project_id = json_data['project_id']
        project_studies = ProjectStudy.objects.filter(project_id=project_id)
        participants = []
        data_to_check = []
        for project_study in project_studies:
            participants_inst = Participant.objects.filter(study=project_study.study, completed_at__isnull=False)
            for participant in participants_inst:
                if not [participant.employee_id, participant.study.id] in data_to_check:
                    data_to_check.append([participant.employee_id, participant.study.id])
                else:
                    for participant_arr in participants:
                        if participant_arr['id'] == participant.id:
                            participants.remove(participant_arr)
                participants.append({
                    'employee_id': participant.employee_id,
                    'id': participant.id,
                    'study_name': participant.study.name,
                    'study_id': participant.study.id,
                    'name': participant.employee.name,
                    'email': participant.employee.email,
                })
        response = {
            'participants': participants
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def get_report_participants_data(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        report_participants = json_data['report_participants']
        # print(report_participants)
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


# def get_participants_data_for_group_report(participants_ids):
#     participants_data = []
#     matrix_filters = MatrixFilter.objects.all()
#     for participant_id in participants_ids:
#         # print(f'participant_id - {participant_id}')
#         participant_inst = Participant.objects.get(id=participant_id)
#         employee_inst = Employee.objects.get(id=participant_inst.employee.id)
#         employee_position_inst = EmployeePosition.objects.get(employee=employee_inst)
#         report = Report.objects.get(participant_id=participant_id)
#         report_data_inst = ReportData.objects.filter(report=report)
#
#         # print(f'report id - {report.id}')
#         participant_squares = []
#         participant_squares_ordered = []
#         for matrix_filter in matrix_filters:
#             participant_position_is_in_filter = False
#             filter_has_positions = False
#             filter_positions_inst = MatrixFilterInclusiveEmployeePosition.objects.filter(
#                 matrix_filter=matrix_filter)
#             if filter_positions_inst:
#                 filter_has_positions = True
#                 for filter_position in filter_positions_inst:
#                     if filter_position.employee_position == employee_position_inst:
#                         participant_position_is_in_filter = True
#             if (filter_has_positions and participant_position_is_in_filter) or not filter_has_positions:
#                 # print(f'---начало--- {matrix_filter.square_code} - {matrix_filter.square_name}')
#
#                 filter_categories = MatrixFilterCategory.objects.filter(matrix_filter=matrix_filter)
#
#                 total_filter_categories = len(filter_categories)
#                 # print(f'report_data_inst = {len(report_data_inst)}')
#                 categories_fits_cnt = 0
#                 for filter_category in filter_categories:
#                     questionnaire_questions_answers_inst = QuestionnaireQuestionAnswers.objects.filter(Q(questionnaire__participant=participant_inst)
#                                                                                         & Q(question__category__code=filter_category.category.code))
#                     raw_points = 0
#                     for questionnaire_question in questionnaire_questions_answers_inst:
#                         raw_points = raw_points + questionnaire_question.answer.raw_point
#
#                     t_points = raw_to_t_point.filter_raw_points_to_t_points(raw_points, participant_inst.employee_id, filter_category.category.id)
#                     # report_data_categories_points_sum = ReportData.objects.filter(Q(report=report) & Q(category_code=filter_category.category.code)).aggregate(Sum('points'))
#                     # print(f't_points = {t_points}')
#                     if filter_category.points_from <= t_points <= filter_category.points_to:
#                         # print(f'шкала {filter_category.category.code} - {filter_category.category.name}')
#                         # print(f'{filter_category.points_from} <= {t_points} <= {filter_category.points_to}')
#                         categories_fits_cnt = categories_fits_cnt + 1
#
#                     # for data in report_data_inst:
#                     #     # print(f'фильтры {data.category_code} - {filter_category.category.code}')
#                     #     # if data.category_code == filter_category.category.code:
#                     #     #     print(f'фильтр {data.category_code}')
#                     #     #     print(f'{filter_category.points_from} <= {data.points} <= {filter_category.points_to}')
#                     #
#                     #
#                     #     if data.category_code == filter_category.category.code and \
#                     #             (filter_category.points_from <= data.points <= filter_category.points_to):
#                     #         print(f'фильтр {filter_category.category.code} сработал')
#                     #         print(f'{filter_category.points_from} <= {data.points} <= {filter_category.points_to}')
#                     #         print(f'categories_fits_cnt = {categories_fits_cnt}')
#                     #         categories_fits_cnt = categories_fits_cnt + 1
#                 # print(f'Категория - {}')
#                 # print(f'categories_fits_cnt = {categories_fits_cnt}')
#                 # print('---конец---')
#                 if categories_fits_cnt > 0:
#                     participant_squares.append({
#                         'square_name': matrix_filter.square_name,
#                         'square_code': matrix_filter.square_code,
#                         'percentage': int(categories_fits_cnt * 100 / total_filter_categories)
#                     })
#                     if len(participant_squares) > 1:
#                         sorted_participant_squares = []
#                         for i in range(len(participant_squares) - 1, 0, -1):
#                             # print(f'i = {i}')
#                             # print(f"{participant_squares[i]['percentage']} > {participant_squares[i - 1]['percentage']}")
#                             if participant_squares[i]['percentage'] > participant_squares[i - 1]['percentage']:
#                                 cur_val_percentage = participant_squares[i]['percentage']
#                                 cur_val_square_name = participant_squares[i]['square_name']
#                                 cur_val_square_code = participant_squares[i]['square_code']
#                                 prev_val_percentage = participant_squares[i - 1]['percentage']
#                                 prev_val_square_name = participant_squares[i - 1]['square_name']
#                                 prev_val_square_code = participant_squares[i - 1]['square_code']
#                                 participant_squares[i - 1]['percentage'] = cur_val_percentage
#                                 participant_squares[i - 1]['square_name'] = cur_val_square_name
#                                 participant_squares[i - 1]['square_code'] = cur_val_square_code
#                                 participant_squares[i]['percentage'] = prev_val_percentage
#                                 participant_squares[i]['square_name'] = prev_val_square_name
#                                 participant_squares[i]['square_code'] = prev_val_square_code
#         if len(participant_squares) == 0:
#             matrix_filters_participant_not_distributed_inst = MatrixFilterParticipantNotDistributed.objects.all()
#             for matrix_filter_participant_not_distributed in matrix_filters_participant_not_distributed_inst:
#                 matrix_filters_participant_not_distributed_employee_position = MatrixFilterParticipantNotDistributedEmployeePosition.objects.filter(
#                     matrix_filter=matrix_filter_participant_not_distributed)
#                 for matrix_filter_participant_not_distributed_employee_position in matrix_filters_participant_not_distributed_employee_position:
#                     if matrix_filter_participant_not_distributed_employee_position.employee_position == employee_position_inst:
#                         participant_squares.append({
#                             'square_name': matrix_filter_participant_not_distributed.square_name,
#                             'square_code': matrix_filter_participant_not_distributed.square_code,
#                             'percentage': 0
#                         })
#
#         participants_data.append({
#             'fio': report.participant.employee.name,
#             'email': report.participant.employee.email,
#             'lie_points': report.lie_points,
#             'role_name': report.participant.employee.role.name_ru,
#             'position': report.participant.employee.position.name_ru,
#             'participant_squares': participant_squares[:3],
#             'employee_id': report.participant.employee.id,
#             'participant_id': report.participant.id,
#         })
#         # print(participant_squares)
#     return participants_data


def get_participants_data_for_group_report(participants_ids):
    participants_data = []
    matrix_filters = MatrixFilter.objects.all()
    for participant_id in participants_ids:
        # print(f'participant_id - {participant_id}')
        participant_inst = Participant.objects.get(id=participant_id)
        employee_inst = Employee.objects.get(id=participant_inst.employee.id)
        employee_position_inst = EmployeePosition.objects.get(employee=employee_inst)
        # print(f'===get_participants_data_for_group_report====')
        # print(f'участник - {participant_inst.employee.name} email - {participant_inst.employee.email}')
        # print(f'===++++++++++++++++++++++++++++====')
        report = Report.objects.filter(participant_id=participant_id).latest('added')
        report_data_inst = ReportData.objects.filter(report=report)

        # print(f'report id - {report.id}')
        participant_squares = []
        participant_squares_ordered = []
        for matrix_filter in matrix_filters:
            participant_position_is_in_filter = False
            filter_has_positions = False
            filter_positions_inst = MatrixFilterInclusiveEmployeePosition.objects.filter(
                matrix_filter=matrix_filter)
            if filter_positions_inst:
                filter_has_positions = True
                for filter_position in filter_positions_inst:
                    if filter_position.employee_position == employee_position_inst:
                        participant_position_is_in_filter = True
            if (filter_has_positions and participant_position_is_in_filter) or not filter_has_positions:
                # print(f'---начало--- {matrix_filter.square_code} - {matrix_filter.square_name}')

                filter_categories = MatrixFilterCategory.objects.filter(matrix_filter=matrix_filter)

                total_filter_categories = len(filter_categories)
                # print(f'report_data_inst = {len(report_data_inst)}')
                categories_fits_cnt = 0
                for filter_category in filter_categories:
                    report_data_by_categories_inst = ReportDataByCategories.objects.filter(Q(report=report) & Q(category_code=filter_category.category.code))
                    if report_data_by_categories_inst:
                        report_data_by_categories_inst = ReportDataByCategories.objects.filter(
                            Q(report=report) & Q(category_code=filter_category.category.code)).latest('created_at')

                        t_points = report_data_by_categories_inst.t_points
                        # report_data_categories_points_sum = ReportData.objects.filter(Q(report=report) & Q(category_code=filter_category.category.code)).aggregate(Sum('points'))
                        # print(f't_points = {t_points}')
                        if filter_category.points_from <= t_points <= filter_category.points_to:
                            # print(f'шкала {filter_category.category.code} - {filter_category.category.name}')
                            # print(f'{filter_category.points_from} <= {t_points} <= {filter_category.points_to}')
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
                    # print(f'categories_fits_cnt = {categories_fits_cnt}')
                # print('---конец---')
                if categories_fits_cnt > 0:
                    participant_squares.append({
                        'square_name': matrix_filter.square_name,
                        'square_code': matrix_filter.square_code,
                        'percentage': int(categories_fits_cnt * 100 / total_filter_categories)
                    })
                    if len(participant_squares) > 1:
                        sorted_participant_squares = []
                        for i in range(len(participant_squares) - 1, 0, -1):
                            # print(f'i = {i}')
                            # print(f"{participant_squares[i]['percentage']} > {participant_squares[i - 1]['percentage']}")
                            if participant_squares[i]['percentage'] > participant_squares[i - 1]['percentage']:
                                cur_val_percentage = participant_squares[i]['percentage']
                                cur_val_square_name = participant_squares[i]['square_name']
                                cur_val_square_code = participant_squares[i]['square_code']
                                prev_val_percentage = participant_squares[i - 1]['percentage']
                                prev_val_square_name = participant_squares[i - 1]['square_name']
                                prev_val_square_code = participant_squares[i - 1]['square_code']
                                participant_squares[i - 1]['percentage'] = cur_val_percentage
                                participant_squares[i - 1]['square_name'] = cur_val_square_name
                                participant_squares[i - 1]['square_code'] = cur_val_square_code
                                participant_squares[i]['percentage'] = prev_val_percentage
                                participant_squares[i]['square_name'] = prev_val_square_name
                                participant_squares[i]['square_code'] = prev_val_square_code
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

        individual_reports_inst = Report.objects.filter(participant=report.participant)
        individual_reports_files = []
        for report in individual_reports_inst:
            individual_reports_files.append(report.file.name)

        participants_data.append({
            'fio': report.participant.employee.name,
            'email': report.participant.employee.email,
            'lie_points': report.lie_points,
            'role_name': report.participant.employee.role.name_ru,
            'position': report.participant.employee.position.name_ru,
            'participant_squares': participant_squares[:3],
            'employee_id': report.participant.employee.id,
            'participant_id': report.participant.id,
            'individual_reports_files': individual_reports_files,
        })
        # print(participant_squares)
    return participants_data


@login_required(redirect_field_name=None, login_url='/login/')
def save_group_report_data(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print('--- 700 ---')
        print(json_data)
        print('==========')
        # return
        # response = JsonResponse({"error": "there was an error"})
        # response.status_code = 403  # To announce that the user isn't allowed to publish
        # return response

        operation = json_data['operation']
        if 'report_type' in json_data:
            report_type = json_data['report_type']
        else:
            report_type = 'new'
        project_id = json_data['project_id']
        square_results = json_data['square_results']

        if operation == 'edit' and report_type == 'edit':
            group_report_id = json_data['group_report_id']
            group_report_inst = ReportGroup.objects.get(id=group_report_id)
            for square_result in square_results:
                participant_number = square_result[7]
                participant_id = square_result[8]
                report_inst = Report.objects.filter(participant_id=participant_id).latest('added')
                group_name = square_result[4]
                square_code = square_result[6]
                square_name = square_result[0]
                bold = square_result[3]
                color = square_result[5]

                if not ReportGroupSquare.objects.filter(Q(report=report_inst) &
                                                        Q(report_group_id=group_report_id)).exists():
                    report_group_square = ReportGroupSquare()
                    report_group_square.report = report_inst
                    # new_particoapnt_number =
                    if participant_number == '':
                        report_group_square_inst = ReportGroupSquare.objects.filter(report_group=group_report_inst)
                        biggest_number = 0
                        if report_group_square_inst:
                            biggest_number = report_group_square_inst.aggregate(Max('participant_number'))['participant_number__max'] + 1
                            # for report_group_square in report_group_square_inst:
                            #     if int(report_group_square.participant_number) > int(biggest_number):
                            #         biggest_number = report_group_square.participant_number
                        else:
                            biggest_number = 1
                        report_group_square.participant_number = biggest_number
                        # print(f'biggest_number = {biggest_number + 1}')
                    else:
                        report_group_square.participant_number = participant_number
                        biggest_number = participant_number
                    report_group_square.report_group = group_report_inst
                    # print(f'new_report_group_square -в = {report_group_square.id}')
                    square_result[7] = biggest_number
                else:
                    report_group_square = ReportGroupSquare.objects.get(Q(report=report_inst) &
                                                        Q(report_group_id=group_report_id))
                report_group_square.square_name = square_name
                report_group_square.square_code = square_code
                report_group_square.participant_group_color = color
                report_group_square.participant_group = group_name
                report_group_square.bold = bold
                report_group_square.save()

            json_data['square_results'] = square_results
            # ReportGroupSquare.objects.filter(report_group=group_report_inst).delete()
            project_participants = ProjectParticipants.objects.filter(report_group=group_report_inst)
            project = project_participants[0].project
            json_data['project_name'] = project.name
            json_data['company_name'] = project.company.name

        else:
            project_id = json_data['project_id']
            project = Project.objects.get(id=project_id)
            json_data['project_name'] = project.name
            json_data['company_name'] = project.company.name
            json_data['report_type'] = report_type

            cnt = 0
            for square_result in square_results:
                cnt = cnt + 1
                # square_result.append(cnt)
                square_result[7] = cnt
        response = pdf_group_generator(json_data)

        return JsonResponse({'response': response})


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
        employees_inst = Employee.objects.filter(company_id=company_id)
        employees = []

        for employee in employees_inst:
            report_group_squares_employee = ReportGroupSquare.objects.filter(Q(report__participant__employee=employee) &
                                                                             Q(report_group=group_report_id))
            if not report_group_squares_employee:
                individual_reports = Report.objects.filter(participant__employee=employee)
                if individual_reports.exists():
                    report_files = []
                    for individual_report in individual_reports:
                        report_files.append(individual_report.file.name)
                    employees.append({
                        'participant_data': get_participants_data_for_group_report([individual_reports.latest('added').participant.id]),
                        'squares_data': squares_data,
                        'report_file': report_files
                    })
        return JsonResponse(employees, safe=False)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_group_report_data(request, report_id,  project_id):
    context = info_common(request)
    group_report_inst = ReportGroup.objects.get(id=report_id)
    group_report_squares_inst = ReportGroupSquare.objects.filter(report_group=group_report_inst).order_by('participant_number')
    group_reports = []
    group_names = []
    for group_report in group_report_squares_inst:

        # participants_emails.append(group_report.report.participant.employee.email)
        participant_data = get_participants_data_for_group_report([group_report.report.participant.id])
        # print(participant_data)
        individual_reports_inst = Report.objects.filter(participant=group_report.report.participant)
        individual_reports_files = []
        for report in individual_reports_inst:
            individual_reports_files.append(report.file.name)

        report_data = {
                'bold': group_report.bold,
                'square_code': group_report.square_code,
                'participant_number': group_report.participant_number,
                'employee_id': group_report.report.participant.employee.id,
                'group_name': group_report.participant_group,
                'group_color': group_report.participant_group_color,
                'individual_reports_files': individual_reports_files,
        }
        if group_report.participant_group not in group_names:
            group_names.append(group_report.participant_group)
            report_data.update({
                'group_name_modal': group_report.participant_group,
                'group_color_modal': group_report.participant_group_color,
            })
        group_reports.append({
            'participant_data': participant_data[0],
            'report': report_data,

        })
    context.update({
        'group_reports': group_reports,
        'squares_data': squares_data,
        'company_id': group_report_inst.company.id,
        'group_report_id': report_id,
        'company_name': group_report_inst.company.name,
        'project_id': project_id,
        'type': 'edit',
        'CONSTANT_SQUARE_NAMES': CONSTANT_SQUARE_NAMES,
    })
    # print(group_reports)

    return render(request, 'panel_edit_group_report.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def copy_group_report_data(request, report_id,  project_id):
    context = info_common(request)
    group_report_inst = ReportGroup.objects.get(id=report_id)
    group_report_squares_inst = ReportGroupSquare.objects.filter(report_group=group_report_inst).order_by('participant_number')
    group_reports = []
    group_names = []
    for group_report in group_report_squares_inst:

        # participants_emails.append(group_report.report.participant.employee.email)
        participant_data = get_participants_data_for_group_report([group_report.report.participant.id])
        # print(participant_data)
        report_data = {
                'bold': group_report.bold,
                'square_code': group_report.square_code,
                'participant_number': group_report.participant_number,
                'employee_id': group_report.report.participant.employee.id,
                'group_name': group_report.participant_group,
                'group_color': group_report.participant_group_color,
        }
        if group_report.participant_group not in group_names:
            group_names.append(group_report.participant_group)
            report_data.update({
                'group_name_modal': group_report.participant_group,
                'group_color_modal': group_report.participant_group_color,
            })
        group_reports.append({
            'participant_data': participant_data[0],
            'report': report_data,

        })

    context.update({
        'group_reports': group_reports,
        'squares_data': squares_data,
        'company_id': group_report_inst.company.id,
        'group_report_id': report_id,
        'company_name': group_report_inst.company.name,
        'project_id': project_id,
        'type': 'copy',
        'CONSTANT_SQUARE_NAMES': CONSTANT_SQUARE_NAMES,
    })
    # print(group_reports)

    return render(request, 'panel_edit_group_report.html', context)


# список командных отчетов
@login_required(redirect_field_name=None, login_url='/login/')
def group_reports_list(request):
    context = info_common(request)
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
        if cur_user_role_name == CONSTANT_USER_ROLES['MANAGER'] or cur_user_role_name == CONSTANT_USER_ROLES['PARTNER']:
            companies = Company.objects.filter(created_by=request.user)
        if cur_user_role_name == CONSTANT_USER_ROLES['CLIENT_ADMIN']:
            companies = Company.objects.filter(id=Employee.objects.get(user=request.user).company.id)
        if cur_user_role_name == CONSTANT_USER_ROLES['ADMIN'] or cur_user_role_name == CONSTANT_USER_ROLES['SUPER_ADMIN']:
            companies = Company.objects.all()
        companies_arr = []
        for company in companies:
            projects = Project.objects.filter(company=company)
            if projects.exists():
                companies_arr.append({
                    'name': company.name,
                    'id': company.id,
                })
        user_companies = UserCompanies.objects.filter(user=request.user)
        for user_company in user_companies:
            projects = Project.objects.filter(company=user_company.company)
            if projects.exists():
                companies_arr.append({
                    'name': user_company.company.name,
                    'id': user_company.company.id,
                })

        context.update(
            {'companies_arr': companies_arr}
        )

        return render(request, 'panel_group_reports_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def get_group_reports_list(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        project_id = json_data['project_id']
        project_participants = ProjectParticipants.objects.filter(project_id=project_id)

        if project_participants.exists():
            report = []
            for project_participant in project_participants:
                group_report = project_participant.report_group
                report_exists = False
                for report_item in report:
                    if report_item['id'] == group_report.id:
                        report_exists = True

                if not report_exists:
                    report_group_square_arr = []
                    reports_group_square = ReportGroupSquare.objects.filter(report_group=group_report)
                    if reports_group_square.exists():
                        for report_group_square in reports_group_square:
                            # print(f'report_group_square - {report_group_square.report.id}')
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
        if cur_user_role_name == 'Консультант':
            consultant_companies = ConsultantCompany.objects.filter(user=request.user)
            companies = []
            if consultant_companies.exists():
                for consultant_company in consultant_companies:
                    companies.append(consultant_company.company)
        if cur_user_role_name == CONSTANT_USER_ROLES['MANAGER'] or cur_user_role_name == CONSTANT_USER_ROLES['PARTNER']:
            companies = Company.objects.filter(created_by=request.user)
        if cur_user_role_name == CONSTANT_USER_ROLES['CLIENT_ADMIN']:
            companies = Company.objects.filter(id=Employee.objects.get(user=request.user).company.id)
        if cur_user_role_name == CONSTANT_USER_ROLES['ADMIN'] or cur_user_role_name == CONSTANT_USER_ROLES['SUPER_ADMIN']:
            companies = Company.objects.all()

        companies_arr = []
        for company in companies:
            reports = Report.objects.filter(participant__employee__company=company)
            if reports.exists():
                companies_arr.append({
                    'name': company.name,
                    'id': company.id
                })
        user_companies = UserCompanies.objects.filter(user=request.user)
        for user_company in user_companies:
            reports = Report.objects.filter(participant__employee__company=user_company.company)
            if reports.exists():
                companies_arr.append({
                    'name': user_company.company.name,
                    'id': user_company.company.id,
                })

        context.update({
            'companies_arr': companies_arr,
            # 'companies_arr': IndividualReportAllowedOptions.objects.all()
        })

        return render(request, 'individual_reports/panel_individual_reports_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def get_individual_reports_list(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        reports = Report.objects.filter(participant__employee__company__id=company_id)

        report_arr = []
        for report in reports:
            if report.study:
                study_name = report.study.name
            else:
                study_name = ""
            if report.comments:
                comments = report.comments
            else:
                comments = ''
            participant_individual_report_allowed_options = ParticipantIndividualReportAllowedOptions.objects.filter(
                participant=report.participant)
            report_allowed_options = []
            for option in participant_individual_report_allowed_options:
                report_allowed_options.append({
                    'option_name': option.option.name,
                    'option_value': option.value,
                })
            employee = report.participant.employee
            report_arr.append({
                'id': report.id,
                'company': report.participant.employee.company.name,
                'study_name': study_name,
                'participant_id': report.participant.id,
                'email': report.participant.employee.email,
                'date': timezone.localtime(report.added).strftime("%d.%m.%Y %H:%M:%S"),
                'name': report.participant.employee.name,
                'file_name': report.file.name,
                'comments': comments,
                'timestamp': report.added,
                'primary': report.primary,
                'type': report.type,
                'report_allowed_options': report_allowed_options,
                'industry': employee.industry.name_ru,
                'position': employee.position.name_ru,
                'role': employee.role.name_ru,
                'birth_year': employee.birth_year,
                'gender': employee.sex.name_ru,
            })
        # study_individual_report_allowed_options = StudyIndividualReportAllowedOptions.objects.filter(study=study)
        company_individual_report_allowed_options = CompanyIndividualReportAllowedOptions.objects.filter(company_id=company_id)
        reports_options = []
        for option in company_individual_report_allowed_options:
            reports_options.append({
                'company_option_id': option.id,
                'individual_option_id': option.option.id,
                'option_name': option.option.name,
                'value': option.value
            })
        modal_report_option = render_to_string('individual_reports/modal_report_option.html', {'options': company_individual_report_allowed_options})
        response = {
            'data': list(report_arr),
            # 'modal_report_option': list(reports_options),
            'modal_report_option': modal_report_option
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def individual_report_group_action(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        action_type = json_data['action_type']
        selected_participants_reports_ids = json_data['selected_participants_reports_ids']
        match action_type:
            case 'download_individual_reports':
                tmp = os.path.join(BASE_DIR, 'media', 'files', 'tmp')
                zip_name = 'Индивидуальные отчеты_' + Report.objects.get(id=selected_participants_reports_ids[0]).participant.employee.company.name + \
                           '_' + str(len(selected_participants_reports_ids)) + '_шт_' + str(time.time()) + '.zip'
                with zipfile.ZipFile(os.path.join(tmp, zip_name), 'w') as zipf:
                    for report_id in selected_participants_reports_ids:
                        report = Report.objects.get(id=report_id)
                        zipf.write(os.path.join(MEDIA_ROOT, 'reportsPDF', 'single', report.file.name), arcname=report.file.name)
                return HttpResponse(zip_name)
            case 'download_t_points':
                categories_names = []
                reports_data = []
                for report_id in selected_participants_reports_ids:
                    report = Report.objects.get(id=report_id)
                    report_data = {
                        'company': report.participant.employee.company.name,
                        'participant': report.participant.employee.name,
                        'email': report.participant.employee.email,
                        'gender': report.participant.employee.sex.name_ru,
                        'position': report.participant.employee.position.name_ru,
                        'industry': report.participant.employee.industry.name_ru,
                        'role': report.participant.employee.role.name_ru,
                        'birth_year': report.participant.employee.birth_year,
                        'completed_at': timezone.localtime(report.participant.completed_at).strftime("%d.%m.%Y %H:%M:%S"),
                        'categories_data': []
                    }
                    categories = Category.objects.all().order_by('code')
                    for category in categories:
                        report_data_by_categories = ReportDataByCategories.objects.filter(Q(report_id=report_id) &
                                                                                          Q(category_code=category.code))
                        if report_data_by_categories:
                            if category.name not in categories_names:
                                categories_names.append(category.name)
                            for report_data_by_category in report_data_by_categories:
                                report_data['categories_data'].append({
                                    'name': category.name,
                                    'points': report_data_by_category.t_points
                                })
                    reports_data.append(report_data)
                return JsonResponse({
                    'reports_data': reports_data,
                    'categories_names': categories_names
                })


@login_required(redirect_field_name=None, login_url='/login/')
def users_list(request):
    context = info_common(request)
    context.update(
        {'user_profiles': UserProfile.objects.all()}
    )

    return render(request, 'panel_users_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def user_profile(request, user_id):
    user_ = User.objects.get(id=user_id)
    context = info_common(request)
    user_companies = Company.objects.filter(created_by=user_)
    companies_set_to_user = UserCompanies.objects.filter(user=user_)
    not_user_companies = Company.objects.filter(~Q(created_by=user_))
    available_companies = []
    companies_set_by_admin = []
    for company in not_user_companies:
        if not UserCompanies.objects.filter(Q(company=company) & Q(user=user_)).exists():
            available_companies.append({
                'id': company.id,
                'name': company.name,
            })
        else:
            companies_set_by_admin.append({
                'id': company.id,
                'name': company.name,
            })
    context.update({
        'user_profile': UserProfile.objects.get(user_id=user_id),
        'roles': UserRole.objects.all(),
        'user_companies': user_companies,
        'companies_set_to_user': companies_set_to_user,
        'available_companies': available_companies,
        'companies_set_by_admin': companies_set_by_admin,
    })
    return render(request, 'panel_user_profile.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_user_company(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        user_id = json_data['user_id']
        company_id = json_data['company_id']
        new_user_company = UserCompanies()
        new_user_company.created_by = request.user
        new_user_company.user = User.objects.get(id=user_id)
        new_user_company.company = Company.objects.get(id=company_id)
        new_user_company.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_user_company(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        user_id = json_data['user_id']
        company_id = json_data['company_id']
        UserCompanies.objects.get(Q(user=User.objects.get(id=user_id)) &
                                  Q(company=Company.objects.get(id=company_id))).delete()
        return HttpResponse(status=200)


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
        user_inst.first_name = fio
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

        if User.objects.filter(username=email).exists():
            response = {
                'error': 'Пользователь с указанным email уже существует'
            }
            return JsonResponse(response)
        else:
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

        return HttpResponse(status=200)


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
        # print(json_data)
        # print(type(json.loads(json_data)))
        companies = json.loads(json_data)['companies']
        # print(type(companies))
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


# def page_not_found(request):
#     return render(request, 'error_pages/error_404.html')


from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.template import Context, Engine, TemplateDoesNotExist, loader


def page_not_found(request, exception, template_name='error_pages/error_404.html'):
    template = loader.get_template(template_name)
    return HttpResponseNotFound(template.render())


def custom_404(request, exception):
    return render(request, 'error_pages/error_404.html', status=404)