from pdf.draw import draw_full_scale, insert_page_number
import time


def page6(pdf, json_section):
    t1 = time.perf_counter()
    scale_element_file = 'media/images/values_page6.png'

    pdf.set_auto_page_break(False)

    pdf.image('media/images/page6.png', x=0, y=0, w=210)

    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    pdf.cell(0, 0, 'Ценности')

    y += 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    text = u'Ниже приведено исследование жизненных ценностей — универсальных человеческих потребностей, определяющих ' \
           u'выборы и предпочтения индивида, его жизненную стратегию.'
    pdf.multi_cell(0, 4, text, align='J')

    y += 13
    x += 6
    scale_legend_left = u'''
    Слабо выражено
    '''
    scale_legend_right = u'''
    Ярко выражено
    '''
    pdf.set_xy(x+37, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(0, 3, scale_legend_left)

    pdf.set_xy(x+37+24, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(50, 3, scale_legend_right, align='R')

    scale_name = u'''Причастность'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Причастность', scale_element_file)

    y += 20
    scale_name = u'''Традиционализм'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Традицонализм', scale_element_file)

    y += 20
    scale_name = u'''Жажда
впечатлений'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Жажда впечатлений', scale_element_file)

    y += 20
    scale_name = u'''Эстетичность'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Эстетичность', scale_element_file)

    y += 20
    scale_name = u'''Гедонизм'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Гедонизм', scale_element_file)

    y += 20
    scale_name = u'''Признание'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Признание', scale_element_file)

    y += 20
    scale_name = u'''Достижения'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Достижения', scale_element_file)

    y += 20
    scale_name = u'''Коммерческий
подход'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Коммерческий подход', scale_element_file)

    y += 20
    scale_name = u'''Безопасность'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Безопасность', scale_element_file)

    y += 20
    scale_name = u'''Интеллект'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Интеллект', scale_element_file)

    insert_page_number(pdf)
    t2 = time.perf_counter()
    print(f'стр 6 - {round(t2 - t1, 2)}')