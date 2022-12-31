from pdf.draw import insert_page_number
from pdf_group.draw import draw_arrow, draw_table
from pdf_group.page_funcs import proceed_scale, block_name, data_by_points
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B


def page11(pdf, square_results, lang, table_y):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    section_code = '4'

    delta_x_between_scales = 28

    x = 8
    y = 5
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    start_block_name_y = y

    category_code = '4_8'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Коммерческий подход
                '''
    scale_discription = '''
Принятие ответственности за
бизнес-результаты, интерес
к запуску продуктов
            '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)

    y = y + delta_x_between_scales

    category_code = '4_9'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Безопасность
                '''
    scale_discription = '''
Стремление к предсказуемости,
структуре и порядку;
потребность ощущать стабильность
            '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)

    y = y + delta_x_between_scales

    category_code = '4_10'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Интеллект
                '''
    scale_discription = '''
Наращивание экспертизы и
интеллектуального потенциала,
созданию сложных
интеллектуальных решений
            '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y, "ФОКУС НА ДОСТИЖЕНИЕ", end_y_delta=30, end_y_text_delta=30)

    draw_table(square_results, pdf, width=90, x=14, y=table_y)
    insert_page_number(pdf)
