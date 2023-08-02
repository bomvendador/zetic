import os

from fpdf import FPDF, XPos, YPos

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
            "YandexSansDisplay-Medium",
            fname=os.path.join(FONT_DIR, font_semi_bold),
        )
        self.add_font(
            "YandexSansDisplay-Regular",
            fname=os.path.join(FONT_DIR, font_regular),
        )
        self.add_font(
            "YandexSansDisplay-Light",
            fname=os.path.join(FONT_DIR, font_light),
        )
        self.add_font(
            "YandexSansDisplay-Bold",
            fname=os.path.join(FONT_DIR, font_bold),
        )
        pass

    def set_title_font(self, size=10):
        self.set_font("YandexSansDisplay-Regular", "", size)

    def set_label_font(self, size=10):
        self.set_font("YandexSansDisplay-Bold", "", size)

    def set_text_font(self, size=10):
        self.set_font("YandexSansDisplay-Light", "", size)

    def paragraph_with_bold_start(
        self,
        paragraph_label,
        paragraph_text,
        paragraph_label_size=10,
        paragraph_text_size=10,
    ):
        self.set_label_font(paragraph_label_size)
        self.cell(0, 5, txt=paragraph_label, border=1, new_x=XPos.LEFT, new_y=YPos.TOP)

        paragraph_width = self.get_string_width(paragraph_label)
        spaces = " " * (round(paragraph_width * 1.2))
        spaces = ""
        self.set_text_font(paragraph_text_size)

        self.multi_cell(
            0,
            5,
            txt=f"{spaces}{paragraph_text}",
            border=1,
            new_x=XPos.LEFT,
            new_y=YPos.NEXT,
        )
