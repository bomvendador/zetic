import os
from typing import Tuple

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
            "Regular",
            "I",
            fname=os.path.join(FONT_DIR, font_light),
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

    def set_light_font(self, size=10):
        self.set_font("Light", "", size)

    def draw_category_header(
        self,
        category_label: str,
        category_description: str,
        arrow_color: Tuple[int, int, int],
        line_delta_y=1.0,
    ):
        start_y = self.y
        line_width = 46
        category_height = 15.5
        self.set_text_color(0, 0, 0)
        self.set_medium_font(9)
        self.multi_cell(
            0, txt=category_label, align=Align.L, new_x=XPos.LEFT, new_y=YPos.NEXT
        )
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)
        self.line(
            self.x, self.y + line_delta_y, self.x + line_width, self.y + line_delta_y
        )
        line_y = self.y + line_delta_y
        self.y = self.y + line_delta_y * 2
        self.set_text_font(7)
        self.multi_cell(0, 4, category_description)
        last_y = self.y

        self.draw_arrow(
            self.l_margin + line_width + 1,
            line_y,
            arrow_color,
        )
        self.set_y(last_y)

    pass

    def draw_arrow(
        self,
        x: int,
        y: int,
        color: Tuple[int, int, int],
        rect_width: int = 140,
        rect_height: int = 4,
    ):
        self.set_draw_color(*color)
        self.set_fill_color(*color)
        # отрисовка прямоугольника
        self.rect(x, y - rect_height / 2, rect_width, rect_height, "FD")
        # отрисовка треугольника
        triangle_width = 7
        # point1 = (x + rect_width, y - rect_height / 2)
        # point2 = (
        #     x + rect_width + triangle_width,
        #     y - rect_height / 2 + rect_height,
        # )
        # point3 = (x + rect_width, y - rect_height / 2 + rect_height * 2)

        points = self._make_triangle_points(
            x + rect_width, y - rect_height / 2, triangle_width, rect_height
        )
        self.polygon(point_list=points, style="FD")

        section_qnt = 10
        section_width = rect_width / section_qnt

        start_x = x
        start_y = y - rect_height / 2
        line_x_start = start_x

        # draw scales 0 .. 10
        for cur_section in range(section_qnt):
            cur_section_width = section_width

            self.set_draw_color(105, 105, 105)
            # draw left line
            self.line(
                line_x_start,
                start_y,
                line_x_start,
                start_y + rect_height,
            )
            # draw right line
            self.line(
                line_x_start + cur_section_width,
                start_y,
                line_x_start + cur_section_width,
                start_y + rect_height,
            )
            self.set_text_color(105, 105, 105)
            # draw section label
            self.set_xy(line_x_start, start_y)
            self.cell(
                w=cur_section_width,
                h=rect_height,
                txt=str(cur_section + 1),
                align=Align.C,
            )
            line_x_start += cur_section_width
            pass
        pass

    def _make_triangle_points(self, x, y, width, height):
        point1 = (x, y)
        point2 = (x + width, y + height / 2)
        point3 = (x, y + height)
        return [point1, point2, point3, point1]

    def draw_scale_as_arrow(self, min_value: int = 0, max_value: int = 10):

        pass
