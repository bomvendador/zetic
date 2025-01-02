from pdf.draw import draw_full_scale, insert_page_number
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y
from pdf_group.page_funcs import block_name_


# def page6(pdf, json_section, lang):
def page6(pages_data):
    pdf = pages_data['pdf']
    lang = pages_data['lang']
    json_section = pages_data['answer_code']
    participant_info = pages_data['participant_info']
    contradiction_filters_data = pages_data['contradiction_filters_data']

    scale_element_file = 'media/images/values_page6.png'

    pdf.set_auto_page_break(False)

    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == 'ru':
        pdf.cell(0, 0, 'Ценности')
    else:
        pdf.cell(0, 0, 'Section V')

    y += 5

    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y, x + 220, y)

    y += 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    if lang == 'ru':
        text = u'Ниже приведено исследование жизненных ценностей — универсальных человеческих потребностей, определяющих ' \
               u'выборы и предпочтения индивида, его жизненную стратегию.'
    else:
        text = u'The following scores reflect life values - fundamental human needs that determine personal choices ' \
               u'life strategies.'

    pdf.multi_cell(0, 4, text, align='J')

    y = pdf.get_y() + 5

    pdf.set_xy(x, y)
    block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, str('Создание гармонии').upper())
    pdf.set_text_color(0, 0, 0)

    y = pdf.get_y()
    pdf.set_xy(x, y)

    y += 13
    x += 6
    if lang == 'ru':
        scale_legend_left = u'''
    Слабо выражено
        '''
        scale_legend_right = u'''
    Ярко выражено
        '''
    else:
        scale_legend_left = u'''
    Weakly expressed
        '''
        scale_legend_right = u'''
    Strongly expressed
        '''

    pdf.set_xy(x+37, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(0, 3, scale_legend_left)

    pdf.set_xy(x+37+24, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(50, 3, scale_legend_right, align='R')

    pdf.set_font("RalewayLight", "", 9)
    # vert_text_y = 72
    # if lang == 'ru':
    #     with pdf.rotation(90, 10, vert_text_y+13):
    #         pdf.text(0, vert_text_y+13, "Создание гармонии")
    # else:
    #     with pdf.rotation(90, 10, vert_text_y+13):
    #         pdf.text(0, vert_text_y+13, "Creating harmony")
    #
    # pdf.set_draw_color(0, 0, 0)
    # pdf.line(13, vert_text_y - 35, 13, vert_text_y + 52)
    if lang == 'ru':
        scale_name = u'''Причастность'''
    else:
        scale_name = u'''Affiliation'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '4_1', scale_element_file, lang, contradiction_filters_data)

    y += 20
    if lang == 'ru':
        scale_name = u'''Традиционализм'''
    else:
        scale_name = u'''Conventionality'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '4_2', scale_element_file, lang, contradiction_filters_data)

    y += 20
    if lang == 'ru':
        scale_name = u'''Жажда
впечатлений'''
    else:
        scale_name = u'''Sensation
seeking'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '4_3', scale_element_file, lang, contradiction_filters_data)

    y += 20
    if lang == 'ru':
        scale_name = u'''Эстетичность'''
    else:
        scale_name = u'''Aesthetic'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '4_4', scale_element_file, lang, contradiction_filters_data)

    y += 20
    if lang == 'ru':
        scale_name = u'''Гедонизм'''
    else:
        scale_name = u'''Hedonism'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '4_5', scale_element_file, lang, contradiction_filters_data)

    pdf.set_font("RalewayLight", "", 9)
    vert_text_y = 172
    if lang == 'ru':

        y = pdf.get_y() + 15

        pdf.set_xy(x, y)
        block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, str('Преодоление').upper())
        pdf.set_text_color(0, 0, 0)

        y = pdf.get_y()
        pdf.set_xy(x, y)

        # with pdf.rotation(90, 10, vert_text_y+7):
        #     pdf.text(0, vert_text_y+7, "Преодоление")
    else:
        with pdf.rotation(90, 10, vert_text_y+12):
            pdf.text(0, vert_text_y+12, "Overcoming resistance")

    pdf.set_draw_color(0, 0, 0)
    # pdf.line(13, vert_text_y - 35, 13, vert_text_y + 52)

    y = pdf.get_y() + 10
    if lang == 'ru':
        scale_name = u'''Признание'''
    else:
        scale_name = u'''Recognition'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '4_6', scale_element_file, lang, contradiction_filters_data)

    y += 20
    if lang == 'ru':
        scale_name = u'''Достижения'''
    else:
        scale_name = u'''Achievement'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '4_7', scale_element_file, lang, contradiction_filters_data)

    y += 20
    if lang == 'ru':
        scale_name = u'''Коммерческий
подход'''
    else:
        scale_name = u'''Commercial
attitude'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '4_8', scale_element_file, lang, contradiction_filters_data)

    y += 20
    if lang == 'ru':
        scale_name = u'''Безопасность'''
    else:
        scale_name = u'''Safety'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '4_9', scale_element_file, lang, contradiction_filters_data)

    y += 20
    if lang == 'ru':
        scale_name = u'''Интеллект'''
    else:
        scale_name = u'''Curiosity'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '4_10', scale_element_file, lang, contradiction_filters_data)

    insert_page_number(pdf)
