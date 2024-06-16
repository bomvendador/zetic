from pdf.draw import draw_full_scale, insert_page_number


def page5(pdf, json_section, lang, participant_info):
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

    # vert_text_y = 73
    vert_text_y = 65
    if lang == 'ru':
        with pdf.rotation(90, 10, vert_text_y+1):
            pdf.text(0, vert_text_y+1, "Фаза 1. Напряжение")
    else:
        with pdf.rotation(90, 10, vert_text_y+1):
            pdf.text(0, vert_text_y, "Phase 1. Tension")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(13, vert_text_y - 25, 13, vert_text_y + 18)

    y += 22
    # y += vert_text_y
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

    if lang == 'ru':
        scale_name = u'''Усталость от нагрузки,
скорости и принципов 
работы'''
    else:
        scale_name = u''''''
    draw_full_scale(pdf, scale_name, x, y + 12, y + 12 - 2, json_section, '3_14', scale_element_file, lang,
                    participant_info)

    y += 20

    if lang == 'ru':
        scale_name = u'''Профессиональный 
тупик'''
    else:
        scale_name = u''''''

    draw_full_scale(pdf, scale_name, x, y + 12, y + 12 - 2, json_section, '3_13', scale_element_file, lang,
                    participant_info)

    # vert_text_y = 152
    vert_text_y = 122
    # vert_text_y = 152
    if lang == 'ru':
        with pdf.rotation(90, 10, vert_text_y+2):
            pdf.text(0, vert_text_y+2, "Фаза 2. Сопротивление")
    else:
        with pdf.rotation(90, 10, vert_text_y+1):
            pdf.text(0, vert_text_y+1, "Phase 2. Resistance")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(13, vert_text_y - 25, 13, vert_text_y + 18)


    y += 40
    # y += vert_text_y - 35
    if lang == 'ru':
        scale_name = u'''Усталость от 
коммуникаций'''
    else:
        scale_name = u''''''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '3_15', scale_element_file, lang, participant_info)

    y += 20
    if lang == 'ru':
        scale_name = u'''Уход от коммуникаций'''
    else:
        scale_name = u''''''

    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '3_16', scale_element_file, lang, participant_info)

    # vert_text_y = 232
    vert_text_y = 179
    if lang == 'ru':
        with pdf.rotation(90, 10, vert_text_y+2):
            pdf.text(0, vert_text_y+2, "Фаза 3. Истощение")
    else:
        with pdf.rotation(90, 10, vert_text_y):
            pdf.text(0, vert_text_y, "Phase 3. Exhaustion")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(13, vert_text_y - 22, 13, vert_text_y + 18)

    y += 40
    # y += vert_text_y
    if lang == 'ru':
        scale_name = u'''Сокращение
внимания'''
    else:
        scale_name = u'''Emotional
    defense'''
    draw_full_scale(pdf, scale_name, x, y + 12, y + 12 - 2, json_section, '3_18', scale_element_file, lang,
                    participant_info)

    y += 20

    if lang == 'ru':
        scale_name = u'''Психосоматика'''
    else:
        scale_name = u'''Selective emotional
    response'''
    draw_full_scale(pdf, scale_name, x, y + 12, y + 12, json_section, '3_17', scale_element_file, lang,
                    participant_info)


    # y += 20
    # if lang == 'ru':
    #     scale_name = u'''Экономия эмоций'''
    # else:
    #     scale_name = u'''Emotional saving'''
    # draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '3_18', scale_element_file, lang, participant_info)

#     y += 20
#     if lang == 'ru':
#         scale_name = u'''Эмпатическая
# усталость'''
#         draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '3_8', scale_element_file, lang, participant_info)
#     else:
#         scale_name = u'''Empathic fatigue'''
#         draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '3_8', scale_element_file, lang, participant_info)
#
#     vert_text_y = 232
#     if lang == 'ru':
#         with pdf.rotation(90, 10, vert_text_y+1):
#             pdf.text(0, vert_text_y+1, "Фаза 3. Истощение")
#     else:
#         with pdf.rotation(90, 10, vert_text_y):
#             pdf.text(0, vert_text_y, "Phase 3. Exhaustion")
#
#     pdf.set_draw_color(0, 0, 0)
#     pdf.line(13, vert_text_y - 35, 13, vert_text_y + 31)
#
#     y += 20
#     if lang == 'ru':
#         scale_name = u'''Эмоциональная
# опустошенность'''
#     else:
#         scale_name = u'''Emotional
# emptiness'''
#     draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '3_9', scale_element_file, lang, participant_info)
#
#     y += 20
#     if lang == 'ru':
#         scale_name = u'''Эмоциональная
# отстраненность'''
#     else:
#         scale_name = u'''Emotional
# detachment'''
#     draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '3_10', scale_element_file, lang, participant_info)
#
#     y += 20
#     if lang == 'ru':
#         scale_name = u'''Личностная
# отстраненность'''
#     else:
#         scale_name = u'''Personal
# detachment'''
#     draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '3_11', scale_element_file, lang, participant_info)
#
#     y += 20
#     if lang == 'ru':
#         scale_name = u'''Психосоматика'''
#     else:
#         scale_name = u'''Physical discomfort'''
#
#     draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '3_12', scale_element_file, lang, participant_info)

    insert_page_number(pdf)
