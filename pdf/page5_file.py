from pdf.draw import draw_full_scale, insert_page_number


def page5(pdf, json_section, lang, participant_info):
    scale_element_file = "media/images/boyko_page5.png"
    pdf.set_auto_page_break(False)

    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == "ru":
        pdf.cell(0, 0, "Факторы профессионального выгорания")
    else:
        pdf.cell(0, 0, "Section B")

    y += 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    if lang == "ru":
        text = (
            "Ниже приведено исследование механизмов эмоционального выгорания из-за последовательного снижения "
            "эмоционального ответа на ситуацию. Вы можете увидеть, какие факторы формируют каждую фазу выгорания и "
            "в какой точке Вы находитесь прямо сейчас."
        )
    else:
        text = (
            "The following scores describe the mechanisms of emotional burnout – a consistent decrease in emotional "
            "response to work situations. You can explore behavioral markers shaping burnout phase."
        )

    pdf.multi_cell(0, 4, text, align="J")

    vert_text_y = 73
    if lang == "ru":
        with pdf.rotation(90, 10, vert_text_y + 1):
            pdf.text(0, vert_text_y + 1, "Фаза 1. Напряжение")
    else:
        with pdf.rotation(90, 10, vert_text_y + 1):
            pdf.text(0, vert_text_y, "Phase 1. Tension")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(13, vert_text_y - 35, 13, vert_text_y + 31)

    y += 13
    x += 6
    if lang == "ru":
        scale_legend_left = """
    Слабо выражено
        """
        scale_legend_right = """
    Ярко выражено
        """
    else:
        scale_legend_left = """
    Weakly expressed
        """
        scale_legend_right = """
    Strongly expressed
        """

    pdf.set_xy(x + 37, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(0, 3, scale_legend_left)

    pdf.set_xy(x + 37 + 24, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(50, 3, scale_legend_right, align="R")

    if lang == "ru":
        scale_name = """Переживание"""
    else:
        scale_name = """Concern"""

    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "3_1",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Неудовлетворенность
собой"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12 - 2,
            json_section,
            "3_2",
            scale_element_file,
            lang,
            participant_info,
        )
    else:
        scale_name = """Self dissatisfaction"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12,
            json_section,
            "3_2",
            scale_element_file,
            lang,
            participant_info,
        )

    y += 20
    if lang == "ru":
        scale_name = """«Загнанность в
клетку»"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12 - 2,
            json_section,
            "3_3",
            scale_element_file,
            lang,
            participant_info,
        )
    else:
        scale_name = """Feeling trapped"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12,
            json_section,
            "3_3",
            scale_element_file,
            lang,
            participant_info,
        )

    y += 20
    if lang == "ru":
        scale_name = """Тревога"""
    else:
        scale_name = """Anxiety"""

    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "3_4",
        scale_element_file,
        lang,
        participant_info,
    )

    vert_text_y = 152
    if lang == "ru":
        with pdf.rotation(90, 10, vert_text_y + 1):
            pdf.text(0, vert_text_y + 1, "Фаза 2. Сопротивление")
    else:
        with pdf.rotation(90, 10, vert_text_y + 1):
            pdf.text(0, vert_text_y + 1, "Phase 2. Resistance")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(13, vert_text_y - 35, 13, vert_text_y + 31)

    y += 20
    if lang == "ru":
        scale_name = """Избирательное
реагирование"""
    else:
        scale_name = """Selective emotional
response"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12 - 2,
        json_section,
        "3_5",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Эмоциональная
защита"""
    else:
        scale_name = """Emotional
defense"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12 - 2,
        json_section,
        "3_6",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Экономия эмоций"""
    else:
        scale_name = """Emotional saving"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "3_7",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Эмпатическая
усталость"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12 - 2,
            json_section,
            "3_8",
            scale_element_file,
            lang,
            participant_info,
        )
    else:
        scale_name = """Empathic fatigue"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12,
            json_section,
            "3_8",
            scale_element_file,
            lang,
            participant_info,
        )

    vert_text_y = 232
    if lang == "ru":
        with pdf.rotation(90, 10, vert_text_y + 1):
            pdf.text(0, vert_text_y + 1, "Фаза 3. Истощение")
    else:
        with pdf.rotation(90, 10, vert_text_y):
            pdf.text(0, vert_text_y, "Phase 3. Exhaustion")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(13, vert_text_y - 35, 13, vert_text_y + 31)

    y += 20
    if lang == "ru":
        scale_name = """Эмоциональная
опустошенность"""
    else:
        scale_name = """Emotional
emptiness"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12 - 2,
        json_section,
        "3_9",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Эмоциональная
отстраненность"""
    else:
        scale_name = """Emotional
detachment"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12 - 2,
        json_section,
        "3_10",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Личностная
отстраненность"""
    else:
        scale_name = """Personal
detachment"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12 - 2,
        json_section,
        "3_11",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Психосоматика"""
    else:
        scale_name = """Physical discomfort"""

    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "3_12",
        scale_element_file,
        lang,
        participant_info,
    )

    insert_page_number(pdf)
