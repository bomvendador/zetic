from pdf.draw import insert_page_number
from pdf_group.draw import draw_table
from pdf_group.page_funcs import proceed_scale, block_name
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B


def page3(pdf, square_results, lang):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    x = 8
    y = 10
    pdf.set_xy(x + 2, y)
    pdf.set_font("RalewayBold", "", 10)

    if lang == 'ru':
        pdf.cell(0, 0, 'Базовые черты личности: групповые результаты')
    else:
        pdf.cell(0, 0, 'Section K')
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1 + 2, y + 5, x + 220, y + 5)

    pdf.set_xy(x, y)

    y = y + 8

    start_block_name_y = y + 3

    scale_name = u'''
Шкала C
Эмоциональная 
стабильность
            '''
    scale_discription = '''
Управление своим состоянием,
обладание личной зрелостью
и стабильностью
        '''
    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Кеттелл', 'Шкала C', description_delta_y=13, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    y = y + 28

    scale_name = u'''
Шкала O
Тревожность
                '''
    scale_discription = u'''
Склонность к беспокойству,
тревоге, вине, повышенной
требовательности к себе
            '''
    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Кеттелл', 'Шкала O',
                  description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    y = y + 28

    scale_name = u'''
Шкала Q4
Внутренний комфорт
            '''

    scale_discription = u'''
Внутренняя расслабленность,
нетерпеливость, мотивация
            '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Кеттелл', 'Шкала Q4', 9, 3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y, "ЭМОЦИОНАЛЬНАЯ УСТОЙЧИВОСТЬ", end_y_delta=20, end_y_text_delta=15)

    y = y + 28

    start_block_name_y = y

    scale_name = u'''
Шкала F
Импульсивность
                '''

    scale_discription = u'''
Экспрессивность, яркость,
энергичность, активное
проявление себя в мире
                '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Кеттелл', 'Шкала F',
                  description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    y = y + 28

    scale_name = u'''
Шкала N
Дипломатичность
            '''

    scale_discription = u'''
Склонность к оказанию влияния,
построению коммуникаций через
эмпатию, утонченность
            '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Кеттелл', 'Шкала N', description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    y = y + 28

    scale_name = u'''
Шкала I
Восприятие
            '''

    scale_discription = u'''
Эмпатия, восприятие мира через
ощущения, сентиментальность            
'''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Кеттелл', 'Шкала I', description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    y = y + 28

    scale_name = u'''
Шкала A
Открытость
            '''

    scale_discription = u'''
Готовность к новым знакомствам,
приветливость, теплота 
коммуникации, уживчивость'''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Кеттелл', 'Шкала A', description_delta_y=9, line_delta_y=3.5, arrow_color_r=34, arrow_color_g=170, arrow_color_b=245)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y + 3, "КОМАНДНАЯ УСТОЙЧИВОСТЬ", end_y_delta=25, end_y_text_delta=35)

    draw_table(square_results, pdf, width=90, x=14, y=230)
    insert_page_number(pdf)


