import math

from pdf.draw import insert_page_number
from pdf_group.draw import draw_table
from pdf_group.page_funcs import proceed_scale, block_name, data_by_points, get_additional_delta_y, block_name_
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y


def page(pdf, square_results, lang):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    section_code = '4'

    x = 10
    y = START_Y
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    if lang == 'ru':
        pdf.cell(0, 0, 'Жизненные ценности: групповые результаты')
    else:
        pdf.cell(0, 0, 'Section K')
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + 5, x + 220, y + 5)

    pdf.set_xy(x, y)
# ------------------------
    y = y + 8

    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, "СОЗДАНИЕ ГАРМОНИИ")

    y = y + 12

    category_code = '4_1'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    scale_name = 'Причастность'
    scale_description = 'Потребность в выстраивании\nсоциальных контактов и\nощущении принадлежности\nк группе'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=5, line_delta_y=2.5, arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)
# -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '4_2'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Традиционализм'
    scale_description = 'Уважение и следование\nнормам, принятым в\nкультуре / социальной\nгруппе'
    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)
# ----------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '4_3'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Жажда впечатлений'

    scale_description = 'Потребность в разнообразии,\nновизне и глубоких\nпереживаниях; желание\nпогружаться в приключения,\nполучать новый опыт'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=5, line_delta_y=2.5, arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)
# -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '4_4'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Эстетичность'

    scale_description = 'Потребность в самовыражении,\nощущение важности\nвизуальности и гармоничности'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=5, line_delta_y=2.5, arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)
# -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '4_5'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Гедонизм'

    scale_description = 'Потребность в наслаждении\nили чувственном удовольствии,\nощущении полноты жизни'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y=5, line_delta_y=2.5, arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)
# -------------------------
    start_block_name_y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    y = y + MIN_SCALE_DELTA_Y + additional_delta_y + 12

    category_code = '4_6'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        start_block_name_y = START_Y
        y = start_block_name_y + 12

    else:
        y = y

    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, start_block_name_y, x, "ФОКУС НА ДОСТИЖЕНИЕ")

    scale_name = 'Признание'

    scale_description = 'Фокус на достижении\nсоциального статуса или\nпрестижа, контроля или\nдоминирования над\nресурсами и людьми'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)
    # -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '4_7'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Достижения'

    scale_description = 'Желание достичь личного успеха\nчерез соревновательность\nи преодоление «вызовов»,\nстремление быть лучшим'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)
    # -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '4_8'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Коммерческий подход'

    scale_description = 'Принятие ответственности за\nбизнес-результаты, интерес\nк запуску продуктов'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)
    # -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '4_9'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Безопасность'

    scale_description = 'Стремление к предсказуемости,\nструктуре и порядку;\nпотребность ощущать стабильность'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)
    # -------------------------
    y = y + MIN_SCALE_DELTA_Y + additional_delta_y

    category_code = '4_10'
    section_data = data_by_points(square_results, section_code, category_code)

    additional_delta_y = get_additional_delta_y(section_data)

    if (y + MIN_SCALE_DELTA_Y + additional_delta_y) > MAX_Y:
        insert_page_number(pdf)
        pdf.add_page()
        y = START_Y
    else:
        y = y

    scale_name = 'Интеллект'

    scale_description = 'Наращивание экспертизы и\nинтеллектуального потенциала,\nсозданию сложных\nинтеллектуальных решений'

    proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code,
                  description_delta_y=5, line_delta_y=2.5, arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)
    # -------------------------

    # draw_table(square_results, pdf, width=90, x=14, y=table_y)
    insert_page_number(pdf)


