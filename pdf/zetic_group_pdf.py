from typing import Tuple

from fpdf.enums import Align, XPos, YPos

from pdf.zetic_pdf import ZeticPDF


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
