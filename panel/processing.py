from pdf.models import Category, Section, CategoryQuestions, CommonBooleanSettings, \
    CompanyIndividualReportAllowedOptions, CompanyGroupReportAllowedOptions, StudyIndividualReportAllowedOptions, \
    ParticipantIndividualReportAllowedOptions, Company, Participant, Study, IndividualReportAllowedOptions, \
    GroupReportAllowedOptions, ProcessingRuns
from login.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone
from django.core import serializers
from django.db.models import Q

from panel.views import info_common
from api import outcoming

from django.utils.dateformat import DateFormat


@login_required(redirect_field_name=None, login_url='/login/')
def processing_main(request):
    context = info_common(request)
    processing_runs = ProcessingRuns.objects.all()
    if context == 'logout':
        return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
    else:
        context.update({
            'processing_runs': processing_runs
        })
        return render(request, 'processing/panel_processings.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def run_processing(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        button_id = json_data['button_id']
        name = json_data['name']
        match name:
            case 'Опции в отчетах':
                individual_report_allowed_options = IndividualReportAllowedOptions.objects.all()
                group_report_allowed_options = GroupReportAllowedOptions.objects.all()
                companies = Company.objects.all()
                for company in companies:
                    for option in individual_report_allowed_options:
                        if not CompanyIndividualReportAllowedOptions.objects.filter(Q(company=company) & Q(option=option)).exists():
                            company_individual_report_allowed_options = CompanyIndividualReportAllowedOptions()
                            company_individual_report_allowed_options.company = company
                            company_individual_report_allowed_options.created_by = request.user
                            company_individual_report_allowed_options.option = option
                            company_individual_report_allowed_options.save()
                    for option in group_report_allowed_options:
                        if not CompanyGroupReportAllowedOptions.objects.filter(Q(company=company) & Q(option=option)).exists():
                            company_group_report_allowed_options = CompanyGroupReportAllowedOptions()
                            company_group_report_allowed_options.company = company
                            company_group_report_allowed_options.created_by = request.user
                            company_group_report_allowed_options.option = option
                            company_group_report_allowed_options.save()
                    studies = Study.objects.filter(company=company)
                    for study in studies:
                        for option in individual_report_allowed_options:
                            if not StudyIndividualReportAllowedOptions.objects.filter(Q(study=study) & Q(option=option)).exists():
                                study_individual_report_allowed_options = StudyIndividualReportAllowedOptions()
                                study_individual_report_allowed_options.created_by = request.user
                                study_individual_report_allowed_options.study = study
                                study_individual_report_allowed_options.option = option
                                study_individual_report_allowed_options.save()
                    participants = Participant.objects.filter(employee__company=company)
                    for participant in participants:
                        for option in individual_report_allowed_options:
                            if not ParticipantIndividualReportAllowedOptions.objects.filter(Q(participant=participant) & Q(option=option)).exists():
                                participant_individual_report_allowed_options = ParticipantIndividualReportAllowedOptions()
                                participant_individual_report_allowed_options.participant = participant
                                participant_individual_report_allowed_options.created_by = request.user
                                participant_individual_report_allowed_options.option = option
                                participant_individual_report_allowed_options.save()
                processing_runs = ProcessingRuns()
                processing_runs.run_by = request.user
                processing_runs.button_id = button_id
                processing_runs.name = name
                processing_runs.save()
        return HttpResponse(status=200)


