from pdf.raw_point_v1 import (
    KOPPINGI_DEFAULT,
    KETTEL_1_MEN_1950_1993,
    KETTEL_1_WOMEN_1950_1993,
    KETTEL_1_WOMEN_1994_2022,
    KETTEL_1_MEN_1994_2022,
    BOYKO_DEFAULT,
    VALUES_DEFAULT,
)


def get_t_point(raw_point, category_code, gender, birth_year):
    section_code = category_code.split("_")[0]
    tpoint = 0
    if section_code == str(1):
        if gender == "Мужской" or gender == "hombre":
            if birth_year >= 1994:
                try:
                    tpoint = KETTEL_1_MEN_1994_2022[category_code][str(raw_point)]
                except KeyError:
                    return "raw point error"
            else:
                try:
                    tpoint = KETTEL_1_MEN_1950_1993[category_code][str(raw_point)]
                except KeyError:
                    return "raw point error"
        if gender == "Женский" or gender == "mujer":
            if birth_year >= 1994:
                try:
                    tpoint = KETTEL_1_WOMEN_1994_2022[category_code][str(raw_point)]
                except KeyError:
                    return "raw point error"
            else:
                try:
                    tpoint = KETTEL_1_WOMEN_1950_1993[category_code][str(raw_point)]
                except KeyError:
                    return "raw point error"

    if section_code == str(2):
        try:
            tpoint = KOPPINGI_DEFAULT[category_code][str(raw_point)]
        except KeyError:
            return "raw point error"
    if section_code == str(3):
        try:
            tpoint = BOYKO_DEFAULT[category_code][str(raw_point)]
        except KeyError:
            return "raw point error"
    if section_code == str(4):
        max_point = VALUES_DEFAULT[category_code]
        tpoint = round(raw_point / max_point * 10)

    return tpoint


# print(get_t_point(30, '1_10', 'мужской', 1995))
# print(get_t_point(20, '1_1', 'женский', 1965))
# print(get_t_point(5, '2_1', '', ''))
# print(get_t_point(10, '3_3', '', ''))
# print(get_t_point(15, '4_1', '', ''))
