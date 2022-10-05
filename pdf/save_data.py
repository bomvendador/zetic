from pdf.models import Report, Participant


def save_data_to_db(request_json, file_name):

    if Participant.objects.filter(email=request_json['participant_info']['email']).exists():
        participant = Participant.objects.get(email=request_json['participant_info']['email'])
    else:
        participant = Participant()
        participant.fio = request_json['participant_info']['name']
        participant.sex = request_json['participant_info']['sex']
        participant.birth_year = request_json['participant_info']['birth_year']
        participant.email = request_json['participant_info']['email']
        participant.save()
    report = Report()
    report.participant = participant
    report.lie_points = request_json['lie_points']
    report.code = request_json['code']
    report.file = file_name
    report.lang = request_json['lang']
    report.save()
