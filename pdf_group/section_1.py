import math

from pdf.draw import insert_page_number
from pdf_group.draw import draw_table
from pdf_group.page_funcs import proceed_scale, block_name, data_by_points, get_additional_delta_y, block_name_
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y


def page(pdf, square_results, lang):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    section_code = '1'

    x = 10
    y = START_Y
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    if lang == 'ru':
        pdf.cell(0, 0, 'Базовые черты личности: групповые результаты')
    else:
        pdf.cell(0, 0, 'Section K')
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + 5, x + 220, y + 5)

    pdf.set_xy(x, y)
# ------------------------
    y = y + 8

    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, "ЭМОЦИОНАЛЬНАЯ УСТОЙЧИВОСТЬ")

    y = y + 12

    category_code = '1_1'
    section_data = data_by_points(square_results, section_code, category_code)
    print(f'section_data - {section_data}')

    additional_delta_y = get_additional_delta_y(section_data)

    scale_name = 'Шкала C\nЭмоциональная\nстабильность'
    scale_description = 'Управление своим состоянием,\nобладание личной зрелостью\nи стабильностью'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=13, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '1_2'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Шкала O\nТревожность'
    scale_description = u'Склонность к беспокойству,\nтревоге, вине, повышенной\nтребовательности к себе'
    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# ----------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '1_3'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Шкала Q4\nВнутренний комфорт'

    scale_description = 'Внутренняя расслабленность,\nнетерпеливость, мотивация'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# -------------------------

    start_block_name_y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 12

    category_code = '1_4'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        start_block_name_y = START_Y
        y = start_block_name_y + 12

    else:
        y = y

    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, start_block_name_y, x, "КОМАНДНАЯ УСТОЙЧИВОСТЬ")

    scale_name = 'Шкала F\nИмпульсивность'

    scale_description = 'Экспрессивность, яркость,\nэнергичность, активное\nпроявление себя в мире'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# -----------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '1_5'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Шкала N\nДипломатичность'

    scale_description = 'Склонность к оказанию влияния,\nпостроению коммуникаций через\nэмпатию, утонченность'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# ---------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '1_6'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Шкала I\nВосприятие'

    scale_description = 'Эмпатия, восприятие мира через\nощущения, сентиментальность'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# -----------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '1_7'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Шкала A\nОткрытость'

    scale_description = 'Готовность к новым знакомствам,\nприветливость, теплота\nкоммуникации, уживчивость'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# --------------

    start_block_name_y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 12

    category_code = '1_8'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        start_block_name_y = START_Y
        y = start_block_name_y + 12

    else:
        y = y

    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, start_block_name_y, x, "УСТОЙЧИВОСТЬ РЕЗУЛЬТАТА")

    scale_name = 'Шкала M\nВосторженность'

    scale_description = 'Богатое воображение,склонность\nк концептуализации, яркость\nпроявления'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
    # -----------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '1_9'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Шкала Q2\nСамостоятельность'

    scale_description = 'Независимость взглядов и мнений,\nсамостоятельность в решениях\nи действиях'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# --------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '1_10'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Шкала G\nОтветственность'

    scale_description = 'Воля и выдержка, решимость,\nобязательность, ответственность,\nследование социальным нормам'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# --------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '1_11'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Шкала Q3\nСамоконтроль'

    scale_description = 'Дисциплина, точное следование\nсоциальным требованиям,\nзабота о репутации'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# --------------
    start_block_name_y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 12

    category_code = '1_12'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        start_block_name_y = START_Y
        y = start_block_name_y + 12

    else:
        y = y

    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, start_block_name_y, x, "УСТОЙЧИВОСТЬ В ИЗМЕНЕНИЯХ")

    scale_name = 'Шкала Q1\nКритичность'

    scale_description = 'Склонность к подробному изучению\nинформации, исследованию новых\nобластей, изучению возможностей\nдля оптимизации работы'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
    # -----------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '1_13'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Шкала L\nОсторожность'

    scale_description = 'Подозрительность,\nраздражительность,\nнедоверие к информации'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# --------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '1_14'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Шкала H\nСмелость'

    scale_description = 'Склонность к авантюризму,\nпредприимчивость'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# --------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '1_15'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Шкала E\nНезависимость'

    scale_description = 'Желание лидировать,\nдоминирование, неуступчивость'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)
# --------------


# draw_table(square_results, pdf, width=90, x=14, y=table_y)
    insert_page_number(pdf)


