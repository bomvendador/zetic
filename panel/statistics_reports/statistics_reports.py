from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, User, Participant, EmployeeGender, \
    Project, ProjectParticipants, Questionnaire, Report, QuestionnaireVisits, QuestionnaireQuestionAnswers, Study, UserCompanies
from login.models import UserProfile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from panel.views import info_common


@login_required(redirect_field_name=None, login_url='/login/')
def report_1(request):
    context = info_common(request)
    cur_user_role_name = context['cur_userprofile'].role.name
    match cur_user_role_name:
        case 'Суперадмин':
            companies = Company.objects.all()
        case 'Админ' | 'Партнер':
            companies = Company.objects.filter(created_by=request.user)
        case _:
            companies = 'No companies for user'
    user_companies = UserCompanies.objects.filter(user=request.user)

    filters = {
        'companies': companies,
        'user_companies': user_companies,
        'genders': EmployeeGender.objects.all(),
        'roles': EmployeeRole.objects.all(),
        'industries': Industry.objects.all(),
        'positions': EmployeePosition.objects.all(),
    }
    print(filters)

    context.update(
        {
            'name': 'Заполнившие опросник участники',
            'filters': filters
        }
    )

    return render(request, 'statistics_reports/report_1/panel_statistics_report_1.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def report_2(request):
    context = info_common(request)
    cur_user_role_name = context['cur_userprofile'].role.name
    match cur_user_role_name:
        case 'Суперадмин':
            companies = Company.objects.all()
        case 'Админ' | 'Партнер':
            companies = Company.objects.filter(created_by=request.user)
        case _:
            companies = 'No companies for user'
    user_companies = UserCompanies.objects.filter(user=request.user)

    filters = {
        'companies': companies,
        'user_companies': user_companies,
        'genders': EmployeeGender.objects.all(),
        'roles': EmployeeRole.objects.all(),
        'industries': Industry.objects.all(),
        'positions': EmployeePosition.objects.all(),
    }

    context.update(
        {
            'name': 'Незаполнившие опросник участники',
            'filters': filters
        }
    )

    return render(request, 'statistics_reports/report_2/panel_statistics_report_2.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def report_3(request):
    context = info_common(request)
    cur_user_role_name = context['cur_userprofile'].role.name
    match cur_user_role_name:
        case 'Суперадмин':
            companies = Company.objects.all()
        case 'Админ' | 'Партнер':
            companies = Company.objects.filter(created_by=request.user)
        case _:
            companies = 'No companies for user'
    user_companies = UserCompanies.objects.filter(user=request.user)

    filters = {
        'companies': companies,
        'user_companies': user_companies,
        'genders': EmployeeGender.objects.all(),
        'roles': EmployeeRole.objects.all(),
        'industries': Industry.objects.all(),
        'positions': EmployeePosition.objects.all(),
    }

    context.update(
        {
            'name': 'Сотрудники компаний',
            'filters': filters
        }
    )

    return render(request, 'statistics_reports/report_3/panel_statistics_report_3.html', context)


