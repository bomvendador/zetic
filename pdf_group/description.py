from pdf.draw import insert_page_number


def page(pdf, lang):
    pdf.set_auto_page_break(False)

    x = 12
    y = 12
    pdf.set_xy(x,y)
    pdf.set_font("RalewayBold", "", 10)
    # if lang == 'ru':
    pdf.cell(0, 0, 'Расшифровка командных ролей на основе модели Исхака Адизеса')
    # else:
    #     pdf.cell(0, 0, 'Introduction')
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + 5, x + 220, y + 5)


    # 17
    pdf.set_font("RalewayLight", "", 9)

    y = y + 8

    pdf.set_xy(x, y)
    # if lang == 'ru':
    text = u'Модель описывает четыре управленческие роли. Выполнение каждой из них помогает команде или организации обеспечить ' \
           u'максимально эффективную деятельность. Роли распределяются исходя из особенностей характера и интуйтивных предпочтений в ' \
           u'работе (ценности, убеждения, мотиваторы). Сотрудник может совмещать одну или несколько ролей. При этом в матрице ролей ' \
           u'будет указываться доминантная роль.'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    pdf.set_font("RalewayBold", "", 9)

    y = y + 20

    pdf.set_xy(x, y)
    # if lang == 'ru':
    text = u'Предприниматель'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    pdf.set_font("RalewayLight", "", 9)
    pdf.set_xy(x, y)

    text = u'                            – роль направлена на формирование и реализацию долгосрочных планов / стратегии, обеспечение' \
           u' развития бизнеса и продуктов. Сотрудникам в этой роли свойственно глубоко погружаться в предметную' \
           u' область, развивать экспертизу, разрабатывать и предлагать варианты развития бизнеса (клиентов, продуктов,' \
           u' вариантов монетизации, новых рыночных ниш и т.д.). Им свойственно фокусироваться на идеях, ' \
           u'ориентироваться на поиск новых / интересных решений, фантазировать. Они комфортно переживают перемены и эксперименты.'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    pdf.set_font("RalewayLight", "", 9)
    # 30

    # if lang == 'ru':
    y += 22
    pdf.set_xy(x+5, y)
    text = u'• Контролер – практичный, инициативный, высокоорганизованный и целеустремленный. Имеет твердые жизненные ' \
           u'убеждения и старается жить и работать согласно своим высоким стандартам. Эффективно управляет работой, планирует ' \
           u'и последовательно работает на развитие бизнеса. Держит свои обещания и ждут этого от других.\n' \
           u'• Изобретатель – обладает острым умом, широкой базой познаний и способностью объединять разрозненные элементы ' \
           u'в единые решения. Находится в постоянном поиске знаний, создания сложных интеллектуальных решений, готов подвергать ' \
           u'сомнению общепринятый образ мышления. Не практичен, не терпит рутины. Недисциплинирован, выполняет задачи скачкообразно.\n' \
           u'• Аналитик – обладает аналитическим мышлением, четко видит будущее и стремится реализовывать процессы максимально ' \
           u'эффективно. Настойчив, упрям, ориентирован на развитие, может не уделять внимание чувствам и переживаниям других.\n' \
           u'• Искатель ресурсов - авантюрный, активный, быстрый. Легко ориентируется в мелких деталях, фактах, цифрах. ' \
           u'Недисциплинирован, может отклоняться от плана, способен эффективно действовать в экстремальных ситуациях, исправляет' \
           u' свои ошибки по пути.  Проницателен, быстро считывает пространство и людей, подстраивается под изменения.'

    pdf.multi_cell(0, 4, text)

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

    pdf.set_font("RalewayBold", "", 9)

    y = y + 60

    pdf.set_xy(x, y)
    # if lang == 'ru':
    text = u'Производитель'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    pdf.set_font("RalewayLight", "", 9)
    pdf.set_xy(x, y)

    text = u'                – роль обеспечивает результативность в краткосрочном аспекте. Действия направлены ' \
           u'на решение операционных «горящих» задач максимально быстро. Сотрудники в этой роли проявляют нетерпеливость, ' \
           u'продуктивность и прагматичность, внутреннюю жесткость. Предрасположены к действию больше, чем к размышлениям и ' \
           u'анализу. Склонны действовать по одиночке. Получают удовлетворение от собственной вовлеченности в работу и достижения результатов.'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    pdf.set_font("RalewayLight", "", 9)
    # 30

    # if lang == 'ru':
    y += 22
    pdf.set_xy(x+5, y)
    text = u'• Организатор – фокусируется на последовательном выполнении задач, предпочитает ясность и четкую организацию. ' \
           u'Склонен игнорировать чувства в пользу логики и фактов. Ориентируется в мелких деталях и цифрах. Способен четко ' \
           u'и внимательно контролировать работу и результаты.\n' \
           u'• Любитель улучшений – рациональный, логичный, целеустремленный. Стремится к совершенству систем и процессов, ' \
           u'ориентирован на поиск возможностей для улучшений, высокопродуктивен. Склонен игнорировать чувства в пользу фактов и ' \
           u'цифр. Быстро принимает решения и реализует их, четко организует работу команды.\n' \
           u'• Решатель проблем - проявляется как высокомерный и критичный к другим. Действует скачкообразно, может' \
           u' отклоняться от плана. Находит быстрые, элегантные решения сложных задач. Нацелен на действие, а не на коммуникации.\n' \
           u'• Исполнитель - погружен в предметную область, прагматичен, стремится понять логику и механизм работы. ' \
           u'С удовольствием сам будет выполнять работу и включаться в детали, делиться опытом с другими. Настойчив, доводит' \
           u' работу до конца. Слонен быть недисциплинированным, достигать цели в последний момент.'

    pdf.multi_cell(0, 4, text)

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

    pdf.set_font("RalewayBold", "", 9)

    y = y + 52

    pdf.set_xy(x, y)
    # if lang == 'ru':
    text = u'Администратор'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    pdf.set_font("RalewayLight", "", 9)
    pdf.set_xy(x, y)

    text = u'                          – роль обеспечивает эффективность, технологичность, стандартизацию в краткосрочном аспекте. ' \
           u'Этим сотрудникам свойственно унифицировать работу, структурировать информацию и процессы, следить за порядком, ' \
           u'согласовывать и поддерживать единые правила работы. Как правило они стремятся мыслить линейно, действовать ' \
           u'осторожно и дисциплинировано, обращать внимание на мелкие детали.'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    pdf.set_font("RalewayLight", "", 9)
    # 30

    # if lang == 'ru':
    y += 18
    pdf.set_xy(x+5, y)
    text = u'• Хранитель – обладает развитыми навыками общения, считывает пространство и команду, чуток к состоянию команды.' \
           u' Внимателен к деталям, мыслит от частного к общему, педантичен, проявляет перфекционизм. Воспринимает рабочие ' \
           u'обязанности как личную ответственность, стремится выполнять их больше и лучше, чем ожидается.\n' \
           u'• Вдохновитель – чуткий и проницательный, вносит гармонию в общение между людьми. Склонен идеализировать мир, ' \
           u'верить в счастливое будущее. Ориентируется на формирование экологичных, гуманистичных, системных решений. ' \
           u'Действует дисциплинировано и аккуратно.\n' \
           u'• Опекун – обладает художественным восприятием и развитым вкусом, открыт к изменениям и экспериментам, ' \
           u'не любит рутину. Находит правильные слова для создания доверительной коммуникации, выстраивает теплое общение ' \
           u'с другими, чуток и тактичен. Готов поддерживать и помогать в развитии другим.\n' \
           u'• Благородный служитель – формирует глубокую и продуманную систему моральных принципов и долга. Обладает ' \
           u'очень хорошей интуицией и творческим чутьем. Располагает к себе, сглаживает острые углы. Ценит возможность быть ' \
           u'частью коллектива и может жертвовать своими интересами ради других. Проявляется как вдумчивый, но не ' \
           u'дистиллированный и непоследовательный.'

    pdf.multi_cell(0, 4, text)

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
    pdf.add_page()

    pdf.set_font("RalewayBold", "", 9)

    y = 12

    pdf.set_xy(x, y)
    # if lang == 'ru':
    text = u'Интегратор'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    pdf.set_font("RalewayLight", "", 9)
    pdf.set_xy(x, y)

    text = u'           – роль направлена на создание целостной организации, формирование единого видения, ' \
           u'правильного организационного климата и культуры, системы ценностей, которые будут стимулировать людей действовать' \
           u' сообща, позволят вплетать цели каждого в цели группы и бизнеса в целом. Представители этой роли социально активны, ' \
           u'стремятся к коммуникации и кросс-функциональному взаимодействию, склонны к эмпатии, умеют выслушать и поддержать, ' \
           u'формируют атмосферу взаимного уважения в коллективе.'
    # else:
    #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
    #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
    #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
    #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
    pdf.multi_cell(0, 4, text)

    pdf.set_font("RalewayLight", "", 9)
    # 30

    # if lang == 'ru':
    y += 22
    pdf.set_xy(x+5, y)
    text = u'• Массовик-затейник – стремится быть в центре внимания, принимает на себя лидерскую роль, пользуется ' \
           u'поддержкой других. Практичный, внимательный к деталям. Умеет планировать и дисциплинировано реализовывать работу.\n' \
           u'• Чуткий наставник - выстраивает крепкие отношения с коллегами, заботится о людях. Мыслит широко и интуитивно. ' \
           u'Умеет планировать и дисциплинировано реализовывать работу. Формирует эффективные процессы, в которых люди могут ' \
           u'комфортно работать.\n' \
           u'• Развлекатель – практичный, оптимистичный, спонтанный. Воспринимает мир и работу как игру, воодушевляет ' \
           u'этим окружающих. Легко адаптируется к переменам, решает проблемы по мере их возникновения. Наблюдателен и прозорлив, ' \
           u'тонко чувствует состояние людей, проявляет активный интерес и всегда готов прийти на помощь.\n' \
           u'• Мотиватор - открыт, любит говорить о людях и делиться планами. С удовольствием обсуждает собственные смелые' \
           u' идеи и фантазии. Ищет свободы, спонтанности и возможности для творчества. Склонен смотреть на жизнь как на большую ' \
           u'сложную головоломку, видеть ее через призму интуиции, эмоций, сострадания, всегда пытается добиться более глубокого понимания.'

    pdf.multi_cell(0, 4, text)

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