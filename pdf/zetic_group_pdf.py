from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Dict, List

from fpdf.enums import Align, XPos, YPos

from pdf.zetic_pdf import ZeticPDF


class SquareId(Enum):
    ESFJ_1_1 = 0
    ENFJ_1_2 = 1
    ESFP_1_3 = 2
    ENFP_1_4 = 3
    ESTJ_2_1 = 4
    ENTJ_2_2 = 5
    ESTP_2_3 = 6
    ENTP_2_4 = 7
    ISFJ_3_1 = 8
    INFJ_3_2 = 9
    ISFP_3_3 = 10
    INFP_3_4 = 11
    ISTJ_4_1 = 12
    INTJ_4_2 = 13
    ISTP_4_3 = 14
    INTP_4_4 = 15


@dataclass
class SquareUiConfig:
    x: int
    y: int
    name: str
    pass


SQUARE_UI_CONFIG: Dict[SquareId, SquareUiConfig] = {
    SquareId.ESFJ_1_1: SquareUiConfig(x=0, y=0, name="Массовик-затейник"),
    SquareId.ENFJ_1_2: SquareUiConfig(
        x=1, y=0, name="Чуткий наставник / Коммуникатор"
    ),  # ?
    SquareId.ESFP_1_3: SquareUiConfig(
        x=0, y=1, name="Развлекатель / Переговорщик"
    ),  # ?
    SquareId.ENFP_1_4: SquareUiConfig(x=1, y=1, name="Мотиватор"),
    SquareId.ESTJ_2_1: SquareUiConfig(x=2, y=0, name="Контролер"),
    SquareId.ENTJ_2_2: SquareUiConfig(x=2, y=1, name="Аналитик"),
    SquareId.ESTP_2_3: SquareUiConfig(x=3, y=0, name="Искатель ресурсов"),
    SquareId.ENTP_2_4: SquareUiConfig(x=3, y=1, name="Изобретатель"),
    SquareId.ISFJ_3_1: SquareUiConfig(x=0, y=2, name="Хранитель / Визионер"),
    SquareId.INFJ_3_2: SquareUiConfig(x=0, y=3, name="Вдохновитель / Авантюрист"),
    SquareId.ISFP_3_3: SquareUiConfig(x=1, y=2, name="Опекун / Искатель ресурсов"),
    SquareId.INFP_3_4: SquareUiConfig(
        x=1, y=3, name="Благородный служитель /Изобретатель"
    ),
    SquareId.ISTJ_4_1: SquareUiConfig(x=2, y=2, name="Организатор"),
    SquareId.INTJ_4_2: SquareUiConfig(x=2, y=3, name="Любитель улучшений"),
    SquareId.ISTP_4_3: SquareUiConfig(x=3, y=2, name="Реализатор"),
    SquareId.INTP_4_4: SquareUiConfig(x=3, y=3, name="Решатель проблем"),
}


class ZeticGroupPDF(ZeticPDF):
    def draw_square(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int],
        label: str = None,
        label_desc: str = None,
    ):
        self.set_draw_color(*color)
        self.set_fill_color(*color)
        self.rect(x, y, width, height, "FD")

        self.set_draw_color(255, 255, 255)
        self.set_fill_color(255, 255, 255)
        # белый вертикальный
        self.rect(
            x=x + width / 2 - 0.3,
            y=y,
            w=0.6,
            h=x + width * 2,
            style="FD",
        )
        # белый горизонтальный
        self.rect(
            x=x,
            y=y + width / 2 - 0.3,
            w=width,
            h=0.6,
            style="FD",
        )

        # square label
        self.set_text_color(0, 0, 0)
        # in the center
        center_x = x + width / 2
        center_y = y + height / 2
        label_with = 28
        rect_width = label_with + 10  # 5*2 padding
        rect_height = 12
        self.rect(
            center_x - rect_width / 2,
            center_y - rect_height / 2,
            rect_width,
            rect_height,
            "FD",
        )
        self.set_xy(x=center_x - rect_width / 2, y=center_y - rect_height / 2 + 1)
        self.set_label_font(8)
        self.cell(
            w=rect_width,
            h=self.font_size,
            align=Align.C,
            txt=label,
            new_x=XPos.LEFT,
            new_y=YPos.NEXT,
        )
        if label_desc:
            self.set_light_font(6)
            self.set_xy(x=self.x, y=self.y + 1)
            self.multi_cell(
                w=rect_width,
                h=self.font_size,
                txt=label_desc,
                align=Align.C,
                new_x=XPos.LEFT,
                new_y=YPos.TOP,
            )
        pass

    def draw_group_profile_squares(self):
        start_x = self.get_x()
        start_y = self.get_y()
        width = (self.w - self.l_margin - self.r_margin) / 2

        self.draw_square(
            start_x,
            start_y,
            width,
            width,
            (255, 240, 193),
            "Интеграторы",
            "отвечают за целостность команды и культуры в долгосрочной перспективе",
        )
        self.draw_square(
            start_x + width,
            start_y,
            width,
            width,
            (253, 219, 246),
            "Предприниматели",
            "отвечают за стратегически важные и долгосрочные задачи",
        )

        self.draw_square(
            start_x,
            start_y + width,
            width,
            width,
            (217, 245, 251),
            "Администраторы",
            "отвечают за эффективность, технологичность и низкие расходы здесь и сейчас",
        )
        # 4
        self.draw_square(
            start_x + width,
            start_y + width,
            width,
            width,
            (226, 239, 218),
            "Производители",
            "достигают краткосрочных результатов здесь и сейчас",
        )

        self.set_text_font(8)
        self.text(start_x + width / 2 - 13, start_y - 2.5, "Фокус на процесс")
        self.text(
            start_x + width / 2 + width - 13.5, start_y - 2.5, "Фокус на результат"
        )
        with self.rotation(
            90, self.l_margin - self.font_size, start_y + width / 2 + 10
        ):
            self.text(0, start_y + width / 2 + 10, "Неструктурированный подход")
        with self.rotation(270, start_x + width * 2 + 3, start_y + width / 2 - 18):
            self.text(
                start_x + width * 2 + 3,
                start_y + width / 2 - 18,
                "Концептуальные решения",
            )
        with self.rotation(
            90, self.l_margin - self.font_size, start_y + width / 2 + 7 + width
        ):
            self.text(
                0,
                start_y + width / 2 + 7 + width,
                "Структурированный подход",
            )
        with self.rotation(
            270,
            start_x + width * 2 + 3,
            start_y + width / 2 - 15 + width,
        ):
            self.text(
                start_x + width * 2 + 3,
                start_y + width / 2 - 15 + width,
                "Локальные решения",
            )

        self.set_light_font(8)

        # self.text(start_x + width / 4 - 3, start_y + 4, 'ESFJ')
        # self.text(start_x + width / 4 - 13, start_y + 7, 'Массовик-затейник')
        self.text(start_x + width / 4 - 13, start_y + 4, "Массовик-затейник")

        # self.text(start_x + width * (3/4) - 3, start_y + 4, 'ENFJ')
        # self.text(start_x + width * (3/4) - 13, start_y + 7, 'Идеалист-харизматик')
        self.text(start_x + width * (3 / 4) - 12, start_y + 4, "Чуткий наставник")

        # self.text(start_x + width + width / 4 - 3, start_y + 4, 'ESTJ')
        # self.text(start_x + width + width / 4 - 14, start_y + 7, 'Контролер по жизни')
        self.text(start_x + width + width / 4 - 8, start_y + 4, "Контролер")

        # self.text(start_x + width + width * (3/4) - 3, start_y + 4, 'ENTJ')
        # self.text(start_x + width + width * (3/4) - 11, start_y + 7, 'Предприниматель')
        self.text(start_x + width + width * (3 / 4) - 5, start_y + 4, "Аналитик")

        # self.text(start_x + width / 4 - 3, start_y + width - 6 , 'ESFP')
        # self.text(start_x + width / 4 - 18.5, start_y + width - 3 , 'Спонтанный коммуникатор')
        self.text(
            start_x + width / 4 - 9,
            start_y + width - 3,
            "Развлекатель",
        )

        # self.text(start_x + width * (3/4) - 3, start_y + width - 6 , 'ENFP')
        # self.text(start_x + width * (3/4) - 7, start_y + width - 3 , 'Инициатор')
        self.text(
            start_x + width * (3 / 4) - 7,
            start_y + width - 3,
            "Мотиватор",
        )

        # self.text(start_x + width + width / 4 - 3, start_y + width - 6 , 'ESTP')
        # self.text(start_x + width + width / 4 - 10, start_y + width - 3 , 'Ультра-реалист')
        self.text(
            start_x + width + width / 4 - 12,
            start_y + width - 3,
            "Искатель ресурсов",
        )

        # self.text(start_x + width + width * (3/4) - 3, start_y + width - 6 , 'ENTP')
        self.text(
            start_x + width + width * (3 / 4) - 9,
            start_y + width - 3,
            "Изобретатель",
        )

        # self.text(start_x + width / 4 - 3, start_y + width + 4 , 'ISFJ')
        # self.text(start_x + width / 4 - 7, start_y + width + 7 , 'Хранитель')
        self.text(start_x + width / 4 - 7, start_y + width + 4, "Хранитель")

        # self.text(start_x + width * (3/4) - 3, start_y + width + 4 , 'INFJ')
        # self.text(start_x + width * (3/4) - 9, start_y + width + 7 , 'Вдохновитель')
        self.text(
            start_x + width * (3 / 4) - 9,
            start_y + width + 4,
            "Вдохновитель",
        )

        # self.text(start_x + width + width / 4 - 3, start_y + width + 4 , 'ISTJ')
        # self.text(start_x + width + width / 4 - 8, start_y + width + 7 , 'Организатор')
        self.text(
            start_x + width + width / 4 - 6,
            start_y + width + 4,
            "Организатор",
        )

        # self.text(start_x + width + width * (3/4) - 3, start_y + width + 4 , 'INTJ')
        # self.text(start_x + width + width * (3/4) - 14, start_y + width + 7 , 'Любитель улучшений')
        self.text(
            start_x + width + width * (3 / 4) - 14,
            start_y + width + 4,
            "Любитель улучшений",
        )

        # self.text(start_x + width / 4 - 3, start_y + width + width - 6 , 'ISFP')
        # self.text(start_x + width / 4 - 7, start_y + width + width - 3 , 'Посредник')
        self.text(
            start_x + width / 4 - 5,
            start_y + width + width - 3,
            "Опекун",
        )

        # self.text(start_x + width * (3/4) - 3, start_y + width + width - 6 , 'INFP')
        self.text(
            start_x + width * (3 / 4) - 16,
            start_y + width + width - 3,
            "Благородный служитель",
        )

        # self.text(start_x + width + width / 4 - 3, start_y + width + width - 6 , 'ISTP')
        # self.text(start_x + width + width / 4 - 12, start_y + width + width - 3 , 'Экспериментатор')
        self.text(
            start_x + width + width / 4 - 9,
            start_y + width + width - 3,
            "Исполнитель",
        )

        # self.text(start_x + width + width * (3/4) - 3, start_y + width + width - 6 , 'INTP')
        self.text(
            start_x + width + width * (3 / 4) - 12,
            start_y + width + width - 3,
            "Решатель проблем",
        )

        self.set_line_width(0.5)
        self.set_draw_color(240)

        pass

    def draw_section_header(self, text: str):
        self.set_fill_color(230, 230, 227)
        self.set_draw_color(230, 230, 227)
        rect_width = 210
        rect_height = 8
        self.rect(self.x, self.y, rect_width, rect_height, "FD")
        self.set_text_color(118, 134, 146)
        self.cell(h=rect_height, txt=text, new_y=YPos.NEXT, new_x=XPos.LEFT)

    def draw_group_profile_square(
        self,
        square: SquareId,
        results: List[int],
        base_y: float,
        color: Dict[int, Tuple[int, int, int]] = None,
    ):
        config = SQUARE_UI_CONFIG[square]
        width = (self.w - self.l_margin - self.r_margin) / 4

        self.set_xy(self.l_margin + config.x * width, base_y + config.y * width)

        self.set_draw_color(240, 100, 40)

        width -= 4
        start_x = self.x + 2
        start_y = self.y + 7
        self.set_xy(start_x, start_y)
        self.set_text_font(7)
        n_per_line = 8
        padding = 1
        text_width = width / n_per_line - padding
        self.set_x(self.x + padding)
        for participant_id in results:
            print(f"Trying to draw {participant_id} in {square} square")
            print(f"{self.x} + {text_width} > {start_x} + {width}, {padding}")
            if int(self.x + text_width) > int(start_x + width):
                self.set_xy(start_x + padding, self.y + text_width + padding)

            self.set_draw_color(*color[participant_id])
            self.set_fill_color(*color[participant_id])
            self.circle(
                self.x,
                self.y,
                text_width,
                style="FD",
            )
            self.cell(
                w=text_width,
                h=text_width,
                txt=str(participant_id),
                new_x=XPos.LEFT,
                new_y=YPos.TOP,
                align=Align.C,
            )
            self.set_x(self.x + text_width + padding)
            print(f"Drawn {participant_id} in {square} square with width {text_width}")
            pass

        pass
