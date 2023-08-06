import os
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
from pdf.zetic_pdf import ZeticPDF, BLOCK_R, BLOCK_G, BLOCK_B, PDF_MODULE_BASE_DIR


@dataclass
class GroupData:
    id: int
    name: str  # Unique Name, used as key
    color: str


@dataclass
class ParticipantData:
    id: int
    name: str
    email: str  # Unique Email, used as key
    group_id: int
    burnout: int = 0


@dataclass
class SquareResult:
    group_id: int
    participant_id: int
    single_report_data: SingleReportData

    @staticmethod
    def from_client_list(
        data: List[str],
        group_data: Dict[str, GroupData],
        participant_data: Dict[str, ParticipantData],
        single_report_data: SingleReportData,
    ):

        return SquareResult(
            single_report_data=single_report_data,
            group_id=group_data[data[4]].id,  # idx=4 - group_name, sent from client
            participant_id=participant_data[
                data[1]
            ].id,  # idx=1 - email, sent from client
        )
        pass


@dataclass
class GroupReportData:
    lang: str
    project_name: str

    group_data: Dict[str, GroupData]
    participant_data: Dict[str, ParticipantData]

    square_results: List[SquareResult]


def _draw_square(
    pdf,
    x: int,
    y: int,
    width: int,
    height: int,
    color: Tuple[int, int, int],
    label: str = None,
):
    pdf.set_draw_color(*color)
    pdf.set_fill_color(*color)
    pdf.rect(x, y, width, height, "FD")

    pdf.set_draw_color(255, 255, 255)
    pdf.set_fill_color(255, 255, 255)
    # белый вертикальный
    pdf.rect(
        x=x + width / 2 - 0.3,
        y=y,
        w=0.6,
        h=x + width * 2,
        style="FD",
    )
    # белый горизонтальный
    pdf.rect(
        x=x,
        y=y + width / 2 - 0.3,
        w=width,
        h=0.6,
        style="FD",
    )

    # square label
    pdf.set_label_font(10)
    pdf.set_text_color(0, 0, 0)
    # in the center
    center_x = x + width / 2
    center_y = y + height / 2
    label_with = pdf.get_string_width(label)
    rect_width = label_with + 10  # 5*2 padding
    rect_height = 10
    pdf.rect(
        center_x - rect_width / 2,
        center_y - rect_height / 2,
        rect_width,
        rect_height,
        "FD",
    )
    pdf.set_xy(x=center_x - rect_width / 2, y=center_y - rect_height / 2)
    pdf.cell(
        w=rect_width,
        h=rect_height,
        align=Align.C,
        txt=label,
    )
    pass


def _draw_group_profile_squares(pdf: ZeticPDF):
    start_x = pdf.get_x()
    start_y = pdf.get_y()
    width = (pdf.w - pdf.l_margin - pdf.r_margin) / 2

    _draw_square(pdf, start_x, start_y, width, width, (255, 240, 193), "Интеграторы")
    _draw_square(
        pdf, start_x + width, start_y, width, width, (253, 219, 246), "Предприниматели"
    )

    _draw_square(
        pdf,
        start_x,
        start_y + width,
        width,
        width,
        (217, 245, 251),
        "Администраторы",
    )
    # 4
    _draw_square(
        pdf,
        start_x + width,
        start_y + width,
        width,
        width,
        (226, 239, 218),
        "Производители",
    )

    pdf.set_text_font(8)
    pdf.text(start_x + width / 2 - 13, start_y - 2.5, "Фокус на процесс")
    pdf.text(start_x + width / 2 + width - 13.5, start_y - 2.5, "Фокус на результат")
    with pdf.rotation(90, pdf.l_margin - pdf.font_size, start_y + width / 2 + 10):
        pdf.text(0, start_y + width / 2 + 10, "Неструктурированный подход")
    with pdf.rotation(270, start_x + width * 2 + 3, start_y + width / 2 - 18):
        pdf.text(
            start_x + width * 2 + 3,
            start_y + width / 2 - 18,
            "Концептуальные решения",
        )
    with pdf.rotation(
        90, pdf.l_margin - pdf.font_size, start_y + width / 2 + 7 + width
    ):
        pdf.text(
            0,
            start_y + width / 2 + 7 + width,
            "Структурированный подход",
        )
    with pdf.rotation(
        270,
        start_x + width * 2 + 3,
        start_y + width / 2 - 15 + width,
    ):
        pdf.text(
            start_x + width * 2 + 3,
            start_y + width / 2 - 15 + width,
            "Локальные решения",
        )

    pdf.set_light_font(8)

    # pdf.text(start_x + width / 4 - 3, start_y + 4, 'ESFJ')
    # pdf.text(start_x + width / 4 - 13, start_y + 7, 'Массовик-затейник')
    pdf.text(start_x + width / 4 - 13, start_y + 4, "Массовик-затейник")

    # pdf.text(start_x + width * (3/4) - 3, start_y + 4, 'ENFJ')
    # pdf.text(start_x + width * (3/4) - 13, start_y + 7, 'Идеалист-харизматик')
    pdf.text(start_x + width * (3 / 4) - 12, start_y + 4, "Чуткий наставник")

    # pdf.text(start_x + width + width / 4 - 3, start_y + 4, 'ESTJ')
    # pdf.text(start_x + width + width / 4 - 14, start_y + 7, 'Контролер по жизни')
    pdf.text(start_x + width + width / 4 - 8, start_y + 4, "Контролер")

    # pdf.text(start_x + width + width * (3/4) - 3, start_y + 4, 'ENTJ')
    # pdf.text(start_x + width + width * (3/4) - 11, start_y + 7, 'Предприниматель')
    pdf.text(start_x + width + width * (3 / 4) - 5, start_y + 4, "Аналитик")

    # pdf.text(start_x + width / 4 - 3, start_y + width - 6 , 'ESFP')
    # pdf.text(start_x + width / 4 - 18.5, start_y + width - 3 , 'Спонтанный коммуникатор')
    pdf.text(
        start_x + width / 4 - 9,
        start_y + width - 3,
        "Развлекатель",
    )

    # pdf.text(start_x + width * (3/4) - 3, start_y + width - 6 , 'ENFP')
    # pdf.text(start_x + width * (3/4) - 7, start_y + width - 3 , 'Инициатор')
    pdf.text(
        start_x + width * (3 / 4) - 7,
        start_y + width - 3,
        "Мотиватор",
    )

    # pdf.text(start_x + width + width / 4 - 3, start_y + width - 6 , 'ESTP')
    # pdf.text(start_x + width + width / 4 - 10, start_y + width - 3 , 'Ультра-реалист')
    pdf.text(
        start_x + width + width / 4 - 12,
        start_y + width - 3,
        "Искатель ресурсов",
    )

    # pdf.text(start_x + width + width * (3/4) - 3, start_y + width - 6 , 'ENTP')
    pdf.text(
        start_x + width + width * (3 / 4) - 9,
        start_y + width - 3,
        "Изобретатель",
    )

    # pdf.text(start_x + width / 4 - 3, start_y + width + 4 , 'ISFJ')
    # pdf.text(start_x + width / 4 - 7, start_y + width + 7 , 'Хранитель')
    pdf.text(start_x + width / 4 - 7, start_y + width + 4, "Хранитель")

    # pdf.text(start_x + width * (3/4) - 3, start_y + width + 4 , 'INFJ')
    # pdf.text(start_x + width * (3/4) - 9, start_y + width + 7 , 'Вдохновитель')
    pdf.text(
        start_x + width * (3 / 4) - 9,
        start_y + width + 4,
        "Вдохновитель",
    )

    # pdf.text(start_x + width + width / 4 - 3, start_y + width + 4 , 'ISTJ')
    # pdf.text(start_x + width + width / 4 - 8, start_y + width + 7 , 'Организатор')
    pdf.text(
        start_x + width + width / 4 - 6,
        start_y + width + 4,
        "Организатор",
    )

    # pdf.text(start_x + width + width * (3/4) - 3, start_y + width + 4 , 'INTJ')
    # pdf.text(start_x + width + width * (3/4) - 14, start_y + width + 7 , 'Любитель улучшений')
    pdf.text(
        start_x + width + width * (3 / 4) - 14,
        start_y + width + 4,
        "Любитель улучшений",
    )

    # pdf.text(start_x + width / 4 - 3, start_y + width + width - 6 , 'ISFP')
    # pdf.text(start_x + width / 4 - 7, start_y + width + width - 3 , 'Посредник')
    pdf.text(
        start_x + width / 4 - 5,
        start_y + width + width - 3,
        "Опекун",
    )

    # pdf.text(start_x + width * (3/4) - 3, start_y + width + width - 6 , 'INFP')
    pdf.text(
        start_x + width * (3 / 4) - 16,
        start_y + width + width - 3,
        "Благородный служитель",
    )

    # pdf.text(start_x + width + width / 4 - 3, start_y + width + width - 6 , 'ISTP')
    # pdf.text(start_x + width + width / 4 - 12, start_y + width + width - 3 , 'Экспериментатор')
    pdf.text(
        start_x + width + width / 4 - 9,
        start_y + width + width - 3,
        "Исполнитель",
    )

    # pdf.text(start_x + width + width * (3/4) - 3, start_y + width + width - 6 , 'INTP')
    pdf.text(
        start_x + width + width * (3 / 4) - 12,
        start_y + width + width - 3,
        "Решатель проблем",
    )

    pdf.set_line_width(0.5)
    pdf.set_draw_color(240)

    pass


def _draw_section_header(pdf: ZeticPDF, text: str):
    pdf.set_fill_color(230, 230, 227)
    pdf.set_draw_color(230, 230, 227)
    rect_width = 210
    rect_height = 8
    pdf.rect(pdf.x, pdf.y, rect_width, rect_height, "FD")
    pdf.set_text_color(118, 134, 146)
    pdf.cell(h=rect_height, txt=text, new_y=YPos.NEXT, new_x=XPos.LEFT)


class GroupReport:
    _pdf: ZeticPDF
    data: GroupReportData

    def __init__(self):
        self._pdf = ZeticPDF(orientation="P", unit="mm", format="A4")

    def generate_pdf(self, data: GroupReportData) -> bytes:
        self.data = data
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
        pdf.rect(197, 287, rect_width, rect_height, "FD")

        pdf.set_xy(200, 290)
        pdf.set_text_color(0, 0, 0)
        pdf.set_text_font(10)
        pdf.set_xy(200, 290)
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
                pdf.set_y(max_y + 5)
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
        pdf.set_y(pdf.get_y() + 5)
        pdf.set_text_font(9)
        pdf.set_text_color(0, 0, 0)
        pdf.set_x(start_x + 5)
        for participant in participants:
            if participant.burnout:
                pdf.set_draw_color(241, 151, 15)
                pdf.set_fill_color(241, 151, 15)
                pdf.circle(
                    x=pdf.get_x() - 2,
                    y=pdf.get_y() + 0.3,
                    r=2,
                    style="FD",
                )
            pdf.cell(txt=participant.name, new_x=XPos.LEFT, new_y=YPos.NEXT)
        pass

    def _add_group_profile(self, lang):
        pdf = self._pdf
        data = self.data
        pdf.add_page()
        self._insert_page_number(pdf)
        self._add_page_header("Командный профиль: распределение внимания в группе")

        pdf.set_y(pdf.get_y() + 5)
        _draw_group_profile_squares(pdf)

        pass

    def _add_group_cattell(self, lang):
        pdf = self._pdf
        data = self.data
        pdf.add_page(orientation="P")
        self._insert_page_number(pdf)
        self._add_page_header("Базовые черты личности: групповые результаты")

        pdf.set_text_font(9)
        # sections = [
        #     "Emotional stability",
        #     "Team resilience",
        #     "Stability of the results",
        #     "Resilience to change",
        # ]
        sections = CATTELL_CATEGORIES
        for section in sections:
            section_label = TRANSLATIONS_DICT.get_translation(section, lang)
            _draw_section_header(pdf, section_label)
            categories = CATTELL_CATEGORIES[section]
            pdf.set_y(pdf.get_y() + 2)

            for category in categories:
                category_label = TRANSLATIONS_DICT.get_translation(category, lang)
                category_description = TRANSLATIONS_DICT.get_translation(
                    f"{category}_group_desc", lang
                )
                pdf.draw_category_header(
                    category_label, category_description, arrow_color=(34, 170, 245)
                )

                pdf.set_y(pdf.get_y() + 2)

            pdf.set_y(pdf.get_y() + 4)
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
            _draw_section_header(pdf, scale_label)

            categories = COPING_CATEGORIES_V1[scale]
            pdf.set_y(pdf.get_y() + 2)
            for category in categories:
                category_label = TRANSLATIONS_DICT.get_translation(category, lang)
                category_desc = TRANSLATIONS_DICT.get_translation(
                    f"{category}_group_desc", lang
                )
                pdf.draw_category_header(
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
            _draw_section_header(pdf, scale_label)

            categories = BOYKO_CATEGORIES_V1[scale]
            pdf.set_y(pdf.get_y() + 2)
            for category in categories:
                category_label = TRANSLATIONS_DICT.get_translation(category, lang)
                category_desc = TRANSLATIONS_DICT.get_translation(
                    f"{category}_group_desc", lang
                )
                pdf.draw_category_header(
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
            _draw_section_header(pdf, scale_label)

            categories = VALUES_CATEGORIES_V1[scale]
            pdf.set_y(pdf.get_y() + 2)
            for category in categories:
                category_label = TRANSLATIONS_DICT.get_translation(category, lang)
                category_desc = TRANSLATIONS_DICT.get_translation(
                    f"{category}_group_desc", lang
                )
                pdf.draw_category_header(
                    category_label, category_desc, arrow_color=(248, 216, 31)
                )

                pdf.set_y(pdf.get_y() + 5)

            pdf.set_y(pdf.get_y() + 5)
        pass
