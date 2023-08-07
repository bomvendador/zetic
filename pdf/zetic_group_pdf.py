import os
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Dict, List

from fpdf.enums import Align, XPos, YPos

from pdf.single_report import SectionData
from pdf.zetic_pdf import ZeticPDF, PDF_MODULE_BASE_DIR


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
    burnout_color: Tuple[int, int, int] = (241, 151, 15)
    crown: int = 0
    cron_image: str = os.path.join(PDF_MODULE_BASE_DIR, "images", "crown.png")


@dataclass
class GroupReportData:
    lang: str
    project_name: str

    group_data: Dict[str, GroupData]
    participant_data: Dict[str, ParticipantData]

    square_results: Dict[SquareId, List[int]]
    cattell_data: Dict[str, SectionData]
    coping_data: Dict[str, SectionData]
    boyko_data: Dict[str, SectionData]
    values_data: Dict[str, SectionData]


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
    SquareId.ENTJ_2_2: SquareUiConfig(x=3, y=0, name="Аналитик"),
    SquareId.ESTP_2_3: SquareUiConfig(x=2, y=1, name="Искатель ресурсов"),
    SquareId.ENTP_2_4: SquareUiConfig(x=3, y=1, name="Изобретатель"),
    SquareId.ISFJ_3_1: SquareUiConfig(x=0, y=2, name="Хранитель / Визионер"),
    SquareId.INFJ_3_2: SquareUiConfig(x=1, y=2, name="Вдохновитель / Авантюрист"),
    SquareId.ISFP_3_3: SquareUiConfig(x=0, y=3, name="Опекун / Искатель ресурсов"),
    SquareId.INFP_3_4: SquareUiConfig(
        x=1, y=3, name="Благородный служитель /Изобретатель"
    ),
    SquareId.ISTJ_4_1: SquareUiConfig(x=2, y=2, name="Организатор"),
    SquareId.INTJ_4_2: SquareUiConfig(x=3, y=2, name="Любитель улучшений"),
    SquareId.ISTP_4_3: SquareUiConfig(x=2, y=3, name="Реализатор"),
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

        self.set_light_font(8)
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

        self.text(start_x + width / 4 - 13, start_y + 4, "Массовик-затейник")

        self.text(start_x + width * (3 / 4) - 12, start_y + 4, "Чуткий наставник")

        self.text(start_x + width + width / 4 - 8, start_y + 4, "Контролер")

        self.text(start_x + width + width * (3 / 4) - 5, start_y + 4, "Аналитик")

        self.text(
            start_x + width / 4 - 9,
            start_y + width - 3,
            "Развлекатель",
        )

        self.text(
            start_x + width * (3 / 4) - 7,
            start_y + width - 3,
            "Мотиватор",
        )

        self.text(
            start_x + width + width / 4 - 12,
            start_y + width - 3,
            "Искатель ресурсов",
        )

        self.text(
            start_x + width + width * (3 / 4) - 9,
            start_y + width - 3,
            "Изобретатель",
        )

        self.text(start_x + width / 4 - 7, start_y + width + 4, "Хранитель")

        self.text(
            start_x + width * (3 / 4) - 9,
            start_y + width + 4,
            "Вдохновитель",
        )

        self.text(
            start_x + width + width / 4 - 6,
            start_y + width + 4,
            "Организатор",
        )

        self.text(
            start_x + width + width * (3 / 4) - 14,
            start_y + width + 4,
            "Любитель улучшений",
        )

        self.text(
            start_x + width / 4 - 5,
            start_y + width + width - 3,
            "Опекун",
        )

        self.text(
            start_x + width * (3 / 4) - 16,
            start_y + width + width - 3,
            "Благородный служитель",
        )

        self.text(
            start_x + width + width / 4 - 9,
            start_y + width + width - 3,
            "Исполнитель",
        )

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
        participant_data: Dict[int, ParticipantData] = None,
    ):
        config = SQUARE_UI_CONFIG[square]
        width = (self.w - self.l_margin - self.r_margin) / 4

        self.set_xy(self.l_margin + config.x * width, base_y + config.y * width)

        # Draw square title
        # self.set_text_color(240, 100, 40)
        # self.cell(w=width, h=4, txt=config.name, new_y=YPos.TOP, new_x=XPos.LEFT)

        width -= 4
        start_x = self.x + 2
        start_y = self.y + 8.5
        self.set_xy(start_x, start_y)
        self.set_text_font(7)
        n_per_line = 8
        padding = 1
        v_padding = 3
        text_width = width / n_per_line - padding
        self.set_x(self.x + padding)
        for participant_id in results:
            if int(self.x + text_width) > int(start_x + width):
                self.set_xy(start_x + padding, self.y + text_width + v_padding)

            participant = participant_data[participant_id]

            circle_x = self.get_x() + text_width / 2
            circle_y = self.get_y()
            self.set_xy(circle_x, circle_y)
            self.draw_participant_circle(
                participant=participant,
                x=circle_x,
                y=circle_y,
                w=3,
                color=color[participant_id],
            )
            self.set_x(circle_x + text_width / 2 + padding)
            pass

        pass

    def draw_participant_circle(
        self,
        participant: ParticipantData,
        x: float,
        y: float,
        w: float,
        color: Tuple[int, int, int],
    ):
        self.set_draw_color(*color)
        self.set_fill_color(*color)
        if participant.burnout:
            self.set_draw_color(*participant.burnout_color)
            pass

        if participant.crown:
            self.image(
                name=participant.cron_image,
                x=x + w / 2,
                y=y - w,
                w=w,
            )
            pass

        self.circle(
            x,
            y,
            w,
            style="FD",
        )

        self.set_text_font(6)
        self.cell(
            w=w,
            h=w,
            txt=str(participant.id),
            new_x=XPos.LEFT,
            new_y=YPos.TOP,
            align=Align.C,
        )
        pass
