from pdf.draw import insert_page_number


def page2(pdf, lie_points, lang):
    pdf.set_auto_page_break(False)

    x = 12
    y = 12
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == "ru":
        pdf.cell(0, 0, "Введение")
    else:
        pdf.cell(0, 0, "Introduction")

    # 17
    pdf.set_font("RalewayLight", "", 9)

    y = y + 5
    pdf.set_xy(x, y)
    if lang == "ru":
        text = (
            "Для разработки опросника ZETIC-4S был использован ряд иностранных и российских психологических исследований."
            "Подход был переработан под бизнес-контекст и апробирован на большой выборке руководителей в течение нескольких лет. "
            "Наше исследование жизнестойкости и поведения в стрессе стало самым крупным в России за последние 15 лет."
        )
    else:
        text = (
            "Based on decades of academic research Zetic has developed a tool for scientific personality measurement "
            "for business. The tool can be used for a variety of recruitment and development purposes. The approach was "
            "tested on a large sample of executives over several years. Our study of resilience and stress behavior has "
            "become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:"
        )
    pdf.multi_cell(0, 4, text)

    pdf.set_font("RalewayLight", "", 9)
    # 30

    if lang == "ru":
        y += 15
        pdf.set_xy(x + 5, y)
        text = """
• Cекция «Базовые черты личности» построена исходя из 5-факторной диспозициональной модели личности, отражающей восприятие людей друг другом. В ее основе - лексический подход, использующий факторный анализ словесных описаний характеристик человека; язык может отразить аспекты личности, которые описывают адаптацию человека к социальной среде с учетом его личных особенностей. Авторы: Г. Олпорт, П. Коста и Р. Маккрэй и Р. Кэттел. 1985-1992г. Метод апробирован на русскоязычной аудитории под руководством к.п.н. В. Хромова (УрФУ им. Б.Н.Ельцина) и д.м.н. Л. Вассермана (НИИ им. В. М. Бехтерева).
• Секция «Поведение в стрессе» сформирована исходя из модели психологического преодоления стресса, описывающей базовые реакции и действия, предпринимаемые человеком, чтобы справиться с переживанием, адаптироваться к нагрузке и найти выход из травмирующей ситуации. Автор: Ричард Лазарус, 1991г. Метод апробирован на русскоязычной аудитории под руководством к.п.н. Е.Битюцкой (МГУ им. М.В. Ломоносова), к.п.н. Е.Осина (НИУ ВШЭ), д.м.н. Л. Вассермана (НИИ им. В. М. Бехтерева).
• Секция «Факторы выгорания» построена на основе модели многофакторного эмоционального выгорания, описывающей механизмы психической защиты и переход в состояние физического и психического истощения, возникающее в ответ на эмоциональное перенапряжение.  Авторы: Б. Фрейденберг, К. Маслач 1992г. Модель апробирована на русскоязычной аудитории под руководством к.п.н. Н. Е. Водопьяновой (СПБГУ), д.м.н. Л.Вассермана (НИИ им. В. М. Бехтерева).
• Секция «Жизненные ценности» разработана на основе модели жизненных ценностей личности, описывающей универсальные устоявшиеся потребности и жизненные приоритеты личности, определяющие условия и порядок принятия личностью важных решений и реализации действий.  Авторы: Ш. Шварц, 1992г. Модель апробирована на русскоязычной аудитории под руководством В.Н. Карандашева (СПБГУ).
"""
        pdf.multi_cell(0, 4, text)

    else:
        y += 15
        pdf.set_xy(x + 5, y)
        text = """
• The section K measures the basic personality traits and its influence of business behavior and performance.
• The section С describes the basic reactions on stress, actions taken by a person to cope with the new worries, to adapt to tension and to find a way out of a traumatic situation.
• The section B reflects the psychological factors that lead to burnout, the burnout indicator and intensity.
• The section V describes the universal well-established needs and life priorities of the individual that influence decisions and choices.
"""
        pdf.multi_cell(0, 5, text)
    # 127
    pdf.set_font("RalewayBold", "", 10)

    if lang == "ru":
        y += 82 + 5 + 3
        pdf.set_xy(x, y)
        pdf.cell(0, 0, "Как читать отчет")
    else:
        y += 40
        pdf.set_xy(x, y)
        pdf.cell(0, 0, "How to read the report")

    # 131
    y += 4
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    if lang == "ru":
        text = (
            "Данные исследования описывают индивидуальный профиль устойчивости. Отчет помогает обозначить особенности "
            "реагирования на ситуации неопределенности или стресса, выявить черты личности, влияющие на рабочее поведение "
            "в сложных условиях. В данном отчете результаты сравниваются с нормативной группой русскоговорящих лидеров. "
            "Информация, содержащаяся в этом документе, является конфиденциальной. Отчет необходимо хранить в соответствии "
            "с принципами защиты персональных данных. Срок достоверности отчета — 2 года."
        )
    else:
        text = (
            "These studies describe an individual resistance profile. The report helps to identify the features of "
            "response to uncertainty and stress and to release personality traits that affect behavior within though "
            "working conditions. In this report, the results are compared with a normative group of Russian-speaking "
            "leaders of the same age and gender comparing to the participant. The information contained in this document "
            "is confidential. The report need to be stored in accordance with the  personal data protection principles. "
            "The report validity period – 2 years."
        )

    pdf.multi_cell(0, 4, text)

    # 160
    pdf.set_font("RalewayBold", "", 10)
    y += 27
    pdf.set_xy(x, y)

    if lang == "ru":
        pdf.cell(0, 0, "Шкала")
    else:
        pdf.cell(0, 0, "The scales")

    # 164
    y += 4
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    if lang == "ru":

        text = (
            "Результаты в отчете показаны в шкале стенов от 0 до 10 (от английского «стандартная десятка»). Стен означает, "
            "что 10 процентам самых низких результатов среди участников, заполнивших опросник в своей категории, присваивается 1 стен, "
            "а 90 процентов самых выраженных результатов получают 9 стен. Чем выше стен, тем ярче Вы проявляете определенное поведение. "
            "Под каждой шкалой указаны «полюсные» характеристики. Обратите внимание, что не существует «плохого» и «хорошего» поведения. "
            "Каждый «полюс» указывает на особенность характера, имеет свои преимущества и ограничения."
        )
    else:
        text = (
            "The results in the report are presented with sten scores (an abbreviation for 'Standard Ten').  The lowest "
            "10 percent of the participants who completed the questionnaire in their category are assigned 1 sten, and the "
            "top 90 percent receive 9 stens. The higher score makes the stronger behavior. Each trait is bipolar, there is no "
            "'bad' and 'good' behavior. Each pole indicates a trait that has its own strengths and limitations."
        )

    pdf.multi_cell(0, 4, text)

    pdf.set_font("RalewayLight", "", 9)
    if lang == "ru":
        y += 116 - 5 - 3
        text = "Валидность отчета"
        pdf.set_xy(x, y)
        pdf.cell(115, 12, text, ln=0)
        pdf.cell(10, 12, str(lie_points), ln=0)

    else:
        y += 158
        text = "Validity"
        pdf.set_xy(x, y)
        pdf.cell(108, 12, text, ln=0)
        pdf.cell(10, 12, str(round(lie_points / 40 * 10)), ln=0)

    pdf.set_font("RalewayLight", "", 7)
    if lang == "ru":
        text = (
            "Значения, находящиеся в пределах красной рамки (слишком высокие), "
            "свидетельствуют о разнице в восприятии между желаемым (правильном) поведении и текущих возможностях"
        )
        pdf.multi_cell(0, 3, text)
    else:
        text = "The values within the red frame (are too high) correspond to insincerity, demonstrative behavior and need for social approval."
        pdf.multi_cell(0, 4, text)

    if lang == "ru":
        draw_lie_scale(
            pdf, 50, 266, 70, 10, lie_points, "media/images/lie_scale_rec.png"
        )
    else:
        draw_lie_scale(
            pdf, 40, 266, 70, 10, lie_points, "media/images/lie_scale_rec.png"
        )

    insert_page_number(pdf)


def draw_lie_scale(pdf, x, y, w, h, lie_points, img_link):
    pdf.set_line_width(0.3)
    pdf.set_fill_color(230, 230, 230)

    pdf.rect(x, y, w, h, "F")

    pdf.set_draw_color(146, 208, 80)
    pdf.rect(x - 1, y - 1, 29.1, h + 2)
    pdf.set_draw_color(255, 0, 0)
    pdf.rect(x - 1 + 29.1, y - 1, 43, h + 2)

    for i in range(lie_points):
        pdf.image(img_link, x=x + 1, y=y + 1, w=5.9)
        x += 5.9 + 1
