import random

from pdf.models import Category, Section, CategoryQuestions, QuestionAnswers, Participant, Employee, EmployeeGender, \
    EmployeePosition, EmployeeRole, Industry, Questionnaire, ResearchTemplateSections, QuestionnaireQuestionAnswers
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone
from django.core import serializers

from datetime import datetime
import math
import random

from django.db.models import Q


def section_view(request, section_id, code):
    print(request)
    participant_inst = Participant.objects.get(invitation_code=code)
    section_inst = Section.objects.get(id=section_id)
    categories_inst = Category.objects.filter(section=section_inst)
    questions = []
    questionnaire_inst = Questionnaire.objects.get(participant__invitation_code=code)
    questionnaire_question_answers_inst = QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire_inst, section_id=section_id)
    questions_already_answered_ids = []
    for questionnaire_question_answer in questionnaire_question_answers_inst:
        questions_already_answered_ids.append(questionnaire_question_answer.question.id)
    # questions_inst = sorted(CategoryQuestions.objects.filter(category__section_id=section_id).exclude()[:5], key=lambda x: random.random())
    CategoryQuestions.objects.filter(Q(category__section_id=section_id) & ~Q(id__in=questions_already_answered_ids))
    questions_inst = sorted(CategoryQuestions.objects.filter(Q(category__section_id=section_id) & ~Q(id__in=questions_already_answered_ids))[:5], key=lambda x: random.random())
    # questions_inst = CategoryQuestions.objects.filter(category__section_id=section_id)
    for question in questions_inst:
        answers_inst = QuestionAnswers.objects.filter(question=question)
        answers = []
        for answer in answers_inst:
            answers.append({
                'text': answer.text,
                'id': answer.id,
            })
        questions.append({
            'text': question.text,
            'id': question.id,
            'answers': answers,
        })
    print(questions)
    section_questions = CategoryQuestions.objects.filter(Q(category__section_id=section_id))
    questions_answered_qnt = len(
        QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire_inst, section_id=section_id))
    progress = 0
    if len(section_questions) > 0:
        progress = int(questions_answered_qnt * 100 / len(section_questions))
    # print(len(questions_inst))
    # print(random.shuffle(questions_inst))
    # for question in questions_inst:
    context = {
        'employee': participant_inst.employee,
        'section': section_inst,
        'code': code,
        'questions': questions,
        'questions_qnt': len(questions),
        'progress': progress,
        'show_back_to_sections': True,
        'participant_id': participant_inst.id
        # 'questionnaire': participant_inst.qu,
    }

    return render(request, 'questionnaire_section_questions.html', context)


def save_answers(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        answers = json_data['answers']
        code = json_data['code']
        section_id = json_data['section_id']
        participant_id = json_data['participant_id']
        questionnaire_inst = Questionnaire.objects.get(participant__invitation_code=code)
        for answer in answers:
            question_id = answer['question_id']
            answer_id = answer['answer_id']
            answer_inst = QuestionnaireQuestionAnswers()
            answer_inst.question = CategoryQuestions.objects.get(id=question_id)
            answer_inst.answer = QuestionAnswers.objects.get(id=answer_id)
            answer_inst.questionnaire = questionnaire_inst
            answer_inst.section = Section.objects.get(id=section_id)
            answer_inst.save()
        total_section_questions_qnt = len(CategoryQuestions.objects.filter(category__section_id=section_id))
        questions_answered_qnt = len(QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire_inst, section_id=section_id))
        total_questionnaire_answers_qnt = len(QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire_inst))

        research_template_inst = questionnaire_inst.participant.study.research_template
        research_template_sections_inst = ResearchTemplateSections.objects.filter(research_template=research_template_inst)
        total_questionnaire_questions_qnt = 0
        for research_template_section in research_template_sections_inst:
            category_inst = Category.objects.filter(section=research_template_section.section)
            for category in category_inst:
                category_questions_inst = CategoryQuestions.objects.filter(category=category)
                total_questionnaire_questions_qnt = total_questionnaire_questions_qnt + len(category_questions_inst)

        response = {
            'total_section_questions_qnt': total_section_questions_qnt,
            'questions_answered_qnt': questions_answered_qnt,
            'total_questionnaire_answers_qnt': total_questionnaire_answers_qnt,
            'total_questionnaire_questions_qnt': total_questionnaire_questions_qnt,
        }
        print(f'total_questionnaire_answers_qnt - {total_questionnaire_answers_qnt} total_questionnaire_questions_qnt - {total_questionnaire_questions_qnt}')
        return JsonResponse({'response': response})

# def get_participant_data(request, code):
#     print(request)
#
#     participant_inst = Participant.objects.get(invitation_code=code)
#     questionnaire_inst = Questionnaire.objects.get(participant=participant_inst)
#     if not questionnaire_inst.data_filled_up_by_participant:
#         years = []
#         current_year = datetime.now().year
#         for i in range(1960, current_year - 18 + 1):
#             years.append(i)
#         context = {
#
#             'employee': participant_inst.employee,
#             'gender': EmployeeGender.objects.all(),
#             'roles': EmployeeRole.objects.all(),
#             'industries': Industry.objects.all(),
#             'positions': EmployeePosition.objects.all(),
#             'years': years,
#             'code': code
#         }
#         return render(request, 'questionnaire_participant_data.html', context)
#     else:
#         research_template_inst = participant_inst.study.research_template
#         research_template_sections_inst = ResearchTemplateSections.objects.filter(
#             research_template=research_template_inst)
#         sections = []
#         for research_template_section in research_template_sections_inst:
#             questions_inst = CategoryQuestions.objects.filter(category__section=research_template_section.section)
#             questions_answered = 0
#             for question in questions_inst:
#                 questions_answered = len(QuestionnaireQuestionAnswers.objects.filter(question=question,
#                                                                                      questionnaire=questionnaire_inst))
#             if not len(questions_inst) == 0:
#                 percentage = int((questions_answered * 100) / len(questions_inst))
#             else:
#                 percentage = 0
#
#             print(f'{questions_answered} * 100 / {len(questions_inst)}')
#             sections.append({
#                 'name': research_template_section.section.name,
#                 'id': research_template_section.section.id,
#                 'total_questions': len(questions_inst),
#                 'questions_answered': questions_answered,
#                 'percentage':  percentage,
#             })
#         print(sections)
#         context = {
#             'employee': participant_inst.employee,
#             'research_template_sections': research_template_sections_inst,
#             'sections': sections
#         }
#         return render(request, 'questionnaire_sections.html', context)
#
#
# def save_participant_data(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         data = json_data['data']
#         code = data['code']
#         year = data['year']
#         gender = data['gender']
#         name = data['name']
#         role_id = data['role_id']
#         position_id = data['position_id']
#         industry_id = data['industry_id']
#         questionnaire_inst = Questionnaire.objects.get(participant__invitation_code=code)
#         questionnaire_inst.data_filled_up_by_participant = True
#         questionnaire_inst.save()
#         employee_inst = Employee.objects.get(id=questionnaire_inst.participant.employee_id)
#         employee_inst.name = name
#         employee_inst.birth_year = year
#         employee_inst.role = EmployeeRole.objects.get(id=role_id)
#         employee_inst.position = EmployeePosition.objects.get(id=position_id)
#         employee_inst.industry = Industry.objects.get(id=industry_id)
#         employee_inst.role = EmployeeRole.objects.get(id=role_id)
#         employee_inst.sex = EmployeeGender.objects.get(name_en=gender)
#         employee_inst.save()
#
#         print(data)
#
#         return HttpResponse(status=200)
