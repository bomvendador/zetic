from pdf.draw import draw_full_scale, insert_page_number
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y
from pdf_group.page_funcs import block_name_


# def page5(pdf, json_section, lang):
def page5(pages_data):
    pdf = pages_data['pdf']
    lang = pages_data['lang']
    json_section = pages_data['answer_code']
    participant_info = pages_data['participant_info']
    contradiction_filters_data = pages_data['contradiction_filters_data']
    scale_element_file = 'media/images/boyko_page5.png'
    pdf.set_auto_page_break(False)

    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == 'ru':
        pdf.cell(0, 0, 'Факторы профессионального выгорания')
    else:
        pdf.cell(0, 0, 'Section B')

    y += 5

    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y, x + 220, y)

    y += 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    if lang == 'ru':
        text = u'Ниже приведено исследование механизмов эмоционального выгорания из-за последовательного снижения ' \
               u'эмоционального ответа на ситуацию. Вы можете увидеть, какие факторы формируют каждую фазу выгорания и ' \
               u'в какой точке Вы находитесь прямо сейчас.'
    else:
        text = u'The following scores describe the mechanisms of emotional burnout – a consistent decrease in emotional ' \
               u'response to work situations. You can explore behavioral markers shaping burnout phase.'

    pdf.multi_cell(0, 4, text, align='J')

    # vert_text_y = 73
    vert_text_y = 65
    if lang == 'ru':

        y = pdf.get_y() + 5

        pdf.set_xy(x, y)
        block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, str('Фаза 1. Напряжение').upper())
        pdf.set_text_color(0, 0, 0)

        y = pdf.get_y() + 10
        pdf.set_xy(x, y)

        text = u'В данной фазе отражается отношение к рабочей нагрузке и рабочим процессам. Показатели выше ' \
               u'4 стенов  говорят о наличии раздражения и разочарования от работы, ощущении себя “не на своем месте”. ' \
               u'Наличие высоких показателей в данных шкалах еще не влияет на качество работы, но уже заставляет ' \
               u'сотрудника находиться в постоянном напряжении и игнорировать собственные чувства.'

        pdf.multi_cell(0, 4, text, align='J')

        # with pdf.rotation(90, 10, vert_text_y+1):
        #     pdf.text(0, vert_text_y+1, "Фаза 1. Напряжение")
    else:
        with pdf.rotation(90, 10, vert_text_y+1):
            pdf.text(0, vert_text_y, "Phase 1. Tension")

    # pdf.set_draw_color(0, 0, 0)
    # pdf.line(13, vert_text_y - 25, 13, vert_text_y + 18)

    pdf.line(0, pdf.get_y() + 2, x + 220,  pdf.get_y() + 2)

    y += 22
    # y += vert_text_y
    # x += 6
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

    if lang == 'ru':
        scale_name = u'''Усталость от нагрузки,
скорости и принципов 
работы'''
    else:
        scale_name = u''''''
    draw_full_scale(pdf, scale_name, x, y + 12, y + 12 - 2, json_section, '3_14', scale_element_file, lang, contradiction_filters_data)

    y += 20

    if lang == 'ru':
        scale_name = u'''Профессиональный 
тупик'''
    else:
        scale_name = u''''''

    draw_full_scale(pdf, scale_name, x, y + 12, y + 12 - 2, json_section, '3_13', scale_element_file, lang, contradiction_filters_data)

    # vert_text_y = 152
    vert_text_y = 122
    # vert_text_y = 152
    if lang == 'ru':

        y = pdf.get_y() + 15
        pdf.set_xy(x, y)
        block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, str('Фаза 2. Сопротивление').upper())
        pdf.set_text_color(0, 0, 0)

        y = pdf.get_y() + 10
        pdf.set_xy(x, y)

        text = u'В данной фазе отражается отношение к взаимодействию с коллегами и партнерами. Показатели выше ' \
               u'4 стенов  говорят об ощущении непродуктивности коммуникаций и их неэкологичности. Наличие высоких ' \
               u'показателей в данных шкалах опосредованно влияет на качество работы, возникает потребность сократить ' \
               u'или дистанцироваться от части рабочих коммуникаций, сохраняя силы и внимание для решения других ' \
               u'важных задач.'

        pdf.multi_cell(0, 4, text, align='J')

        # with pdf.rotation(90, 10, vert_text_y+2):
        #     pdf.text(0, vert_text_y+2, "Фаза 2. Сопротивление")
    else:
        with pdf.rotation(90, 10, vert_text_y+1):
            pdf.text(0, vert_text_y+1, "Phase 2. Resistance")

    # pdf.set_draw_color(0, 0, 0)
    # pdf.line(13, vert_text_y - 25, 13, vert_text_y + 18)
    pdf.line(0, pdf.get_y() + 2, x + 220,  pdf.get_y() + 2)

    y = pdf.get_y()
    # y += vert_text_y - 35
    if lang == 'ru':
        scale_name = u'''Усталость от 
коммуникаций'''
    else:
        scale_name = u''''''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '3_15', scale_element_file, lang, contradiction_filters_data)

    y += 20
    if lang == 'ru':
        scale_name = u'''Уход от коммуникаций'''
    else:
        scale_name = u''''''

    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '3_16', scale_element_file, lang, contradiction_filters_data)

    # vert_text_y = 232
    vert_text_y = 179
    if lang == 'ru':

        y = pdf.get_y() + 15

        pdf.set_xy(x, y)
        block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, str('Фаза 3. Истощение').upper())
        pdf.set_text_color(0, 0, 0)

        y = pdf.get_y() + 10
        pdf.set_xy(x, y)

        text = u'В данной фазе отражается уровень усталости и потери мотивации. Показатели выше 4 стенов  говорят ' \
               u'об ощущении истощения, потере внимания и снижении интереса к работе. Наличие высоких показателей ' \
               u'в данных шкалах говорит о необходимости преодолевать свою усталость и раздражение, потребности ' \
               u'пересмотреть свой рабочий режим и круг обязанностей.'

        pdf.multi_cell(0, 4, text, align='J')

        # with pdf.rotation(90, 10, vert_text_y+2):
        #     pdf.text(0, vert_text_y+2, "Фаза 3. Истощение")
    else:
        with pdf.rotation(90, 10, vert_text_y):
            pdf.text(0, vert_text_y, "Phase 3. Exhaustion")

    # pdf.set_draw_color(0, 0, 0)
    # pdf.line(13, vert_text_y - 22, 13, vert_text_y + 18)

    pdf.line(0, pdf.get_y() + 2, x + 220,  pdf.get_y() + 2)

    y = pdf.get_y()
    # y += vert_text_y
    if lang == 'ru':
        scale_name = u'''Сокращение
внимания'''
    else:
        scale_name = u'''Emotional
    defense'''
    draw_full_scale(pdf, scale_name, x, y + 12, y + 12 - 2, json_section, '3_18', scale_element_file, lang, contradiction_filters_data)

    y += 20

    if lang == 'ru':
        scale_name = u'''Психосоматика'''
    else:
        scale_name = u'''Selective emotional
    response'''
    draw_full_scale(pdf, scale_name, x, y + 12, y + 12, json_section, '3_17', scale_element_file, lang,
                    participant_info)
    insert_page_number(pdf)
