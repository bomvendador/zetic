import os
from dataclasses import dataclass
from typing import List

from fpdf import XPos, YPos

from pdf.single_report import SingleReportData
from pdf.translations import TRANSLATIONS_DICT
from pdf.zetic_pdf import ZeticPDF, BLOCK_R, BLOCK_G, BLOCK_B, PDF_MODULE_BASE_DIR


@dataclass
class SquareResult:
    group_name: str
    group_color: str
    name: str
    email: str
    bold: bool
    idx: int
    single_report_data: SingleReportData

    @staticmethod
    def from_client_list(
        data: List[str], idx: int, single_report_data: SingleReportData
    ):
        return SquareResult(
            group_name=data[4],
            group_color=data[6],
            email=data[1],
            name=data[2],
            bold=data[3] == "1",
            idx=idx,
            single_report_data=SingleReportData(),
        )
        pass


@dataclass
class GroupReportData:
    lang: str
    project_name: str

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

        # 17
        pdf.set_text_font(9)

        # x is reset to pdf.l_margin
        pdf.set_y(pdf.get_y() + 5)

        text = TRANSLATIONS_DICT.get_translation("group_report_description", lang)
        pdf.multi_cell(0, 4, text)

        pdf.set_label_font(9)

        pdf.set_y(pdf.get_y() + 20)

        text_label = TRANSLATIONS_DICT.get_translation("Предприниматель", lang)
        text = TRANSLATIONS_DICT.get_translation("Предприниматель Описание", lang)

        pdf.paragraph_with_bold_start(
            paragraph_label=text_label,
            paragraph_text=text,
            paragraph_label_size=9,
            paragraph_text_size=8,
        )

        pdf.set_text_font(9)

        pdf.set_y(pdf.get_y() + 5)
        text = (
            "• Контролер – практичный, инициативный, высокоорганизованный и целеустремленный. Имеет твердые жизненные "
            "убеждения и старается жить и работать согласно своим высоким стандартам. Эффективно управляет работой, планирует "
            "и последовательно работает на развитие бизнеса. Держит свои обещания и ждут этого от других.\n"
            "• Изобретатель – обладает острым умом, широкой базой познаний и способностью объединять разрозненные элементы "
            "в единые решения. Находится в постоянном поиске знаний, создания сложных интеллектуальных решений, готов подвергать "
            "сомнению общепринятый образ мышления. Не практичен, не терпит рутины. Недисциплинирован, выполняет задачи скачкообразно.\n"
            "• Аналитик – обладает аналитическим мышлением, четко видит будущее и стремится реализовывать процессы максимально "
            "эффективно. Настойчив, упрям, ориентирован на развитие, может не уделять внимание чувствам и переживаниям других.\n"
            "• Искатель ресурсов - авантюрный, активный, быстрый. Легко ориентируется в мелких деталях, фактах, цифрах. "
            "Недисциплинирован, может отклоняться от плана, способен эффективно действовать в экстремальных ситуациях, исправляет"
            " свои ошибки по пути.  Проницателен, быстро считывает пространство и людей, подстраивается под изменения."
        )

        pdf.multi_cell(0, 4, text)

        #     else:
        #         y += 15
        #         pdf.set_xy(x+5, y)
        #         text = u'''
        # • The section K measures the basic personality traits and its influence of business behavior and performance.
        # • The section С describes the basic reactions on stress, actions taken by a person to cope with the new worries, to adapt to tension and to find a way out of a traumatic situation.
        # • The section B reflects the psychological factors that lead to burnout, the burnout indicator and intensity.
        # • The section V describes the universal well-established needs and life priorities of the individual that influence decisions and choices.
        # '''
        #         pdf.multi_cell(0, 5, text)

        pdf.set_label_font(9)

        pdf.set_y(pdf.get_y() + 5)

        text_label = "Производитель"
        text = (
            "                – роль обеспечивает результативность в краткосрочном аспекте. Действия направлены "
            "на решение операционных «горящих» задач максимально быстро. Сотрудники в этой роли проявляют нетерпеливость, "
            "продуктивность и прагматичность, внутреннюю жесткость. Предрасположены к действию больше, чем к размышлениям и "
            "анализу. Склонны действовать по одиночке. Получают удовлетворение от собственной вовлеченности в работу и достижения результатов."
        )
        pdf.paragraph_with_bold_start(text_label, text, 9, 8)
        # else:
        #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
        #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
        #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
        #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'

        # else:
        #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
        #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
        #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
        #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'
        # pdf.multi_cell(0, 4, text)

        pdf.set_text_font(9)
        # 30

        # if lang == 'ru':
        pdf.set_y(pdf.get_y() + 5)
        text = (
            "• Организатор – фокусируется на последовательном выполнении задач, предпочитает ясность и четкую организацию. "
            "Склонен игнорировать чувства в пользу логики и фактов. Ориентируется в мелких деталях и цифрах. Способен четко "
            "и внимательно контролировать работу и результаты.\n"
            "• Любитель улучшений – рациональный, логичный, целеустремленный. Стремится к совершенству систем и процессов, "
            "ориентирован на поиск возможностей для улучшений, высокопродуктивен. Склонен игнорировать чувства в пользу фактов и "
            "цифр. Быстро принимает решения и реализует их, четко организует работу команды.\n"
            "• Решатель проблем - проявляется как высокомерный и критичный к другим. Действует скачкообразно, может"
            " отклоняться от плана. Находит быстрые, элегантные решения сложных задач. Нацелен на действие, а не на коммуникации.\n"
            "• Исполнитель - погружен в предметную область, прагматичен, стремится понять логику и механизм работы. "
            "С удовольствием сам будет выполнять работу и включаться в детали, делиться опытом с другими. Настойчив, доводит"
            " работу до конца. Слонен быть недисциплинированным, достигать цели в последний момент."
        )

        pdf.multi_cell(0, 4, text)

        #     else:
        #         y += 15
        #         pdf.set_xy(x+5, y)
        #         text = u'''
        # • The section K measures the basic personality traits and its influence of business behavior and performance.
        # • The section С describes the basic reactions on stress, actions taken by a person to cope with the new worries, to adapt to tension and to find a way out of a traumatic situation.
        # • The section B reflects the psychological factors that lead to burnout, the burnout indicator and intensity.
        # • The section V describes the universal well-established needs and life priorities of the individual that influence decisions and choices.
        # '''
        #         pdf.multi_cell(0, 5, text)

        pdf.set_label_font(9)

        pdf.set_y(pdf.get_y() + 5)
        # if lang == 'ru':
        text_label = "Администратор"
        text = (
            "                                – роль обеспечивает эффективность, технологичность, стандартизацию в краткосрочном аспекте. "
            "Этим сотрудникам свойственно унифицировать работу, структурировать информацию и процессы, следить за порядком, "
            "согласовывать и поддерживать единые правила работы. Как правило они стремятся мыслить линейно, действовать "
            "осторожно и дисциплинировано, обращать внимание на мелкие детали."
        )
        pdf.paragraph_with_bold_start(text_label, text, 9, 8)
        # else:
        #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
        #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
        #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
        #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'

        # else:
        #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
        #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
        #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
        #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'

        pdf.set_text_font(9)
        # 30

        # if lang == 'ru':
        pdf.set_y(pdf.get_y() + 5)
        text = (
            "• Хранитель – обладает развитыми навыками общения, считывает пространство и команду, чуток к состоянию команды."
            " Внимателен к деталям, мыслит от частного к общему, педантичен, проявляет перфекционизм. Воспринимает рабочие "
            "обязанности как личную ответственность, стремится выполнять их больше и лучше, чем ожидается.\n"
            "• Вдохновитель – чуткий и проницательный, вносит гармонию в общение между людьми. Склонен идеализировать мир, "
            "верить в счастливое будущее. Ориентируется на формирование экологичных, гуманистичных, системных решений. "
            "Действует дисциплинировано и аккуратно.\n"
            "• Опекун – обладает художественным восприятием и развитым вкусом, открыт к изменениям и экспериментам, "
            "не любит рутину. Находит правильные слова для создания доверительной коммуникации, выстраивает теплое общение "
            "с другими, чуток и тактичен. Готов поддерживать и помогать в развитии другим.\n"
            "• Благородный служитель – формирует глубокую и продуманную систему моральных принципов и долга. Обладает "
            "очень хорошей интуицией и творческим чутьем. Располагает к себе, сглаживает острые углы. Ценит возможность быть "
            "частью коллектива и может жертвовать своими интересами ради других. Проявляется как вдумчивый, но не "
            "дистиллированный и непоследовательный."
        )

        pdf.multi_cell(0, 4, text)

        #     else:
        #         y += 15
        #         pdf.set_xy(x+5, y)
        #         text = u'''
        # • The section K measures the basic personality traits and its influence of business behavior and performance.
        # • The section С describes the basic reactions on stress, actions taken by a person to cope with the new worries, to adapt to tension and to find a way out of a traumatic situation.
        # • The section B reflects the psychological factors that lead to burnout, the burnout indicator and intensity.
        # • The section V describes the universal well-established needs and life priorities of the individual that influence decisions and choices.
        # '''
        #         pdf.multi_cell(0, 5, text)

        # pdf.add_page()
        pdf.set_y(pdf.get_y() + 5)

        pdf.set_label_font(9)

        # if lang == 'ru':
        text_label = "Интегратор"
        text = (
            "           – роль направлена на создание целостной организации, формирование единого видения, "
            "правильного организационного климата и культуры, системы ценностей, которые будут стимулировать людей действовать"
            " сообща, позволят вплетать цели каждого в цели группы и бизнеса в целом. Представители этой роли социально активны, "
            "стремятся к коммуникации и кросс-функциональному взаимодействию, склонны к эмпатии, умеют выслушать и поддержать, "
            "формируют атмосферу взаимного уважения в коллективе."
        )
        pdf.paragraph_with_bold_start(text_label, text, 9, 8)
        # else:
        #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
        #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
        #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
        #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'

        # else:
        #     text = u'Based on decades of academic research Zetic has developed a tool for scientific personality measurement ' \
        #            u'for business. The tool can be used for a variety of recruitment and development purposes. The approach was ' \
        #            u'tested on a large sample of executives over several years. Our study of resilience and stress behavior has ' \
        #            u'become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:'

        pdf.set_text_font(9)
        # 30

        # if lang == 'ru':
        pdf.set_y(pdf.get_y() + 5)
        text = (
            "• Массовик-затейник – стремится быть в центре внимания, принимает на себя лидерскую роль, пользуется "
            "поддержкой других. Практичный, внимательный к деталям. Умеет планировать и дисциплинировано реализовывать работу.\n"
            "• Чуткий наставник - выстраивает крепкие отношения с коллегами, заботится о людях. Мыслит широко и интуитивно. "
            "Умеет планировать и дисциплинировано реализовывать работу. Формирует эффективные процессы, в которых люди могут "
            "комфортно работать.\n"
            "• Развлекатель – практичный, оптимистичный, спонтанный. Воспринимает мир и работу как игру, воодушевляет "
            "этим окружающих. Легко адаптируется к переменам, решает проблемы по мере их возникновения. Наблюдателен и прозорлив, "
            "тонко чувствует состояние людей, проявляет активный интерес и всегда готов прийти на помощь.\n"
            "• Мотиватор - открыт, любит говорить о людях и делиться планами. С удовольствием обсуждает собственные смелые"
            " идеи и фантазии. Ищет свободы, спонтанности и возможности для творчества. Склонен смотреть на жизнь как на большую "
            "сложную головоломку, видеть ее через призму интуиции, эмоций, сострадания, всегда пытается добиться более глубокого понимания."
        )

        pdf.multi_cell(0, 4, text)

        #     else:
        #         y += 15
        #         pdf.set_xy(x+5, y)
        #         text = u'''
        # • The section K measures the basic personality traits and its influence of business behavior and performance.
        # • The section С describes the basic reactions on stress, actions taken by a person to cope with the new worries, to adapt to tension and to find a way out of a traumatic situation.
        # • The section B reflects the psychological factors that lead to burnout, the burnout indicator and intensity.
        # • The section V describes the universal well-established needs and life priorities of the individual that influence decisions and choices.
        # '''
        #         pdf.multi_cell(0, 5, text)
        self._insert_page_number(pdf)
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
