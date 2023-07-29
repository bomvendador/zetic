import os
import time
from abc import ABC
from dataclasses import dataclass

from fpdf import fpdf
from fpdf.enums import Align

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


@dataclass
class SingleReportData:
    participant_name: str = ""
    lie_points: int = 7  # from 0 to 10
    lang: str = "ru"


class SingleReport(ABC):
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
                os.path.join(BASE_DIR, "images", "lie_scale_green.png"),
                x=pdf.get_x() + (i * (w + 1)),
                y=267,
                w=w,
            )

        for i in range(min(6, lie_points - 4)):
            pdf.image(
                os.path.join(BASE_DIR, "images", "lie_scale_red.png"),
                x=pdf.get_x() + ((i + 4) * (w + 1)),
                y=267,
                w=w,
            )

        self._insert_page_number()
        pass

    def _insert_page_number(self):
        self._pdf.set_fill_color(BLOCK_R, BLOCK_G, BLOCK_B)
        self._pdf.set_draw_color(BLOCK_R, BLOCK_G, BLOCK_B)
        rect_width = 20
        rect_height = 6
        self._pdf.rect(197, 287, rect_width, rect_height, "FD")

        self._pdf.set_xy(200, 290)
        self._pdf.set_text_color(0, 0, 0)
        self._pdf.set_font("RalewayLight", "", 10)
        self._pdf.set_xy(200, 290)
        self._pdf.cell(0, 0, txt=str(self._pdf.page_no()))
