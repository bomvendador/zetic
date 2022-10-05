from pdf.draw import draw_full_scale, insert_page_number


def page5(pdf, json_section, lang):
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

    vert_text_y = 73
    if lang == 'ru':
        with pdf.rotation(90, 10, vert_text_y+1):
            pdf.text(0, vert_text_y+1, "Фаза 1. Напряжение")
    else:
        with pdf.rotation(90, 10, vert_text_y+1):
            pdf.text(0, vert_text_y, "Phase 1. Tension")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(13, vert_text_y - 35, 13, vert_text_y + 31)

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

    if lang== 'ru':
        scale_name = u'''Переживание'''
    else:
        scale_name = u'''Concern'''

    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Напряжение_Переживание', scale_element_file, lang)

    y += 20
    if lang == 'ru':
        scale_name = u'''Неудовлетворенность
собой'''
        draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Напряжение_Неудовлетворенность собой', scale_element_file, lang)
    else:
        scale_name = u'''Self dissatisfaction'''
        draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Напряжение_Неудовлетворенность собой', scale_element_file, lang)

    y += 20
    if lang == 'ru':
        scale_name = u'''«Загнанность в
клетку»'''
        draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Напряжение_Загнанность в клетку', scale_element_file, lang)
    else:
        scale_name = u'''Feeling trapped'''
        draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Напряжение_Загнанность в клетку', scale_element_file, lang)

    y += 20
    if lang == 'ru':
        scale_name = u'''Тревога'''
    else:
        scale_name = u'''Anxiety'''

    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Напряжение_Тревога', scale_element_file, lang)

    vert_text_y = 152
    if lang == 'ru':
        with pdf.rotation(90, 10, vert_text_y+1):
            pdf.text(0, vert_text_y+1, "Фаза 2. Сопротивление")
    else:
        with pdf.rotation(90, 10, vert_text_y+1):
            pdf.text(0, vert_text_y+1, "Phase 2. Resistance")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(13, vert_text_y - 35, 13, vert_text_y + 31)

    y += 20
    if lang == 'ru':
        scale_name = u'''Избирательное
реагирование'''
    else:
        scale_name = u'''Selective emotional
response'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Сопротивление_Избирательное реагирование', scale_element_file, lang)

    y += 20
    if lang == 'ru':
        scale_name = u'''Эмоциональная
защита'''
    else:
        scale_name = u'''Emotional
defense'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Сопротивление_Эмоциональная защита', scale_element_file, lang)

    y += 20
    if lang == 'ru':
        scale_name = u'''Экономия эмоций'''
    else:
        scale_name = u'''Emotional saving'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Сопротивление_Экономия эмоций', scale_element_file, lang)

    y += 20
    if lang == 'ru':
        scale_name = u'''Эмпатическая
усталость'''
        draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Сопротивление_Эмпатическая усталость', scale_element_file, lang)
    else:
        scale_name = u'''Empathic fatigue'''
        draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Сопротивление_Эмпатическая усталость', scale_element_file, lang)

    vert_text_y = 232
    if lang == 'ru':
        with pdf.rotation(90, 10, vert_text_y+1):
            pdf.text(0, vert_text_y+1, "Фаза 3. Истощение")
    else:
        with pdf.rotation(90, 10, vert_text_y):
            pdf.text(0, vert_text_y, "Phase 3. Exhaustion")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(13, vert_text_y - 35, 13, vert_text_y + 31)

    y += 20
    if lang == 'ru':
        scale_name = u'''Эмоциональная
опустошенность'''
    else:
        scale_name = u'''Emotional
emptiness'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Истощение_Эмоциональная опустошенность', scale_element_file, lang)

    y += 20
    if lang == 'ru':
        scale_name = u'''Эмоциональная
отстраненность'''
    else:
        scale_name = u'''Emotional
detachment'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Истощение_Эмоциональная отстраненность', scale_element_file, lang)

    y += 20
    if lang == 'ru':
        scale_name = u'''Личностная
отстраненность'''
    else:
        scale_name = u'''Personal
detachment'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Истощение_Личностная отстраненность', scale_element_file, lang)

    y += 20
    if lang == 'ru':
        scale_name = u'''Психосоматика'''
    else:
        scale_name = u'''Physical discomfort'''

    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Истощение_Психосоматика', scale_element_file, lang)

    insert_page_number(pdf)
