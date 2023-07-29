from pdf.draw import draw_full_scale, insert_page_number


def page6(pdf, json_section, lang, participant_info):
    scale_element_file = "media/images/values_page6.png"

    pdf.set_auto_page_break(False)

    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == "ru":
        pdf.cell(0, 0, "Ценности")
    else:
        pdf.cell(0, 0, "Section V")

    y += 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    if lang == "ru":
        text = (
            "Ниже приведено исследование жизненных ценностей — универсальных человеческих потребностей, определяющих "
            "выборы и предпочтения индивида, его жизненную стратегию."
        )
    else:
        text = (
            "The following scores reflect life values - fundamental human needs that determine personal choices "
            "life strategies."
        )

    pdf.multi_cell(0, 4, text, align="J")

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

    pdf.set_font("RalewayLight", "", 9)
    vert_text_y = 72
    if lang == "ru":
        with pdf.rotation(90, 10, vert_text_y + 13):
            pdf.text(0, vert_text_y + 13, "Создание гармонии")
    else:
        with pdf.rotation(90, 10, vert_text_y + 13):
            pdf.text(0, vert_text_y + 13, "Creating harmony")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(13, vert_text_y - 35, 13, vert_text_y + 52)
    if lang == "ru":
        scale_name = """Причастность"""
    else:
        scale_name = """Affiliation"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "4_1",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Традиционализм"""
    else:
        scale_name = """Conventionality"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "4_2",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Жажда
впечатлений"""
    else:
        scale_name = """Sensation
seeking"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12 - 2,
        json_section,
        "4_3",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Эстетичность"""
    else:
        scale_name = """Aesthetic"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "4_4",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Гедонизм"""
    else:
        scale_name = """Hedonism"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "4_5",
        scale_element_file,
        lang,
        participant_info,
    )

    pdf.set_font("RalewayLight", "", 9)
    vert_text_y = 172
    if lang == "ru":
        with pdf.rotation(90, 10, vert_text_y + 7):
            pdf.text(0, vert_text_y + 7, "Преодоление")
    else:
        with pdf.rotation(90, 10, vert_text_y + 12):
            pdf.text(0, vert_text_y + 12, "Overcoming resistance")

    pdf.set_draw_color(0, 0, 0)
    pdf.line(13, vert_text_y - 35, 13, vert_text_y + 52)

    y += 20
    if lang == "ru":
        scale_name = """Признание"""
    else:
        scale_name = """Recognition"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "4_6",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Достижения"""
    else:
        scale_name = """Achievement"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "4_7",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Коммерческий
подход"""
    else:
        scale_name = """Commercial
attitude"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12 - 2,
        json_section,
        "4_8",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Безопасность"""
    else:
        scale_name = """Safety"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "4_9",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 20
    if lang == "ru":
        scale_name = """Интеллект"""
    else:
        scale_name = """Curiosity"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "4_10",
        scale_element_file,
        lang,
        participant_info,
    )

    insert_page_number(pdf)
