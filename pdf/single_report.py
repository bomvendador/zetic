import os
import textwrap
import time
from abc import ABC
from dataclasses import dataclass
from typing import Dict

from fpdf import fpdf, FPDF, drawing
from fpdf.drawing import DeviceRGB
from fpdf.enums import Align, XPos, YPos

from pdf.report_sections_configuration import (
    CATTELL_CATEGORIES,
    COPING_CATEGORIES,
    BOYKO_CATEGORIES,
    VALUES_CATEGORIES,
)
from pdf.raw_to_t_point_mapper import RawToTPointMapper, AgeGroup
from pdf.translations import TRANSLATIONS_DICT

mujer_joven = RawToTPointMapper("mujer", AgeGroup.JOVEN, {})
mujer_mayor = RawToTPointMapper("mujer", AgeGroup.MAYOR, {})
hombre_joven = RawToTPointMapper("hombre", AgeGroup.JOVEN, {})
hombre_mayor = RawToTPointMapper("hombre", AgeGroup.MAYOR, {})

# Assuming your settings.py is located at the project's root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the font directory path to your settings
FONT_DIR = os.path.join(BASE_DIR, "fonts")

BLOCK_R = 230
BLOCK_G = 230
BLOCK_B = 227

text_border = 1


# category: str, points: int
@dataclass
class SectionData:
    data: Dict[str, int]

    def __post_init__(self):
        # check if points are in range
        for points in self.data.values():
            if points < 0 or points > 10:
                raise ValueError(f"points must be between 0 and 10, got {points}")

    def __getitem__(self, item):
        return self.data[item]

    def is_empty(self):
        return len(self.data) == 0


@dataclass
class SingleReportData:
    participant_name: str = ""
    lie_points: int = 7  # from 0 to 10
    lang: str = "ru"
    cattell_data: SectionData = SectionData({})
    coping_data: SectionData = SectionData({})
    boyko_data: SectionData = SectionData({})
    values_data: SectionData = SectionData({})

    def __post_init__(self):
        # check if lang is supported
        if self.lang not in ["ru", "en"]:
            raise ValueError(f"lang must be either ru or en, got {self.lang}")
        # check if lie_points is in range
        if self.lie_points < 0 or self.lie_points > 10:
            raise ValueError(
                f"lie_points must be between 0 and 10, got {self.lie_points}"
            )


class SingleReport(ABC):
    _pdf: FPDF

    def __init__(self):
        self._pdf = fpdf.FPDF(orientation="P", unit="mm", format="A4")
        self._pdf.set_auto_page_break(False)

    def _add_fonts(self):
        self._pdf.add_font(
            "RalewayMedium", fname=os.path.join(FONT_DIR, "Raleway-Medium.ttf")
        )
        self._pdf.add_font(
            "RalewayRegular", fname=os.path.join(FONT_DIR, "Raleway-Regular.ttf")
        )
        self._pdf.add_font(
            "RalewayLight", fname=os.path.join(FONT_DIR, "Raleway-Light.ttf")
        )
        self._pdf.add_font(
            "RalewayBold", fname=os.path.join(FONT_DIR, "Raleway-Bold.ttf")
        )
        self._pdf.add_font(
            "NotoSansDisplayMedium",
            fname=os.path.join(FONT_DIR, "NotoSansDisplay-Medium.ttf"),
        )

    def generate_pdf(self, data: SingleReportData, path: str = "test"):
        time_start = time.perf_counter()
        self._add_fonts()
        self._title_page(data.participant_name, data.lang)
        self._add_report_description(data.lie_points, data.lang)

        self._add_cattell_page(data.cattell_data, data.lang)
        self._add_coping_page(data.coping_data, data.lang)
        self._add_boyko_page(data.boyko_data, data.lang)
        self._add_values_page(data.values_data, data.lang)

        time_end = time.perf_counter() - time_start
        self._pdf.output(f"{path}-{data.lang}.pdf")
        print(f"Time elapsed: {time_end:.2f} seconds")

    def _title_page(self, name, lang):
        pdf = self._pdf
        pdf.add_page()
        pdf.image(os.path.join(BASE_DIR, "images", "title_page.png"), x=0, y=0, w=210)

        pdf.set_xy(20, 150)
        pdf.set_font("RalewayRegular", size=18)
        pdf.cell(0, 0, txt=TRANSLATIONS_DICT.get_translation("report", lang))

        pdf.set_xy(20, 170)
        pdf.set_font("RalewayLight", size=12)
        participant_label = TRANSLATIONS_DICT.get_translation("participant", lang)
        pdf.cell(20, txt=participant_label)

        if lang == "en":
            pdf.set_x(pdf.get_x() + 2)

        pdf.set_font("RalewayRegular", size=12)
        pdf.write(txt=name)

        pdf.set_xy(20, 180)
        pdf.set_font("RalewayRegular", size=12)
        pdf.cell(0, txt=TRANSLATIONS_DICT.get_translation("zetic", lang))

    def _add_report_description(self, lie_points: int, lang):
        pdf = self._pdf
        pdf.add_page()
        # pdf.set_xy(10, 10)
        pdf.set_font("RalewayBold", "", 10)
        pdf.cell(0, 0, TRANSLATIONS_DICT.get_translation("Introduction", lang))

        pdf.set_font("RalewayLight", "", 9)
        pdf.set_y(pdf.get_y() + 5)
        pdf.multi_cell(
            0, 4, txt=TRANSLATIONS_DICT.get_translation("Introduction_text", lang)
        )

        pdf.set_xy(pdf.l_margin + 5, pdf.get_y() + 5)
        pdf.multi_cell(
            0, 4, txt=TRANSLATIONS_DICT.get_translation("Introduction_text_2", lang)
        )

        pdf.set_font("RalewayBold", "", 10)
        pdf.set_xy(pdf.l_margin, pdf.get_y() + 5)
        pdf.cell(
            0, 0, txt=TRANSLATIONS_DICT.get_translation("How to read the report", lang)
        )

        pdf.set_font("RalewayLight", "", 9)
        pdf.set_xy(pdf.l_margin, pdf.get_y() + 5)
        pdf.multi_cell(
            0,
            4,
            txt=TRANSLATIONS_DICT.get_translation("How to read the report_text", lang),
        )

        pdf.set_font("RalewayBold", "", 10)
        pdf.set_xy(pdf.l_margin, pdf.get_y() + 5)
        pdf.cell(0, 0, txt=TRANSLATIONS_DICT.get_translation("The scales", lang))

        pdf.set_font("RalewayLight", "", 9)
        pdf.set_xy(pdf.l_margin, pdf.get_y() + 5)
        pdf.multi_cell(
            0, 4, txt=TRANSLATIONS_DICT.get_translation("The scales_text", lang)
        )

        # 210 x 297
        # 10 margin
        #
        # lie scale text
        pdf.set_font("RalewayLight", "", 9)
        pdf.set_xy(pdf.l_margin, 265)
        pdf.cell(30, 12, txt=TRANSLATIONS_DICT.get_translation("Validity", lang))

        # lie scale points
        # 45 + 70 = 115 = box size
        pdf.set_x(116)
        pdf.cell(14, 12, txt=str(lie_points), align=Align.C)

        pdf.set_font("RalewayLight", "", 7)

        # 115 + 15 = 130
        pdf.set_x(130)
        validity_text = TRANSLATIONS_DICT.get_translation("Validity_text", lang)
        line_height = 3
        if lang == "en":
            line_height = 4
        pdf.multi_cell(0, line_height, txt=validity_text)

        # lie scale box
        pdf.set_line_width(0.3)
        pdf.set_fill_color(230, 230, 230)

        # background
        box_x = 45
        pdf.rect(box_x, 266, 70, 10, "F")

        # green box
        pdf.set_draw_color(146, 208, 80)
        pdf.rect(box_x - 1, 265, 29.1, 12)

        # red box
        pdf.set_draw_color(255, 0, 0)
        pdf.rect(box_x - 1 + 29.1, 266 - 1, 43, 10 + 2)

        pdf.set_x(box_x + 1)
        w = 5.9
        for i in range(min(4, lie_points)):
            pdf.image(
                os.path.join(BASE_DIR, "images", "scale_lie_green.png"),
                x=pdf.get_x() + (i * (w + 1)),
                y=267,
                w=w,
            )

        for i in range(min(6, lie_points - 4)):
            pdf.image(
                os.path.join(BASE_DIR, "images", "scale_lie_red.png"),
                x=pdf.get_x() + ((i + 4) * (w + 1)),
                y=267,
                w=w,
            )

        self._insert_page_number(pdf)
        pass

    def _add_cattell_page(self, data: SectionData, lang: str):
        if data.is_empty():
            return

        pdf = self._pdf
        pdf.add_page()

        cattell_img = os.path.join(BASE_DIR, "images", "scale_cattell.png")

        # Header
        self._draw_header(
            pdf,
            TRANSLATIONS_DICT.get_translation("Section K", lang),
            TRANSLATIONS_DICT.get_translation("Section K_text", lang),
        )

        scale_y = pdf.get_y() + 5

        # Categories
        category_height = 15.5
        for category in CATTELL_CATEGORIES:
            scales = CATTELL_CATEGORIES[category]
            height = category_height * len(scales)

            # Draw category header
            category_name = TRANSLATIONS_DICT.get_translation(category, lang)
            self._draw_category_vertically(
                pdf, category_name, start_y=scale_y, height=height
            )

            for scale in scales:
                points = data[scale]
                pdf.set_xy(pdf.l_margin + 8, scale_y)
                pdf.set_font("RalewayLight", "", 9)

                scale_name = TRANSLATIONS_DICT.get_translation(scale, lang)
                self._draw_multi_text(
                    pdf,
                    text=scale_name,
                    start_y=scale_y,
                    start_x=pdf.l_margin + 8,
                    label_width=32,
                    line_height=4,
                    block_height=category_height,
                    border=text_border,
                )

                self._draw_rectangle_scale(
                    pdf, start_y=scale_y, points=points, img=cattell_img
                )

                # draw under rectangle
                pdf.set_xy(50, scale_y + 10)
                self._draw_scale_min_max(
                    pdf,
                    scale_min=TRANSLATIONS_DICT.get_translation(scale + "_min", lang),
                    scale_max=TRANSLATIONS_DICT.get_translation(scale + "_max", lang),
                )

                pdf.set_xy(134, scale_y)

                # draw points description
                # pdf.set_xy(134, start_y - 3)
                # w = 210-10-134
                pdf.multi_cell(
                    0,
                    h=4,
                    txt=textwrap.dedent(
                        """\
                        Критичность к информации, исследование
                        неочевидных скрытых факторов, недоверие
                        авторитетам; исследование разных сценариев
                        Консерватизм, развития ситуации."""
                    ),
                    border=text_border,
                    align=Align.L,
                    new_x=XPos.LEFT,
                    new_y=YPos.TOP,
                )

                # padding between scales
                scale_y += category_height + 1

            # padding between categories
            scale_y += 5

        self._insert_page_number(pdf)
        pass

    def _add_coping_page(self, coping_data: SectionData, lang: str):
        if coping_data.is_empty():
            return

        pdf = self._pdf
        pdf.add_page()

        self._draw_header(
            pdf,
            TRANSLATIONS_DICT.get_translation("Section C", lang),
            TRANSLATIONS_DICT.get_translation("Section C_text", lang),
        )

        for category in COPING_CATEGORIES:
            scales = COPING_CATEGORIES[category]
            pdf.set_xy(pdf.l_margin, pdf.get_y() + 5)

            category_label = TRANSLATIONS_DICT.get_translation(category, lang)
            pdf.set_font("RalewayBold", "", 10)
            pdf.multi_cell(
                0,
                0,
                txt=category_label,
                new_y=YPos.NEXT,
                align=Align.L,
            )

            pdf.set_xy(50, pdf.get_y() + 2)
            self._draw_scale_min_max(
                pdf,
                scale_min=TRANSLATIONS_DICT.get_translation("scale_min", lang),
                scale_max=TRANSLATIONS_DICT.get_translation("scale_max", lang),
            )

            for scale in scales:
                scale_name = TRANSLATIONS_DICT.get_translation(scale, lang)
                points = coping_data[scale]

                # padding between scales
                scale_y = pdf.get_y() + 5
                pdf.set_xy(pdf.l_margin, scale_y)
                pdf.set_font("RalewayLight", "", 9)

                # find height of the text depending on the number of lines
                lines = len(
                    pdf.multi_cell(32, 4, scale_name, align=Align.L, split_only=True)
                )

                # top corner (10-4) / 2
                pdf.set_xy(pdf.l_margin, scale_y + (10 - (lines * 4)) / 2)
                # w = 50 - l_margin
                pdf.multi_cell(
                    40, 4, scale_name, new_y=YPos.TOP, border=text_border, align=Align.L
                )

                # draw rectangle
                pdf.set_line_width(0.3)
                pdf.set_fill_color(230, 230, 230)
                pdf.rect(50, scale_y, 70, 10, "F")

                # draw images
                for i in range(points):
                    pdf.image(
                        os.path.join(BASE_DIR, "images", "scale_coping.png"),
                        x=51 + (6.9 * i),
                        y=scale_y + 1,
                        w=5.9,
                    )

                # draw points
                pdf.set_xy(120, scale_y)
                pdf.cell(
                    14,
                    h=10,
                    txt=str(points),
                    align="C",
                    border=text_border,
                    new_x=XPos.RIGHT,
                    new_y=YPos.TOP,
                )

                pdf.set_font("RalewayLight", "", 8)
                text = textwrap.dedent(
                    """\
                    Стратегия проявляется локально: ощущение
                    раздражения, злость на себя и ситуацию;
                    потребность жестоко шутить /отстаивать свое
                    мнение / проявлять эмоции."""
                )
                lines = text.count("\n") + 1
                pdf.set_xy(pdf.get_x(), scale_y + (10 - (lines * 4)) / 2)

                pdf.multi_cell(
                    0,
                    h=4,
                    txt=text,
                    align="L",
                    border=text_border,
                )
                pdf.set_y(scale_y + 10)

        pass

    def _add_boyko_page(self, data: SectionData, lang: str):
        if data.is_empty():
            return

        pdf = self._pdf
        pdf.add_page()
        boyko_img = os.path.join(BASE_DIR, "images", "scale_boyko.png")

        # Header
        self._draw_header(
            pdf,
            TRANSLATIONS_DICT.get_translation("Section B", lang),
            TRANSLATIONS_DICT.get_translation("Section B_text", lang),
        )

        pdf.set_xy(50, pdf.get_y() + 2)
        self._draw_scale_min_max(
            pdf,
            scale_min=TRANSLATIONS_DICT.get_translation("scale_min", lang),
            scale_max=TRANSLATIONS_DICT.get_translation("scale_max", lang),
        )

        # Categories
        category_height = 15.5
        scale_y = pdf.get_y() + 5
        for category in BOYKO_CATEGORIES:
            scales = BOYKO_CATEGORIES[category]
            height = category_height * len(scales)

            # Draw category header
            category_name = TRANSLATIONS_DICT.get_translation(category, lang)
            self._draw_category_vertically(
                pdf, category_name, start_y=scale_y, height=height
            )

            # Draw scales
            # | l_margin | 10 v_line | 3 padding txt | 35 text | 3 padding points | 14 points | 3 padding text | 31 txt
            # 1_1, 1_2, ...
            for scale in scales:
                points = data[scale]
                pdf.set_xy(pdf.l_margin + 8, scale_y)
                pdf.set_font("RalewayLight", "", 9)

                scale_name = TRANSLATIONS_DICT.get_translation(scale, lang)
                self._draw_scale_label(pdf, scale_name=scale_name, start_y=scale_y)
                self._draw_rectangle_scale(
                    pdf,
                    start_y=scale_y,
                    points=points,
                    img=boyko_img,
                )

                pdf.set_font("RalewayLight", "", 8)
                # draw points description
                # pdf.set_xy(134, start_y - 3)
                # w = 210-10-134

                text = textwrap.dedent(
                    """\
                    Стратегия проявляется локально: ощущение
                    раздражения, злость на себя и ситуацию;
                    потребность жестоко шутить /отстаивать свое
                    мнение / проявлять эмоции."""
                )
                self._draw_multi_text(
                    pdf,
                    start_y=scale_y,
                    text=text,
                    start_x=pdf.get_x(),
                    line_height=4,
                    block_height=10,
                )

                lines = text.count("\n") + 1
                pdf.set_xy(pdf.get_x(), pdf.get_y() + (10 - (lines * 4)) / 2)

                pdf.multi_cell(
                    0,
                    h=4,
                    txt=text,
                    border=text_border,
                    align=Align.L,
                    new_x=XPos.LEFT,
                    new_y=YPos.TOP,
                )

                scale_y += category_height + 1

            # padding between categories
            scale_y += 5

        self._insert_page_number(pdf)
        pass

    def _add_values_page(self, data, lang):
        if data.is_empty():
            return

        pdf = self._pdf
        pdf.add_page()
        values_img = os.path.join(BASE_DIR, "images", "scale_values.png")

        # Header
        self._draw_header(
            pdf,
            TRANSLATIONS_DICT.get_translation("Section V", lang),
            TRANSLATIONS_DICT.get_translation("Section V_text", lang),
        )

        pdf.set_xy(50, pdf.get_y() + 2)
        self._draw_scale_min_max(
            pdf,
            scale_min=TRANSLATIONS_DICT.get_translation("scale_min", lang),
            scale_max=TRANSLATIONS_DICT.get_translation("scale_max", lang),
        )

        # Categories
        category_height = 15.5
        scale_y = pdf.get_y() + 5
        for category in VALUES_CATEGORIES:
            scales = VALUES_CATEGORIES[category]
            height = category_height * len(scales)

            # Draw category header
            category_name = TRANSLATIONS_DICT.get_translation(category, lang)
            self._draw_category_vertically(
                pdf, category_name, start_y=scale_y, height=height
            )

            # Draw scales
            for scale in scales:
                points = data[scale]
                pdf.set_xy(pdf.l_margin + 8, scale_y)
                pdf.set_font("RalewayLight", "", 9)

                scale_name = TRANSLATIONS_DICT.get_translation(scale, lang)
                self._draw_scale_label(pdf, scale_name=scale_name, start_y=scale_y)

                self._draw_rectangle_scale(
                    pdf,
                    start_y=scale_y,
                    points=points,
                    img=values_img,
                )

                pdf.set_font("RalewayLight", "", 8)
                # draw points description
                # pdf.set_xy(134, start_y)
                # w = 210-10-134
                pdf.multi_cell(
                    0,
                    h=4,
                    txt=textwrap.dedent(
                        """\
                        Критичность к информации, исследование
                        неочевидных скрытых факторов, недоверие
                        авторитетам; исследование разных сценариев
                        Консерватизм, развития ситуации."""
                    ),
                    border=text_border,
                    align=Align.L,
                    new_x=XPos.LEFT,
                    new_y=YPos.TOP,
                )

                scale_y += category_height + 1

            # padding between categories
            scale_y += 5

        self._insert_page_number(pdf)

    @staticmethod
    def _draw_header(pdf: FPDF, section_name, section_text):
        pdf.set_font("RalewayBold", "", 10)
        pdf.cell(0, 0, txt=section_name)

        pdf.set_font("RalewayLight", "", 9)
        pdf.set_xy(pdf.l_margin, pdf.get_y() + 5)
        pdf.multi_cell(
            0,
            4,
            txt=section_text,
            align=Align.J,
        )
        pass

    @staticmethod
    def _draw_category_vertically(
        pdf: FPDF, category_name: str, start_y: float, height: float
    ):
        pdf.set_font("RalewayLight", "", 9)
        pdf.set_xy(pdf.l_margin, start_y + height)
        with pdf.rotation(90):
            pdf.cell(
                height,
                0,
                txt=category_name,
                align=Align.C,
                new_x=XPos.LEFT,
                new_y=YPos.TOP,
            )

        prev_color: drawing.DeviceGray = pdf.draw_color
        pdf.set_draw_color(0, 0, 0)
        pdf.line(pdf.l_margin + 5, pdf.get_y() - height, pdf.l_margin + 5, pdf.get_y())
        pdf.set_draw_color(prev_color.r * 255, prev_color.g * 255, prev_color.b * 255)

    @staticmethod
    def _draw_scale_min_max(pdf: FPDF, scale_min, scale_max):
        pdf.set_font("RalewayLight", "", 6)
        pdf.multi_cell(
            35,
            3,
            txt=scale_min,
            align=Align.L,
            new_y=YPos.TOP,
            border=text_border,
        )
        pdf.multi_cell(
            35,
            3,
            txt=scale_max,
            align=Align.R,
            new_y=YPos.TOP,
            border=text_border,
        )

    @staticmethod
    def _draw_rectangle_scale(pdf: FPDF, start_y: float, points: int, img: str = None):
        block_width = 5.9

        # draw rectangle
        pdf.set_line_width(0.3)
        pdf.set_fill_color(230, 230, 230)
        pdf.rect(50, start_y, 70, 10, "F")

        # draw images
        for i in range(points):
            pdf.image(
                img,
                x=51 + ((block_width + 1) * i),
                y=start_y + 1,
                w=block_width,
                h=8,
            )

        # 120 = 50 + 70
        pdf.set_xy(120, start_y)
        pdf.cell(
            14,
            h=10,
            txt=str(points),
            align="C",
            border=text_border,
            new_x=XPos.RIGHT,
            new_y=YPos.TOP,
        )

    @staticmethod
    def _draw_scale_label(
        pdf: FPDF,
        start_y: float,
        scale_name: str,
        label_width: float = 32,
        label_height: float = 4,
        block_height: float = 10,
    ):
        lines = len(
            pdf.multi_cell(
                label_width,
                label_height,
                scale_name,
                align=Align.L,
                split_only=True,
            )
        )

        # top corner (10-4) / 2
        pdf.set_xy(pdf.l_margin + 8, start_y + (block_height - (lines * 4)) / 2)
        # scale label
        pdf.multi_cell(
            label_width,  # 50 - 10 - 8
            label_height,
            scale_name,
            new_x=XPos.LEFT,
            new_y=YPos.NEXT,
            align=Align.L,
            border=text_border,
        )

    @staticmethod
    def _insert_page_number(pdf: FPDF):
        pdf.set_fill_color(BLOCK_R, BLOCK_G, BLOCK_B)
        pdf.set_draw_color(BLOCK_R, BLOCK_G, BLOCK_B)
        rect_width = 20
        rect_height = 6
        pdf.rect(197, 287, rect_width, rect_height, "FD")

        pdf.set_xy(200, 290)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("RalewayLight", "", 10)
        pdf.set_xy(200, 290)
        pdf.cell(0, 0, txt=str(pdf.page_no()))

    @staticmethod
    def _draw_section(pdf: FPDF):
        pass

    @staticmethod
    def _draw_multi_text(
        pdf: FPDF,
        text: str,
        start_y: float,
        start_x: float,
        line_height: float = 4,
        block_height: float = 10,
        label_width: float = 0,
        border: int = 0,
    ):
        lines = len(
            pdf.multi_cell(
                label_width,
                line_height,
                text,
                align=Align.L,
                split_only=True,
            )
        )

        # top corner (10-4) / 2
        pdf.set_xy(start_x, start_y + (block_height - (lines * line_height)) / 2)
        # scale label
        pdf.multi_cell(
            label_width,
            line_height,
            text,
            new_x=XPos.LEFT,
            new_y=YPos.NEXT,
            align=Align.L,
            border=border,
        )
        pass
