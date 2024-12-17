import datetime

from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, Study, ConsultantCompany, \
    ConsultantStudy, Participant, TrafficLightReportFilter, \
    ConsultantForm, ConsultantFormGrowthZone, ConsultantFormResources, ConsultantFormResourcesComments, \
    ConsultantFormGrowthZoneComments, ConsultantFormEmailSentToParticipant
from login.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone

from reports.settings import DEBUG
from ..views import info_common
from api import outcoming
from django.db.models import Sum, Q

from django.template.loader import render_to_string

from sendemail.tasks import send_report_to_participant_with_consultant_text_task
from panel.constants import CONSTANT_USER_ROLES


@login_required(redirect_field_name=None, login_url='/login/')
def add_consultant_form(request):
    context = info_common(request)
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
        if cur_user_role_name == CONSTANT_USER_ROLES['CONSULTANT']:
            companies = ConsultantCompany.objects.filter(user=request.user)
        if cur_user_role_name == CONSTANT_USER_ROLES['MANAGER']:
            companies = Company.objects.filter(created_by=request.user)
        if cur_user_role_name == CONSTANT_USER_ROLES['ADMIN'] or cur_user_role_name == CONSTANT_USER_ROLES['SUPER_ADMIN']:
            companies = Company.objects.all()
        context.update(
            {
                'companies': companies,
                'user_role_name': cur_user_role_name,
            }
        )

        return render(request, 'consultant_form/panel_add_consultant_form.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_consultant_form_list(request):
    context = info_common(request)
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
        companies_result = []

        if cur_user_role_name == CONSTANT_USER_ROLES['CONSULTANT']:
            companies = ConsultantCompany.objects.filter(user=request.user)
            for company in companies:
                if ConsultantForm.objects.filter(Q(user=request.user) & Q(participant__employee__company=company.company)).exists():
                    companies_result.append({
                        'id': company.company.id,
                        'name': company.company.name,
                    })
        if cur_user_role_name == CONSTANT_USER_ROLES['MANAGER']:
            companies = Company.objects.filter(created_by=request.user)
            consultant_forms = ConsultantForm.objects.filter(participant__employee__company__created_by =request.user)
        if cur_user_role_name == CONSTANT_USER_ROLES['ADMIN'] or cur_user_role_name == CONSTANT_USER_ROLES['SUPER_ADMIN']:
            companies = Company.objects.all()
            for company in companies:
                if ConsultantForm.objects.filter(Q(participant__employee__company=company)).exists():
                    companies_result.append({
                        'id': company.id,
                        'name': company.name,
                    })
        context.update(
            {
                'companies': companies_result,
                'user_role_name': cur_user_role_name,
            }
        )

        return render(request, 'consultant_form/panel_edit_consultant_form_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_consultant_form_template(request, participant_id):
    context = info_common(request)
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        participant = Participant.objects.get(id=participant_id)
        traffic_light = TrafficLightReportFilter.objects.all()
        context.update(
            {
                'participant': participant,
                'traffic_light': traffic_light,
                'title': 'Создание анкеты респондента',
                'form_type': 'new'
            }
        )

        return render(request, 'consultant_form/panel_add_consultant_form_template.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_consultant_form(request, form_id):
    context = info_common(request)
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        form = ConsultantForm.objects.get(id=form_id)
        resources = ConsultantFormResources.objects.filter(consultant_form=form)
        resources_comments = ConsultantFormResourcesComments.objects.filter(consultant_form_resource__consultant_form=form)
        growth_zones = ConsultantFormGrowthZone.objects.filter(consultant_form=form)
        growth_zones_comments = ConsultantFormGrowthZoneComments.objects.filter(consultant_form_growth_zone__consultant_form=form)
        traffic_light = TrafficLightReportFilter.objects.all()
        context.update(
            {
                'form': form,
                'resources': resources,
                'resources_comments': resources_comments,
                'growth_zones': growth_zones,
                'growth_zones_comments': growth_zones_comments,
                'participant': form.participant,
                'traffic_light': traffic_light,
                'title': 'Редактирование анкеты респондента',
                'form_type': 'edit'

            }
        )

        return render(request, 'consultant_form/panel_add_consultant_form_template.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def get_consultant_company_studies(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
        studies = []
        if cur_user_role_name == CONSTANT_USER_ROLES['CONSULTANT']:
            consultant_company = ConsultantCompany.objects.get(Q(company_id=company_id) & Q(user=request.user))
            consultant_studies = ConsultantStudy.objects.filter(consultant_company=consultant_company)
            if consultant_studies.exists():
                for consultant_study in consultant_studies:
                    participant_completed = Participant.objects.filter(Q(study=consultant_study.study) & Q(completed_at__isnull=False))
                    if participant_completed.exists():
                        studies.append({
                            'id': consultant_study.study.id,
                            'name': consultant_study.study.name,
                        })
        else:
            company_studies = Study.objects.filter(company_id=company_id)
            if company_studies.exists():
                for company_study in company_studies:
                    participant_completed = Participant.objects.filter(Q(study=company_study) & Q(completed_at__isnull=False))
                    if participant_completed.exists():
                        studies.append({
                            'id': company_study.id,
                            'name': company_study.name,
                        })
        result = {
            'studies': studies,
        }
        return JsonResponse(result)


@login_required(redirect_field_name=None, login_url='/login/')
def get_consultant_forms(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_id = json_data['company_id']
        cur_user_role_name = UserProfile.objects.get(user=request.user).role.name
        consultant_forms = []
        if cur_user_role_name == CONSTANT_USER_ROLES['CONSULTANT']:
            if company_id == 'all':
                consultant_form_inst = ConsultantForm.objects.filter(Q(user=request.user))
            else:
                consultant_form_inst = ConsultantForm.objects.filter(Q(participant__employee__company_id=company_id) & Q(user=request.user))
        else:
            if company_id == 'all':
                consultant_form_inst = ConsultantForm.objects.all()
            else:
                consultant_form_inst = ConsultantForm.objects.filter(Q(participant__employee__company_id=company_id))
        for form in consultant_form_inst:
            consultant_form_sent_participant_inst = ConsultantFormEmailSentToParticipant.objects.filter(consultant_form=form)
            consultant_form_sent_participant = []
            for consultant_form_sent in consultant_form_sent_participant_inst:
                consultant_form_sent_participant.append({
                    'created_at': timezone.localtime(consultant_form_sent.created_at).strftime("%d.%m.%Y %H:%M:%S"),
                    # 'created_by': consultant_form_sent.created_by.first_name
                })
            consultant_forms.append({
                'id': form.id,
                'fio': form.participant.employee.name,
                'email': form.participant.employee.email,
                'company': form.participant.employee.company.name,
                'study': form.participant.study.name,
                'created_by': form.user.first_name,
                'created_at': timezone.localtime(form.created_at).strftime("%d.%m.%Y %H:%M:%S"),
                'consultant_form_sent_participant': consultant_form_sent_participant
            })
            print(consultant_forms)
        rows_context = {
            'cur_user_role_name': cur_user_role_name,
            'data': consultant_forms
        }
        rows = render_to_string('consultant_form/tr_consultant_form_table.html', rows_context).rstrip()
        return JsonResponse({'rows': rows})


@login_required(redirect_field_name=None, login_url='/login/')
def get_study_participants(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        study_id = json_data['study_id']
        participants_inst = Participant.objects.filter(Q(study_id=study_id) & Q(completed_at__isnull=False))
        participants = []
        for participant in participants_inst:
            participants.append({
                'id': participant.id,
                'name': participant.employee.name,
                'email': participant.employee.email,
            })
        result = {
            'participants': participants,
        }
        return JsonResponse(result)


# @login_required(redirect_field_name=None, login_url='/login/')
# def create_consultant_for(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         participant_id = json_data['participant_id']
#         participants_inst = Participant.objects.get(id=participant_id)
#
#         participants = []
#         for participant in participants_inst:
#             participants.append({
#                 'id': participant.id,
#                 'name': participant.employee.name,
#                 'email': participant.employee.email,
#             })
#         result = {
#             'participants': participants,
#         }
#         return JsonResponse(result)


@login_required(redirect_field_name=None, login_url='/login/')
def save_consultant_form(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        special_comments = json_data['special_comments']
        risks = json_data['risks']
        career_track = json_data['career_track']
        resources = json_data['resources']
        growth_zones = json_data['growth_zones']
        participant_id = json_data['participant_id']
        form_type = json_data['form_type']

        if form_type == 'new':
            consultant_form = ConsultantForm()
            consultant_form.user = request.user
            consultant_form.participant = Participant.objects.get(id=participant_id)
        else:
            consultant_form = ConsultantForm.objects.get(id=json_data['form_id'])
            ConsultantFormResources.objects.filter(consultant_form=consultant_form).delete()
            ConsultantFormGrowthZone.objects.filter(consultant_form=consultant_form).delete()
        consultant_form.special_comments = special_comments
        consultant_form.risks = risks
        consultant_form.career_track = career_track
        consultant_form.save()
        for resource in resources:
            consultant_form_resource = ConsultantFormResources()
            consultant_form_resource.name = resource['name']
            consultant_form_resource.consultant_form = consultant_form
            consultant_form_resource.created_by = request.user
            consultant_form_resource.save()
            for comment in resource['comments']:
                consultant_form_resource_comment = ConsultantFormResourcesComments()
                consultant_form_resource_comment.created_by = request.user
                consultant_form_resource_comment.consultant_form_resource = consultant_form_resource
                consultant_form_resource_comment.text = comment
                consultant_form_resource_comment.save()
        for growth_zone in growth_zones:
            consultant_form_growth_zone = ConsultantFormGrowthZone()
            consultant_form_growth_zone.name = growth_zone['name']
            consultant_form_growth_zone.consultant_form = consultant_form
            consultant_form_growth_zone.created_by = request.user
            consultant_form_growth_zone.save()
            for comment in growth_zone['comments']:
                consultant_form_growth_zone_comment = ConsultantFormGrowthZoneComments()
                consultant_form_growth_zone_comment.created_by = request.user
                consultant_form_growth_zone_comment.consultant_form_growth_zone = consultant_form_growth_zone
                consultant_form_growth_zone_comment.text = comment
                consultant_form_growth_zone_comment.save()

        print(json_data)
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_consultant_form(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        form_id = json_data['form_id']
        ConsultantForm.objects.get(id=form_id).delete()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def send_report_to_participant_with_consultant_text(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        forms_ids_to_send = json_data['forms_ids_to_send']
        if DEBUG == 0:
            response = send_report_to_participant_with_consultant_text_task.delay(forms_ids_to_send)
        else:
            response = send_report_to_participant_with_consultant_text_task(forms_ids_to_send)
    # return JsonResponse({'response': response})
    return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def download_consultant_forms(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        date_from = json_data['date_from']
        date_to = json_data['date_to']
        forms_ids = json_data['forms_ids']
        forms_arr = []
        for form_id in forms_ids:
            if date_from != '' and date_to != '':
                date_from_date = datetime.datetime(int(date_from.split('.')[2]), int(date_from.split('.')[1]), int(date_from.split('.')[0]))
                date_to_date = datetime.datetime(int(date_to.split('.')[2]), int(date_to.split('.')[1]), int(date_to.split('.')[0]), 23, 59, 59)
                form = ConsultantForm.objects.filter(Q(id=form_id) &
                                                      (Q(created_at__lt=date_to_date) | Q(created_at=date_to_date)) &
                                                      (Q(created_at__gt=date_from_date) | Q(created_at__gt=date_from_date)))
                if form.exists():
                    form = ConsultantForm.objects.get(id=form_id)
                    forms_arr.append({
                        'id': form.id
                    })
            if date_from == '' and date_to != '':
                date_to_date = datetime.datetime(int(date_to.split('.')[2]), int(date_to.split('.')[1]), int(date_to.split('.')[0]), 23, 59, 59)
                form = ConsultantForm.objects.filter(Q(id=form_id) &
                                                      (Q(created_at__lt=date_to_date) | Q(created_at=date_to_date)))
                if form.exists():
                    form = ConsultantForm.objects.get(id=form_id)
                    forms_arr.append({
                        'id': form.id
                    })

            if date_from != '' and date_to == '':
                date_from_date = datetime.datetime(int(date_from.split('.')[2]), int(date_from.split('.')[1]), int(date_from.split('.')[0]))
                form = ConsultantForm.objects.filter(Q(id=form_id) &
                                                      (Q(created_at__gt=date_from_date) | Q(created_at=date_from_date)))
                if form.exists():
                    form = ConsultantForm.objects.get(id=form_id)
                    forms_arr.append({
                        'id': form.id
                    })

            if date_from == '' and date_to == '':
                form = ConsultantForm.objects.get(id=form_id)
                forms_arr.append({
                    'id': form.id
                })
        # print(datetime.datetime(int(date_from[2]), int(date_from[1]), int(date_from[0])))
        print(json_data)
        print(forms_arr)
        forms_for_response = []

        for form_id_selected in forms_arr:
            data = {}
            row = []
            consultant_form = ConsultantForm.objects.get(id=form_id_selected['id'])
            form_data = {
                'created_at': timezone.localtime(consultant_form.created_at).strftime("%d.%m.%Y %H:%M:%S"),
                'special_comments': consultant_form.special_comments,
                'risks': consultant_form.risks,
                'career_track': consultant_form.career_track,
            }
            participant = consultant_form.participant
            participant_data = {
                'fio': participant.employee.name,
                'company_name': participant.employee.company.name,
                'birth_year': participant.employee.birth_year,
                'role_name': participant.employee.role.name_ru,
                'position': participant.employee.position.name_ru,
                'industry': participant.employee.industry.name_ru,
                'gender': participant.employee.sex.name_ru,
                'email': participant.employee.email,
            }
            form_resources = ConsultantFormResources.objects.filter(consultant_form=consultant_form)
            consultant_texts = []
            if form_resources.exists():
                for resource in form_resources:
                    comments_data = []
                    comments = ConsultantFormResourcesComments.objects.filter(consultant_form_resource=resource)
                    if comments.exists():
                        for comment in comments:
                            comments_data.append(comment.text)
                    consultant_texts.append({
                        'type': 'Ресурс',
                        'name': resource.name,
                        'comments_data': comments_data
                    })
            form_growth_zones = ConsultantFormGrowthZone.objects.filter(consultant_form=consultant_form)
            if form_growth_zones.exists():
                for growth_zone in form_growth_zones:
                    comments_data = []
                    comments = ConsultantFormGrowthZoneComments.objects.filter(consultant_form_growth_zone=growth_zone)
                    if comments.exists():
                        for comment in comments:
                            comments_data.append(comment.text)
                    consultant_texts.append({
                        'type': 'Зона роста',
                        'name': growth_zone.name,
                        'comments_data': comments_data
                    })

            forms_for_response.append({
                'participant': participant_data,
                'consultant_texts': consultant_texts,
                'form_data': form_data,
            })
        print(forms_for_response)
        return JsonResponse({'response': forms_for_response})
