from pdf.draw import draw_full_scale, insert_page_number


def page4(pdf, json_section):
    scale_element_file = 'media/images/kopingi_page4.png'
    pdf.set_auto_page_break(False)
    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    pdf.cell(0, 0, 'Поведение в стрессе и неопределенности')

    y += 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    text = u'Ниже приведены результаты исследования, отражающие наиболее типичные реакции и действия в ситуации стресса ' \
           u'или высокой неопределенности. Изучив свои стратегии поведения, Вы можете изменить их, осознанно действовать ' \
           u'иначе, повышая личную эффективность.'
    pdf.multi_cell(0, 4, text, align='J')

    y += 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    pdf.cell(0, 0, 'Стратегии, направленные на активный поиск выхода и преодоление сложностей')

    y += 2

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

    scale_name = u'''Самообладание'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Самообладание', scale_element_file)

    y += 15
    scale_name = u'''Контроль над ситуацией'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Контроль над ситуацией', scale_element_file)

    y += 15
    scale_name = u'''Позитивная
самомотивация'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Позитивная самомотивация', scale_element_file)

    y += 15
    scale_name = u'''Снижение значения
стрессовой ситуации'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Снижение значения стрессовой ситуации', scale_element_file)

    y += 15
    scale_name = u'''Самоутверждение'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Самоутверждение', scale_element_file)

    y += 23
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    pdf.cell(0, 0, 'Стратегии, направленные на игнорирование проблемы и отказ искать выход из ситуации')

    y -= 2

    scale_name = u'''Отвлечение'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Отвлечение', scale_element_file)

    y += 15
    scale_name = u'''Бегство от стрессовой
ситуации'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Бегство от стрессовой ситуации', scale_element_file)

    y += 15
    scale_name = u'''Антиципирующее
избегание'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Антиципирующее избегание', scale_element_file)

    y += 15
    scale_name = u'''Замещение'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Замещение', 'media/images/kopingi_page4.png')

    y += 15
    scale_name = u'''Поиск социальной
поддержки'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Поиск социальной поддержки', scale_element_file)

    y += 23
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    pdf.cell(0, 0, 'Стратегии, провоцирующие дальнейшее нахождение в стрессе и усиление переживаний', scale_element_file)

    y -= 2

    scale_name = u'''Жалость к себе'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Жалость к себе', scale_element_file)

    y += 15
    scale_name = u'''Социальная
замкнутость'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Социальная замкнутость', scale_element_file)

    y += 15
    scale_name = u'''Самообвинение'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Самообвинение', scale_element_file)

    y += 15
    scale_name = u'''«Заезженная
пластинка»'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, 'Заезженная пластинка', scale_element_file)

    y += 15
    scale_name = u'''Самооправдание'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Самооправдание', scale_element_file)

    y += 15
    scale_name = u'''Агрессия'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, 'Агрессия', scale_element_file)

    insert_page_number(pdf)

