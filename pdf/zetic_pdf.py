import os
from dataclasses import dataclass
from typing import Tuple, Dict

from django.db.models import Q
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


@dataclass
class SectionData:
    data: Dict[str, int]

    def __post_init__(self):
        # check if points are in range
        for points in self.data.values():
            if points < 0 or points > 10:
                raise ValueError(f"points must be between 0 and 10, got {points}")

    def __getitem__(self, item):
        # print(f"item: {item} {type(item)} {self.data}")
        return self.data[item]

    def __len__(self):
        return len(self.data)

    def add(self, category: str, points: int):
        if points < 0 or points > 10:
            raise ValueError(f"points must be between 0 and 10, got {points}")
        if category in self.data:
            raise ValueError(f"category {category} already exists")
        self.data[category] = points

    def to_query(self) -> Q:
        q_objects = map(
            lambda kv: Q(category__code=kv[0], value=kv[1]), self.data.items()
        )
        return Q(*q_objects, _connector=Q.OR)

    def is_empty(self):
        return len(self.data) == 0


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

    def draw_category_header_and_arrow(
        self,
        category_label: str,
        category_description: str,
        arrow_color: Tuple[int, int, int],
        line_delta_y: float = 1.0,
        line_width: int = 46,
        arrow_width: int = 140,
    ):
        start_y = self.y
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
            rect_width=arrow_width,
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

        section_qnt = 11
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
                txt=str(cur_section),
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

    def draw_section(self, section_data: Dict[str, SectionData]):

        pass
