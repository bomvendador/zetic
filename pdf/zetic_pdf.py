import os

from fpdf import FPDF, XPos, YPos
from fpdf.enums import Align

# Assuming your settings.py is located at the project's root directory
PDF_MODULE_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the font directory path to your settings
FONT_DIR = os.path.join(PDF_MODULE_BASE_DIR, "fonts")

BLOCK_R = 230
BLOCK_G = 230
BLOCK_B = 227

text_border = 0


class ZeticPDF(FPDF):
    def add_fonts(self):
        prefix = "Inter"
        font_semi_bold = f"{prefix}-SemiBold.ttf"
        font_regular = f"{prefix}-Regular.ttf"
        font_light = f"{prefix}-Light.ttf"
        font_bold = f"{prefix}-Bold.ttf"
        self.add_font(
            "Medium",
            fname=os.path.join(FONT_DIR, font_semi_bold),
        )
        self.add_font(
            "Regular",
            fname=os.path.join(FONT_DIR, font_regular),
        )
        self.add_font(
            "Regular",
            "B",
            fname=os.path.join(FONT_DIR, font_bold),
        )
        self.add_font(
            "Light",
            fname=os.path.join(FONT_DIR, font_light),
        )
        self.add_font(
            "Bold",
            fname=os.path.join(FONT_DIR, font_bold),
        )
        pass

    def set_title_font(self, size=10):
        self.set_font("Medium", "", size)

    def set_label_font(self, size=10):
        self.set_font("Bold", "", size)

    def set_text_font(self, size=10):
        self.set_font("Regular", "", size)

    def set_medium_font(self, size=10):
        self.set_font("Medium", "", size)

    def paragraph_with_bold_start(
        self,
        paragraph_label,
        paragraph_text,
        paragraph_label_size=10,
        paragraph_text_size=10,
        h=5,
        border=0,
    ):

        pass
