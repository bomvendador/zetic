from pdf.models import Report, Participant, Company, ReportData, Section, Category, ReportGroup, ReportGroupSquare, \
    Project, ProjectStudy, ProjectParticipants


def save_data_to_db(request_json, file_name):

    company_inst = Company.objects.get(id=request_json['company_id'])
    operation = request_json['operation']
    report_type = request_json['report_type']

    if operation == 'edit':
        if report_type == 'copy':
            report_group_inst = ReportGroup()
        else:
            report_group_inst = ReportGroup.objects.get(id=request_json['group_report_id'])
    else:
        report_group_inst = ReportGroup()
    report_group_inst.file = file_name
    report_group_inst.company = company_inst
    report_group_inst.comments = request_json['comments']
    report_group_inst.save()
    # participant_number = 0
    for participant_data in request_json['square_results']:
        participant_number = participant_data[7]
        participant_id = participant_data[8]
        square_name = participant_data[0]
        square_code = participant_data[6]
        bold = participant_data[3]
        group_name = participant_data[4]
        group_color = participant_data[5]
        employee_email = participant_data[1]
        if operation == 'new' or report_type == 'copy':
            project_inst = Project.objects.get(id=request_json['project_id'])
            project_participant_inst = ProjectParticipants()
            project_participant_inst.participant = Participant.objects.get(id=participant_id)
            project_participant_inst.project = project_inst
            project_participant_inst.report_group = report_group_inst
            # project_participant_inst.created_by = request.user
            project_participant_inst.save()

            report_group_square_inst = ReportGroupSquare()
            report_group_square_inst.report_group = report_group_inst
            report_group_square_inst.square_name = square_name
            report_group_square_inst.square_code = square_code
            report_group_square_inst.report = Report.objects.filter(participant__employee__email=employee_email).latest('added')
            report_group_square_inst.bold = bold
            report_group_square_inst.participant_group = group_name
            report_group_square_inst.participant_group_color = group_color
            report_group_square_inst.participant_number = participant_number
            report_group_square_inst.save()
    return report_group_inst.id
