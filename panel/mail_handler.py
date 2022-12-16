from django.conf import settings
from django.core.mail import send_mail
from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, Study, Section, StudyQuestionGroups, Participant, EmailSentToParticipant
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import json
from api.outcoming import get_code_for_invitation


def send_invitation_email(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        study_id = json_request['study_id']
        participant_id = json_request['participant_id']
        question_groups = json_request['question_groups']

        participant_inst = Participant.objects.get(id=participant_id)
        participant_email = participant_inst.employee.email

        code_for_participant = get_code_for_invitation(request, json_request)
        print(participant_email)
        print(code_for_participant)

        context = {
            'code_for_participant': code_for_participant,
            'participant_email': participant_email,
        }
        html_message = render_to_string('invitation_message.html', context)
        plain_text = strip_tags(html_message)
        from_email = 'rodin@rp-tech.ru'
        to_email = 'bomvendador@yandex.ru'

        subject = 'Опросник ZETIC'

        send_mail(
            subject,
            plain_text,
            from_email,
            [to_email],
            html_message=html_message
        )

    return HttpResponse(status=200)