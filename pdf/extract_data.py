from pdf.models import PointDescription


def extract_section(request_json, section_name):
    for section in request_json['appraisal_data']:
        if section['section'] == section_name:
            return section['point']


def extract_categories(json_section, category_name):
    for category in json_section:
        print(f"category - {category['category']}")
        if category['category'] == category_name:
            # category_inst = Category.objects.filter(name=category_name)
            point_description = PointDescription.objects.get(category__name=category_name, value=category['points']).text
            return {'points': category['points'], 'point_description': point_description}
