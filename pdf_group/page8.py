from pdf.draw import insert_page_number
from pdf_group.draw import draw_table
from pdf_group.page_funcs import proceed_scale, block_name, data_by_points
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B


def page8(pdf, square_results, lang, table_y):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    delta_x_between_scales = 28

    section_code = '3'

    x = 8
    y = 10
    pdf.set_xy(x + 2, y)
    pdf.set_font("RalewayBold", "", 10)

    if lang == 'ru':
        pdf.cell(0, 0, 'Интенсивность выгорания: групповые результаты')
    else:
        pdf.cell(0, 0, 'Section K')
    pdf.set_draw_color(0,0,0)
    pdf.line(x + 1 + 2, y + 5, x + 220, y + 5)

    pdf.set_xy(x, y)

    y = y + 8

    category_code = '3_1'
    section_data = data_by_points(square_results, section_code, category_code)

    start_block_name_y = y + 3

    scale_name = u'''
Переживание
            '''
    scale_discription = '''
Ощущение дискомфорта
в работе, раздражение
при решении стандартных
рабочих задач
        '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code, description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    y = y + delta_x_between_scales

    category_code = '3_2'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Неудовлетворенность
собой
            '''
    scale_discription = '''
Недовольство собой и 
ситуацией, потребность
сменить условия работы,
ощущение
        '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code, description_delta_y=9, line_delta_y=3.5,
                  arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    y = y + delta_x_between_scales

    category_code = '3_3'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
«Загнанность в клетку»
            '''
    scale_discription = '''
Ощущение невозможности
изменить ситуацию,
бессилие; отсутствие
энергии, ощущение
пустоты внутри
        '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code, description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    y = y + delta_x_between_scales

    category_code = '3_4'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Тревога
            '''
    scale_discription = '''
Эмоциональное напряжение,
ощущение тревоги и
беспричинного беспокойства,
желание «остановиться»
        '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code, description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y, "ФАЗА 1. НАПРЯЖЕНИЕ", end_y_delta=25, end_y_text_delta=45)

    y = y + delta_x_between_scales

    category_code = '3_5'
    section_data = data_by_points(square_results, section_code, category_code)

    start_block_name_y = y + 3

    scale_name = u'''
Избирательное 
реагирование
            '''
    scale_discription = '''
Зависимость коммуникации
от настроения («хочу или
не хочу»), эмоциональная
черствость, равнодушие
        '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code, description_delta_y=9, line_delta_y=3.5,
                  arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    y = y + delta_x_between_scales

    category_code = '3_6'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Эмоциональная защита
            '''
    scale_discription = '''
Эмоциональная защита,
неготовность принимать
на себя дополнительные
эмоции и справляться
с ними
        '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code, description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    y = y + delta_x_between_scales

    category_code = '3_7'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Экономия эмоций
            '''
    scale_discription = '''
Перенос защиты на другие
сферы жизни (общение с
близкими, семьей),
потребность в изоляции
от других людей
        '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code, description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y, "ФАЗА 2. СОПРОТИВЛЕНИЕ", end_y_delta=30, end_y_text_delta=30)

    draw_table(square_results, pdf, width=90, x=14, y=table_y)
    insert_page_number(pdf)
