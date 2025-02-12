from pdf.models import Report, Participant, Company, ReportData, Section, Category, Employee, Study, EmployeeRole, \
    EmployeeGender, QuestionnaireQuestionAnswers, Questionnaire, RawToTPointsType, RawToTPoints, ReportDataByCategories, \
    ConsultantForm, ConsultantFormEmailSentToParticipant, CommonBooleanSettings
from login.models import UserProfile
from . import raw_to_t_point
from panel import mail_handler
from django.utils import timezone
from reports.settings import DEBUG


# def create_report(questionnaire_id):
#     questionnaire_inst = Questionnaire.objects.get(id=questionnaire_id)
#     report_inst = Report()


# def save_data_to_db(request_json, file_name):
#     # print(request_json)
#
#     # if 'company_name' in request_json:
#     #     if Company.objects.filter(name=request_json['company_name']).exists():
#     #         company = Company.objects.get(name=request_json['company_name'])
#     #     else:
#     #         company = Company()
#     #         company.name = request_json['company_name']
#     #         company.save()
#     #
#     # if Employee.objects.filter(email=request_json['participant_info']['email']).exists():
#     #     employee = Employee.objects.get(email=request_json['participant_info']['email'])
#     # else:
#     #     employee = Employee()
#     #     employee.name = request_json['participant_info']['name']
#     #     employee.sex = EmployeeGender.objects.get(public_code=request_json['participant_info']['sex'])
#     #     # employee.sex = EmployeeGender.objects.get(name_ru=request_json['participant_info']['sex'])
#     #     employee.birth_year = request_json['participant_info']['year']
#     #     employee.email = request_json['participant_info']['email']
#     #     # employee.company = company
#     #     employee.save()
#     #
#     #
#
#     if Study.objects.filter(public_code=request_json['study']['id']).exists():
#         study = Study.objects.get(public_code=request_json['study']['id'])
#     else:
#         study = Study()
#         # study.company = company
#         study.name = request_json['study']['name']
#         # study.name = request_json['study_name']
#         study.save()
#
#     if Participant.objects.filter(employee__email=request_json['participant_info']['email'], study=study).exists():
#
#         participant = Participant.objects.get(employee__email=request_json['participant_info']['email'], study=study)
#     else:
#         participant = Participant()
#     participant.completed_at = timezone.now()
#     participant.current_percentage = 100
#     participant.answered_questions_qnt = participant.total_questions_qnt
#     participant.save()
#
#     if Report.objects.filter(code=request_json['code']).exists():
#         report = Report.objects.get(code=request_json['code'])
#         ReportData.objects.filter(report=report).delete()
#     else:
#         report = Report()
#     lie_points = round(request_json['lie_points'] / 40 * 10)
#     report.participant = participant
#     report.lie_points = lie_points
#     report.code = request_json['code']
#     report.file = file_name
#     report.lang = request_json['lang']
#     report.study = study
#     report.save()
#
#     for section in request_json['appraisal_data']:
#         # print(section['point'])
#         for point in section['point']:
#             # print(f"{point['category']} - {point['points']}")
#             report_data = ReportData()
#             report_data.report = report
#             report_data.section_code = section['code']
#             report_data.section_name = section['section']
#             # print(point['code'])
#             report_data.category_name = point['category']
#             report_data.category_code = point['code']
#             report_data.points = raw_to_t_point.get_t_point(point['points'], point['code'], request_json['participant_info']['sex'], int(request_json['participant_info']['year']))
#             # report_data.points = point['points']
#             report_data.save()
#
#     if participant.send_admin_notification_after_filling_up:
#         created_by_user = participant.created_by
#         user_profile = UserProfile.objects.get(user=created_by_user)
#         role_name = user_profile.role.name
#         if role_name == 'Админ заказчика':
#             to_email = created_by_user.email
#         else:
#             to_email = 'info@zetic.ru'
#         data_for_mail = {
#             'participant_name': participant.employee.name,
#             'email': request_json['participant_info']['email'],
#             'company_name': participant.employee.company.name,
#             'study_name': participant.study.name,
#             'to_email': to_email
#         }
#         mail_handler.send_notification_to_participant_report_made(data_for_mail)


# def save_data_to_db_and_send_report(questionnaire_id, file_name, study_id, lie_points, lang, report_id):
def save_data_to_db_and_send_report(data):
    questionnaire_id = data['questionnaire_id']
    file_name = data['file_name']
    study_id = data['study_id']
    lie_points = data['lie_points']
    lang = data['lang']
    report_id = data['report_id']
    request_type = data['request_type']

    # print(request_json)

    # if 'company_name' in request_json:
    #     if Company.objects.filter(name=request_json['company_name']).exists():
    #         company = Company.objects.get(name=request_json['company_name'])
    #     else:
    #         company = Company()
    #         company.name = request_json['company_name']
    #         company.save()
    #
    # if Employee.objects.filter(email=request_json['participant_info']['email']).exists():
    #     employee = Employee.objects.get(email=request_json['participant_info']['email'])
    # else:
    #     employee = Employee()
    #     employee.name = request_json['participant_info']['name']
    #     employee.sex = EmployeeGender.objects.get(public_code=request_json['participant_info']['sex'])
    #     # employee.sex = EmployeeGender.objects.get(name_ru=request_json['participant_info']['sex'])
    #     employee.birth_year = request_json['participant_info']['year']
    #     employee.email = request_json['participant_info']['email']
    #     # employee.company = company
    #     employee.save()
    #
    #

    study = Study.objects.get(id=study_id)
    questionnaire_inst = Questionnaire.objects.get(id=questionnaire_id)
    participant_id = questionnaire_inst.participant.id

    participant = Participant.objects.get(id=participant_id, study=study)
    participant.completed_at = timezone.now()
    participant.current_percentage = 100
    participant.answered_questions_qnt = participant.total_questions_qnt
    participant.save()

    report = Report()
    # lie_points = round(request_json['lie_points'] / 40 * 10)
    report.participant = participant
    report.lie_points = lie_points
    report.file = file_name
    report.lang = lang
    report.study = study
    if request_type == 'consultant_form':
        report.type = request_type
    report.save()

    if report_id != '':
        cur_report_inst = Report.objects.get(id=report_id)
        report.primary = False
        report.lie_points = cur_report_inst.lie_points
        report.save()
        cur_report_by_categories_inst = ReportDataByCategories.objects.filter(report_id=report_id)
        for report_by_categories in cur_report_by_categories_inst:
            new_report_by_categories = ReportDataByCategories()
            new_report_by_categories.report = report
            new_report_by_categories.section_name = report_by_categories.section_name
            new_report_by_categories.category_name = report_by_categories.category_name
            new_report_by_categories.category_code = report_by_categories.category_code
            new_report_by_categories.t_points = report_by_categories.t_points
            new_report_by_categories.save()

    study_inst = Study.objects.get(id=study_id)
    questionnaire_question_answers = QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire_inst)

    categories = Category.objects.all()
    for category in categories:
        category_raw_points = 0
        category_in_answers = False

        for answer in questionnaire_question_answers:
            if not answer.question.category.for_validity:
                # report_data = ReportData()
                # report_data.report = report
                # # report_data.section_code = section['code']
                # report_data.section_name = answer.section.name
                # # print(point['code'])
                # report_data.category_name = answer.question.category.name
                # report_data.category_code = answer.question.category.code
                #
                # report_data.points = raw_to_t_point.filter_raw_points_to_t_points(answer.answer.raw_point, participant.employee_id, answer.question.category.id)
                # # report_data.points = point['points']
                # report_data.save()

                if answer.answer.question.category.code == category.code:
                    category_in_answers = True
                    category_raw_points = category_raw_points + answer.answer.raw_point
                    # print(f'category_raw_points = {category_raw_points} + {answer.answer.raw_point}')

        if category_in_answers:
            report_data_by_categories = ReportDataByCategories()
            report_data_by_categories.report = report
            # report_data.section_code = section['code']
            report_data_by_categories.section_name = category.section.name
            # print(point['code'])
            report_data_by_categories.category_name = category.name
            report_data_by_categories.category_code = category.code

            report_data_by_categories.t_points = raw_to_t_point.filter_raw_points_to_t_points(category_raw_points, participant.employee_id, category.id)
            # report_data.points = point['points']
            report_data_by_categories.save()


    # for section in request_json['appraisal_data']:
    #     # print(section['point'])
    #     for point in section['point']:
    #         # print(f"{point['category']} - {point['points']}")
    #         report_data = ReportData()
    #         report_data.report = report
    #         report_data.section_code = section['code']
    #         report_data.section_name = section['section']
    #         # print(point['code'])
    #         report_data.category_name = point['category']
    #         report_data.category_code = point['code']
    #         report_data.points = raw_to_t_point.get_t_point(point['points'], point['code'], request_json['participant_info']['sex'], int(request_json['participant_info']['year']))
    #         # report_data.points = point['points']
    #         report_data.save()

    data_for_mail = {
        'participant_name': participant.employee.name,
        'email': participant.employee.email,
        'company_name': participant.employee.company.name,
        'study_name': participant.study.name,
        # 'to_email': to_email
    }

    send_email_result_to_participant = {}
    send_email_result_to_zetic_admin = {}
    send_emails_after_individual_report_filled_up_setting = CommonBooleanSettings.objects.get(name='Отправлять письма после заполнения личного отчета').value
    if send_emails_after_individual_report_filled_up_setting:
        if report_id == '':
            if request_type == 'consultant_form':
                consultant_form_id = data['consultant_form_id']
                consultant_name = ConsultantForm.objects.get(id=consultant_form_id).user.first_name
                data_for_mail.update({
                    'consultant_name': consultant_name
                })
                send_email_result_to_participant = mail_handler.send_notification_to_participant_report_made(data_for_mail, report.id, request_type)
            else:
                if participant.send_report_to_participant_after_filling_up:
                    send_email_result_to_participant = mail_handler.send_notification_to_participant_report_made(data_for_mail, report.id, request_type)
                send_email_result_to_zetic_admin = mail_handler.send_notification_report_made(data_for_mail, report.id)

    # сохраняем инфо об отправке письма респонденту с выводами ээкперта
    if 'consultant_form_id' in data:
        consultant_form = ConsultantForm.objects.get(id=data['consultant_form_id'])
        consultant_form_email_sent_to_participant = ConsultantFormEmailSentToParticipant()
        consultant_form_email_sent_to_participant.consultant_form = consultant_form
        consultant_form_email_sent_to_participant.save()

    if 'error' in send_email_result_to_participant or 'error' in send_email_result_to_zetic_admin:
        return {'error': 'Указан некорректный Email'}
    else:
        return {'result': 200}
