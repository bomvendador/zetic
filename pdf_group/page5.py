from pdf.draw import insert_page_number
from pdf_group.draw import draw_table
from pdf_group.page_funcs import proceed_scale, block_name
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B


def page5(pdf, square_results, lang):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    x = 8
    y = 10
    pdf.set_xy(x + 2, y)
    pdf.set_font("RalewayBold", "", 10)

    if lang == 'ru':
        pdf.cell(0, 0, 'Реакция на стресс: групповые результаты')
    else:
        pdf.cell(0, 0, 'Section K')
    pdf.set_draw_color(0,0,0)
    pdf.line(x + 1 + 2, y + 5, x + 220, y + 5)

    pdf.set_xy(x, y)

    y = y + 8

    start_block_name_y = y + 3

    scale_name = u'''
Самообладание
            '''
    scale_discription = '''
Контроль собственных
реакций,чрезмерная
требовательность к себе
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Копинги', 'Самообладание', description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    y = y + 28

    scale_name = u'''
Контроль над ситуацией
            '''
    scale_discription = '''
Поиск и реализация решений
для преодоления проблемы
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Копинги', 'Контроль над ситуацией', description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    y = y + 28

    scale_name = u'''
Позитивная
самомотивация
            '''
    scale_discription = '''
Приписывание себе
способности управлять
ситуацией
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Копинги', 'Позитивная самомотивация', description_delta_y=9, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    y = y + 28

    scale_name = u'''
Снижение значения
стрессовой ситуации
            '''
    scale_discription = '''
Снижение значения или
тяжести напряжения
(рационализация, юмор,
обесценивание)
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Копинги', 'Снижение значения стрессовой ситуации', description_delta_y=9, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    y = y + 28

    scale_name = u'''
Самоутверждение
            '''
    scale_discription = '''
Получение признания от
других, самоутверждение
в иной области
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Копинги', 'Самоутверждение', description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y, "СТРАТЕГИИ ПРЕОДОЛЕНИЯ СТРЕССА", end_y_delta=21, end_y_text_delta=42)

    y = y + 28

    start_block_name_y = y + 3

    scale_name = u'''
Отвлечение
                '''
    scale_discription = '''
Отвлечение от стрессовой
ситуаций
            '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Копинги', 'Отвлечение',
                  description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    y = y + 28

    scale_name = u'''
Бегство от стрессовой 
ситуации
                '''
    scale_discription = '''
Отказ от преодоления ситуации,
отрицание/игнорирование
проблемы, уклонение от
ответственности, нетерпение
            '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Копинги', 'Бегство от стрессовой ситуации',
                  description_delta_y=9, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y, "", end_y_delta=28, end_y_text_delta=35)

    draw_table(square_results, pdf, width=90, x=14, y=230)
    insert_page_number(pdf)
