from django.conf import settings
from django.core.mail import send_mail
from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, Study, Section, StudyQuestionGroups, Participant, EmailSentToParticipant
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from reports import settings
from smtplib import SMTPException, SMTPRecipientsRefused

import json
from api.outcoming import get_code_for_invitation


def send_invitation_email(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        study_id = json_request['study_id']
        participant_id = json_request['participant_id']
        question_groups = json_request['question_groups']
        email_type = json_request['type']

        participant_inst = Participant.objects.get(id=participant_id)
        participant_email = participant_inst.employee.email

        if type == 'initial':
            code_for_participant = get_code_for_invitation(request, json_request)
        else:
            code_for_participant = participant_inst.invitation_code

        context = {
            'code_for_participant': code_for_participant,
            'participant_email': participant_email,
        }

        subject = 'Опросник ZETIC'
        if email_type == 'initial':
            html_message = render_to_string('invitation_message.html', context)
        else:
            html_message = render_to_string('invitation_message_reminder.html', context)

        plain_text = strip_tags(html_message)
        from_email = 'info@zetic.ru'
        to_email = participant_email

        result = {}

        try:
            send_mail(
                subject,
                plain_text,
                from_email,
                [to_email],
                html_message=html_message
            )
            participant_inst.invitation_sent = True
            participant_inst.invitation_sent_datetime = timezone.now()
            participant_inst.invitation_code = code_for_participant
            participant_inst.save()

            email_sent_to_participant_inst = EmailSentToParticipant()
            email_sent_to_participant_inst.participant = participant_inst
            email_sent_to_participant_inst.type = email_type
            email_sent_to_participant_inst.save()

            result.update({
                'datetime_invitation_sent': timezone.localtime(participant_inst.invitation_sent_datetime).strftime("%d.%m.%Y %H:%M"),
            })

        except SMTPRecipientsRefused as e:
            print(e)
            result.update({
                'error': 'Указан некорректный Email участника'
            })
        response = {
            'response': result
        }

        return JsonResponse(response)


def send_reminder(data):
    participant_id = data['participant_id']
    email_type = data['reminder']
    participant_inst = Participant.objects.get(id=participant_id)
    participant_email = participant_inst.employee.email

    code_for_participant = participant_inst.invitation_code

    context = {
        'code_for_participant': code_for_participant,
        'participant_email': participant_email,
    }
    subject = 'Опросник ZETIC (напоминание)'
    html_message = render_to_string('invitation_message_reminder.html', context)

    plain_text = strip_tags(html_message)
    from_email = 'info@zetic.ru'
    to_email = participant_email

    try:
        send_mail(
            subject,
            plain_text,
            from_email,
            [to_email],
            html_message=html_message
        )

        email_sent_to_participant_inst = EmailSentToParticipant()
        email_sent_to_participant_inst.participant = participant_inst
        email_sent_to_participant_inst.type = email_type
        email_sent_to_participant_inst.save()

    except SMTPRecipientsRefused as e:
        result = {
            'error': 'Указан некорректный Email участника'
        }
        return result