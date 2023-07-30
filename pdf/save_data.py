from django.utils import timezone
from fpdf import FPDF

from panel import mail_handler
from pdf.models import (
    Report,
    Participant,
    ReportData,
    Employee,
    Study,
    EmployeeRole,
    EmployeeGender,
    EmployeePosition,
    Industry,
)
from . import raw_to_t_point
from .single_report import IncomingSingleReportData, SingleReportData


def save_data_to_db(
    report_data: SingleReportData,
    data: IncomingSingleReportData,
    file_name: str,
    pdf: FPDF,
):
    employees = Employee.objects.filter(email=data.participant_info.email)
    if employees.exists():
        sexes = EmployeeGender.objects.filter(public_code=data.participant_info.sex)
        roles = EmployeeRole.objects.filter(public_code=data.participant_info.role)
        industries = Industry.objects.filter(public_code=data.participant_info.industry)
        positions = EmployeePosition.objects.filter(
            public_code=data.participant_info.position
        )

        employee = employees.first()
        employee.name = data.participant_info.name
        employee.birth_year = data.participant_info.year
        employee.sex = sexes.first() if sexes.exists() else None
        employee.role = roles.first() if roles.exists() else None
        employee.industry = industries.first() if industries.exists() else None
        employee.position = positions.first() if positions.exists() else None
        employee.save()
        print(
            f"Employee updated {employee.birth_year} {employee.sex} {employee.role} {employee.industry} {employee.position}"
        )

    study = Study.objects.get(public_code=data.study.id)

    if Participant.objects.filter(
        employee__email=data.participant_info.email, study=study
    ).exists():

        participant = Participant.objects.get(
            employee__email=data.participant_info.email, study=study
        )
    else:
        participant = Participant()
    participant.completed_at = timezone.now()
    participant.current_percentage = 100
    participant.answered_questions_qnt = participant.total_questions_qnt
    participant.save()

    if Report.objects.filter(code=data.code).exists():
        report = Report.objects.get(code=data.code)
        ReportData.objects.filter(report=report).delete()
    else:
        report = Report()
    lie_points = round(data.lie_points / 40 * 10)
    report.participant = participant
    report.lie_points = lie_points
    report.code = data.code
    report.file = file_name
    report.lang = data.lang
    report.study = study
    report.save()

    for section in report_data.cattell_data:
        # print(section['point'])
        for point in section.point:
            # print(f"{point['category']} - {point['points']}")
            report_data = ReportData()
            report_data.report = report
            report_data.section_code = section.code
            report_data.section_name = section.section
            # print(point['code'])
            report_data.category_name = point.category[:50]
            report_data.category_code = point.code
            report_data.points = raw_to_t_point.get_t_point(
                point.points,
                point.code,
                data.participant_info.sex,
                data.participant_info.year,
            )
            # report_data.points = point['points']
            report_data.save()

    if participant.send_admin_notification_after_filling_up:
        to_email = "info@zetic.ru"
        data_for_mail = {
            "participant_name": participant.employee.name,
            "email": data.participant_info.email,
            "company_name": participant.employee.company.name,
            "study_name": participant.study.name,
            "to_email": to_email,
        }
        mail_handler.send_notification_report_made(data_for_mail)

    if participant.send_report_on_complete and participant.report_sent_at is None:
        participant.report_sent_at = timezone.now()
        participant.save()
        to_email = participant.employee.email
        data_for_mail = {
            "participant_name": participant.employee.name,
            "company_name": participant.employee.company.name,
            "study_name": participant.study.name,
            "to_email": to_email,
        }
        mail_handler.send_participant_report(
            to_email=to_email,
            pdf_report=pdf.output(),
        )
