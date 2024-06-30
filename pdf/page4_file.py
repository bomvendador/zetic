from pdf.draw import draw_full_scale, insert_page_number


def page4(pdf, json_section, lang, participant_info):
    scale_element_file = 'media/images/kopingi_page4.png'
    pdf.set_auto_page_break(False)
    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == 'ru':
        pdf.cell(0, 0, 'Поведение в стрессе и неопределенности')
    else:
        pdf.cell(0, 0, 'Section C')

    y += 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    if lang == 'ru':
        text = u'Ниже приведены результаты исследования, отражающие наиболее типичные реакции и действия в ситуации стресса ' \
               u'или высокой неопределенности. Изучив свои стратегии поведения, Вы можете изменить их, осознанно действовать ' \
               u'иначе, повышая личную эффективность.'
    else:
        text = u'The following scores reflect the most typical reactions and actions under stressful situations or uncertainty. ' \
               u'Having studied your behavioral strategies, you can change them, consciously act differently, increasing your ' \
               u'personal effectiveness.'

    pdf.multi_cell(0, 4, text, align='J')

    y += 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == 'ru':
        pdf.cell(0, 0, 'Стратегии, направленные на активный поиск выхода и преодоление сложностей')
        scale_legend_left = u'''
    Слабо выражено
    '''
        scale_legend_right = u'''
    Ярко выражено
    '''

    else:
        pdf.cell(0, 0, 'Strategies to actively find a way out and overcome difficulties')
        scale_legend_left = u'''
    Weakly expressed
    '''
        scale_legend_right = u'''
    Strongly expressed
    '''

    y += 2

    pdf.set_xy(x+37, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(0, 3, scale_legend_left)

    pdf.set_xy(x+37+24, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(50, 3, scale_legend_right, align='R')
    if lang == 'ru':
        scale_name = u'''Самообладание и 
самоутверждение'''
    else:
        scale_name = u'''Response control'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '2_20', scale_element_file, lang, participant_info)

    y += 15
    if lang == 'ru':
        scale_name = u'''Контроль над ситуацией'''
    else:
        scale_name = u'''Situation control'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '2_2', scale_element_file, lang, participant_info)

    y += 15
    if lang == 'ru':
        scale_name = u'''Позитивная мотивация
и снижение стресса'''
    else:
        scale_name = u'''Positive
self-affirmation'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '2_18', scale_element_file, lang, participant_info)

# #     y += 15
# #     if lang == 'ru':
# #         scale_name = u'''Снижение значения
# # стрессовой ситуации'''
# #         draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '2_4', scale_element_file, lang, participant_info)
# #
# #     else:
# #         scale_name = u'''Stress minimization'''
# #         draw_full_scale(pdf, scale_name, x, y + 12, y + 12, json_section, '2_4',
# #                         scale_element_file, lang)
#
#     y += 15
#     if lang == 'ru':
#         scale_name = u'''Самоутверждение'''
#     else:
#         scale_name = u'''Self-assertion'''
#     draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '2_5', scale_element_file, lang, participant_info)

    y += 23
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == 'ru':
        pdf.cell(0, 0, 'Стратегии, направленные на игнорирование проблемы и отказ искать выход из ситуации')
    else:
        pdf.cell(0, 0, 'Strategies for ignoring problems and avoiding solutions research')

    y -= 2
    if lang == 'ru':
        scale_name = u'''Замещение, отвлечение,
бегство от стресса'''
    else:
        scale_name = u'''Distraction'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '2_17', scale_element_file, lang, participant_info)

#     y += 15
#     if lang == 'ru':
#         scale_name = u'''Бегство от стрессовой
# ситуации'''
#         draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '2_7', scale_element_file, lang, participant_info)
#     else:
#         scale_name = u'''Escape'''
#         draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '2_7', scale_element_file, lang, participant_info)

    y += 15
    if lang == 'ru':
        scale_name = u'''Антиципирующее
избегание'''
        draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '2_8', scale_element_file, lang, participant_info)
    else:
        scale_name = u'''Avoidance'''
        draw_full_scale(pdf, scale_name, x, y + 12, y + 12 - 2, json_section, '2_8',
                        scale_element_file, lang, participant_info)

        y += 15
    if lang == 'ru':
        scale_name = u'''Поиск социальной
поддержки'''
    else:
        scale_name = u'''Need for
Social Support'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '2_10', scale_element_file, lang, participant_info)

    y += 23
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == 'ru':
        pdf.cell(0, 0, 'Стратегии, провоцирующие дальнейшее нахождение в стрессе и усиление переживаний', scale_element_file)
    else:
        pdf.cell(0, 0, 'Strategies leading to further stress and strengthening worries', scale_element_file)

    y -= 2
    if lang == 'ru':
        scale_name = u'''Самообвинение 
и жалость к себе'''
    else:
        scale_name = u'''Self-pity'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '2_19', scale_element_file, lang, participant_info)

    y += 15
    if lang == 'ru':
        scale_name = u'''Социальная
замкнутость'''
    else:
        scale_name = u'''Social
withdrawal'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '2_12', scale_element_file, lang, participant_info)

    # y += 15
    # if lang == 'ru':
    #     scale_name = u'''Самообвинение'''
    # else:
    #     scale_name = u'''Self-blame'''
    # draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '2_13', scale_element_file, lang, participant_info)

    y += 15
    if lang == 'ru':
        scale_name = u'''«Заезженная
пластинка»'''
        draw_full_scale(pdf, scale_name, x, y+12, y+12-2, json_section, '2_14', scale_element_file, lang, participant_info)
    else:
        scale_name = u'''Rumination'''
        draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '2_14', scale_element_file, lang, participant_info)

    y += 15
    if lang == 'ru':
        scale_name = u'''Самооправдание'''
    else:
        scale_name = u'''Denial of guilt'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '2_15', scale_element_file, lang, participant_info)

    y += 15
    if lang == 'ru':
        scale_name = u'''Агрессия'''
    else:
        scale_name = u'''Aggression'''
    draw_full_scale(pdf, scale_name, x, y+12, y+12, json_section, '2_16', scale_element_file, lang, participant_info)

    insert_page_number(pdf)

