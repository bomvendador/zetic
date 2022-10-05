from pdf.extract_data import extract_categories
from pdf.draw import draw_scale, insert_page_number


def page3(pdf, json_section, lang):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    if lang == 'ru':
        pdf.cell(0, 0, 'Базовые черты личности')
    else:
        pdf.cell(0, 0, 'Section K')

    y = y + 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)

    vert_text_y = 63
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
    points_with_description = extract_categories(json_section, 'Шкала C', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала O
    Тревожность        '''
        scale_legend_left = u'''
    Безмятежность,
    Энергичность
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
    points_with_description = extract_categories(json_section, 'Шкала O', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала Q4
    Внутренний комфорт
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
    points_with_description = extract_categories(json_section, 'Шкала Q4', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    pdf.set_font("RalewayLight", "", 9)
    vert_text_y = 117
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
    points_with_description = extract_categories(json_section, 'Шкала F', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала N
    Дипломатичность
        '''
        scale_legend_left = u'''
    Прямолинейность, 
    Бестактность
        '''
        scale_legend_right = u'''
    Влияние, Хитрость
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
    points_with_description = extract_categories(json_section, 'Шкала N', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала I
    Восприятие
        '''
        scale_legend_left = u'''
    Рассудительность, Циничность,
    Ответственность
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
    points_with_description = extract_categories(json_section, 'Шкала I', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

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
    points_with_description = extract_categories(json_section, 'Шкала A', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    pdf.set_font("RalewayLight", "", 9)
    vert_text_y = 185
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
    Восторженность
        '''
        scale_legend_left = u'''
    Практичность, Принципиальность
    Реалистичность, Прозаичность
        '''
        scale_legend_right = u'''
    Восторженность,
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
    points_with_description = extract_categories(json_section, 'Шкала M', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала Q2
    Самостоятельность
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
    points_with_description = extract_categories(json_section, 'Шкала Q2', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

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
    Настойчивость,
    Дисциплина, Долг
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
    points_with_description = extract_categories(json_section, 'Шкала G', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

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
    Сильная воля, Точность
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
    points_with_description = extract_categories(json_section, 'Шкала Q3', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    pdf.set_font("RalewayLight", "", 9)
    vert_text_y = 252
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
    Консерватизм, 
    Неприятие перемен
        '''
        scale_legend_right = u'''
    Критичность, Анализ информации,
    Оптимизация работы 
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
    points_with_description = extract_categories(json_section, 'Шкала Q1', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

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
    points_with_description = extract_categories(json_section, 'Шкала L', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

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
    points_with_description = extract_categories(json_section, 'Шкала H', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    if lang == 'ru':
        scale_name = u'''
    Шкала E
    Независимость
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
    points_with_description = extract_categories(json_section, 'Шкала E', lang)
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    insert_page_number(pdf)


def draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points, points_description):
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

    draw_scale(pdf, x+3, y-7, 70, 10, points, 'media/images/kettel_page3.png')

    x += 24
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(50, 3, scale_legend_right, align='R')
