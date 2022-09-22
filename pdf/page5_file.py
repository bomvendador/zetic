from pdf.draw import draw_full_scale, insert_page_number


def page5(pdf, json_section):
    scale_element_file = 'media/images/boyko_page5.png'
    pdf.set_auto_page_break(False)

    pdf.image('media/images/page5.png', x=0, y=0, w=210)

    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    pdf.cell(0, 0, 'Факторы профессионального выгорания')

    y += 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    text = u'Ниже приведено исследование механизмов эмоционального выгорания из-за последовательного снижения ' \
           u'эмоционального ответа на ситуацию. Вы можете увидеть, какие факторы формируют каждую фазу выгорания и ' \
           u'в какой точке Вы находитесь прямо сейчас.'
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

    scale_name = u'''Переживание'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Напряжение_Переживание', scale_element_file)

    y += 20
    scale_name = u'''Неудовлетворенность
собой'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Напряжение_Неудовлетворенность собой', scale_element_file)

    y += 20
    scale_name = u'''«Загнанность в
клетку»'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Напряжение_Загнанность в клетку', scale_element_file)

    y += 20
    scale_name = u'''Тревога'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Напряжение_Тревога', scale_element_file)

    y += 20
    scale_name = u'''Избирательное
реагирование'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Сопротивление_Избирательное реагирование', scale_element_file)

    y += 20
    scale_name = u'''Эмоциональная
защита'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Сопротивление_Эмоциональная защита', scale_element_file)

    y += 20
    scale_name = u'''Экономия эмоций'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Сопротивление_Экономия эмоций', scale_element_file)

    y += 20
    scale_name = u'''Эмпатическая
усталость'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Сопротивление_Эмпатическая усталость', scale_element_file)

    y += 20
    scale_name = u'''Эмоциональная
опустошенность'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Истощение_Эмоциональная опустошенность', scale_element_file)

    y += 20
    scale_name = u'''Эмоциональная
отстраненность'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Истощение_Эмоциональная отстраненность', scale_element_file)

    y += 20
    scale_name = u'''Личностная
отстраненность'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Истощение_Личностная отстраненность', scale_element_file)

    y += 20
    scale_name = u'''Психосоматика'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Истощение_Психосоматика', scale_element_file)

    insert_page_number(pdf)