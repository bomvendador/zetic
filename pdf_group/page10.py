from pdf.draw import insert_page_number
from pdf_group.draw import draw_table
from pdf_group.page_funcs import proceed_scale, block_name
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B


def page10(pdf, square_results, lang):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    delta_x_between_scales = 28

    x = 8
    y = 10
    pdf.set_xy(x + 2, y)
    pdf.set_font("RalewayBold", "", 10)

    if lang == 'ru':
        pdf.cell(0, 0, 'Жизненные ценности: групповые результаты')
    else:
        pdf.cell(0, 0, 'Section K')
    pdf.set_draw_color(0,0,0)
    pdf.line(x + 1 + 2, y + 5, x + 220, y + 5)

    pdf.set_xy(x, y)

    y = y + 8

    start_block_name_y = y + 3

    scale_name = u'''
Причастность
            '''
    scale_discription = '''
Потребность в выстраивании
социальных контактов и
ощущении принадлежности
к группе
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Ценности', 'Причастность', description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)

    y = y + delta_x_between_scales

    scale_name = u'''
Традиционализм
            '''
    scale_discription = '''
Уважение и следование
нормам, принятым в
культуре / социальной
группе
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Ценности', 'Традицонализм', description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)

    y = y + delta_x_between_scales

    scale_name = u'''
Жажда впечатлений
            '''
    scale_discription = '''
Потребность в разнообразии,
новизне и глубоких
переживаниях; желание
погружаться в приключения,
получать новый опыт
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Ценности', 'Жажда впечатлений', description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)

    y = y + delta_x_between_scales

    scale_name = u'''
Эстетичность
            '''
    scale_discription = '''
Потребность в самовыражении,
ощущение важности
визуальности и гармоничности
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Ценности', 'Эстетичность', description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)

    y = y + delta_x_between_scales

    scale_name = u'''
Гедонизм
            '''
    scale_discription = '''
Потребность в наслаждении
или чувственном удовольствии,
ощущении полноты жизни

        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Ценности', 'Гедонизм', description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y, "СОЗДАНИЕ ГАРМОНИИ", end_y_delta=27, end_y_text_delta=60)

    y = y + delta_x_between_scales

    start_block_name_y = y + 3

    scale_name = u'''
Признание
            '''
    scale_discription = '''
Фокус на достижении
социального статуса или
престижа, контроля или
доминирования над
ресурсами и людьми
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Ценности', 'Признание', description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)

    y = y + delta_x_between_scales

    scale_name = u'''
Достижения
            '''
    scale_discription = '''
Желание достичь личного успеха
через соревновательность
и преодоление «вызовов»,
стремление быть лучшим
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Ценности', 'Достижения', description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=248, arrow_color_g=216, arrow_color_b=31)


    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y, "", end_y_delta=30, end_y_text_delta=50)

    draw_table(square_results, pdf, width=90, x=14, y=230)
    insert_page_number(pdf)

