from pdf.extract_data import extract_categories, point_with_description
from pdf.draw import draw_scale, insert_page_number


# def page3(pdf, answers_code_1, lang, participant_info):
def page3(pages_data):
    pdf = pages_data['pdf']
    lang = pages_data['lang']
    answers_code_1 = pages_data['answer_code']
    participant_info = pages_data['participant_info']
    contradiction_filters_data = pages_data['contradiction_filters_data']
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    if lang == 'ru':
        pdf.cell(0, 0, 'Черты личности')
    else:
        pdf.cell(0, 0, 'Section K')

    y += 5

    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y, x + 220, y)

    y = y + 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)

    vert_text_y = 63 + 5
    if lang == 'ru':
        with pdf.rotation(90, 12, vert_text_y+1):
            pdf.text(0, vert_text_y + 1, "Эмоциональная устойчивость")
    else:
        with pdf.rotation(90, 12, vert_text_y - 7):
            pdf.text(0, vert_text_y - 7, "Emotional stability")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(15, vert_text_y - 33, 15, vert_text_y + 14)
    if lang == 'ru':
        text = u'Приведенные ниже результаты исследования отражают фундаментальные черты личности, определяющие стиль ' \
               u'деятельности и взаимоотношения с окружением. Обнаружив эти черты, Вы можете осознанно усиливать или ослаблять их'
    else:
        text = u'The scores reflect the fundamental personality traits that determine business performance and relationship ' \
               u'attitude. By discovering these traits, you can consciously strengthen or weaken them, increasing your effectiveness.'

    pdf.multi_cell(0, 4, text, align='J')

    y += 10
    x += 3

    if lang == 'ru':
        scale_name = u'''
    Шкала С
    Эмоциональная
    стабильность
        '''
        scale_legend_left = u'''
    Следование эмоциям,
    Утомляемость
        '''
        scale_legend_right = u'''
        Стабильность, Зрелость,
        Работоспособность
        '''
    else:
        scale_name = u'''
    Scale C
    Emotional
    stability
        '''
        scale_legend_left = u'''
    Affection by feelings,
    Fatigue, Irritableness
        '''
        scale_legend_right = u'''
        Stability, Maturity,
        Workability
        '''
    category_code = '1_1'
    # points_with_description = extract_categories(answers_code_1, '1_1', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    # points_with_description = extract_categories(answers_code_1, 'Шкала C', lang)
    draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)
    print(points_with_description)
    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала O
    Тревожность        '''
        scale_legend_left = u'''
    Безмятежность
        '''
        scale_legend_right = u'''
    Чувство вины, Тревожность,
    Впечатлительность
        '''
    else:
        scale_name = u'''
    Scale O
    Apprehension
        '''
        scale_legend_left = u'''
    Self-assureness, free of guilt,
    Untroubleness, Energy
        '''
        scale_legend_right = u'''
    Self-blaming, Anxiety,
    Impressionability
        '''
    category_code = '1_2'
    # points_with_description = extract_categories(answers_code_1, '1_2', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)

    # points_with_description = extract_categories(answers_code_1, 'Шкала O', lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)
    # print(points_with_description)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала Q4
    Внутреннее
    напряжение
        '''
        scale_legend_left = u'''
    Расслабленность,
    Низкая мотивация
        '''
        scale_legend_right = u'''
    Собранность, Напряженность,
    Раздражительность
        '''
    else:
        scale_name = u'''
    Scale Q4
    Tension
        '''
        scale_legend_left = u'''
    Relaxation, Tranquility,
    Low drive,  Composure
        '''
        scale_legend_right = u'''
    Tension, Overthought,
    High drive, Irritability
        '''
    category_code = '1_3'
    # points_with_description = extract_categories(answers_code_1, '1_3', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    # points_with_description = extract_categories(answers_code_1, 'Шкала Q4', lang, participant_info)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    pdf.set_font("RalewayLight", "", 9)
    vert_text_y = 117 + 5
    if lang == 'ru':
        with pdf.rotation(90, 12, vert_text_y+1):
            pdf.text(0, vert_text_y + 1, "Командная устойчивость")
    else:
        with pdf.rotation(90, 12, vert_text_y - 6):
            pdf.text(0, vert_text_y - 6, "Team resilience")
    pdf.set_draw_color(0, 0, 0)
    pdf.line(15, vert_text_y - 36, 15, vert_text_y + 26)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала F
    Импульсивность
        '''
        scale_legend_left = u'''
    Молчаливость,
    Расчетливость
        '''
        scale_legend_right = u'''
    Беззаботность, Беспечность,
    Экспрессивность
        '''
    else:
        scale_name = u'''
    Scale F
    Impulsiveness
        '''
        scale_legend_left = u'''
    Taciturnity, Prudence,
    Temperance
        '''
        scale_legend_right = u'''
    Carelessness, Enthusiasm,
    Expressiveness
        '''
    category_code = '1_4'
    # points_with_description = extract_categories(answers_code_1, '1_4', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала N
    Дипломатичность
        '''
        scale_legend_left = u'''
    Прямолинейность,
    Четкость
        '''
        scale_legend_right = u'''
    Влияние,
    Хитрость
        '''
    else:
        scale_name = u'''
    Scale N
    Diplomacy
        '''
        scale_legend_left = u'''
    Straightforwardness,
    Tactlessness, Genuiness
        '''
        scale_legend_right = u'''
    Social awareness,
    Influence, Cunning
        '''
    category_code = '1_5'
    # points_with_description = extract_categories(answers_code_1, '1_5', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала I
    Восприятие
        '''
        scale_legend_left = u'''
    Рассудительность, Циничность
        '''
        scale_legend_right = u'''
    Эмпатичность,
    Интуитивность
        '''
    else:
        scale_name = u'''
    Scale I
    Sensitivity
        '''
        scale_legend_left = u'''
    Cynicism, Tough-mind,
    Self-reliance
        '''
        scale_legend_right = u'''
    Tender-mind, Empathy,
    Intuitiveness
        '''
    category_code = '1_6'
    # points_with_description = extract_categories(answers_code_1, '1_6', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала A
    Открытость
        '''
        scale_legend_left = u'''
    Замкнутость, Холодность,
    Безучастность, Строгость
        '''
        scale_legend_right = u'''
    Общительность,
    Открытость
        '''
    else:
        scale_name = u'''
    Scale A
    Warmth
        '''
        scale_legend_left = u'''
    Reserveness, Coldness,
    Indifference, Severity
        '''
        scale_legend_right = u'''
    Sociability, Warmth,
    Kindness, Openness
        '''
    category_code = '1_7'
    # points_with_description = extract_categories(answers_code_1, '1_7', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    pdf.set_font("RalewayLight", "", 9)
    vert_text_y = 185 + 5
    if lang == 'ru':
        with pdf.rotation(90, 12, vert_text_y):
            pdf.text(0, vert_text_y, "Устойчивость результата")
    else:
        with pdf.rotation(90, 12, vert_text_y):
            pdf.text(0, vert_text_y, "Stability of the results")
    pdf.set_draw_color(0, 0, 0)
    pdf.line(15, vert_text_y - 36, 15, vert_text_y + 26)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала M
    Концептуальность
        '''
        scale_legend_left = u'''
    Практичность,
    Реалистичность, Прозаичность
        '''
        scale_legend_right = u'''
    Абстрактное мышление,
    Воображение
        '''
    else:
        scale_name = u'''
    Scale M
    Abstractedness
        '''
        scale_legend_left = u'''
    Practicality, Integrity,
    Realism, Grounding
        '''
        scale_legend_right = u'''
    Abstracteness, Imagination,
    Idea-oriention
        '''
    category_code = '1_9'
    # points_with_description = extract_categories(answers_code_1, '1_8', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала Q2
    Автономность
        '''
        scale_legend_left = u'''
    Зависимость от группы,
    Разделение ответственности
        '''
        scale_legend_right = u'''
    Самостоятельность,
    Независимость
        '''
    else:
        scale_name = u'''
    Scale Q2
    Self-reliance
        '''
        scale_legend_left = u'''
    Group-dependence,
    Division of responsibility
        '''
        scale_legend_right = u'''
    Independence,
    Resourcefulness
        '''
    category_code = '1_9'
    # points_with_description = extract_categories(answers_code_1, '1_9', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала G
    Ответственность
        '''
        scale_legend_left = u'''
    Непостоянство, Ненадежность
        '''
        scale_legend_right = u'''
    Планирование,
    Дисциплина
        '''
    else:
        scale_name = u'''
    Scale G
    Rule-consciousness
        '''
        scale_legend_left = u'''
    Volatility, Insecurity,
    Expediency
        '''
        scale_legend_right = u'''
    Perseverance, Conformity
    Discipline, Obligation
        '''
    category_code = '1_10'
    # points_with_description = extract_categories(answers_code_1, '1_10', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала Q3
    Самоконтроль
        '''
        scale_legend_left = u'''
    Конфликтность,
    Невнимательность
        '''
        scale_legend_right = u'''
    Самоконтроль,
    Сильная воля, Долг
        '''
    else:
        scale_name = u'''
    Scale Q3
    Self-control
        '''
        scale_legend_left = u'''
    Self-conflict, Disorder Tolerance,
    Inattention
        '''
        scale_legend_right = u'''
    Self control
    Strong will, Accuracy
        '''
    category_code = '1_11'
    # points_with_description = extract_categories(answers_code_1, '1_11', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    pdf.set_font("RalewayLight", "", 9)
    vert_text_y = 252 + 5
    if lang == 'ru':
        with pdf.rotation(90, 12, vert_text_y+2):

            pdf.text(0, vert_text_y+2, "Устойчивость в изменениях")
    else:
        with pdf.rotation(90, 12, vert_text_y):
            pdf.text(0, vert_text_y, "Resilience to change")
    pdf.set_draw_color(0, 0, 0)
    pdf.line(15, vert_text_y - 36, 15, vert_text_y + 26)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала Q1
    Критичность
        '''
        scale_legend_left = u'''
    Консерватизм, Интуиция
    Принятие быстрых решений
        '''
        scale_legend_right = u'''
    Экспериментирование,
    Анализ информации
        '''
    else:
        scale_name = u'''
    Scale Q1
    Critical thinking
        '''
        scale_legend_left = u'''
    Judgement-orientation
    Change intolerance, Conservatism
        '''
        scale_legend_right = u'''
    Information analysis, Criticality
    Work optimization
        '''
    category_code = '1_13'
    # points_with_description = extract_categories(answers_code_1, '1_12', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала L
    Осторожность
        '''
        scale_legend_left = u'''
    Доверчивость, Терпимость,
    Откровенность
        '''
        scale_legend_right = u'''
    Подозрительность,
    Осторожность
        '''
    else:
        scale_name = u'''
    Scale L
    Vigilance
        '''
        scale_legend_left = u'''
    Confidence, Tolerance
    Frankness
        '''
        scale_legend_right = u'''
    Suspicion
    Caution
        '''

    category_code = '1_13'
    # points_with_description = extract_categories(answers_code_1, '1_13', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала H
    Смелость
        '''
        scale_legend_left = u'''
    Робость, Деликатность
        '''
        scale_legend_right = u'''
    Смелость, Авантюрность
        '''
    else:
        scale_name = u'''
    Scale H
    Social boldness
        '''
        scale_legend_left = u'''
    Timidity, Delicacy
        '''
        scale_legend_right = u'''
    Courage, Boldness
    Adventurism
        '''
    # points_with_description = extract_categories(answers_code_1, '1_14', lang, participant_info)
    category_code = '1_14'
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала E
    Лидерство
        '''
        scale_legend_left = u'''
    Мягкость, Тактичность,
    Уступчивость
        '''
        scale_legend_right = u'''
    Напористость, Властность,
    Самоуверенность
        '''
    else:
        scale_name = u'''
    Scale E
    Dominance
        '''
        scale_legend_left = u'''
    Softness, Tact
    Compliance
        '''
        scale_legend_right = u'''
    Assertiveness, Dominance
    Self-confidence
        '''

    category_code = '1_15'
    # points_with_description = extract_categories(answers_code_1, '1_15', lang, participant_info)
    points_with_description = point_with_description(answers_code_1, category_code, lang)
    if points_with_description:
        draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'], contradiction_filters_data)

    insert_page_number(pdf)


def draw_scale_page3(pdf, x, y, category_code, scale_name, scale_legend_left, scale_legend_right, points, points_description, contradiction_filters_data):
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    pdf.multi_cell(0, 4, scale_name)
    pdf.set_xy(x+110, y+2)
    pdf.cell(10, h=12, txt=str(points), ln=0, align='C')
    pdf.set_font("RalewayLight", "", 8)
    pdf.multi_cell(0, h=4, txt=points_description, align='L')

    y += 10
    x += 35
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(0, 3, scale_legend_left)

    border_red_color = False
    for contradiction_filter in contradiction_filters_data:
        for contradiction_category in contradiction_filter:
            if contradiction_category == category_code:
                border_red_color = True
    draw_scale(pdf, x+3, y-7, 70, 10, points, 'media/images/kettel_page3.png', border_red_color)

    x += 24
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(50, 3, scale_legend_right, align='R')


