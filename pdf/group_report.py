import os
import textwrap
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Tuple

from PIL import ImageColor
from fpdf import XPos, YPos
from fpdf.enums import Align

from pdf.report_sections_configuration import (
    CATTELL_CATEGORIES,
    COPING_CATEGORIES_V1,
    BOYKO_CATEGORIES_V1,
    VALUES_CATEGORIES_V1,
)
from pdf.single_report import SingleReportData
from pdf.translations import TRANSLATIONS_DICT
from pdf.zetic_group_pdf import (
    ZeticGroupPDF,
    SquareId,
    GroupReportData,
    GroupData,
    ParticipantData,
)
from pdf.zetic_pdf import ZeticPDF, BLOCK_R, BLOCK_G, BLOCK_B, PDF_MODULE_BASE_DIR


class GroupReport:
    _pdf: ZeticGroupPDF
    data: GroupReportData

    def __init__(self):
        self._group_data_by_id = None
        self._pdf = ZeticGroupPDF(orientation="P", unit="mm", format="A4")

    def generate_pdf(self, data: GroupReportData) -> bytes:
        self.data = data

        self._group_data_by_id = {group.id: group for group in data.group_data.values()}
        self._pdf.add_fonts()
        self._add_title_page(data.project_name, data.lang)
        self.add_description(data.lang)
        self._add_participants(data.lang)

        self._add_group_profile(data.lang)
        self._add_group_cattell(data.lang)
        self._add_group_coping(data.lang)
        self._add_group_boyko(data.lang)
        self._add_group_values(data.lang)

        return self._pdf.output()
        pass

    def _add_title_page(self, project_name, lang):
        pdf = self._pdf

        pdf.add_page()
        pdf.image(
            os.path.join(PDF_MODULE_BASE_DIR, "images", "title_page.png"),
            x=0,
            y=0,
            w=210,
        )

        pdf.set_xy(20, 150)
        pdf.set_title_font(18)
        pdf.cell(0, 0, txt=TRANSLATIONS_DICT.get_translation("Team Report", lang))

        pdf.set_xy(20, 170)
        pdf.set_label_font(12)
        label = TRANSLATIONS_DICT.get_translation("Project", lang)
        pdf.cell(20, txt=label)

        if lang == "en":
            pdf.set_x(pdf.get_x() + 2)

        pdf.set_title_font(12)
        pdf.write(txt=project_name)

        pdf.set_xy(20, 180)
        pdf.set_title_font(12)
        pdf.cell(0, txt=TRANSLATIONS_DICT.get_translation("zetic", lang))

    pass

    def add_description(self, lang: str):
        pdf = self._pdf
        pdf.add_page()
        self._insert_page_number(pdf)

        page_header = TRANSLATIONS_DICT.get_translation(
            "Расшифровка командных ролей на основе модели Исхака Адизеса", lang
        )
        self._add_page_header(page_header)

        text = TRANSLATIONS_DICT.get_translation("group_report_description", lang)
        pdf.set_text_font(9)
        pdf.multi_cell(0, 4, text)
        pdf.set_xy(pdf.l_margin, pdf.get_y() + 5)

        self._add_description_section(
            "Производитель Описание", "Производитель Подробнее", lang
        )
        pdf.set_y(pdf.get_y() + 5)
        self._add_description_section(
            "Предприниматель Описание",
            "Предприниматель Подробнее",
            lang,
        )
        pdf.set_y(pdf.get_y() + 5)
        self._add_description_section(
            "Администратор Описание", "Администратор Подробнее", lang
        )
        pdf.set_y(pdf.get_y() + 5)
        self._add_description_section(
            "Интегратор Описание", "Интегратор Подробнее", lang
        )

        pass

    def _add_description_section(self, text, description, lang):
        pdf = self._pdf
        pdf.set_text_font(9)

        text = TRANSLATIONS_DICT.get_translation(text, lang)
        text_description = TRANSLATIONS_DICT.get_translation(description, lang)

        # calculate possible height of texts
        height_left = pdf.h - pdf.get_y() - pdf.b_margin
        pdf.set_x(pdf.l_margin)
        text_lines = pdf.multi_cell(0, h=4, txt=text, split_only=True)
        pdf.set_x(pdf.l_margin + 5)
        description_lines = pdf.multi_cell(
            0, h=4, txt=text_description, split_only=True, markdown=True
        )
        text_height = len(text_lines) * 4
        description_height = len(description_lines) * 4
        padding = 2
        height_to_consume = text_height + description_height + padding

        if height_left < height_to_consume:
            pdf.add_page()
            pdf.set_y(pdf.t_margin)
            self._insert_page_number(pdf)
        # end of page check

        pdf.set_x(pdf.l_margin)
        pdf.set_text_font(9)
        pdf.multi_cell(
            0,
            4,
            txt=text,
            markdown=True,
        )

        pdf.set_xy(pdf.l_margin + 5, pdf.get_y() + padding)
        pdf.set_text_font(9)
        lines = pdf.multi_cell(
            0, 4, text_description, align=Align.L, split_only=True, markdown=True
        )
        height_left = pdf.h - pdf.get_y() - pdf.b_margin
        lines_height = len(lines) * 4
        if height_left < lines_height:
            pdf.add_page()
            pdf.set_y(pdf.t_margin)
            self._insert_page_number(pdf)

        pdf.multi_cell(0, 4, text_description, align=Align.L, markdown=True)
        pass

    def _add_page_header(self, header_text):
        pdf = self._pdf
        pdf.set_label_font(10)
        pdf.cell(
            0,
            0,
            header_text,
        )

        # draw underline
        prev_color = pdf.draw_color
        pdf.set_draw_color(0, 0, 0)
        line_padding = 2
        pdf.line(
            pdf.l_margin, pdf.get_y() + line_padding, pdf.w, pdf.get_y() + line_padding
        )
        pdf.set_y(pdf.get_y() + 5)
        pdf.set_draw_color(prev_color.r * 255, prev_color.g * 255, prev_color.b * 255)
        pass

    @staticmethod
    def _insert_page_number(pdf: ZeticPDF):
        prev = pdf.auto_page_break
        pdf.set_auto_page_break(False)
        pdf.set_fill_color(BLOCK_R, BLOCK_G, BLOCK_B)
        pdf.set_draw_color(BLOCK_R, BLOCK_G, BLOCK_B)
        rect_width = 20
        rect_height = 6
        pdf.rect(
            pdf.w - pdf.r_margin - 3,
            pdf.h - pdf.t_margin,
            rect_width,
            rect_height,
            "FD",
        )

        pdf.set_text_color(0, 0, 0)
        pdf.set_text_font(10)
        pdf.set_xy(pdf.w - pdf.r_margin, pdf.h - pdf.t_margin + 3)
        pdf.cell(0, 0, txt=str(pdf.page_no()))
        pdf.set_xy(pdf.l_margin, pdf.t_margin)
        pdf.set_auto_page_break(prev)

    def _add_participants(self, lang: str):
        pdf = self._pdf
        data = self.data
        pdf.add_page()
        self._insert_page_number(pdf)

        self._add_page_header(
            TRANSLATIONS_DICT.get_translation("Состав участников исследования", lang)
        )

        participants_by_group = defaultdict(list)
        for participant in data.participant_data.values():
            participants_by_group[participant.group_id].append(participant)

        groups_by_name = sorted(
            self.data.group_data.values(),
            key=lambda x: len(participants_by_group[x.id]),
        )
        cols = 3
        current_col = 0
        current_y = pdf.get_y()
        max_y = 0
        for group in groups_by_name:
            self._add_group_section(group, participants_by_group[group.id])
            max_y = max(max_y, pdf.get_y())
            pdf.set_y(current_y)
            current_col += 1
            if current_col == cols:
                current_col = 0
                pdf.set_y(max_y + 2)
                current_y = pdf.get_y()
                max_y = 0

            pdf.set_x(
                pdf.l_margin
                + (pdf.w - pdf.l_margin - pdf.r_margin) / cols * current_col
            )

        pass

    def _add_group_section(self, group: GroupData, participants: List[ParticipantData]):
        pdf = self._pdf

        start_x = pdf.get_x()

        pdf.set_label_font(10)
        color = ImageColor.getrgb(group.color)
        pdf.set_text_color(*color)
        # draw circle
        pdf.set_fill_color(*color)
        pdf.set_draw_color(*color)
        pdf.circle(
            pdf.get_x(),
            pdf.get_y(),
            pdf.font_size,
            "FD",
        )

        pdf.set_x(start_x + pdf.font_size)
        pdf.cell(txt=group.name)
        pdf.set_y(pdf.get_y() + 4)
        pdf.set_text_font(8)
        pdf.set_text_color(0, 0, 0)
        pdf.set_x(start_x + 5)
        for participant in participants:
            pdf.set_font(style="")
            if participant.burnout:
                pdf.set_draw_color(241, 151, 15)
                pdf.set_fill_color(241, 151, 15)
                pdf.circle(
                    x=pdf.get_x() - 2,
                    y=pdf.get_y() + 0.3,
                    r=2,
                    style="FD",
                )
            if participant.crown:
                name_width = pdf.get_string_width(participant.name)
                pdf.image(
                    name=participant.cron_image,
                    x=pdf.get_x() + name_width + 1,
                    y=pdf.get_y() - pdf.font_size * 0.6,
                    w=3,
                )
                pdf.set_font(style="B")

            pdf.cell(txt=participant.name, new_x=XPos.LEFT, new_y=YPos.NEXT)
        pass

    def _add_group_profile(self, lang):
        pdf = self._pdf
        data = self.data
        pdf.add_page()
        self._insert_page_number(pdf)
        self._add_page_header("Командный профиль: распределение внимания в группе")

        pdf.set_y(pdf.get_y() + 5)
        base_y = pdf.get_y()
        pdf.draw_group_profile_squares()

        participant_colors: Dict[int, Tuple[int, int, int]] = {
            key: value
            for key, value in map(
                lambda participant: (
                    participant.id,
                    ImageColor.getrgb(
                        self._group_data_by_id[participant.group_id].color
                    ),
                ),
                data.participant_data.values(),
            )
        }
        participant_by_id = {
            participant.id: participant
            for participant in data.participant_data.values()
        }

        for square in data.square_results:
            results = data.square_results[square]
            # print(f"Square {square} results: {results}")
            pdf.draw_group_profile_square(
                square,
                results,
                base_y,
                color=participant_colors,
                participant_data=participant_by_id,
            )

        # draw legend
        # groups inline + crown image + burnout border
        # magic numbers
        height = pdf.w - pdf.l_margin - pdf.r_margin + 15
        pdf.set_y(pdf.t_margin + height)
        for group in data.group_data:
            group_data = data.group_data[group]
            pdf.set_fill_color(*ImageColor.getrgb(group_data.color))
            pdf.set_draw_color(*ImageColor.getrgb(group_data.color))
            pdf.circle(
                x=pdf.get_x(),
                y=pdf.get_y(),
                r=pdf.font_size,
                style="FD",
            )
            pdf.set_x(pdf.get_x() + pdf.font_size)
            pdf.cell(txt=group_data.name, new_x=XPos.RIGHT, new_y=YPos.TOP)
            pdf.set_x(pdf.get_x() + pdf.font_size)

        pdf.set_y(pdf.get_y() + 5)

        pass

    def _add_group_cattell(self, lang):
        pdf = self._pdf
        data = self.data

        pdf.set_text_font(9)
        # sections = [
        #     "Emotional stability",
        #     "Team resilience",
        #     "Stability of the results",
        #     "Resilience to change",
        # ]

        data_by_section: Dict[str, List[Tuple[int, ParticipantData]]] = defaultdict(
            list
        )
        for email in data.cattell_data:
            participant = data.participant_data[email]
            section_data = data.cattell_data[email]
            for section, value in section_data.data.items():
                data_by_section[section].append((value, participant))

        sections = CATTELL_CATEGORIES
        for section in sections:
            pdf.add_page(orientation="L")
            self._insert_page_number(pdf)
            self._add_page_header("Базовые черты личности: групповые результаты")

            section_label = TRANSLATIONS_DICT.get_translation(section, lang)
            pdf.draw_section_header(section_label)
            categories = CATTELL_CATEGORIES[section]
            pdf.set_y(pdf.get_y() + 2)

            # category format expected 1_1
            for category in categories:
                category_label = TRANSLATIONS_DICT.get_translation(category, lang)
                category_description = TRANSLATIONS_DICT.get_translation(
                    f"{category}_group_desc", lang
                )
                line_width = 46
                start_x = pdf.get_x()
                start_y = pdf.get_y()
                arrow_width = (
                    pdf.w - line_width - pdf.l_margin - pdf.r_margin - pdf.l_margin
                )
                pdf.draw_category_header_and_arrow(
                    category_label,
                    category_description,
                    arrow_color=(34, 170, 245),
                    line_width=line_width,
                    arrow_width=arrow_width,
                )

                section_data = data_by_section[category]
                section_data.sort(key=lambda x: x[0])
                count_per_score = defaultdict(int)
                participant_per_score = defaultdict(list)
                for score, participant in section_data:
                    count_per_score[score] += 1
                    participant_per_score[score].append(participant)
                    pass

                pdf.set_medium_font(9)
                rows = pdf.multi_cell(split_only=True, txt=category_label, w=line_width)
                # magic number 14 = 140/11 - width of arrow
                score_width = arrow_width / 11
                start_x += line_width
                for score in range(11):
                    pdf.set_xy(
                        start_x + score * score_width + 1,
                        start_y + len(rows) * 4 + 1,
                    )
                    participants = participant_per_score[score]
                    per_group = defaultdict(list)
                    for participant in participants:
                        group = self._group_data_by_id[participant.group_id]
                        per_group[group.id].append(
                            (participant.email, participant.burnout, participant.crown)
                        )
                        pass

                    # sort per_group by len and print in order
                    per_group = sorted(
                        per_group.items(), key=lambda x: len(x[1]), reverse=True
                    )
                    max_per_group = 1.0
                    if per_group:
                        max_per_group = float(len(per_group[0][1]))

                    v_padding = 3
                    padding = 1
                    n_per_line = 7
                    text_width = score_width / n_per_line - padding
                    score_start_x = start_x + score * score_width + 1
                    pdf.set_x(score_start_x + padding)
                    for group_id, group_data in per_group:
                        group = self._group_data_by_id[group_id]
                        # calc width based on max_per_group
                        for participant_id, burnout, crown in group_data:
                            participant = data.participant_data[participant_id]

                            if int(pdf.x + text_width) > int(start_x + score_width):
                                pdf.set_xy(
                                    score_start_x + padding,
                                    pdf.y + text_width + v_padding,
                                )

                            pdf.draw_participant_circle(
                                participant=participant,
                                x=pdf.x,
                                y=pdf.y,
                                color=ImageColor.getrgb(group.color),
                                w=2,
                            )
                            pdf.set_x(pdf.get_x() + padding)

                        # width = score_width * (current_len / max_per_group)
                        # pdf.cell(
                        #     txt=f"{current_len}",
                        #     h=4.0,
                        #     w=width,
                        #     new_x=XPos.LEFT,
                        #     new_y=YPos.NEXT,
                        #     border=0,
                        #     fill=True,
                        # )
                        # font_size * 2 for borders
                        pdf.set_xy(pdf.x, pdf.y)
                    pass
                pdf.set_y(pdf.get_y() + 2)

            # pdf.set_y(pdf.get_y() + 4)
        pass

    def _add_group_coping(self, lang):
        pdf = self._pdf
        data = self.data
        pdf.add_page()
        self._insert_page_number(pdf)
        self._add_page_header("Реакция на стресс: групповые результаты")

        scales = COPING_CATEGORIES_V1
        for scale in scales:
            scale_label = TRANSLATIONS_DICT.get_translation(scale, lang)
            pdf.draw_section_header(scale_label)

            categories = COPING_CATEGORIES_V1[scale]
            pdf.set_y(pdf.get_y() + 2)
            for category in categories:
                category_label = TRANSLATIONS_DICT.get_translation(category, lang)
                category_desc = TRANSLATIONS_DICT.get_translation(
                    f"{category}_group_desc", lang
                )
                pdf.draw_category_header_and_arrow(
                    category_label, category_desc, arrow_color=(107, 196, 38)
                )

                pdf.set_y(pdf.get_y() + 5)

            pdf.set_y(pdf.get_y() + 5)
        pass

    def _add_group_boyko(self, lang):
        pdf = self._pdf
        data = self.data
        pdf.add_page()
        self._insert_page_number(pdf)
        self._add_page_header("Интенсивность выгорания: групповые результаты")

        scales = BOYKO_CATEGORIES_V1
        for scale in scales:
            scale_label = TRANSLATIONS_DICT.get_translation(scale, lang)
            pdf.draw_section_header(scale_label)

            categories = BOYKO_CATEGORIES_V1[scale]
            pdf.set_y(pdf.get_y() + 2)
            for category in categories:
                category_label = TRANSLATIONS_DICT.get_translation(category, lang)
                category_desc = TRANSLATIONS_DICT.get_translation(
                    f"{category}_group_desc", lang
                )
                pdf.draw_category_header_and_arrow(
                    category_label, category_desc, arrow_color=(255, 168, 29)
                )

                pdf.set_y(pdf.get_y() + 5)

            pdf.set_y(pdf.get_y() + 5)
        pass

    def _add_group_values(self, lang):
        pdf = self._pdf
        data = self.data
        pdf.add_page()
        self._insert_page_number(pdf)
        self._add_page_header("Жизненные ценности: групповые результаты")

        scales = VALUES_CATEGORIES_V1
        for scale in scales:
            scale_label = TRANSLATIONS_DICT.get_translation(scale, lang)
            pdf.draw_section_header(scale_label)

            categories = VALUES_CATEGORIES_V1[scale]
            pdf.set_y(pdf.get_y() + 2)
            for category in categories:
                category_label = TRANSLATIONS_DICT.get_translation(category, lang)
                category_desc = TRANSLATIONS_DICT.get_translation(
                    f"{category}_group_desc", lang
                )
                pdf.draw_category_header_and_arrow(
                    category_label, category_desc, arrow_color=(248, 216, 31)
                )

                pdf.set_y(pdf.get_y() + 5)

            pdf.set_y(pdf.get_y() + 5)
        pass
