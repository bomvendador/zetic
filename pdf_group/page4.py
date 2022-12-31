from pdf.draw import insert_page_number
from pdf_group.draw import draw_arrow, draw_table
from pdf_group.page_funcs import proceed_scale, block_name, data_by_points
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B


def page4(pdf, square_results, lang, table_y):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    section_code = '1'

    x = 8
    y = 5
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    # pdf.line(x + 1, y + 5, x + 220, y + 5)

    # y = y + 10

    start_block_name_y = y + 3

    category_code = '1_8'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Шкала M
Восторженность
'''
    scale_discription = '''
Богатое воображение,склонность
к концептуализации, яркость
проявления            
        '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code, description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    y = y + 28

    category_code = '1_9'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Шкала Q2
Самостоятельность
'''
    scale_discription = '''
Независимость взглядов и мнений,
самостоятельность в решениях
и действиях
'''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code, description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    y = y + 28

    category_code = '1_10'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Шкала G
Ответственность
'''
    scale_discription = '''
Воля и выдержка, решимость,
обязательность, ответственность,
следование социальным нормам'''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code, description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    y = y + 28

    category_code = '1_11'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Шкала Q3
Самоконтроль
'''
    scale_discription = '''
Дисциплина, точное следование
социальным требованиям,
забота о репутации
'''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code, description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y, "УСТОЙЧИВОСТЬ РЕЗУЛЬТАТА", end_y_delta=25, end_y_text_delta=35)

    y = y + 28

    category_code = '1_12'
    section_data = data_by_points(square_results, section_code, category_code)

    start_block_name_y = y

    scale_name = u'''
Шкала Q1
Критичность
    '''
    scale_discription = '''
Склонность к подробному изучению
информации, исследованию новых
областей, изучению возможностей
для оптимизации работы
    '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    y = y + 28

    category_code = '1_13'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Шкала L
Осторожность
    '''
    scale_discription = '''
Подозрительность, 
раздражительность,
недоверие к информации
    '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    y = y + 28

    category_code = '1_14'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Шкала H
Смелость
    '''
    scale_discription = '''
Склонность к авантюризму,
предприимчивость
    '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    y = y + 28

    category_code = '1_15'
    section_data = data_by_points(square_results, section_code, category_code)

    scale_name = u'''
Шкала E
Независимость
    '''
    scale_discription = '''
Желание лидировать, 
доминирование, неуступчивость
    '''

    proceed_scale(pdf, x + 5, y, scale_name, section_data, scale_discription, section_code, category_code,
                  description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y + 3, "УСТОЙЧИВОСТЬ В ИЗМЕНЕНИЯХ", end_y_delta=21, end_y_text_delta=35)

    draw_table(square_results, pdf, width=90, x=14, y=table_y)
    insert_page_number(pdf)
