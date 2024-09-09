from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, User, Participant, EmployeeGender, \
    Project, ProjectParticipants, Questionnaire, Report, QuestionnaireVisits, QuestionnaireQuestionAnswers, Study
from login.models import UserProfile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from reports import settings
import json
from django.utils import timezone
import requests

from .views import info_common
from api.outcoming import Attributes, sync_add_employee
from .custom_funcs import update_attributes
from django.db.models import Sum, Q

from django.template.loader import render_to_string


@login_required(redirect_field_name=None, login_url='/login/')
def search_employees(request):
    context = info_common(request)

    context.update(
        {
            'type': 'search_employees_select'
        }
    )

    return render(request, 'search/panel_employees_search.html', context)


def search_questionnaire_status(request):
    context = info_common(request)
    companies = Company.objects.all().order_by('name')
    context.update(
        {
            'type': 'search_questionnaire_status_select',
            'companies': companies
        }
    )

    return render(request, 'search/panel_questionnaire_status_search.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def search_for_employees(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        # print(json_data)
        fio = json_data['fio']
        email = json_data['email']
        employee_role_name = UserProfile.objects.get(user=request.user).role.name
        if not fio == '' and not email == '':
            if employee_role_name == 'Партнер':
                employees_inst = Employee.objects.filter(Q(name=fio) & Q(email=email) & Q(created_by=request.user))
            else:
                employees_inst = Employee.objects.filter(Q(name=fio) & Q(email=email))
        elif not fio == '':
            if employee_role_name == 'Партнер':
                employees_inst = Employee.objects.filter(Q(name=fio) & Q(created_by=request.user))
            else:
                employees_inst = Employee.objects.filter(Q(name=fio))
        else:
            if employee_role_name == 'Партнер':
                employees_inst = Employee.objects.filter(Q(email=email) & Q(created_by=request.user))
            else:
                employees_inst = Employee.objects.filter(Q(email=email))
        data = []
        for employee in employees_inst:
            employee_data = {
                'name': employee.name,
                'email': employee.email,
                'company_name': employee.company.name,
            }
            participants = Participant.objects.filter(employee=employee)
            projects = []
            questionnaires = []
            reports_dates = []
            reports_files = []
            questionnaires_visits = []
            studies = []
            invitation_code = ''
            if participants.exists():
                for participant in participants:
                    studies.append({
                        'name': participant.study.name
                    })
                    project_participants_inst = ProjectParticipants.objects.filter(participant=participant)
                    invitation_code = participant.invitation_code
                    for project_participant in project_participants_inst:
                        projects.append(project_participant.project.name)
                    questionnaires_inst = Questionnaire.objects.filter(participant=participant)
                    for questionnaire in questionnaires_inst:
                        questionnaires_visits_inst = QuestionnaireVisits.objects.filter(questionnaire=questionnaire)
                        questionnaire_visits = []
                        for questionnaire_visit in questionnaires_visits_inst:
                            questionnaire_visits.append(
                                timezone.localtime(questionnaire_visit.created_at).strftime("%d.%m.%Y %H:%M:%S"))
                        questionnaires.append({
                            'created_at': timezone.localtime(questionnaire.created_at).strftime("%d.%m.%Y %H:%M:%S"),
                            'questionnaire_visits': questionnaire_visits
                        })

                    reports_inst = Report.objects.filter(participant=participant)
                    for report in reports_inst:
                        reports_dates.append(timezone.localtime(report.added).strftime("%d.%m.%Y %H:%M:%S"))
                        reports_files.append(report.file.name)

                employee_data.update({
                    'projects': projects,
                    'questionnaires': questionnaires,
                    'reports_dates': reports_dates,
                    'reports_files': reports_files,
                    'invitation_code': invitation_code,
                    'url_origin': f'{request._current_scheme_host}',
                    'studies': studies
                })

            data.append(employee_data)
        rows = render_to_string('search/tr_employee_search.html', {'data': data}).rstrip()
        return JsonResponse({'rows': rows})


@login_required(redirect_field_name=None, login_url='/login/')
def search_for_questionnaire_status(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        status = json_data['status']
        all_companies = False
        if company_id == '' or company_id == 'all':
            all_companies = True
        if status == 'not_started':
            if all_companies:
                questionnaires_inst = Questionnaire.objects.filter(Q(participant__invitation_sent=True) &
                                                                   Q(participant__answered_questions_qnt=0))
            else:
                questionnaires_inst = Questionnaire.objects.filter(Q(participant__invitation_sent=True) &
                                                                   Q(participant__answered_questions_qnt=0) &
                                                                   Q(participant__employee__company_id=company_id))
        elif status == 'not_finished':
            if all_companies:
                questionnaires_inst = Questionnaire.objects.filter(Q(participant__invitation_sent=True) &
                                                                   ~Q(participant__answered_questions_qnt=0) &
                                                                   Q(participant__completed_at=None))
            else:
                questionnaires_inst = Questionnaire.objects.filter(Q(participant__invitation_sent=True) &
                                                                   ~Q(participant__answered_questions_qnt=0) &
                                                                   Q(participant__completed_at=None) &
                                                                   Q(participant__employee__company_id=company_id))

        result = []
        for questionnaire in questionnaires_inst:
            data = {
                'fio': questionnaire.participant.employee.name,
                'email': questionnaire.participant.employee.email,
                'answers': f'{questionnaire.participant.answered_questions_qnt} / {questionnaire.participant.total_questions_qnt}',
                'created_at': timezone.localtime(questionnaire.created_at).strftime("%d.%m.%Y %H:%M:%S"),
                'active': questionnaire.active
            }
            if questionnaire.participant.employee.company:
                data.update({
                    'company': f'{questionnaire.participant.employee.company.id}. {questionnaire.participant.employee.company.name}',
                })
            questionnaires_visits_inst = QuestionnaireVisits.objects.filter(questionnaire=questionnaire)
            questionnaire_visits = []
            for questionnaire_visit in questionnaires_visits_inst:
                questionnaire_visits.append(
                    timezone.localtime(questionnaire_visit.created_at).strftime("%d.%m.%Y %H:%M:%S"))
            data.update({
                'questionnaire_visits': questionnaire_visits
            })
            if QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire).exists():
                last_answer_date = timezone.localtime(QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire).latest('created_at').created_at).strftime("%d.%m.%Y %H:%M:%S")
            else:
                last_answer_date = ''
            data.update({
                'last_answer_date': last_answer_date
            })
            # questionnaire['additional_data'] = {
            #     'questionnaire_visits': questionnaire_visits,
            #     'last_answer_date': last_answer_date
            # }
            result.append(data)
        rows = render_to_string('search/tr_questionnaire_status_search.html', {'data': result}).rstrip()
        return JsonResponse({'rows': rows})


@login_required(redirect_field_name=None, login_url='/login/')
def get_company_no_admins(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        company_id = json_data['company_id']
        employees = Employee.objects.filter(company_id=company_id, company_admin=False)
        employees_arr = []
        for employee in employees:
            if employee.name:
                name = employee.name
            else:
                name = ''
            if employee.created_by:
                created_by = employee.created_by.first_name
            else:
                created_by = ''
            employees_arr.append({
                'name': name,
                'id': employee.id,
                'email': employee.email,
                'active': employee.company_admin_active,
            })
        response = {
            'data': list(employees_arr)
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def deactivate_company_admin(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        employee_id = json_data['employee_id']
        operation_type = json_data['operation_type']
        employee = Employee.objects.get(id=employee_id)
        if operation_type == 'deactivate':
            employee.company_admin_active = False
        else:
            employee.company_admin_active = True
        employee.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_company_admin(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        employee_id = json_data['employee_id']
        employee = Employee.objects.get(id=employee_id)
        employee.company_admin_active = False
        employee.company_admin = False
        employee.user.delete()
        employee.user = None
        employee.save()

        return HttpResponse(status=200)
