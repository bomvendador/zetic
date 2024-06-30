from pdf.models import Section, Industry, EmployeeRole, EmployeePosition, EmployeeGender, Company, Employee, Report, \
    Category, ReportDataByCategories, Study, Questionnaire, Participant
from login.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone

from .views import info_common
from api import outcoming
from datetime import datetime
from django.utils.dateparse import parse_datetime

from django.db.models import Q

@login_required(redirect_field_name=None, login_url='/login/')
def migration_home(request):
    context = info_common(request)
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        context.update({
            'categories': Category.objects.all(),
            'industries': Industry.objects.all(),
            'roles': EmployeeRole.objects.all(),
            'positions': EmployeePosition.objects.all(),
            'genders': EmployeeGender.objects.all()
        })

        return render(request, 'panel_add_questionnaire_results_xls.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def save_report_data_from_xls(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        questionnaire_results_arr = json_data['questionnaire_results_arr']
        # print(questionnaire_results_arr)
        categories = Category.objects.all()
        participants_not_allowed = []
        for result in questionnaire_results_arr:
            participant_allowed = True
            completed_at_str = str(result['Дата заполнения']).strip()
            # completed_at = parse_datetime(completed_at_str)
            split_time_date = completed_at_str.split(' ')
            split_date_by_slash = split_time_date[0].split('/')
            split_date_by_dot = split_time_date[0].split('.')
            if len(split_date_by_slash) > 1:
                split_date = split_date_by_slash
            else:
                split_date = split_date_by_dot
            split_time = split_time_date[1].split(':')
            # print('------------------')
            # print(len(split_date_by_slash))
            # print(len(split_date_by_dot))
            # print(split_time_date)
            # print(split_date)
            # print(split_time)
            # print('+++++++++++++++++++')
            year_str = split_date[2]
            if len(year_str) < 4:
                year_int = int('20' + split_date[2])
            else:
                year_int = int(split_date[2])
            # print(split_date[1][0])
            if split_date[1][0] == '0':
                month_int = int(split_date[1][1])
            else:
                month_int = int(split_date[1])
            print(month_int)

            completed_at = datetime(year_int, month_int, int(split_date[0]), int(split_time[0]), int(split_time[1]))
            # print(completed_at.year)
            # print(completed_at.month)
            # print(completed_at.day)

            # datetime.date()
            # print(completed_at)

            company_name = str(result['Компания']).strip()
            company_inst = Company.objects.filter(name=company_name)
            if company_inst.exists():
                company_inst = Company.objects.get(name=company_name)
            else:
                company_inst = Company()
                company_inst.name = company_name
                company_inst.created_by = request.user
                company_inst.save()
            employee_email = str(result['Email']).strip()
            employee_fio = str(result['ФИО']).strip()
            employee_gender = str(result['Пол']).strip()
            employee_position = str(result['Должности']).strip()
            employee_industry = str(result['Индустрии']).strip()
            employee_role = str(result['Роли/Функции сотрудников']).strip()
            employee_birth_year = str(result['Год рождения']).strip()
            employee_inst = Employee.objects.filter(email=employee_email)
            if employee_inst.exists():
                employee_inst = Employee.objects.get(email=employee_email)
            else:
                employee_inst = Employee()
                employee_inst.name = employee_fio
                employee_inst.sex = EmployeeGender.objects.get(name_ru=employee_gender)
                employee_inst.position = EmployeePosition.objects.get(name_ru=employee_position)
                employee_inst.industry = Industry.objects.get(name_ru=employee_industry)
                employee_inst.role = EmployeeRole.objects.get(name_ru=employee_role)
                employee_inst.birth_year = employee_birth_year
                employee_inst.company = company_inst
                employee_inst.created_by = request.user
                employee_inst.created_at = completed_at
                employee_inst.email = employee_email
                employee_inst.save()
            study_name = f'Исследование миграции ({company_name})'
            study_inst = Study.objects.filter(name=study_name)
            if study_inst.exists():
                study_inst = Study.objects.get(name=study_name)
            else:
                study_inst = Study()
                study_inst.created_by = request.user
                study_inst.company = company_inst
                study_inst.name = study_name
                study_inst.save()
            participant_inst = Participant.objects.filter(Q(study=study_inst) & Q(employee=employee_inst) & Q(completed_at=completed_at))
            if participant_inst.exists():
                participant_allowed = False
                participants_not_allowed.append({
                    'name': employee_inst.name,
                    'company': employee_inst.company.name,
                })
            else:
                participant_inst = Participant()
                participant_inst.created_by = request.user
                participant_inst.completed_at = completed_at
                participant_inst.study = study_inst
                participant_inst.invitation_sent = True
                total_questions_qnt = result['Заполнение'].split('/')
                participant_inst.total_questions_qnt = total_questions_qnt[0].strip()
                participant_inst.answered_questions_qnt = total_questions_qnt[0].strip()
                participant_inst.current_percentage = 100
                participant_inst.employee = employee_inst
                participant_inst.save()

                questionnaire_inst = Questionnaire()
                questionnaire_inst.participant = participant_inst
                questionnaire_inst.data_filled_up_by_participant = True
                questionnaire_inst.save()

            if participant_allowed:
                categories = result['categories']
                report_inst = Report()
                report_inst.participant = participant_inst
                report_inst.lang = 'ru'
                report_inst.study = study_inst
                report_inst.added = completed_at
                report_inst.save()
                for category in categories:
                    for cat_key in category:
                        if cat_key == '1_100':
                            report_inst.lie_points = category[cat_key]
                            report_inst.save()
                        else:
                            category_inst = Category.objects.get(code=cat_key)
                            report_data_by_categories = ReportDataByCategories()
                            report_data_by_categories.category_code = cat_key
                            report_data_by_categories.category_name = category_inst.name
                            report_data_by_categories.section_name = category_inst.section.name
                            report_data_by_categories.report = report_inst
                            report_data_by_categories.t_points = category[cat_key]
                            report_data_by_categories.save()
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
