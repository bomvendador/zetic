from pdf.draw import draw_scale, insert_page_number
from pdf.extract_data import extract_categories


def page3(pdf, json_section, lang, participant_info):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    if lang == "ru":
        pdf.cell(0, 0, "Базовые черты личности")
    else:
        pdf.cell(0, 0, "Section K")

    y = y + 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)

    vert_text_y = 63
    if lang == "ru":
        with pdf.rotation(90, 12, vert_text_y + 1):
            pdf.text(0, vert_text_y + 1, "Эмоциональная устойчивость")
    else:
        with pdf.rotation(90, 12, vert_text_y - 7):
            pdf.text(0, vert_text_y - 7, "Emotional stability")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(15, vert_text_y - 33, 15, vert_text_y + 14)
    if lang == "ru":
        text = (
            "Приведенные ниже результаты исследования отражают фундаментальные черты личности, определяющие стиль "
            "деятельности и взаимоотношения с окружением. Обнаружив эти черты, Вы можете осознанно усиливать или ослаблять их"
        )
    else:
        text = (
            "The scores reflect the fundamental personality traits that determine business performance and relationship "
            "attitude. By discovering these traits, you can consciously strengthen or weaken them, increasing your effectiveness."
        )

    pdf.multi_cell(0, 4, text, align="J")

    y += 10
    x += 3

    if lang == "ru":
        scale_name = """
    Шкала С
    Эмоциональная
    стабильность
        """
        scale_legend_left = """
    Следование эмоциям,
    Утомляемость
        """
        scale_legend_right = """
        Стабильность, Зрелость,
        Работоспособность
        """
    else:
        scale_name = """
    Scale C
    Emotional
    stability
        """
        scale_legend_left = """
    Affection by feelings,
    Fatigue, Irritableness
        """
        scale_legend_right = """
        Stability, Maturity,
        Workability
        """
    points_with_description = extract_categories(
        json_section, "1_1", lang, participant_info
    )
    # points_with_description = extract_categories(json_section, 'Шкала C', lang)
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала O
    Тревожность        """
        scale_legend_left = """
    Безмятежность,
    Энергичность
        """
        scale_legend_right = """
    Чувство вины, Тревожность,
    Впечатлительность
        """
    else:
        scale_name = """
    Scale O
    Apprehension
        """
        scale_legend_left = """
    Self-assureness, free of guilt,
    Untroubleness, Energy
        """
        scale_legend_right = """
    Self-blaming, Anxiety,
    Impressionability
        """
    points_with_description = extract_categories(
        json_section, "1_2", lang, participant_info
    )
    # points_with_description = extract_categories(json_section, 'Шкала O', lang)
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала Q4
    Внутреннее
    напряжение
        """
        scale_legend_left = """
    Расслабленность,
    Низкая мотивация
        """
        scale_legend_right = """
    Собранность, Напряженность,
    Раздражительность
        """
    else:
        scale_name = """
    Scale Q4
    Tension
        """
        scale_legend_left = """
    Relaxation, Tranquility,
    Low drive,  Composure
        """
        scale_legend_right = """
    Tension, Overthought,
    High drive, Irritability
        """
    points_with_description = extract_categories(
        json_section, "1_3", lang, participant_info
    )
    # points_with_description = extract_categories(json_section, 'Шкала Q4', lang, participant_info)
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    pdf.set_font("RalewayLight", "", 9)
    vert_text_y = 117
    if lang == "ru":
        with pdf.rotation(90, 12, vert_text_y + 1):
            pdf.text(0, vert_text_y + 1, "Командная устойчивость")
    else:
        with pdf.rotation(90, 12, vert_text_y - 6):
            pdf.text(0, vert_text_y - 6, "Team resilience")
    pdf.set_draw_color(0, 0, 0)
    pdf.line(15, vert_text_y - 36, 15, vert_text_y + 26)

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала F
    Импульсивность
        """
        scale_legend_left = """
    Молчаливость,
    Расчетливость
        """
        scale_legend_right = """
    Беззаботность, Беспечность,
    Экспрессивность
        """
    else:
        scale_name = """
    Scale F
    Impulsiveness
        """
        scale_legend_left = """
    Taciturnity, Prudence,
    Temperance
        """
        scale_legend_right = """
    Carelessness, Enthusiasm,
    Expressiveness
        """
    points_with_description = extract_categories(
        json_section, "1_4", lang, participant_info
    )
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала N
    Дипломатичность
        """
        scale_legend_left = """
    Прямолинейность,
    Четкость
        """
        scale_legend_right = """
    Влияние,
    Хитрость
        """
    else:
        scale_name = """
    Scale N
    Diplomacy
        """
        scale_legend_left = """
    Straightforwardness,
    Tactlessness, Genuiness
        """
        scale_legend_right = """
    Social awareness,
    Influence, Cunning
        """
    points_with_description = extract_categories(
        json_section, "1_5", lang, participant_info
    )
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала I
    Восприятие
        """
        scale_legend_left = """
    Рассудительность, Циничность,
    Ответственность
        """
        scale_legend_right = """
    Эмпатичность,
    Интуитивность
        """
    else:
        scale_name = """
    Scale I
    Sensitivity
        """
        scale_legend_left = """
    Cynicism, Tough-mind,
    Self-reliance
        """
        scale_legend_right = """
    Tender-mind, Empathy,
    Intuitiveness
        """
    points_with_description = extract_categories(
        json_section, "1_6", lang, participant_info
    )
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала A
    Открытость
        """
        scale_legend_left = """
    Замкнутость, Холодность,
    Безучастность, Строгость
        """
        scale_legend_right = """
    Общительность,
    Открытость
        """
    else:
        scale_name = """
    Scale A
    Warmth
        """
        scale_legend_left = """
    Reserveness, Coldness,
    Indifference, Severity
        """
        scale_legend_right = """
    Sociability, Warmth,
    Kindness, Openness
        """
    points_with_description = extract_categories(
        json_section, "1_7", lang, participant_info
    )
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    pdf.set_font("RalewayLight", "", 9)
    vert_text_y = 185
    if lang == "ru":
        with pdf.rotation(90, 12, vert_text_y):
            pdf.text(0, vert_text_y, "Устойчивость результата")
    else:
        with pdf.rotation(90, 12, vert_text_y):
            pdf.text(0, vert_text_y, "Stability of the results")
    pdf.set_draw_color(0, 0, 0)
    pdf.line(15, vert_text_y - 36, 15, vert_text_y + 26)

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала M
    Восторженность
        """
        scale_legend_left = """
    Практичность,
    Реалистичность, Прозаичность
        """
        scale_legend_right = """
    Восторженность,
    Воображение
        """
    else:
        scale_name = """
    Scale M
    Abstractedness
        """
        scale_legend_left = """
    Practicality, Integrity,
    Realism, Grounding
        """
        scale_legend_right = """
    Abstracteness, Imagination,
    Idea-oriention
        """
    points_with_description = extract_categories(
        json_section, "1_8", lang, participant_info
    )
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала Q2
    Самостоятельность
        """
        scale_legend_left = """
    Зависимость от группы,
    Разделение ответственности
        """
        scale_legend_right = """
    Самостоятельность,
    Независимость
        """
    else:
        scale_name = """
    Scale Q2
    Self-reliance
        """
        scale_legend_left = """
    Group-dependence,
    Division of responsibility
        """
        scale_legend_right = """
    Independence,
    Resourcefulness
        """
    points_with_description = extract_categories(
        json_section, "1_9", lang, participant_info
    )
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала G
    Ответственность
        """
        scale_legend_left = """
    Непостоянство, Ненадежность
        """
        scale_legend_right = """
    Настойчивость,
    Дисциплина, Долг
        """
    else:
        scale_name = """
    Scale G
    Rule-consciousness
        """
        scale_legend_left = """
    Volatility, Insecurity,
    Expediency
        """
        scale_legend_right = """
    Perseverance, Conformity
    Discipline, Obligation
        """
    points_with_description = extract_categories(
        json_section, "1_10", lang, participant_info
    )
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала Q3
    Самоконтроль
        """
        scale_legend_left = """
    Конфликтность,
    Невнимательность
        """
        scale_legend_right = """
    Самоконтроль,
    Сильная воля, Точность
        """
    else:
        scale_name = """
    Scale Q3
    Self-control
        """
        scale_legend_left = """
    Self-conflict, Disorder Tolerance,
    Inattention
        """
        scale_legend_right = """
    Self control
    Strong will, Accuracy
        """
    points_with_description = extract_categories(
        json_section, "1_11", lang, participant_info
    )
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    pdf.set_font("RalewayLight", "", 9)
    vert_text_y = 252
    if lang == "ru":
        with pdf.rotation(90, 12, vert_text_y + 2):
            pdf.text(0, vert_text_y + 2, "Устойчивость в изменениях")
    else:
        with pdf.rotation(90, 12, vert_text_y):
            pdf.text(0, vert_text_y, "Resilience to change")
    pdf.set_draw_color(0, 0, 0)
    pdf.line(15, vert_text_y - 36, 15, vert_text_y + 26)

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала Q1
    Критичность
        """
        scale_legend_left = """
    Консерватизм,
    Принятие быстрых решений
        """
        scale_legend_right = """
    Экспериментирование,
    Анализ информации
        """
    else:
        scale_name = """
    Scale Q1
    Critical thinking
        """
        scale_legend_left = """
    Judgement-orientation
    Change intolerance, Conservatism
        """
        scale_legend_right = """
    Information analysis, Criticality
    Work optimization
        """
    points_with_description = extract_categories(
        json_section, "1_12", lang, participant_info
    )
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала L
    Осторожность
        """
        scale_legend_left = """
    Доверчивость, Терпимость,
    Откровенность
        """
        scale_legend_right = """
    Подозрительность,
    Осторожность
        """
    else:
        scale_name = """
    Scale L
    Vigilance
        """
        scale_legend_left = """
    Confidence, Tolerance
    Frankness
        """
        scale_legend_right = """
    Suspicion
    Caution
        """
    points_with_description = extract_categories(
        json_section, "1_13", lang, participant_info
    )
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала H
    Смелость
        """
        scale_legend_left = """
    Робость, Деликатность
        """
        scale_legend_right = """
    Смелость, Авантюрность
        """
    else:
        scale_name = """
    Scale H
    Social boldness
        """
        scale_legend_left = """
    Timidity, Delicacy
        """
        scale_legend_right = """
    Courage, Boldness
    Adventurism
        """
    points_with_description = extract_categories(
        json_section, "1_14", lang, participant_info
    )
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    y += 17
    if lang == "ru":
        scale_name = """
    Шкала E
    Независимость
        """
        scale_legend_left = """
    Мягкость, Тактичность,
    Уступчивость
        """
        scale_legend_right = """
    Напористость, Властность,
    Самоуверенность
        """
    else:
        scale_name = """
    Scale E
    Dominance
        """
        scale_legend_left = """
    Softness, Tact
    Compliance
        """
        scale_legend_right = """
    Assertiveness, Dominance
    Self-confidence
        """
    points_with_description = extract_categories(
        json_section, "1_15", lang, participant_info
    )
    draw_scale_page3(
        pdf,
        x,
        y,
        scale_name,
        scale_legend_left,
        scale_legend_right,
        points_with_description["points"],
        points_with_description["point_description"],
    )

    insert_page_number(pdf)


def draw_scale_page3(
    pdf,
    x,
    y,
    scale_name,
    scale_legend_left,
    scale_legend_right,
    points,
    points_description,
):
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    pdf.multi_cell(0, 4, scale_name)
    pdf.set_xy(x + 110, y + 2)
    pdf.cell(10, h=12, txt=str(points), ln=0, align="C")
    pdf.set_font("RalewayLight", "", 8)
    pdf.multi_cell(0, h=4, txt=points_description, align="L")

    y += 10
    x += 35
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(0, 3, scale_legend_left)

    draw_scale(pdf, x + 3, y - 7, 70, 10, points, "media/images/kettel_page3.png")

    x += 24
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(50, 3, scale_legend_right, align="R")
