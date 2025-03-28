import random

# from pdf.views import pdf_single_generator
from sendemail.tasks import pdf_single_generator_task

from pdf.models import Category, Section, CategoryQuestions, QuestionAnswers, Participant, Employee, EmployeeGender, \
    EmployeePosition, EmployeeRole, Industry, Questionnaire, ResearchTemplateSections, QuestionnaireQuestionAnswers, \
    CommonBooleanSettings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone
from django.core import serializers

from datetime import datetime
import math
import random

from .views import questionnaire_context
from django.db.models import Q

from reports.settings import DEBUG


def section_view(request, section_id, code):
    print(request)
    context = questionnaire_context()
    participant_inst = Participant.objects.get(invitation_code=code)
    section_inst = Section.objects.get(id=section_id)
    categories_inst = Category.objects.filter(section=section_inst)
    questions = []
    questionnaire_inst = Questionnaire.objects.get(participant__invitation_code=code)
    tech_works_mode = CommonBooleanSettings.objects.get(name='Технические работы').value
    if tech_works_mode:
        return render(request, 'tech_works/tech_works_page.html', context)

    if not questionnaire_inst.active:
        context.update({
            'employee': participant_inst.employee,
            # 'research_template_sections': research_template_sections_inst,
            # 'sections': sections,
            # 'code': code,
            # 'show_back_to_sections': False
        })
        return render(request, 'questionnaire_blocked.html', context)
    else:

        questionnaire_question_answers_inst = QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire_inst, section_id=section_id)
        questions_already_answered_ids = []
        for questionnaire_question_answer in questionnaire_question_answers_inst:
            questions_already_answered_ids.append(questionnaire_question_answer.question.id)
        # questions_inst = sorted(CategoryQuestions.objects.filter(category__section_id=section_id).exclude()[:5], key=lambda x: random.random())
        CategoryQuestions.objects.filter(Q(category__section_id=section_id) & ~Q(id__in=questions_already_answered_ids))
        questions_inst = sorted(CategoryQuestions.objects.filter(Q(category__section_id=section_id) & ~Q(id__in=questions_already_answered_ids)), key=lambda x: random.random())
        # questions_sections_inst_all = CategoryQuestions.objects.filter(Q(category__section_id=section_id) & ~Q(id__in=questions_already_answered_ids))
        # questions_inst = random.sample(questions_sections_inst_all, 5)
        # questions_inst = CategoryQuestions.objects.filter(category__section_id=section_id)
        questions_limit = 15
        cur_questions_cnt = 0
        for question in questions_inst:
            cur_questions_cnt = cur_questions_cnt + 1
            if cur_questions_cnt <= questions_limit:
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
        # print(questions)
        section_questions = CategoryQuestions.objects.filter(Q(category__section_id=section_id))
        questions_answered_qnt = len(
            QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire_inst, section_id=section_id))
        progress = 0
        if len(section_questions) > 0:
            progress = int(questions_answered_qnt * 100 / len(section_questions))
        # print(len(questions_inst))
        # print(random.shuffle(questions_inst))
        # for question in questions_inst:
        context.update({
            'employee': participant_inst.employee,
            'section': section_inst,
            'code': code,
            'questions': questions,
            'questions_qnt': len(questions),
            'progress': progress,
            'show_back_to_sections': True,
            'participant_id': participant_inst.id
            # 'questionnaire': participant_inst.qu,
        })

        return render(request, 'questionnaire_section_questions.html', context)


def save_answers(request):
    if request.method == 'POST':
        tech_works_mode = CommonBooleanSettings.objects.get(name='Технические работы').value
        if tech_works_mode:
            return HttpResponse('tech_works')

        json_data = json.loads(request.body.decode('utf-8'))
        answers = json_data['answers']
        questions_answered_cnt = len(answers)
        questions_answered_repeatedly_cnt = 0
        code = json_data['code']
        section_id = json_data['section_id']

        # participant_id = json_data['participant_id']
        questionnaire_inst = Questionnaire.objects.get(participant__invitation_code=code)
        for answer in answers:
            question_id = answer['question_id']
            answer_id = answer['answer_id']
            existing_answer = QuestionnaireQuestionAnswers.objects.filter(Q(question_id=question_id) &
                                                                          Q(questionnaire=questionnaire_inst))
            print(f'existing_answer = {len(existing_answer)}')
            if not existing_answer.exists():
                answer_inst = QuestionnaireQuestionAnswers()
                answer_inst.question = CategoryQuestions.objects.get(id=question_id)
                answer_inst.answer = QuestionAnswers.objects.get(id=answer_id)
                answer_inst.questionnaire = questionnaire_inst
                answer_inst.section = Section.objects.get(id=section_id)
                answer_inst.save()
            else:
                questions_answered_repeatedly_cnt += 1
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

        participant_inst = Participant.objects.get(id=questionnaire_inst.participant_id)
        participant_inst.answered_questions_qnt = total_questionnaire_answers_qnt
        participant_inst.current_percentage = int(total_questionnaire_answers_qnt / total_questionnaire_questions_qnt * 100)
        participant_inst.save()

        all_questions_answered_repeatedly = False
        if questions_answered_cnt == questions_answered_repeatedly_cnt:
            all_questions_answered_repeatedly = True
        else:
            if total_questionnaire_questions_qnt == total_questionnaire_answers_qnt:
                if DEBUG == 0:
                    pdf_single_generator_task.delay(questionnaire_inst.id, '')
                    # pdf_single_generator(questionnaire_inst.id, '')
                else:
                    pdf_single_generator_task(questionnaire_inst.id, '')
        response = {
            'all_questions_answered_repeatedly': all_questions_answered_repeatedly,
            'total_section_questions_qnt': total_section_questions_qnt,
            'questions_answered_qnt': questions_answered_qnt,
            'total_questionnaire_answers_qnt': total_questionnaire_answers_qnt,
            'total_questionnaire_questions_qnt': total_questionnaire_questions_qnt,
            'email': participant_inst.employee.email,
        }
        # print(f'total_questionnaire_answers_qnt - {total_questionnaire_answers_qnt} total_questionnaire_questions_qnt - {total_questionnaire_questions_qnt}')
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
