from pdf.models import PointDescription
from . import raw_to_t_point
from django.utils import timezone


def extract_section(request_json, section_code):
    for section in request_json['appraisal_data']:
        if section['code'] == section_code:
            return section['point']


def extract_categories(json_section, category_code, lang, participant_info):
    for category in json_section:
        if category['code'] == category_code:
            category_point = raw_to_t_point.get_t_point(category['points'], category_code, participant_info['sex'], int(participant_info['year']))
            # category_point = category['points']
            # print(f'{timezone.localtime(timezone.now()).strftime("%d.%m.%Y %H:%M:%S")} - {category_code} - {category["points"]} - {category_point}')
            if category_point == 0:
                return {'points': category_point, 'point_description': ''}
            else:
                if lang == 'ru':
                    point_description = PointDescription.objects.get(category__code=category_code, value=category_point).text
                else:
                    point_description = PointDescription.objects.get(category__code=category_code, value=category_point).text_en
                return {'points': category_point, 'point_description': point_description}


def point_with_description(data, category_code, lang):
    # print(f'==== data ====')
    # print(data)
    # print('=============')
    for answer in data:
        if answer['code'] == category_code:
            if lang == 'ru':
                if PointDescription.objects.filter(category__code=category_code, value=answer['points']).exists():
                    point_description = PointDescription.objects.get(category__code=category_code, value=answer['points']).text
                else:
                    point_description = 'Описание отутствует'
            else:
                if PointDescription.objects.filter(category__code=category_code, value=answer['points']).exists():
                    point_description = PointDescription.objects.get(category__code=category_code,
                                                                     value=answer['points']).text_en
                else:
                    point_description = 'Описание отутствует'

            return {'points': answer['points'], 'point_description': point_description}
