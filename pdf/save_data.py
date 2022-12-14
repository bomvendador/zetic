from pdf.models import Report, Participant, Company, ReportData, Section, Category


def save_data_to_db(request_json, file_name):

    if Company.objects.filter(name=request_json['project']).exists():
        company = Company.objects.get(name=request_json['project'])
    else:
        company = Company()
        company.name = request_json['project']
        company.save()

    if Participant.objects.filter(email=request_json['participant_info']['email']).exists():
        participant = Participant.objects.get(email=request_json['participant_info']['email'])
    else:
        participant = Participant()
        participant.fio = request_json['participant_info']['name']
        participant.sex = request_json['participant_info']['sex']
        participant.birth_year = request_json['participant_info']['birth_year']
        participant.email = request_json['participant_info']['email']
        participant.company = company
        participant.save()

    if Report.objects.filter(code=request_json['code']).exists():
        report = Report.objects.get(code=request_json['code'])
        ReportData.objects.filter(report=report).delete()
    else:
        report = Report()
    report.participant = participant
    report.lie_points = request_json['lie_points']
    report.code = request_json['code']
    report.file = file_name
    report.lang = request_json['lang']
    report.save()

    for section in request_json['appraisal_data']:
        # print(section['point'])
        for point in section['point']:
            # print(f"{point['category']} - {point['points']}")
            report_data = ReportData()
            report_data.report = report
            report_data.section = Section.objects.get(name=section['section'])
            report_data.category = Category.objects.get(name=point['category'])
            report_data.points = point['points']
            report_data.save()
