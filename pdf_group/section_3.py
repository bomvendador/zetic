import math

from pdf.draw import insert_page_number
# from pdf_group.draw import draw_table
from pdf_group.page_funcs import proceed_scale, block_name, data_by_points, get_additional_delta_y, block_name_, proceed_scale_average_points
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y


def calculate_section_points(section_data):
    participants_cnt = 0
    participant_points = 0
    for key, value in section_data.items():
        if len(value) > 0:
            participants_cnt += 1
            participant_points += value[0][1]
    return round(participant_points/participants_cnt)


def page(pdf, square_results, lang):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    average_points = []
    average_points_by_participants = []

    section_code = '3'

    x = 5
    y = START_Y
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    if lang == 'ru':
        pdf.cell(0, 0, 'Интенсивность выгорания: групповые результаты')
    else:
        pdf.cell(0, 0, 'Section K')
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + 5, x + 220, y + 5)

    pdf.set_xy(x, y)
# ------------------------
    y = y + 8

    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, "ФАЗА 1. НАПРЯЖЕНИЕ")

    y = y + 12

    category_code = '3_14'
    section_data = data_by_points(square_results, section_code, category_code)

    average_points_by_participants.append(section_data)
    average_points.append(round(calculate_section_points(section_data)))

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Усталость от нагрузки,\nскорости и принципов\nработы'
    scale_description = 'Ощущение дискомфорта\nот нагрузки и условий работы'
    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9 + 4, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

# -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '3_13'
    section_data = data_by_points(square_results, section_code, category_code)

    average_points_by_participants.append(section_data)
    average_points.append(round(calculate_section_points(section_data)))

    additional_delta_y = get_additional_delta_y(section_data)

    scale_name = 'Профессиональный тупик'
    scale_description = 'Ощущение пустоты и проф.\nнереализованности'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=5, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)
    # ----------------------

    start_block_name_y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 5
    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, start_block_name_y, x, "ФАЗА 2. СОПРОТИВЛЕНИЕ")

    # ----------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 12 + 5

    category_code = '3_15'
    section_data = data_by_points(square_results, section_code, category_code)

    average_points_by_participants.append(section_data)
    average_points.append(round(calculate_section_points(section_data)))

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Усталость от коммуникаций'

    scale_description = 'Усталость от объема\nкоммуникации'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=5, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)
# -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '3_16'
    section_data = data_by_points(square_results, section_code, category_code)

    average_points_by_participants.append(section_data)
    average_points.append(round(calculate_section_points(section_data)))

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Уход от\nкоммуникаций'

    scale_description = 'Эмоциональная защита,\nформализация коммуникаций'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=9, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)
    # -------------------------

    start_block_name_y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 5
    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, start_block_name_y, x, "ФАЗА 3. ИСТОЩЕНИЕ")

    # -------------------------

    y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 12 + 5

    category_code = '3_18'

    section_data = data_by_points(square_results, section_code, category_code)

    average_points_by_participants.append(section_data)
    average_points.append(round(calculate_section_points(section_data)))

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Сокращение внимания'

    scale_description = 'Снижение качества работы,\nигнорирование ошибок'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    # -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y


    category_code = '3_17'
    section_data = data_by_points(square_results, section_code, category_code)

    average_points_by_participants.append(section_data)
    average_points.append(round(calculate_section_points(section_data)))

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        start_block_name_y = START_Y
        y = start_block_name_y + 12

    else:
        y = y


    scale_name = 'Психосоматика'

    scale_description = 'Постоянное напряжение,\nусталость, отсутствие сил'
    print('==============section_data===============')
    print(section_data)
    print('=======================================')
    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    y += 35
    pdf.set_xy(x, y)
    pdf.set_fill_color(BLOCK_R, BLOCK_G, BLOCK_B)
    pdf.set_draw_color(BLOCK_R, BLOCK_G, BLOCK_B)
    rect_width = 210
    rect_height = 2
    pdf.rect(0, y, rect_width, rect_height, 'FD')

    y += 10

    # average_points_for_scale = round(sum(average_points) / len(average_points))

    # print('----average_points_by_participants----')
    # print(average_points_by_participants)
    scale_name = 'Общий уровень\nвыгорания'
    proceed_scale_average_points(pdf, x, y, scale_name, average_points_by_participants, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    insert_page_number(pdf)


