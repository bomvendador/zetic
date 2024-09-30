import math

from pdf.draw import insert_page_number
# from pdf_group.draw import draw_table
from pdf_group.page_funcs import proceed_scale, block_name, data_by_points, get_additional_delta_y, block_name_
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y


def page(pdf, square_results, lang):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

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

    additional_delta_y = get_additional_delta_y(section_data)

    scale_name = 'Профессиональный тупик'
    scale_description = 'Ощущение пустоты и проф.\nнереализованности'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=5, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)
    # ----------------------

    start_block_name_y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 15
    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, start_block_name_y, x, "ФАЗА 2. СОПРОТИВЛЕНИЕ")

    # ----------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 12 + 15

    category_code = '3_15'
    section_data = data_by_points(square_results, section_code, category_code)

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

    start_block_name_y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 15
    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, start_block_name_y, x, "ФАЗА 3. ИСТОЩЕНИЕ")

    # -------------------------

    y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 12 + 15

    category_code = '3_18'

    section_data = data_by_points(square_results, section_code, category_code)

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

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    # -------------------------
    # y = y + MIN_SCALE_DELTA_Y + additional_delta_y
    #
    # category_code = '3_7'
    # section_data = data_by_points(square_results, section_code, category_code)
    #
    # additional_delta_y = get_additional_delta_y(section_data)
    #
    # if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
    #     insert_page_number(pdf)
    #     pdf.add_page()
    #     y = START_Y
    # else:
    #     y = y
    #
    # scale_name = 'Экономия эмоций'
    #
    # scale_description = 'Перенос защиты на другие\nсферы жизни (общение с\nблизкими, семьей),\nпотребность в изоляции\nот других людей'
    #
    # proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
    #               description_delta_y=5, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)
    # # -------------------------
    # y = y + MIN_SCALE_DELTA_Y + additional_delta_y
    #
    # category_code = '3_8'
    # section_data = data_by_points(square_results, section_code, category_code)
    #
    # additional_delta_y = get_additional_delta_y(section_data)
    #
    # if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
    #     insert_page_number(pdf)
    #     pdf.add_page()
    #     y = START_Y
    # else:
    #     y = y
    #
    # scale_name = 'Эмпатическая усталость'
    #
    # scale_description = 'Попытки облегчить или\nсократить обязанности,\nтребующие эмоциональных\nзатрат или эмоционального\nвовлечения'
    #
    # proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
    #               description_delta_y=5, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)
    # # -------------------------
    # start_block_name_y = y + MIN_SCALE_DELTA_Y + additional_delta_y
    #
    # y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 12
    #
    # category_code = '3_9'
    # section_data = data_by_points(square_results, section_code, category_code)
    #
    # additional_delta_y = get_additional_delta_y(section_data)
    #
    # if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
    #     insert_page_number(pdf)
    #     pdf.add_page()
    #     start_block_name_y = START_Y
    #     y = start_block_name_y + 12
    #
    # else:
    #     y = y
    #
    # block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, start_block_name_y, x, "ФАЗА 3. ИСТОЩЕНИЕ")
    #
    # scale_name = 'Эмоциональная\nопустошенность'
    #
    # scale_description = 'Избегание эмоционального\nответа на важные ситуации\nи коммуникации'
    #
    # proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
    #               description_delta_y=9, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)
    # # -------------------------
    # y = y + MIN_SCALE_DELTA_Y + additional_delta_y
    #
    # category_code = '3_10'
    # section_data = data_by_points(square_results, section_code, category_code)
    #
    # additional_delta_y = get_additional_delta_y(section_data)
    #
    # if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
    #     insert_page_number(pdf)
    #     pdf.add_page()
    #     y = START_Y
    # else:
    #     y = y
    #
    # scale_name = 'Эмоциональная\nотстраненность'
    #
    # scale_description = 'Сокращение эмоционального\nотклика на рабочие ситуации,\nнеготовность активно\nобщаться с другими'
    #
    # proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
    #               description_delta_y=9, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)
    # # -------------------------
    # y = y + MIN_SCALE_DELTA_Y + additional_delta_y
    #
    # category_code = '3_11'
    # section_data = data_by_points(square_results, section_code, category_code)
    #
    # additional_delta_y = get_additional_delta_y(section_data)
    #
    # if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
    #     insert_page_number(pdf)
    #     pdf.add_page()
    #     y = START_Y
    # else:
    #     y = y
    #
    # scale_name = 'Личностная\nотстраненность'
    #
    # scale_description = 'Обесценивание рабочих задач,\nагрессия на стандартные\nрабочие ситуации ("ненавижу",\n"не выношу", "не хочу")'
    #
    # proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
    #               description_delta_y=9, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)
    # # -------------------------
    # y = y + MIN_SCALE_DELTA_Y + additional_delta_y
    #
    # category_code = '3_12'
    # section_data = data_by_points(square_results, section_code, category_code)
    #
    # additional_delta_y = get_additional_delta_y(section_data)
    #
    # if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
    #     insert_page_number(pdf)
    #     pdf.add_page()
    #     y = START_Y
    # else:
    #     y = y
    #
    # scale_name = 'Психосоматика'
    #
    # scale_description = 'Телесные неприятные\nсостояния, плохое\nсамочувствие, отсутствие\nсил/энергии'
    #
    # proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
    #               description_delta_y=5, line_delta_y=2.5, arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)
    # -------------------------

    # draw_table(square_results, pdf, width=90, x=14, y=table_y)
    insert_page_number(pdf)


