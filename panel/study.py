from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, Study, Section, Participant, \
    EmailSentToParticipant, Report, ResearchTemplate, ResearchTemplateSections, Questionnaire, QuestionnaireVisits, \
    CommonBooleanSettings, Category, CategoryQuestions, QuestionnaireQuestionAnswers, \
    ParticipantIndividualReportAllowedOptions, StudyIndividualReportAllowedOptions, CompanyIndividualReportAllowedOptions, \
    UserCompanies
from login.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone

from .views import info_common
from api import outcoming
from django.db.models import Sum, Q
from panel.constants import CONSTANT_INVITATION_MESSAGE_TEXT, CONSTANT_INVITATION_REMINDER_MESSAGE_TEXT

from panel.mail_handler import generate_participant_link_code


@login_required(redirect_field_name=None, login_url='/login/')
def studies_list(request):
    context = info_common(request)
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:

        cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
        if cur_user_role_name == 'Менеджер' or cur_user_role_name == 'Партнер':
            companies = Company.objects.filter(created_by=request.user)
        if cur_user_role_name == 'Админ заказчика':
            company = Employee.objects.get(user=request.user).company
            companies = Company.objects.filter(id=company.id)
        if cur_user_role_name == 'Админ' or cur_user_role_name == 'Суперадмин':
            companies = Company.objects.all()
        user_companies = UserCompanies.objects.filter(user=request.user)
        context.update({
            'companies': companies,
            'user_companies': user_companies,
            'employee_positions': EmployeePosition.objects.all(),
            'employee_roles': EmployeeRole.objects.all(),
            'industries': Industry.objects.all()
        })

        return render(request, 'panel_studies_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def study_details(request, study_id):
    context = info_common(request)
    # url_origin = request._current_scheme_host
    # current_url = request._current_scheme_host + request.path
    # print(f'HTTP_HOST - {request.get_host()}')
    # print(f'REMOTE_HOST - {request.META["REMOTE_HOST"]}')
    # print(f'SERVER_NAME - {request.META["SERVER_NAME"]}')
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        study = Study.objects.get(id=study_id)
        # participant_questions_groups = ParticipantQuestionGroups.objects.filter(participant__study=study)
        # study_question_groups = StudyQuestionGroup.objects.filter(study=study)
        reports = Report.objects.filter(study=study).order_by('-added')
        if study.research_template:
            research_template = ResearchTemplate.objects.get(id=study.research_template.id)
            sections = ResearchTemplateSections.objects.filter(research_template=research_template).order_by('position')
            context.update({
                'sections': sections,
            })
        questionnaires_inst = Questionnaire.objects.filter(participant__study=study)
        questionnaires_visits_inst = QuestionnaireVisits.objects.filter(questionnaire__participant__study=study)

        company_inst = study.company
        company_questionnaires_qnt = len(Questionnaire.objects.filter(participant__employee__company=company_inst))
        if company_inst.demo_status_questionnaires_limit <= company_questionnaires_qnt:
            questionnaires_left = 0
        else:
            questionnaires_left = company_inst.demo_status_questionnaires_limit - company_questionnaires_qnt
        participant_individual_report_allowed_options = ParticipantIndividualReportAllowedOptions.objects.filter(participant__study=study)
        study_individual_report_allowed_options = StudyIndividualReportAllowedOptions.objects.filter(study=study)
        company_individual_report_allowed_options = CompanyIndividualReportAllowedOptions.objects.filter(company=company_inst)

        if 'Исследование миграции' in study.name:
            made_by_migration = True
        else:
            made_by_migration = False
        context.update(
            {
                'made_by_migration': made_by_migration,
                'study': study,
                'invitation_message_text': CONSTANT_INVITATION_MESSAGE_TEXT,
                'invitation_reminder_message_text': CONSTANT_INVITATION_REMINDER_MESSAGE_TEXT,
                'participant_individual_report_allowed_options': participant_individual_report_allowed_options,
                'study_individual_report_allowed_options': study_individual_report_allowed_options,
                'company_individual_report_allowed_options': company_individual_report_allowed_options,
                'demo_status_setting': CommonBooleanSettings.objects.get(name='Демо-режимы для компаний').value,
                'company_questionnaires_qnt': company_questionnaires_qnt,
                'company': company_inst,
                'questionnaires_left': questionnaires_left,
                # 'participant_questions_groups': participant_questions_groups,
                # 'study_question_groups': study_question_groups,
                'participants': Participant.objects.filter(study=study),
                'emails_sent': EmailSentToParticipant.objects.filter(participant__study=study, type='reminder'),
                'reports': reports,
                'questionnaires_visits': questionnaires_visits_inst,
                'questionnaires': questionnaires_inst,
                'url_origin': f'{request._current_scheme_host}'
            }
        )

        return render(request, 'panel_study_details.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def change_questionnaire_status(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        questionnaire_id = json_data['questionnaire_id']
        operation = json_data['operation']
        questionnaire_inst = Questionnaire.objects.get(id=questionnaire_id)
        if operation == 'block':
            questionnaire_inst.active = False
        else:
            questionnaire_inst.active = True
        questionnaire_inst.save()
    return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def get_company_studies(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        company_id = json_data['company_id']
        # studies = Study.objects.filter(company_id=company_id)
        company = Company.objects.get(id=company_id)
        # studies = outcoming.get_company_studies(company.public_code)
        studies = Study.objects.filter(company_id=company_id)
        studies_arr = []
        for study in studies:
            name = study.name
            if study.research_template:
                research_name = study.research_template.name
            else:
                research_name = ''
            studies_arr.append({
                'name': name,
                'id': study.id,
                'company_name': company.name,
                'research_name': research_name,
                'created_at': timezone.localtime(study.created_at).strftime("%d.%m.%Y %H:%M:%S")
            })
            # studies_db_qnt = Study.objects.filter(public_code=study['public_code']).count()
            # studies_db_qnt = studies.count()
            # if studies_db_qnt == 0:
            #     study_inst = Study()
            #     study_inst.company = company
            #     study_inst.name = name
            #     study_inst.public_code = study['public_code']
            #     study_inst.save()
            # else:
            #     study_inst = Study.objects.get(public_code=study['public_code'])

            # for section in study['sections']:
            # study_question_group_qnt = StudyQuestionGroup.objects.filter(study=study_inst, section__code=section['public_code']).count()
            # if study_question_group_qnt == 0:
            #     study_question_group_inst = StudyQuestionGroup()
            #     study_question_group_inst.study = study_inst
            #     study_question_group_inst.section = Section.objects.get(code=section['public_code'])
            #     study_question_group_inst.save()

        response = {
            'data': list(studies_arr)
        }
        return JsonResponse(response)


# @login_required(redirect_field_name=None, login_url='/login/')
# def get_question_groups(request):
#     if request.method == 'POST':
#         question_groups_inst = Section.objects.all()
#         question_groups = []
#         for question_group in question_groups_inst:
#             question = {
#                 'id': question_group.id,
#                 'name': question_group.name
#             }
#             question_groups.append(question)
#
#         if len(question_groups) > 0:
#             result = list(question_groups)
#         else:
#             result = 'None'
#         response = {
#             'response': result,
#         }
#         return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_participants_from_study(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        participants_ids_to_send_invitation_to = json_request['participants_ids_to_send_invitation_to']
        for participant_id in participants_ids_to_send_invitation_to:
            Participant.objects.get(id=participant_id['id']).delete()
    return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def get_participants_raw_points(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        participants_ids_to_send_invitation_to = json_request['participants_ids_to_send_invitation_to']
        study_id = json_request['study_id']
        study_inst = Study.objects.get(id=study_id)
        categories = Category.objects.all().order_by('code')
        data = []
        categories_codes = []
        for category in categories:
            code_split = category.code.split('_')
            if not code_split[1] == '100':
                categories_codes.append(category.code)
        for participant_id in participants_ids_to_send_invitation_to:
            categories_data = []
            for category in categories:
                code_split = category.code.split('_')
                if not code_split[1] == '100':
                    raw_points = 0
                    question_answers = QuestionnaireQuestionAnswers.objects.filter(
                        Q(questionnaire__participant_id=participant_id) &
                        Q(question__category=category))
                    for question_answer in question_answers:
                        raw_points = raw_points + question_answer.answer.raw_point
                    if not question_answers.exists():
                        raw_points = ''
                    categories_data.append({
                        'code': category.code,
                        'raw_points': raw_points
                    })
            data.append({
                'name': Participant.objects.get(id=participant_id).employee.name,
                'categories_data': categories_data,
            })
        results = {
            'categories_codes': categories_codes,
            'participants_data': data,
            'study_name': study_inst.name,
            'company_name': study_inst.company.name,
        }
    return JsonResponse(results)


# @login_required(redirect_field_name=None, login_url='/login/')
# def save_participant_questions_groups(request):
#     if request.method == 'POST':
#         json_request = json.loads(request.body.decode('utf-8'))
#         json_data = json_request['data']
#         study_id = json_request['study_id']
#         user_profile = UserProfile.objects.get(user=request.user)
#         check_passed = True
#         response = {}
#         company = Study.objects.get(id=study_id).company
#
#         if user_profile.role.name == 'Админ заказчика':
#
#             company_admin = Employee.objects.get(user=request.user)
#             if not company_admin.company_admin_active:
#                 logout(request)
#                 result = 'logout'
#                 check_passed = False
#
#         if not company.active:
#             response.update({
#                 'warning': 'Обратите внимание - компания деактивирована!'
#             })
#             result = 'company_deactivated'
#             if not user_profile.role.name == 'Админ заказчика':
#                 check_passed = True
#
#         if check_passed:
#             result = '200'
#             questions_groups_selected = json_data['questions_groups_selected']
#             participant_id = json_data['participant_id']
#             participant_inst = Participant.objects.get(id=participant_id)
#             ParticipantQuestionGroups.objects.filter(participant=participant_inst).delete()
#
#             for questions_group_selected in questions_groups_selected:
#                 participant_questions_group_inst = ParticipantQuestionGroups()
#                 participant_questions_group_inst.question_group_name = questions_group_selected['name']
#                 participant_questions_group_inst.question_group_code = questions_group_selected['code']
#                 participant_questions_group_inst.created_by = request.user
#                 participant_questions_group_inst.participant = participant_inst
#                 participant_questions_group_inst.save()
#         response.update({
#             'response': result,
#         })
#         return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def get_employees_for_study(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        study_id = json_request['study_id']
        study_inst = Study.objects.get(id=study_id)
        company = study_inst.company
        employees = Employee.objects.filter(company=company)
        user_profile = UserProfile.objects.get(user=request.user)
        check_passed = True

        employees_arr = []
        response = {}
        if not company.active:
            response.update({
                'warning': 'Обратите внимание - компания деактивирована!'
            })
            if user_profile.role.name == 'Админ заказчика':
                company_admin = Employee.objects.get(user=request.user)
                if company_admin.company_admin_active:
                    result = 'company_deactivated'
                    check_passed = False
                else:
                    logout(request)
                    result = 'logout'
                    check_passed = False
        if check_passed:
            for employee in employees:
                can_be_sent = True
                participant_id = 0
                # if Participant.objects.filter(employee=employee, study=study_inst).exists():
                #     participant = Participant.objects.get(employee=employee, study=study_inst)
                #     participant_id = participant.id
                #     if participant.invitation_sent:
                #         can_be_sent = False
                # if can_be_sent:
                #     if employee.name:
                #         name = employee.name
                #     else:
                #         name = ''
                if not Participant.objects.filter(employee=employee, study=study_inst).exists():
                    item = {
                        'employee_id': employee.id,
                        'participant_id': participant_id,
                        'name': employee.name,
                        'email': employee.email
                    }
                    employees_arr.append(item)

            if len(employees_arr) > 0:
                result = list(employees_arr)
            else:
                result = 'None'
        response.update({
            'response': result,
        })
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def save_study_participants(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        json_data = json_request['data']
        employees_ids = json_data['employees_ids']
        study_id = json_data['study_id']
        study_inst = Study.objects.get(id=study_id)
        participants = Participant.objects.filter(study=study_inst, invitation_sent=False)
        # for participant in participants:
        #     check_employee_id = participant.employee.id
        #     participant_exists = False
        #     for employee_id in employees_ids:
        #         if int(check_employee_id) == int(employee_id):
        #             participant_exists = True
        #     if not participant_exists:
        #         participant.delete()
        for employee_id in employees_ids:
            employee = Employee.objects.get(id=employee_id)
            if not Participant.objects.filter(employee=employee, study=study_inst).exists():
                participant = Participant()
                participant.study = study_inst
                participant.employee = employee
                participant.created_by = request.user
                participant.save()
                study_individual_report_allowed_options = StudyIndividualReportAllowedOptions.objects.filter(study_id=study_id)
                for study_individual_report_allowed_option in study_individual_report_allowed_options:
                    participant_individual_report_allowed_options = ParticipantIndividualReportAllowedOptions()
                    participant_individual_report_allowed_options.participant = participant
                    participant_individual_report_allowed_options.option = study_individual_report_allowed_option.option
                    participant_individual_report_allowed_options.value = study_individual_report_allowed_option.value
                    participant_individual_report_allowed_options.created_by = request.user
                    participant_individual_report_allowed_options.save()
        participants = Participant.objects.filter(study=study_inst)
        result = []
        for participant in participants:
            if participant.employee.name:
                name = participant.employee.name
            else:
                name = ''
            if participant.invitation_sent_datetime:
                invitation_sent_datetime = timezone.localtime(participant.invitation_sent_datetime).strftime(
                    "%d.%m.%Y %H:%M:%S")
            else:
                invitation_sent_datetime = ''
            if participant.completed_at:
                completed_at_datetime = timezone.localtime(participant.completed_at).strftime("%d.%m.%Y %H:%M:%S")
            else:
                completed_at_datetime = ''
            reminders_sent = EmailSentToParticipant.objects.filter(participant=participant, type='reminder')
            if len(reminders_sent) > 0:
                reminders_arr = []
                for reminder in reminders_sent:
                    reminders_arr.append(timezone.localtime(reminder.created_at).strftime("%d.%m.%Y %H:%M:%S"))
            else:
                reminders_arr = ''
            questions_groups_arr = []
            # questions_groups = ParticipantQuestionGroups.objects.filter(participant=participant)
            # for question_groups in questions_groups:
            #     questions_groups_arr.append({
            #         'name': question_groups.question_group_name,
            #         'code': question_groups.question_group_code,
            #     })
            if Report.objects.filter(participant=participant).exists():
                filename = Report.objects.filter(participant=participant).latest('added').filename()
            else:
                filename = ''
            result.append({
                'id': participant.id,
                'name': name,
                'email': participant.employee.email,
                'invitation': participant.invitation_sent,
                'invitation_sent_datetime': invitation_sent_datetime,
                'reminder': reminders_arr,
                'completed_at_datetime': completed_at_datetime,
                'questions_groups_arr': questions_groups_arr,
                'current_percentage': participant.current_percentage,
                'total_questions_qnt': participant.total_questions_qnt,
                'answered_questions_qnt': participant.answered_questions_qnt,
                'filename': filename
            })

        response = {
            'response': result,
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def save_study_name(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        study_name = json_request['study_name']
        study_id = json_request['study_id']
        study_inst = Study.objects.get(id=study_id)
        study_inst.name = study_name
        study_inst.save()
        response = {
            'study_name': study_name,
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def save_participants_individual_report_options(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        participants_ids_to_change_report_options = json_request['participants_ids_to_change_report_options']
        options_data = json_request['options_data']
        print(json_request)
        for participant_id in participants_ids_to_change_report_options:
            for option in options_data:
                participant_individual_report_allowed_options = ParticipantIndividualReportAllowedOptions.objects.get(Q(participant_id=participant_id) &
                                                                                                                  Q(option_id=option['id']))
                participant_individual_report_allowed_options.value = option['value']
                participant_individual_report_allowed_options.save()

        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def save_study_invitation_message(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        study_id = json_request['study_id']
        message_text = json_request['message_text']
        reminder_message_text = json_request['reminder_message_text']
        study_inst = Study.objects.get(id=study_id)
        study_inst.invitation_message_text = message_text
        study_inst.reminder_message_text = reminder_message_text
        study_inst.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def create_invitation_link_excel_import(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        print(json_request)
        study_id = json_request['study_id']
        study_inst = Study.objects.get(id=study_id)
        company = study_inst.company
        participants_ids_to_send_invitation_to = json_request['participants_ids_to_send_invitation_to']
        send_report_to_participant_after_filling_up_mass = json_request['send_report_to_participant_after_filling_up_mass']
        # send_admin_notification_after_filling_up_mass = json_request['send_admin_notification_after_filling_up_mass']
        protocol = json_request['protocol']
        hostname = json_request['hostname']
        email_type = json_request['type']
        user_profile = UserProfile.objects.get(user=request.user)
        check_passed = True
        file_rows = []

        if user_profile.role.name == 'Админ заказчика' or user_profile.role.name == 'Партнер':
            if not company.active:
                result = {
                    'company_error': 'company_deactivated'
                }
                check_passed = False
        if check_passed:
            participant_total_questions = 0
            research_template_sections = ResearchTemplateSections.objects.filter(
                research_template__study=Study.objects.get(id=study_id))
            study_inst = Study.objects.get(id=study_id)
            for research_template_section in research_template_sections:

                categories = Category.objects.filter(section_id=research_template_section.section_id)
                # print(f'categories = {len(categories)}')

                for category in categories:
                    category_question = CategoryQuestions.objects.filter(category=category)
                    # print(f'category_question = {len(category_question)}')

                    participant_total_questions = participant_total_questions + len(category_question)
            file_rows.append(['Имя', 'Email', 'Компания', 'Позиция', 'Индустрия', 'Роль', 'Пол', 'Год рождения', 'Ссылка на опросник'])
            for participant in participants_ids_to_send_invitation_to:
                # participant_id = participant['id']
                # print(f'id - {participant["id"]}')
                participant_inst = Participant.objects.get(id=participant['id'])
                if participant_inst.invitation_code:
                    code_for_participant = participant_inst.invitation_code
                else:
                    code_for_participant = generate_participant_link_code(20)
                    participant_inst.invitation_code = code_for_participant
                    if send_report_to_participant_after_filling_up_mass:
                        participant_inst.send_report_to_participant_after_filling_up = True
                    participant_inst.total_questions_qnt = participant_total_questions

                    participant_inst.save()

                questionnaire_inst = Questionnaire()
                questionnaire_inst.participant = participant_inst
                questionnaire_inst.save()

                participant_name = participant_inst.employee.name
                participant_email = participant_inst.employee.email
                participant_company_name = participant_inst.employee.company.name
                participant_position = participant_inst.employee.position.name_ru
                participant_industry = participant_inst.employee.industry.name_ru
                participant_role = participant_inst.employee.role.name_ru
                participant_gender = participant_inst.employee.sex.name_ru
                participant_birth_year = participant_inst.employee.birth_year
                questionnaire_link = f'{protocol}//{hostname}/questionnaire/{code_for_participant}'

                file_rows.append([participant_name, participant_email, participant_company_name, participant_position, participant_industry, participant_role, participant_gender, participant_birth_year, questionnaire_link])
            print(file_rows)
        response = {
            'file_rows': file_rows,
            'company': company.name,
            'study': study_inst.name
        }
        return JsonResponse(response)
