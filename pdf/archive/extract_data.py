from pdf.models import PointDescription
from . import raw_to_t_point


def extract_section(request_json, section_code):
    for section in request_json["appraisal_data"]:
        if section["code"] == section_code:
            return section["point"]


def extract_categories(json_section, category_code, lang, participant_info):
    for category in json_section:
        if category["code"] == category_code:
            category_point = raw_to_t_point.get_t_point(
                category["points"],
                category_code,
                participant_info["sex"],
                int(participant_info["year"]),
            )
            # category_point = category['points']
            # print(f'{category_code} - {category["points"]} - {category_point} {participant_info["sex"]} {participant_info["year"]}')
            # print(f'{timezone.localtime(timezone.now()).strftime("%d.%m.%Y %H:%M:%S")} - {category_code} - {category["points"]} - {category_point}')
            try:
                if category_point == 0:
                    return {"points": category_point, "point_description": ""}
                else:
                    if lang == "ru":
                        point_description = PointDescription.objects.get(
                            category__code=category_code, value=category_point
                        ).text
                    else:
                        point_description = PointDescription.objects.get(
                            category__code=category_code, value=category_point
                        ).text_en
                    return {
                        "points": category_point,
                        "point_description": point_description,
                    }
            except PointDescription.DoesNotExist as e:
                print(
                    f"PointDescription does not exist for {category_code} - {category_point}"
                )
                raise e