from pdf.models import Category, Section, CategoryQuestions, QuestionAnswers, Participant, Employee, EmployeeGender, \
    EmployeePosition, EmployeeRole, Industry, Questionnaire, ResearchTemplateSections, QuestionnaireQuestionAnswers, \
    QuestionnaireVisits, CommonBooleanSettings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone
from django.core import serializers

from .views import questionnaire_context

from reports.settings import EMAIL_SUBJECT_PREFIX
from datetime import datetime
import math


def get_participant_data(request, code):
    print(request)
    context = questionnaire_context()
    participant_inst = Participant.objects.get(invitation_code=code)
    questionnaire_inst = Questionnaire.objects.get(participant=participant_inst)
    email_subject_prefix = EMAIL_SUBJECT_PREFIX

    tech_works_mode = CommonBooleanSettings.objects.get(name='Технические работы').value
    if tech_works_mode:
        return render(request, 'tech_works/tech_works_page.html', context)

    if not questionnaire_inst.data_filled_up_by_participant:
        years = []
        current_year = datetime.now().year
        for i in range(1960, current_year - 18 + 1):
            years.append(i)
        context.update({

            'employee': participant_inst.employee,
            'gender': EmployeeGender.objects.all(),
            'roles': EmployeeRole.objects.all(),
            'industries': Industry.objects.all(),
            'positions': EmployeePosition.objects.all(),
            'years': years,
            'code': code,
            'email_subject_prefix': email_subject_prefix
        })
        return render(request, 'questionnaire_participant_data.html', context)
    else:
        if not questionnaire_inst.active:
            context = {
                'employee': participant_inst.employee,
                'email_subject_prefix': email_subject_prefix
                # 'research_template_sections': research_template_sections_inst,
                # 'sections': sections,
                # 'code': code,
                # 'show_back_to_sections': False
            }
            return render(request, 'questionnaire_blocked.html', context)
        else:
            questionnaire_visit_inst = QuestionnaireVisits()
            questionnaire_visit_inst.questionnaire = questionnaire_inst
            questionnaire_visit_inst.save()
            research_template_inst = participant_inst.study.research_template
            research_template_sections_inst = ResearchTemplateSections.objects.filter(
                research_template=research_template_inst)
            sections = []
            for research_template_section in research_template_sections_inst:
                questions_inst = CategoryQuestions.objects.filter(category__section=research_template_section.section)
                # questions_answered = 0
                questions_answered = len(
                    QuestionnaireQuestionAnswers.objects.filter(section=research_template_section.section,
                                                                questionnaire=questionnaire_inst))

                # for question in questions_inst:
                #     questions_answered = len(QuestionnaireQuestionAnswers.objects.filter(section=research_template_section.section,
                #                                                                          questionnaire=questionnaire_inst))
                if not len(questions_inst) == 0:
                    percentage = int((questions_answered * 100) / len(questions_inst))
                else:
                    percentage = 0

                print(f'{questions_answered} * 100 / {len(questions_inst)}')
                sections.append({
                    'email_subject_prefix': email_subject_prefix,
                    'name': research_template_section.section.name,
                    'id': research_template_section.section.id,
                    'total_questions': len(questions_inst),
                    'questions_answered': questions_answered,
                    'percentage':  percentage,
                })
            print(sections)
            context = {
                'email_subject_prefix': email_subject_prefix,
                'employee': participant_inst.employee,
                'research_template_sections': research_template_sections_inst,
                'sections': sections,
                'code': code,
                'show_back_to_sections': False
            }
            return render(request, 'questionnaire_sections.html', context)


def save_participant_data(request):
    if request.method == 'POST':
        tech_works_mode = CommonBooleanSettings.objects.get(name='Технические работы').value
        if tech_works_mode:
            return HttpResponse('tech_works')
        else:
            json_data = json.loads(request.body.decode('utf-8'))
            data = json_data['data']
            code = data['code']
            year = data['year']
            gender = data['gender']
            name = data['name']
            role_id = data['role_id']
            position_id = data['position_id']
            industry_id = data['industry_id']
            questionnaire_inst = Questionnaire.objects.get(participant__invitation_code=code)
            questionnaire_inst.data_filled_up_by_participant = True
            questionnaire_inst.save()
            employee_inst = Employee.objects.get(id=questionnaire_inst.participant.employee_id)
            employee_inst.name = name
            employee_inst.birth_year = year
            employee_inst.role = EmployeeRole.objects.get(id=role_id)
            employee_inst.position = EmployeePosition.objects.get(id=position_id)
            employee_inst.industry = Industry.objects.get(id=industry_id)
            employee_inst.role = EmployeeRole.objects.get(id=role_id)
            employee_inst.sex = EmployeeGender.objects.get(name_en=gender)
            employee_inst.save()
            return HttpResponse(status=200)
