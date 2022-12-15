from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, Study, Section, StudyQuestionGroups, Participant, EmailSentToParticipant
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone

from .views import info_common


@login_required(redirect_field_name=None, login_url='/login/')
def studies_list(request):
    context = info_common(request)
    context.update({
        'companies': Company.objects.all(),
        'employee_positions': EmployeePosition.objects.all(),
        'employee_roles': EmployeeRole.objects.all(),
        'industries': Industry.objects.all()
    })

    return render(request, 'panel_studies_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def study_details(request, study_id):
    context = info_common(request)
    study = Study.objects.get(id=study_id)
    question_groups = StudyQuestionGroups.objects.filter(study=study)
    context.update(
        {
            'study': study,
            'question_groups': question_groups,
            'participants': Participant.objects.filter(study=study)
        }
    )

    return render(request, 'panel_study_details.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def get_company_studies(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        company_id = json_data['company_id']
        studies = Study.objects.filter(company_id=company_id)
        studies_arr = []
        for study in studies:
            name = study.name
            studies_arr.append({
                'name': name,
                'id': study.id,
                'company_name': study.company.name,
                'research_name': study.research_name,
            })
        response = {
            'data': list(studies_arr)
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def get_question_groups(request):
    if request.method == 'POST':
        question_groups_inst = Section.objects.all()
        question_groups = []
        for question_group in question_groups_inst:
            question = {
                'id': question_group.id,
                'name': question_group.name
            }
            question_groups.append(question)

        if len(question_groups) > 0:
            result = list(question_groups)
        else:
            result = 'None'
        response = {
            'response': result,
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def save_study_questions_groups(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        json_data = json_request['data']
        questions_groups_id = json_data['questions_groups_ids']
        study_id = json_data['study_id']
        study_inst = Study.objects.get(id=study_id)
        StudyQuestionGroups.objects.filter(study=study_inst).delete()

        for questions_group_id in questions_groups_id:
            questions_group_inst = Section.objects.get(id=questions_group_id)
            study_questions_group_inst = StudyQuestionGroups()
            study_questions_group_inst.study = study_inst
            study_questions_group_inst.question_group = questions_group_inst
            study_questions_group_inst.created_by = request.user
            study_questions_group_inst.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def get_employees_for_study(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        study_id = json_request['study_id']
        study_inst = Study.objects.get(id=study_id)
        company = study_inst.company
        employees = Employee.objects.filter(company=company)

        employees_arr = []

        for employee in employees:
            can_be_sent = True
            if Participant.objects.filter(employee=employee, study=study_inst).exists():
                participant = Participant.objects.get(employee=employee, study=study_inst)
                if participant.invitation_sent:
                    can_be_sent = False
            if can_be_sent:
                if employee.name:
                    name = employee.name
                else:
                    name = ''

                item = {
                    'id': employee.id,
                    'name': name,
                    'email': employee.email
                }
                employees_arr.append(item)

        if len(employees_arr) > 0:
            result = list(employees_arr)
        else:
            result = 'None'
        response = {
            'response': result,
        }
        return JsonResponse(response)


@login_required(redirect_field_name=None, login_url='/login/')
def save_study_participants(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        json_data = json_request['data']
        employees_ids = json_data['employees_ids']
        study_id = json_data['study_id']
        study_inst = Study.objects.get(id=study_id)
        Participant.objects.filter(study=study_inst, invitation_sent=False).delete()
        for employee_id in employees_ids:
            employee = Employee.objects.get(id=employee_id)
            participant = Participant()
            participant.study = study_inst
            participant.employee = employee
            participant.created_by = request.user
            participant.save()
        participants = Participant.objects.filter(study=study_inst)
        result = []
        for participant in participants:
            if participant.employee.name:
                name = participant.employee.name
            else:
                name = ''
            if participant.invitation_sent_datetime:
                invitation_sent_datetime = timezone.localtime(participant.invitation_sent_datetime).strftime("%d.%m.%Y %H:%M:%S")
            else:
                invitation_sent_datetime = ''
            result.append({
                'name': name,
                'email': participant.employee.email,
                'invitation': participant.invitation_sent,
                'invitation_sent_datetime': invitation_sent_datetime
            })
            # if participant.invitation_sent:
            #     email_sent_inst = EmailSentToParticipant.objects.get(participant=participant, type='Первичная отправка')
            #     sent_datetime = timezone.localtime(email_sent_inst.created_at).strftime("%Y-%m-%d %H:%M:%S")
            #     result.append({
            #         'invitation_datetime': sent_datetime
            #     })
            # else:
            #     result.append({
            #         'invitation_datetime': ''
            #     })

        response = {
            'response': result,
        }
        return JsonResponse(response)
