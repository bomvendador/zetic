import math

from pdf.draw import insert_page_number
from pdf_group.draw import draw_table
from pdf_group.page_funcs import proceed_scale, block_name, data_by_points, get_additional_delta_y, block_name_
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y


def page(pdf, square_results, lang):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    section_code = '2'

    x = 10
    y = START_Y
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    if lang == 'ru':
        pdf.cell(0, 0, 'Реакция на стресс: групповые результаты')
    else:
        pdf.cell(0, 0, 'Section K')
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + 5, x + 220, y + 5)

    pdf.set_xy(x, y)
# ------------------------
    y = y + 8

    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, "СТРАТЕГИИ ПРЕОДОЛЕНИЯ СТРЕССА")

    y = y + 12
    #
    # category_code = '2_1'
    # section_data = data_by_points(square_results, section_code, category_code)
    #
    # additional_delta_y = get_additional_delta_y(section_data)
    #
    # scale_name = 'Самообладание'
    # scale_description = 'Контроль собственных\nреакций,чрезмерная\nтребовательность к себе'
    #
    # proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=5, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
# -------------------------
#     y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '2_2'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Контроль над ситуацией'
    scale_description = 'Поиск и реализация решений\nдля преодоления проблемы'
    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
# ----------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '2_8'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Антиципирующее\nизбегание'

    scale_description = 'Попытка предотвратить\nаналогичные стрессовые\nситуации в будущем'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=9, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
# -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '2_10'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Поиск социальной\nподдержки'

    scale_description = 'Стремление быть\nвыслушанным, разделить\nс кем-либо переживания'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=9, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
# -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '2_12'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Социальная замкнутость'

    scale_description = 'Избегание социальных контактов,\nсамоизоляция от\nкоммуникации/информации'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=5, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
# -------------------------

    start_block_name_y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 12

    category_code = '2_14'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        start_block_name_y = START_Y
        y = start_block_name_y + 12

    else:
        y = y

    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, start_block_name_y, x, "СТРАТЕГИИ ИГНОРИРОВАНИЯ СТРЕССА")

    scale_name = '«Заезженная пластинка»'

    scale_description = 'Постоянное мысленное\nпрокручивание аспектов\nстрессовой ситуации'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
    # -----------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '2_15'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Бегство от стрессовой\nситуации'

    scale_description = 'Отказ от преодоления ситуации,\nотрицание/игнорирование\nпроблемы, уклонение от\nответственности, нетерпение'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
    # -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '2_16'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Антиципирующее\nизбегание'

    scale_description = 'Попытка предотвратить\nаналогичные стрессовые\nситуации в будущем'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
    # -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '2_17'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Замещение'

    scale_description = 'Обращение к позитивным\nаспектам; создание\nкомфортной среды для\nсебя и команды'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
    # -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '2_18'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Поиск социальной\nподдержки'

    scale_description = 'Стремление быть\nвыслушанным, разделить\nс кем-либо переживания'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=9, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
    # -------------------------
    start_block_name_y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 12

    category_code = '2_19'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        start_block_name_y = START_Y
        y = start_block_name_y + 12

    else:
        y = y

    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, start_block_name_y, x, "СТРАТЕГИИ ПОГРУЖЕНИЯ В СТРЕСС")

    scale_name = 'Жалость к себе'

    scale_description = 'Пребывание в жалости к себе,\nзависти к другим;\nнедооценивание собственных\nсил и возможностей'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
    # -----------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '2_20'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Социальная замкнутость'

    scale_description = 'Избегание социальных контактов,\nсамоизоляция от\nкоммуникации/информации'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
    # -------------------------
    # y = y + MIN_SCALE_DELTA_Y + additional_delta_y
    #
    # category_code = '2_13'
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
    # scale_name = 'Самообвинение'
    #
    # scale_description = 'Обвинение себя в\nпроизошедшем,\nпоиск причин в себе'
    #
    # proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
    #               description_delta_y=5, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
    # # -------------------------
    # y = y + MIN_SCALE_DELTA_Y + additional_delta_y
    #
    # category_code = '2_14'
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
    # scale_name = '«Заезженная пластинка»'
    #
    # scale_description = 'Постоянное мысленное\nпрокручивание аспектов\nстрессовой ситуации'
    #
    # proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
    #               description_delta_y=5, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
    # # -------------------------
    # y = y + MIN_SCALE_DELTA_Y + additional_delta_y
    #
    # category_code = '2_15'
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
    # scale_name = 'Самооправдание'
    #
    # scale_description = 'Отказ от ответственности,\nотказ от поиска решения'
    #
    # proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
    #               description_delta_y=5, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
    # # -------------------------
    # y = y + MIN_SCALE_DELTA_Y + additional_delta_y
    #
    # category_code = '2_16'
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
    # scale_name = 'Агрессия'
    #
    # scale_description = 'Пребывание в состоянии \n' \
    #                     'сопротивления, ярость/агрессия'
    #
    # proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
    #               description_delta_y=5, line_delta_y=2.5, arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)
    # -------------------------

    # draw_table(square_results, pdf, width=90, x=14, y=table_y)
    insert_page_number(pdf)


