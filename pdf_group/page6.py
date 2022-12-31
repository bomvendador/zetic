from pdf.draw import insert_page_number
from pdf_group.draw import draw_arrow, draw_table
from pdf_group.page_funcs import proceed_scale, block_name, data_by_points
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B


def page6(pdf, square_results, lang, table_y):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    section_code = '2'

    x = 8
    y = 5
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    # pdf.line(x + 1, y + 5, x + 220, y + 5)

    category_code = '2_8'
    section_data = data_by_points(square_results, section_code, category_code)

    # y = y + 10

    start_block_name_y = y

    scale_name = u'''
Антиципирующее 
избегание
'''
    scale_discription = '''
Попытка предотвратить
аналогичные стрессовые
ситуации в будущем
        '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code, description_delta_y=9, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    y = y + 28

    category_code = '2_9'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Замещение
                '''
    scale_discription = '''
Обращение к позитивным
аспектам; создание
комфортной среды для
себя и команды
            '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    y = y + 28

    category_code = '2_10'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Поиск социальной
поддержки
                '''
    scale_discription = '''
Стремление быть
выслушанным, разделить
с кем-либо переживания
            '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=9, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y, "СТРАТЕГИИ ИГНОРИРОВАНИЯ СТРЕССА", end_y_delta=25, end_y_text_delta=15)

    y = y + 28

    category_code = '2_11'
    section_data = data_by_points(square_results, section_code, category_code)

    start_block_name_y = y

    scale_name = u'''
Жалость к себе
                '''
    scale_discription = '''
Пребывание в жалости к себе,
зависти к другим;
недооценивание собственных
сил и возможностей
            '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    y = y + 28

    category_code = '2_12'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Социальная замкнутость
                '''
    scale_discription = '''
Избегание социальных контактов,
самоизоляция от
коммуникации/информации
            '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    y = y + 28

    category_code = '2_13'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Самообвинение
                '''
    scale_discription = '''
Обвинение себя в
произошедшем,
поиск причин в себе  
          '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    y = y + 28

    category_code = '2_14'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
«Заезженная пластинка»
                '''
    scale_discription = '''
Постоянное мысленное
прокручивание аспектов
стрессовой ситуации    
        '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    y = y + 28

    category_code = '2_15'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Самооправдание
                '''
    scale_discription = '''
Отказ от ответственности,
отказ от поиска решения
        '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y + 3, "СТРАТЕГИИ ПОГРУЖЕНИЯ В СТРЕСС", end_y_delta=22, end_y_text_delta=45)

    draw_table(square_results, pdf, width=90, x=14, y=table_y)
    insert_page_number(pdf)
