from pdf.models import PointDescription


def extract_section(request_json, section_name):
    for section in request_json['appraisal_data']:
        if section['section'] == section_name:
            return section['point']


def extract_categories(json_section, category_name, lang):
    for category in json_section:
        if category['category'] == category_name:
            category_point = category['points']
            if category_point == 0:
                return {'points': category['points'], 'point_description': ''}
            else:
                if lang == 'ru':
                    point_description = PointDescription.objects.get(category__name=category_name, value=category['points']).text
                else:
                    point_description = PointDescription.objects.get(category__name=category_name, value=category['points']).text_en
                return {'points': category['points'], 'point_description': point_description}
