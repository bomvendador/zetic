from pdf.draw import draw_full_scale, insert_page_number


def page4(pdf, json_section, lang, participant_info):
    scale_element_file = "media/images/kopingi_page4.png"
    pdf.set_auto_page_break(False)
    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == "ru":
        pdf.cell(0, 0, "Поведение в стрессе и неопределенности")
    else:
        pdf.cell(0, 0, "Section C")

    y += 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    if lang == "ru":
        text = (
            "Ниже приведены результаты исследования, отражающие наиболее типичные реакции и действия в ситуации стресса "
            "или высокой неопределенности. Изучив свои стратегии поведения, Вы можете изменить их, осознанно действовать "
            "иначе, повышая личную эффективность."
        )
    else:
        text = (
            "The following scores reflect the most typical reactions and actions under stressful situations or uncertainty. "
            "Having studied your behavioral strategies, you can change them, consciously act differently, increasing your "
            "personal effectiveness."
        )

    pdf.multi_cell(0, 4, text, align="J")

    y += 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == "ru":
        pdf.cell(
            0,
            0,
            "Стратегии, направленные на активный поиск выхода и преодоление сложностей",
        )
        scale_legend_left = """
    Слабо выражено
    """
        scale_legend_right = """
    Ярко выражено
    """

    else:
        pdf.cell(
            0, 0, "Strategies to actively find a way out and overcome difficulties"
        )
        scale_legend_left = """
    Weakly expressed
    """
        scale_legend_right = """
    Strongly expressed
    """

    y += 2

    pdf.set_xy(x + 37, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(0, 3, scale_legend_left)

    pdf.set_xy(x + 37 + 24, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(50, 3, scale_legend_right, align="R")
    if lang == "ru":
        scale_name = """Самообладание"""
    else:
        scale_name = """Response control"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "2_1",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 15
    if lang == "ru":
        scale_name = """Контроль над ситуацией"""
    else:
        scale_name = """Situation control"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "2_2",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 15
    if lang == "ru":
        scale_name = """Позитивная
самомотивация"""
    else:
        scale_name = """Positive
self-affirmation"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12 - 2,
        json_section,
        "2_3",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 15
    if lang == "ru":
        scale_name = """Снижение значения
стрессовой ситуации"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12 - 2,
            json_section,
            "2_4",
            scale_element_file,
            lang,
            participant_info,
        )

    else:
        scale_name = """Stress minimization"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12,
            json_section,
            "2_4",
            scale_element_file,
            lang,
            participant_info,
        )

    y += 15
    if lang == "ru":
        scale_name = """Самоутверждение"""
    else:
        scale_name = """Self-assertion"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "2_5",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 23
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == "ru":
        pdf.cell(
            0,
            0,
            "Стратегии, направленные на игнорирование проблемы и отказ искать выход из ситуации",
        )
    else:
        pdf.cell(
            0, 0, "Strategies for ignoring problems and avoiding solutions research"
        )

    y -= 2
    if lang == "ru":
        scale_name = """Отвлечение"""
    else:
        scale_name = """Distraction"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "2_6",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 15
    if lang == "ru":
        scale_name = """Бегство от стрессовой
ситуации"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12 - 2,
            json_section,
            "2_7",
            scale_element_file,
            lang,
            participant_info,
        )
    else:
        scale_name = """Escape"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12,
            json_section,
            "2_7",
            scale_element_file,
            lang,
            participant_info,
        )

    y += 15
    if lang == "ru":
        scale_name = """Антиципирующее
избегание"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12 - 2,
            json_section,
            "2_8",
            scale_element_file,
            lang,
            participant_info,
        )
    else:
        scale_name = """Avoidance"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12 - 2,
            json_section,
            "2_8",
            scale_element_file,
            lang,
            participant_info,
        )

    y += 15
    if lang == "ru":
        scale_name = """Замещение"""
    else:
        scale_name = """Substitution"""

    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "2_9",
        "media/images/kopingi_page4.png",
        lang,
        participant_info,
    )

    y += 15
    if lang == "ru":
        scale_name = """Поиск социальной
поддержки"""
    else:
        scale_name = """Need for
Social Support"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12 - 2,
        json_section,
        "2_10",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 23
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    if lang == "ru":
        pdf.cell(
            0,
            0,
            "Стратегии, провоцирующие дальнейшее нахождение в стрессе и усиление переживаний",
            scale_element_file,
        )
    else:
        pdf.cell(
            0,
            0,
            "Strategies leading to further stress and strengthening worries",
            scale_element_file,
        )

    y -= 2
    if lang == "ru":
        scale_name = """Жалость к себе"""
    else:
        scale_name = """Self-pity"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "2_11",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 15
    if lang == "ru":
        scale_name = """Социальная
замкнутость"""
    else:
        scale_name = """Social
withdrawal"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12 - 2,
        json_section,
        "2_12",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 15
    if lang == "ru":
        scale_name = """Самообвинение"""
    else:
        scale_name = """Self-blame"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "2_13",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 15
    if lang == "ru":
        scale_name = """«Заезженная
пластинка»"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12 - 2,
            json_section,
            "2_14",
            scale_element_file,
            lang,
            participant_info,
        )
    else:
        scale_name = """Rumination"""
        draw_full_scale(
            pdf,
            scale_name,
            x,
            y + 12,
            y + 12,
            json_section,
            "2_14",
            scale_element_file,
            lang,
            participant_info,
        )

    y += 15
    if lang == "ru":
        scale_name = """Самооправдание"""
    else:
        scale_name = """Denial of guilt"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "2_15",
        scale_element_file,
        lang,
        participant_info,
    )

    y += 15
    if lang == "ru":
        scale_name = """Агрессия"""
    else:
        scale_name = """Aggression"""
    draw_full_scale(
        pdf,
        scale_name,
        x,
        y + 12,
        y + 12,
        json_section,
        "2_16",
        scale_element_file,
        lang,
        participant_info,
    )

    insert_page_number(pdf)
