from pdf.models import Report, Participant, Company, ReportData, Section, Category, ReportGroup, ReportGroupSquare


def save_data_to_db(request_json, file_name):

    project_inst = Company.objects.get(name=request_json['project'])
    report_group_inst = ReportGroup()
    report_group_inst.file = file_name
    report_group_inst.project = project_inst
    report_group_inst.comments = request_json['comments']
    report_group_inst.save()

    for participant_data in request_json['square_results']:
        report_group_square_inst = ReportGroupSquare()
        report_group_square_inst.report_group = report_group_inst
        report_group_square_inst.square_name = participant_data[0]
        report_group_square_inst.report = Report.objects.get(participant__email=participant_data[1])
        report_group_square_inst.save()