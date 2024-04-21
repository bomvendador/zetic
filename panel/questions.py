from pdf.models import Category, Section, CategoryQuestions, QuestionAnswers
from login.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.utils import timezone
from django.core import serializers

from .views import info_common
from api import outcoming

from django.utils.dateformat import DateFormat


@login_required(redirect_field_name=None, login_url='/login/')
def questions_list(request, category_id):
    context = info_common(request)

    category_inst = Category.objects.get(id=category_id)
    questions_inst = CategoryQuestions.objects.filter(category_id=category_id)
    answers_inst = QuestionAnswers.objects.filter(question__category=category_id).order_by('position')
    context.update(
        {
            'questions': questions_inst,
            'category': category_inst,
            'answers': answers_inst
        }
    )

    return render(request, 'panel_questions_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_new_question(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        question_text = json_data['question_text']
        category_id = json_data['category_id']
        answers = json_data['answers']
        new_question = CategoryQuestions()
        new_question.text = question_text
        new_question.category = Category.objects.get(id=category_id)
        new_question.created_by = request.user
        new_question.save()
        position = 0
        for answer in answers:
            position = position + 1
            new_answer = QuestionAnswers()
            new_answer.text = answer['text']
            new_answer.raw_point = answer['point']
            new_answer.question = new_question
            new_answer.created_by = request.user
            new_answer.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def get_question_data(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        question_id = json_data['question_id']
        question_inst = CategoryQuestions.objects.get(id=question_id)
        answers_inst = QuestionAnswers.objects.filter(question=question_inst).order_by('position')
        answers = []
        if answers_inst:
            for answer in answers_inst:
                answers.append({
                    'text': answer.text,
                    'point': answer.raw_point,
                    'id': answer.id,
                })
                # response.append()
        response = {
            'answers': answers,
            'question_text': question_inst.text,
            'question_id': question_id
        }
        return JsonResponse({'response': response})


@login_required(redirect_field_name=None, login_url='/login/')
def delete_answer(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        answer_id = json_data['answer_id']
        answer_inst = QuestionAnswers.objects.get(id=answer_id)
        try:
            answer_inst.delete()
            return HttpResponse(status=200)
        except Exception:
            return JsonResponse({"error": "Ответ связан с одним из объектов и не может быть удален"})


@login_required(redirect_field_name=None, login_url='/login/')
def delete_question(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        question_id = json_data['question_id']
        question_inst = CategoryQuestions.objects.get(id=question_id)
        try:
            question_inst.delete()
            return HttpResponse(status=200)
        except Exception:
            return JsonResponse({"error": "Вопрос связан с одним из объектов и не может быть удален"})


@login_required(redirect_field_name=None, login_url='/login/')
def edit_question(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        question_text = json_data['question_text']
        question_id = json_data['question_id']
        answers = json_data['answers']

        question_inst = CategoryQuestions.objects.get(id=question_id)
        question_inst.text = question_text
        question_inst.save()
        print(len(answers))
        position = 0
        if len(answers) > 0:
            print('>0')
            for answer in answers:
                position = position + 1
                if answer['answer_id'] == '':
                    answer_inst = QuestionAnswers()
                else:
                    answer_inst = QuestionAnswers.objects.get(id=answer['answer_id'])
                answer_inst.text = answer['text']
                answer_inst.raw_point = answer['point']
                answer_inst.question = question_inst
                answer_inst.position = position
                answer_inst.save()

        return HttpResponse(status=200)

# @login_required(redirect_field_name=None, login_url='/login/')
# def categories_list(request):
#     context = info_common(request)
#     if context == 'logout':
#         return render(request, 'login.html', {'error': 'Ваша учетная запись деактивирована'})
#     else:
#         sections = Section.objects.all()
#         context.update({
#             'sections': sections,
#         })
#
#         return render(request, 'panel_categories_list.html', context)
#
#
#
#
#
#
#
#
# @login_required(redirect_field_name=None, login_url='/login/')
# def save_new_category(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         name = json_data['name']
#         section_id = json_data['section_id']
#         section_inst = Section.objects.get(id=section_id)
#         category_inst = Category()
#         category_inst.name = name
#         category_inst.section = section_inst
#         category_inst.created_by = request.user
#
#         category_inst.save()
#
#         return HttpResponse(status=200)
