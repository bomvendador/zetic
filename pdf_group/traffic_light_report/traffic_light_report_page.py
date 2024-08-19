import math

from pdf.draw import insert_page_number
from pdf_group.traffic_light_report.draw import draw_traffic_light_report_table


def page(pdf, lang, square_results):
    # questionnaire_inst = Questionnaire.objects.filter(participant__employee__email=participant_email).latest('created_at')
    pdf.set_auto_page_break(False)

    x = 12
    y = 12
    pdf.set_xy(x,y)
    pdf.set_font("RalewayBold", "", 10)

    # if lang == 'ru':
    pdf.cell(0, 0, 'Сводные данные по ключевым характеристикам')
    # else:
    #     pdf.cell(0, 0, 'Section K')
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.1)

    y = y + 5
    pdf.line(x + 1, y, x + 220, y)

    y = y + 5
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.set_font("RalewayLight", "", 10)
    pdf.set_xy(x, y)
    text = u'Данная таблица визуально отражает результаты оценки участников по ключевым шкалам. Формат «светофора» ' \
           u'обозначает наиболее слабые и наиболее сильные компетенции у участников. Данные формируются автоматически ' \
           u'на основе результатов заполнения опросника.'

    pdf.multi_cell(0, 4, text)

    pdf.line(x + 1, pdf.get_y() + 4, x + 220,  pdf.get_y() + 4)

    draw_traffic_light_report_table(pdf, lang, x, y, square_results)

    insert_page_number(pdf)
