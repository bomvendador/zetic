from django.conf import settings
from django.core.mail import send_mail
from login.models import UserProfile
from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, Study, Section, Participant, EmailSentToParticipant, \
    CategoryQuestions, ResearchTemplate, ResearchTemplateSections, Category, Questionnaire, Report, \
    CompanyReportMadeNotificationReceivers, UsersReportMadeNotificationReceivers
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from reports import settings
from smtplib import SMTPException, SMTPRecipientsRefused
import uuid
from reports.settings import DEBUG

import json
# from api.outcoming import get_code_for_invitation
from django.core.mail import EmailMessage


def generate_participant_link_code(string_length):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.


def set_message_text(invitation_message_text):
    message_html = ''
    split_lines = invitation_message_text.splitlines()
    for line in split_lines:
        message_html += '<p>' + line + '</p>'
    return message_html


def send_email_by_email_type(study_id, participants_ids_to_send_invitation_to, email_type, send_report_to_participant_after_filling_up_mass, protocol, hostname):
    wrong_emails = []
    participant_total_questions = 0
    research_template_sections = ResearchTemplateSections.objects.filter(research_template__study=Study.objects.get(id=study_id))
    study_inst = Study.objects.get(id=study_id)
    for research_template_section in research_template_sections:

        categories = Category.objects.filter(section_id=research_template_section.section_id)
        # print(f'categories = {len(categories)}')

        for category in categories:
            category_question = CategoryQuestions.objects.filter(category=category)
            # print(f'category_question = {len(category_question)}')

            participant_total_questions = participant_total_questions + len(category_question)

    for participant in participants_ids_to_send_invitation_to:
        # participant_id = participant['id']
        # print(f'id - {participant["id"]}')
        participant_inst = Participant.objects.get(id=participant['id'])
        participant_email = participant_inst.employee.email
        context = {
            'protocol': protocol,
            'hostname': hostname,
        }
        if email_type == 'initial':
            code_for_participant = generate_participant_link_code(20)
            participant_inst.invitation_code = code_for_participant
            participant_inst.save()

            questionnaire_inst = Questionnaire()
            questionnaire_inst.participant = participant_inst
            questionnaire_inst.save()
            invitation_message_text = study_inst.invitation_message_text
            if invitation_message_text:
                context.update({
                    'message_text': set_message_text(invitation_message_text)
                })

            context.update({
                'code_for_participant': code_for_participant,
            })
            html_message = render_to_string('email_templates/invitation_message.html', context)
        elif email_type == 'reminder':
            invitation_message_text = study_inst.reminder_message_text
            if invitation_message_text:
                context.update({
                    'message_text': set_message_text(invitation_message_text)
                })
            context.update({
                'code_for_participant': participant_inst.invitation_code,
            })
            html_message = render_to_string('email_templates/invitation_message_reminder.html', context)
        elif email_type == 'self_questionnaire':
            context.update({
                'code_for_participant': participant_inst.invitation_code,
            })
            html_message = render_to_string('email_templates/invitation_message.html', context)

        plain_text = strip_tags(html_message)
        from_email = 'бот ZETIC <bot@zetic.ru>'
        to_email = participant_email
        subject = 'Опросник ZETIC'
        success_sent_qnt = 0
        # print(f'-------html_message--------')
        # print(html_message)
        # print(f'---------------------')
        #
        try:
            send_mail(
                subject,
                plain_text,
                from_email,
                [to_email],
                html_message=html_message,
                fail_silently=False,
            )
            participant_inst.invitation_sent = True
            participant_inst.invitation_sent_datetime = timezone.now()
            # participant_inst.invitation_code = code_for_participant
            # if send_admin_notification_after_filling_up_mass:
            #     participant_inst.send_admin_notification_after_filling_up = True
            if send_report_to_participant_after_filling_up_mass:
                participant_inst.send_report_to_participant_after_filling_up = True
            participant_inst.total_questions_qnt = participant_total_questions
            participant_inst.save()

            email_sent_to_participant_inst = EmailSentToParticipant()
            email_sent_to_participant_inst.participant = participant_inst
            email_sent_to_participant_inst.type = email_type
            email_sent_to_participant_inst.save()

            # result.update({
            #     'datetime_invitation_sent': timezone.localtime(participant_inst.invitation_sent_datetime).strftime("%d.%m.%Y %H:%M"),
            #     'questions_count': participant_total_questions
            # })

        except SMTPRecipientsRefused as e:
            # print(f'wrong email - {participant_email}')
            wrong_emails.append(participant_email)
            # result.update({
            #     'wrong_emails': wrong_emails,
            #     'error': 'Указан некорректный Email участника'
            # })
        except SMTPException as e:
            print('There was an error sending an email: ', e)
        except:
            print("Mail Sending Failed!")

    response = {
        'participant_total_questions': participant_total_questions,
        'wrong_emails': wrong_emails
    }

    return response


def mass_send_invitation_email(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        # print(json_request)
        study_id = json_request['study_id']
        study_inst = Study.objects.get(id=study_id)
        company = study_inst.company
        participants_ids_to_send_invitation_to = json_request['participants_ids_to_send_invitation_to']
        send_report_to_participant_after_filling_up_mass = json_request['send_report_to_participant_after_filling_up_mass']
        # send_admin_notification_after_filling_up_mass = json_request['send_admin_notification_after_filling_up_mass']
        protocol = json_request['protocol']
        hostname = json_request['hostname']
        email_type = json_request['type']
        user_profile = UserProfile.objects.get(user=request.user)
        check_passed = True
        result = {}

        if user_profile.role.name == 'Админ заказчика' or user_profile.role.name == 'Партнер':
            if not company.active:
                result = {
                    'company_error': 'company_deactivated'
                }
                check_passed = False
        if check_passed:

            # wrong_emails = []
            # participant_total_questions = 0
            # research_template_sections = ResearchTemplateSections.objects.filter(research_template__study=study_inst)
            # for research_template_section in research_template_sections:
            #
            #     categories = Category.objects.filter(section_id=research_template_section.section_id)
            #     # print(f'categories = {len(categories)}')
            #
            #     for category in categories:
            #         category_question = CategoryQuestions.objects.filter(category=category)
            #         # print(f'category_question = {len(category_question)}')
            #
            #         participant_total_questions = participant_total_questions + len(category_question)
            #
            # for participant in participants_ids_to_send_invitation_to:
            #     # participant_id = participant['id']
            #     print(f'id - {participant["id"]}')
            #     participant_inst = Participant.objects.get(id=participant['id'])
            #     participant_email = participant_inst.employee.email
            #
            #     if email_type == 'initial':
            #         code_for_participant = generate_participant_link_code(20)
            #         participant_inst.invitation_code = code_for_participant
            #         participant_inst.save()
            #
            #         questionnaire_inst = Questionnaire()
            #         questionnaire_inst.participant = participant_inst
            #         questionnaire_inst.save()
            #
            #         context = {
            #             'code_for_participant': code_for_participant,
            #         }
            #
            #         html_message = render_to_string('invitation_message.html', context)
            #     else:
            #         context = {
            #             'code_for_participant': participant_inst.invitation_code,
            #         }
            #         html_message = render_to_string('invitation_message_reminder.html', context)
            #     plain_text = strip_tags(html_message)
            #     from_email = 'ZETIC <info@zetic.ru>'
            #     to_email = participant_email
            #     subject = 'Опросник ZETIC'
            #     success_sent_qnt = 0
            #     try:
            #         send_mail(
            #             subject,
            #             plain_text,
            #             from_email,
            #             [to_email],
            #             html_message=html_message,
            #             fail_silently=False,
            #         )
            #         participant_inst.invitation_sent = True
            #         participant_inst.invitation_sent_datetime = timezone.now()
            #         # participant_inst.invitation_code = code_for_participant
            #         if send_admin_notification_after_filling_up_mass == 1:
            #             participant_inst.send_admin_notification_after_filling_up = True
            #         if send_report_to_participant_after_filling_up_mass == 1:
            #             participant_inst.send_report_to_participant_after_filling_up = True
            #         participant_inst.total_questions_qnt = participant_total_questions
            #         participant_inst.save()
            #
            #         email_sent_to_participant_inst = EmailSentToParticipant()
            #         email_sent_to_participant_inst.participant = participant_inst
            #         email_sent_to_participant_inst.type = email_type
            #         email_sent_to_participant_inst.save()
            #
            #         # result.update({
            #         #     'datetime_invitation_sent': timezone.localtime(participant_inst.invitation_sent_datetime).strftime("%d.%m.%Y %H:%M"),
            #         #     'questions_count': participant_total_questions
            #         # })
            #
            #     except SMTPRecipientsRefused as e:
            #         print(f'wrong email - {participant_email}')
            #         wrong_emails.append(participant_email)
            #         # result.update({
            #         #     'wrong_emails': wrong_emails,
            #         #     'error': 'Указан некорректный Email участника'
            #         # })
            #     except SMTPException as e:
            #         print('There was an error sending an email: ', e)
            #     except:
            #         print("Mail Sending Failed!")
            send_email_by_email_type_var = send_email_by_email_type(study_id, participants_ids_to_send_invitation_to, email_type, send_report_to_participant_after_filling_up_mass, protocol, hostname)


            result.update({
                'questions_count': send_email_by_email_type_var['participant_total_questions'],
                'wrong_emails': send_email_by_email_type_var['wrong_emails'],

            })
            # result.update({
            #     'questions_count': participant_total_questions,
            #     'wrong_emails': wrong_emails,
            #
            # })




        # email_type = json_request['type']
        # send_admin_notification_after_filling_up = json_request['send_admin_notification_after_filling_up']
        #
        # participant_inst = Participant.objects.get(id=participant_id)
        # participant_email = participant_inst.employee.email
        #
        # user_profile = UserProfile.objects.get(user=request.user)
        # check_passed = True
        #
        # result = {}
        #
        # if user_profile.role.name == 'Админ заказчика':
        #     company = participant_inst.employee.company
        #     if not company.active:
        #         result = {
        #             'company_error': 'company_deactivated'
        #         }
        #         check_passed = False
        # if check_passed:
        #     if email_type == 'initial':
        #         if participant_inst.invitation_code is None:
        #             get_code_for_invitation_response = get_code_for_invitation(request, json_request)
        #             code_for_participant = get_code_for_invitation_response['public_code']
        #             participant_inst.invitation_code = code_for_participant
        #             participant_inst.total_questions_qnt = get_code_for_invitation_response['questions_count']
        #             participant_inst.save()
        #         else:
        #             code_for_participant = participant_inst.invitation_code
        #     else:
        #         code_for_participant = participant_inst.invitation_code
        #
        #     context = {
        #         'code_for_participant': code_for_participant,
        #         'participant_email': participant_email,
        #     }
        #
        #     subject = 'Опросник ZETIC'
        #     if email_type == 'initial':
        #         html_message = render_to_string('invitation_message.html', context)
        #     else:
        #         html_message = render_to_string('invitation_message_reminder.html', context)
        #
        #     plain_text = strip_tags(html_message)
        #     from_email = 'ZETIC <info@zetic.ru>'
        #     to_email = participant_email
        #
        #
        #     try:
        #         send_mail(
        #             subject,
        #             plain_text,
        #             from_email,
        #             [to_email],
        #             html_message=html_message
        #         )
        #         participant_inst.invitation_sent = True
        #         participant_inst.invitation_sent_datetime = timezone.now()
        #         participant_inst.invitation_code = code_for_participant
        #         if send_admin_notification_after_filling_up == 1:
        #             participant_inst.send_admin_notification_after_filling_up = True
        #         participant_inst.save()
        #
        #         email_sent_to_participant_inst = EmailSentToParticipant()
        #         email_sent_to_participant_inst.participant = participant_inst
        #         email_sent_to_participant_inst.type = email_type
        #         email_sent_to_participant_inst.save()
        #
        #         result.update({
        #             'datetime_invitation_sent': timezone.localtime(participant_inst.invitation_sent_datetime).strftime("%d.%m.%Y %H:%M"),
        #             'questions_count': participant_inst.total_questions_qnt
        #         })
        #
        #     except SMTPRecipientsRefused as e:
        #         print(e)
        #         result.update({
        #             'error': 'Указан некорректный Email участника'
        #         })
        # response = {
        #     'response': result
        # }
        #
        print(result)
        return JsonResponse(result)

        # return HttpResponse(status=200)


def send_invitation_email(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        print(json_request)
        study_id = json_request['study_id']
        participant_id = json_request['participant_id']
        email_type = json_request['type']
        send_admin_notification_after_filling_up = json_request['send_admin_notification_after_filling_up']

        participant_inst = Participant.objects.get(id=participant_id)
        participant_email = participant_inst.employee.email

        user_profile = UserProfile.objects.get(user=request.user)
        check_passed = True

        result = {}

        if user_profile.role.name == 'Админ заказчика':
            company = participant_inst.employee.company
            if not company.active:
                result = {
                    'company_error': 'company_deactivated'
                }
                check_passed = False
        if check_passed:
            if email_type == 'initial':
                if participant_inst.invitation_code is None:
                    # get_code_for_invitation_response = get_code_for_invitation(request, json_request)
                    # code_for_participant = get_code_for_invitation_response['public_code']
                    # participant_inst.invitation_code = code_for_participant
                    # participant_inst.total_questions_qnt = get_code_for_invitation_response['questions_count']
                    participant_inst.save()
                else:
                    code_for_participant = participant_inst.invitation_code
            else:
                code_for_participant = participant_inst.invitation_code

            context = {
                # 'code_for_participant': code_for_participant,
                'participant_email': participant_email,
            }

            subject = 'Опросник ZETIC'
            if email_type == 'initial':
                html_message = render_to_string('email_templates/invitation_message.html', context)
            else:
                html_message = render_to_string('email_templates/invitation_message_reminder.html', context)

            plain_text = strip_tags(html_message)
            from_email = 'ZETIC <info@zetic.ru>'
            to_email = participant_email


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
                if send_admin_notification_after_filling_up == 1:
                    participant_inst.send_admin_notification_after_filling_up = True
                participant_inst.save()

                email_sent_to_participant_inst = EmailSentToParticipant()
                email_sent_to_participant_inst.participant = participant_inst
                email_sent_to_participant_inst.type = email_type
                email_sent_to_participant_inst.save()

                result.update({
                    'datetime_invitation_sent': timezone.localtime(participant_inst.invitation_sent_datetime).strftime("%d.%m.%Y %H:%M"),
                    'questions_count': participant_inst.total_questions_qnt
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
    email_type = data['type']
    participant_inst = Participant.objects.get(id=participant_id)
    participant_email = participant_inst.employee.email

    code_for_participant = participant_inst.invitation_code

    context = {
        'code_for_participant': code_for_participant,
        'participant_email': participant_email,
    }
    subject = 'Опросник ZETIC (напоминание)'
    html_message = render_to_string('email_templates/invitation_message_reminder.html', context)

    plain_text = strip_tags(html_message)
    from_email = 'ZETIC <info@zetic.ru>'
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


def send_month_report(data):
    context = {
        'reports': data,
    }
    print('++++++++ report sent +++++++++++')
    subject = 'Ежемесячный отчет'
    html_message = render_to_string('month_report.html', context)

    plain_text = strip_tags(html_message)
    from_email = 'ZETIC <info@zetic.ru>'
    to_email = 'info@zetic.ru'

    try:
        send_mail(
            subject,
            plain_text,
            from_email,
            [to_email],
            html_message=html_message
        )

    except SMTPRecipientsRefused as e:
        result = {
            'error': 'Указан некорректный Email'
        }
        return result


def send_notification_report_made(data, report_id):
    report = Report.objects.get(id=report_id)
    participant_name = data['participant_name']
    to_email = []
    to_email.append('info@zetic.ru')
    company = report.participant.employee.company
    company_receivers = CompanyReportMadeNotificationReceivers.objects.filter(company=company)
    common_receivers = UsersReportMadeNotificationReceivers.objects.all()
    for receiver in common_receivers:
        user_profile = UserProfile.objects.get(user=receiver.user)
        if user_profile.role.name == 'Партнер':
            if company.created_by == receiver.user:
                to_email.append(receiver.user.email)
        else:
            to_email.append(receiver.user.email)
    for receiver in company_receivers:
        to_email.append(receiver.employee.email)
    context = {
        'data': data,
        'employee': report.participant.employee,
        'created_by': {
            'role': UserProfile.objects.get(user=report.participant.employee.created_by).role.name,
            'name': UserProfile.objects.get(user=report.participant.employee.created_by).fio,
            'email': UserProfile.objects.get(user=report.participant.employee.created_by).user.email
        },
        'debug': DEBUG
    }
    if DEBUG == 0:
        subject = participant_name + ' окончил(а) заполнение опросника'
    else:
        subject = participant_name + ' окончил(а) заполнение опросника (тестовое сообщение)'

    html_message = render_to_string('notification_report_made.html', context)

    from_email = 'ZETIC <info@zetic.ru>'

    email = EmailMessage(
        subject, html_message, from_email, to_email)
    email.attach_file(settings.MEDIA_ROOT + '/reportsPDF/single/' + report.file.name, 'application/pdf')
    email.content_subtype = "html"
    try:
        email.send()
        result = {
            'result': 200
        }

    except SMTPRecipientsRefused as e:
        result = {
            'error': 'Указан некорректный Email'
        }
    return result


def send_notification_to_participant_report_made(data, report_id, request_type):
    report = Report.objects.get(id=report_id)
    participant_name = data['participant_name']
    to_email = data['email']
    context = {
        'data': data,
    }
    if request_type == 'consultant_form':
        subject = 'Опросник ZETIC дополнен выводами'
        html_message = render_to_string('notification_report_to_participant_made_consultant_text.html', context)
    else:
        subject = 'Опросник ZETIC'
        html_message = render_to_string('notification_report_to_participant_made.html', context)

    from_email = 'ZETIC <info@zetic.ru>'

    if settings.DEBUG == 1:
        to_email = 'bomvendador@yandex.ru'
    email = EmailMessage(
        subject, html_message, from_email, [to_email])
    email.attach_file(settings.MEDIA_ROOT + '/reportsPDF/single/' + report.file.name, 'application/pdf')
    email.content_subtype = "html"
    try:
        email.send()
        result = {
            'result': 200
        }

    except SMTPRecipientsRefused as e:
        result = {
            'error': 'Указан некорректный Email'
        }
    return result


    # try:
    #     send_mail(
    #         subject,
    #         plain_text,
    #         from_email,
    #         [to_email],
    #         html_message=html_message
    #     )
    #
    # except SMTPRecipientsRefused as e:
    #     result = {
    #         'error': 'Указан некорректный Email'
    #     }
    #     return result