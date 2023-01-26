from pdf.models import Report, Participant, Company, ReportData, Section, Category, Employee, Study
from login.models import UserProfile
from . import raw_to_t_point
from panel import mail_handler
from django.utils import timezone


def save_data_to_db(request_json, file_name):

    # if 'company_name' in request_json:
    #     if Company.objects.filter(name=request_json['company_name']).exists():
    #         company = Company.objects.get(name=request_json['company_name'])
    #     else:
    #         company = Company()
    #         company.name = request_json['company_name']
    #         company.save()

    if Study.objects.filter(public_code=request_json['study']['id']).exists():
        study = Study.objects.get(public_code=request_json['study']['id'])
    else:
        study = Study()
        # study.company = company
        study.name = request_json['study_name']
        study.save()

    # if Employee.objects.filter(email=request_json['participant_info']['email']).exists():
    #     employee = Employee.objects.get(email=request_json['participant_info']['email'])
    # else:
    #     employee = Employee()
    #     employee.name = request_json['participant_info']['name']
    #     employee.sex = request_json['participant_info']['sex']
    #     employee.birth_year = request_json['participant_info']['year']
    #     employee.email = request_json['participant_info']['email']
    #     # employee.company = company
    #     employee.save()

    participant = Participant.objects.get(employee__email=request_json['participant_info']['email'], study=study)
    participant.completed_at = timezone.now()
    participant.current_percentage = 100
    participant.answered_questions_qnt = participant.total_questions_qnt
    participant.save()

    if Report.objects.filter(code=request_json['code']).exists():
        report = Report.objects.get(code=request_json['code'])
        ReportData.objects.filter(report=report).delete()
    else:
        report = Report()
    lie_points = round(request_json['lie_points'] / 40 * 10)
    report.participant = participant
    report.lie_points = lie_points
    report.code = request_json['code']
    report.file = file_name
    report.lang = request_json['lang']
    report.study = study
    report.save()

    for section in request_json['appraisal_data']:
        # print(section['point'])
        for point in section['point']:
            # print(f"{point['category']} - {point['points']}")
            report_data = ReportData()
            report_data.report = report
            report_data.section_code = section['code']
            report_data.section_name = section['section']
            print(point['code'])
            report_data.category_name = point['category']
            report_data.category_code = point['code']
            report_data.points = point['points']
            # report_data.points = raw_to_t_point.get_t_point(point['points'], point['code'], request_json['participant_info']['sex'], int(request_json['participant_info']['year']))
            report_data.points = point['points']
            report_data.save()

    if participant.send_admin_notification_after_filling_up:
        created_by_user = participant.created_by
        user_profile = UserProfile.objects.get(user=created_by_user)
        role_name = user_profile.role.name
        if role_name == 'Админ заказчика':
            to_email = created_by_user.email
        else:
            to_email = 'info@zetic.ru'
        data_for_mail = {
            'participant_name': participant.employee.name,
            'email': request_json['participant_info']['email'],
            'company_name': participant.employee.company.name,
            'study_name': participant.study.name,
            'to_email': to_email
        }
        mail_handler.send_notification_report_made(data_for_mail)

