import os
from dataclasses import dataclass
from typing import List, Dict

from fpdf import XPos, YPos
from fpdf.enums import Align

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
        self._add_participants()

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

        pdf.set_label_font(10)
        pdf.cell(
            0,
            0,
            TRANSLATIONS_DICT.get_translation(
                "Расшифровка командных ролей на основе модели Исхака Адизеса", lang
            ),
        )

        # draw underline
        pdf.set_draw_color(0, 0, 0)

        line_padding = 2
        pdf.line(
            pdf.l_margin, pdf.get_y() + line_padding, pdf.w, pdf.get_y() + line_padding
        )
        pdf.set_y(pdf.get_y() + 5)

        text = TRANSLATIONS_DICT.get_translation("group_report_description", lang)
        pdf.set_text_font(9)
        pdf.multi_cell(0, 4, text)
        pdf.set_xy(pdf.l_margin, pdf.get_y() + 5)

        self._add_description_section(
            "Производитель", "Производитель Описание", "Производитель Подробнее", lang
        )
        pdf.set_y(pdf.get_y() + 5)
        self._add_description_section(
            "Предприниматель",
            "Предприниматель Описание",
            "Предприниматель Подробнее",
            lang,
        )
        pdf.set_y(pdf.get_y() + 5)
        self._add_description_section(
            "Администратор", "Администратор Описание", "Администратор Подробнее", lang
        )
        pdf.set_y(pdf.get_y() + 5)
        self._add_description_section(
            "Интегратор", "Интегратор Описание", "Интегратор Подробнее", lang
        )

        pass

    def _add_description_section(self, label, text, description, lang):
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

    def _add_participants(self):
        pdf = self._pdf
        data = self.data
        pdf.add_page()
        self._insert_page_number(pdf)

        for square in data.square_results:

            pass
        pass
