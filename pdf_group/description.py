from pdf.draw import insert_page_number


def draw_list_item(pdf, x, text):
    x_list_padding = 2
    x_list_marker_padding = 2
    y_list_line_padding = 2
    text_marker = u'•'
    y = pdf.get_y() + y_list_line_padding

    pdf.set_xy(x + x_list_marker_padding, y)
    pdf.multi_cell(0, 4, text_marker)

    pdf.set_xy(x + x_list_marker_padding + x_list_padding, y)
    pdf.multi_cell(0, 4, text)


def page(pdf, lang):
    font_regular_name = 'RalewayRegular'
    font_bold_mame = 'RalewayBold'
    pdf.set_auto_page_break(False)
    pdf.set_line_width(0.1)

    x = 12
    y = 12
    pdf.set_xy(x,y)
    # pdf.set_font("CambriaBold", "", 11)
    pdf.set_font(font_bold_mame, "", 10)
    # if lang == 'ru':
    pdf.cell(0, 0, 'Расшифровка профилей')
    # else:
    #     pdf.cell(0, 0, 'Introduction')
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + 5, x + 220, y + 5)


    # 17
    # pdf.set_font("cambria", "", 10)
    pdf.set_font(font_regular_name, "", 9)

    y = y + 8

    pdf.set_xy(x, y)
    # if lang == 'ru':
    text = u'Командные профили описывают предпочитаемый способ выполнения работы в данный период.'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    pdf.set_font(font_bold_mame, "", 9)
    # pdf.set_font("CambriaBold", "", 10)

    y = y + 7

    pdf.set_xy(x, y)
    # if lang == 'ru':
    text = u'Предприниматель'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    y = y + 5

    # pdf.set_font("cambria", "", 10)
    pdf.set_font(font_regular_name, "", 9)
    pdf.set_xy(x, y)

    text = u'Стремится к развитию продуктов и бизнеса в долгосрочной перспективе. Таким сотрудникам' \
           u' свойственно глубоко погружаться в запросы рынка / клиентов, разрабатывать и предлагать варианты' \
           u' развития бизнеса (клиентов, продуктов/решений, монетизации, новых рыночных ниш и т.д.).'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    # pdf.set_font("cambria", "", 10)
    pdf.set_font(font_regular_name, "", 9)
    # 30

    # if lang == 'ru':
    y += 13
    pdf.set_y(y)

    text = u'Авантюрист – действует и принимает решения по ситуации, смело идет в новые задачи / зону неопределенности, ' \
           u'терпим к рискам и сигналам об опасности.'
    draw_list_item(pdf, x, text)

    text = u'Изобретатель – обладает острым умом, способностью объединять разрозненные элементы в единые решения; ' \
           u'стремится расширять свой кругозор и проф. экспертизу, получает удовольствие от создания сложных интеллектуальных решений.'
    draw_list_item(pdf, x, text)

    text = u'Визионер –  обладает абстрактным и концептуальным мышлением, видит и создает образ будущего.'
    draw_list_item(pdf, x, text)

    text = u'Искатель ресурсов - гибко реагирует на изменения в среде и прогнозирует их влияние в долгосрочной перспективе, ' \
           u'привлекает ресурсы и направляет их на развитие бизнеса.'
    draw_list_item(pdf, x, text)

#     else:
#         y += 15
#         pdf.set_xy(x+5, y)
#         text = u'''
# • The section K measures the basic personality traits and its influence of business behavior and performance.
# • The section С describes the basic reactions on stress, actions taken by a person to cope with the new worries, to adapt to tension and to find a way out of a traumatic situation.
# • The section B reflects the psychological factors that lead to burnout, the burnout indicator and intensity.
# • The section V describes the universal well-established needs and life priorities of the individual that influence decisions and choices.
# '''
#         pdf.multi_cell(0, 5, text)

    pdf.set_font(font_bold_mame, "", 9)
    y = pdf.get_y() + 5
    pdf.set_xy(x, y)
    # if lang == 'ru':
    text = u'Производитель'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    # pdf.multi_cell(0, 4, text)
    # pdf.write(5,
    # """Производитель"""
    # )
    pdf.multi_cell(0, 4, text)

    y = y + 5
    pdf.set_font(font_regular_name, "", 9)
    # pdf.set_font("cambria", "", 10)
    pdf.set_xy(x, y)

    text = u"Нацелен на выполнение планов и продуктивность здесь и сейчас; нетерпелив, прагматичен на целен на организацию " \
           u"работы и достижение целей командой; получает удовлетворение от собственной вовлеченности в работу и достижения результатов."

    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    # pdf.multi_cell(0, 4, text, markdown=True)
    pdf.multi_cell(0, 4, text)

    y += 13
    pdf.set_y(y)

    text = u'Организатор – добивается достижения целей командой, собирает нужные ресурсы, участников, инструменты для ' \
           u'реализации задач и организует работу других.'
    draw_list_item(pdf, x, text)

    text = u'Любитель улучшений – стремится к повышению продуктивности, ищет возможности для улучшений.'
    draw_list_item(pdf, x, text)

    text = u'Решатель проблем - включается по ситуации, находит быстрые работающие решения сложных задач; нацелен на действие,' \
           u'а не на коммуникации.'
    draw_list_item(pdf, x, text)

    text = u'Реализатор - ориентирован на выполнение поставленных задач, с удовольствием сам будет выполнять работу ' \
           u'включаться в детали; настойчив в достижении целей.'
    draw_list_item(pdf, x, text)

    # pdf.set_font("CambriaBold", "", 10)
    pdf.set_font(font_bold_mame, "", 9)

    y = pdf.get_y() + 5
    pdf.set_xy(x, y)
    # if lang == 'ru':
    text = u'Администратор'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    y = y + 5
    pdf.set_font(font_regular_name, "", 9)
    # pdf.set_font("cambria", "", 10)
    pdf.set_xy(x, y)

    text = u'Обеспечивает прозрачность и стандартизацию работы в краткосрочном аспекте; таким сотрудникам свойственно ' \
           u'унифицировать работу, структурировать информацию и процессы, следить за порядком, согласовывать и поддерживать единые правила работы.' \
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    y += 13
    pdf.set_y(y)

    text = u'Хранитель – выстраивает процессы и поддерживает порядок в коллективе.'
    draw_list_item(pdf, x, text)

    text = u'Вдохновитель – чуткий и проницательный, нацелен на формирование системных решений, готов поддерживать и помогать ' \
           u'в других в структурировании работы.'
    draw_list_item(pdf, x, text)

    text = u'Контроллер – отслеживает корректность процессов и решений, убеждается в соблюдении правил и стандартов работы' \
           u'другими; склонен игнорировать чувства в пользу фактов и цифр.'
    draw_list_item(pdf, x, text)

    text = u'Благородный служитель – проявляет ответственность за выполнение работы, ценит возможность быть частью коллектива,' \
           u'дисциплинированно выполняет работу, внимателен к деталям.'
    draw_list_item(pdf, x, text)

    # pdf.set_font("CambriaBold", "", 10)
    pdf.set_font(font_bold_mame, "", 9)

    y = pdf.get_y() + 5
    pdf.set_xy(x, y)
    # if lang == 'ru':
    text = u'Интегратор'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    y = y + 5
    # pdf.set_font("Cambria", "", 10)
    pdf.set_font(font_regular_name, "", 9)
    pdf.set_xy(x, y)

    text = u'Стремится к передаче знаний, обеспечению целостности культуры в долгосрочной перспективе; настраивает ' \
           u'сотрудников на совместную работу, формируют атмосферу взаимного уважения в коллективе.'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    # pdf.set_font("cambria", "", 10)
    # 30

    y = pdf.get_y() + 2
    pdf.set_y(y)

    text = u'Магнит – стремится быть в центре внимания, пользуется поддержкой; объединяет коллектив, создает среду для' \
           u' совместной работы и развития коммуникаций.'
    draw_list_item(pdf, x, text)

    text = u'Переговорщик - умеет договариваться с выгодой для себя и компании; принимает решения и реализовывает работу ' \
           u'через общение с другими.'
    draw_list_item(pdf, x, text)

    text = u'Фасилитатор –  организует работу через построение коммуникаций, помогает коллегам договориться.'
    draw_list_item(pdf, x, text)

    text = u'Коннектор - обладает развитой эмпатией, легко выстраивает новые связи и взаимоотношения с коллегами/' \
           u'партнерами/ клиентами.'
    draw_list_item(pdf, x, text)

#     else:
#         y += 15
#         pdf.set_xy(x+5, y)
#         text = u'''
# • The section K measures the basic personality traits and its influence of business behavior and performance.
# • The section С describes the basic reactions on stress, actions taken by a person to cope with the new worries, to adapt to tension and to find a way out of a traumatic situation.
# • The section B reflects the psychological factors that lead to burnout, the burnout indicator and intensity.
# • The section V describes the universal well-established needs and life priorities of the individual that influence decisions and choices.
# '''
#         pdf.multi_cell(0, 5, text)
    insert_page_number(pdf)