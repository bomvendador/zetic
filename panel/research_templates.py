from pdf.models import Category, Section, ResearchTemplate, ResearchTemplateSections, Participant, Study
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
def research_templates_list(request):
    context = info_common(request)

    researches_templates_inst = ResearchTemplate.objects.all()
    researches_templates_sections_inst = ResearchTemplateSections.objects.all().order_by('position')
    context.update(
        {
            'researches_templates': researches_templates_inst,
            'researches_templates_sections': researches_templates_sections_inst,
        }
    )

    return render(request, 'panel_research_templates_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_new_research_template(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        sections = json_data['sections']
        template_name = json_data['template_name']
        template_inst = ResearchTemplate()
        template_inst.name = template_name
        template_inst.created_by = request.user
        template_inst.save()
        position = 0
        for section in sections:
            position = position + 1
            section_inst = Section.objects.get(id=section['section_id'])
            template_section_inst = ResearchTemplateSections()
            template_section_inst.section = section_inst
            template_section_inst.research_template = template_inst
            template_section_inst.position = position
            template_section_inst.save()
        return HttpResponse(status=200)


@login_required(redirect_field_name=None, login_url='/login/')
def get_research_template_data(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        research_template_id = json_data['research_template_id']
        research_template_inst = ResearchTemplate.objects.get(id=research_template_id)
        research_template_sections_inst = ResearchTemplateSections.objects.filter(research_template=research_template_inst).order_by('position')
        sections = []
        sections_not_in_template = []
        all_sections_inst = Section.objects.all()
        if research_template_sections_inst:
            for research_template_section in research_template_sections_inst:
                sections.append({
                    'name': research_template_section.section.name,
                    'id': research_template_section.id,
                    'research_template_section_id': research_template_section.id,
                    'section_id': research_template_section.section.id
                })
                # response.append()
        for section_in_all_sections in all_sections_inst:
            section_is_in_sections_arr = False
            for section_in_section_arr in sections:
                if section_in_section_arr['section_id'] == section_in_all_sections.id:
                    section_is_in_sections_arr = True
            if not section_is_in_sections_arr:
                sections_not_in_template.append({
                    'name': section_in_all_sections.name,
                    'id': section_in_all_sections.id,
                })
        response = {
            'sections': sections,
            'research_template_name': research_template_inst.name,
            'research_template_id': research_template_id,
            'sections_not_in_template': sections_not_in_template
        }
        return JsonResponse({'response': response})


@login_required(redirect_field_name=None, login_url='/login/')
def get_all_sections(request):
    if request.method == 'POST':
        sections_inst = Section.objects.all()
        sections = []
        for section in sections_inst:
            sections.append({
                'id': section.id,
                'name': section.name
            })
        response = {
            'sections': sections,
        }
        return JsonResponse({'response': response})


@login_required(redirect_field_name=None, login_url='/login/')
def delete_section_from_template(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        template_section_id = json_data['template_section_id']
        template_section_inst = ResearchTemplateSections.objects.get(id=template_section_id)
        research_template_inst = template_section_inst.research_template
        studies_inst = Study.objects.filter(research_template=research_template_inst)
        invitations_sent_to_participants = False
        for study in studies_inst:
            participants_inst = Participant.objects.filter(study=study)
            if participants_inst:
                invitations_sent_to_participants = True
        if not invitations_sent_to_participants:
            try:
                template_section_inst.delete()
                return HttpResponse(status=200)
            except Exception:
                return JsonResponse({"error": "Секция связана с одним из объектов и не может быть удален"})
        else:
            return JsonResponse({"error": "Приглашения участникам в этом исследовании уже были отправлены. Секции не могут быть удалены"})


@login_required(redirect_field_name=None, login_url='/login/')
def delete_template(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        template_id = json_data['template_id']
        template_inst = ResearchTemplate.objects.get(id=template_id)
        try:
            template_inst.delete()
            return HttpResponse(status=200)
        except Exception:
            return JsonResponse({"error": "Шаблон связан с одним из объектов и не может быть удален"})


@login_required(redirect_field_name=None, login_url='/login/')
def edit_research_template(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        sections = json_data['sections']
        template_name = json_data['template_name']
        template_id = json_data['template_id']
        research_template_inst = ResearchTemplate.objects.get(id=template_id)
        research_template_inst.name = template_name
        research_template_inst.save()
        position = 0
        for section in sections:
            position = position + 1
            if 'template_section_id' in section:
                edit_research_template_section_inst = ResearchTemplateSections.objects.get(id=section['template_section_id'])
                edit_research_template_section_inst.position = position
                edit_research_template_section_inst.save()
            if 'section_id' in section:
                section_inst = Section.objects.get(id=section['section_id'])
                new_research_template_section_inst = ResearchTemplateSections()
                new_research_template_section_inst.section = section_inst
                new_research_template_section_inst.research_template = research_template_inst
                new_research_template_section_inst.position = position
                new_research_template_section_inst.save()

        # question_text = json_data['question_text']
        # question_id = json_data['question_id']
        # answers = json_data['answers']
        #
        # question_inst = CategoryQuestions.objects.get(id=question_id)
        # question_inst.text = question_text
        # question_inst.save()
        # print(len(answers))
        # position = 0
        # if len(answers) > 0:
        #     print('>0')
        #     for answer in answers:
        #         position = position + 1
        #         if answer['answer_id'] == '':
        #             answer_inst = QuestionAnswers()
        #         else:
        #             answer_inst = QuestionAnswers.objects.get(id=answer['answer_id'])
        #         answer_inst.text = answer['text']
        #         answer_inst.raw_point = answer['point']
        #         answer_inst.question = question_inst
        #         answer_inst.position = position
        #         answer_inst.save()

        return HttpResponse(status=200)

