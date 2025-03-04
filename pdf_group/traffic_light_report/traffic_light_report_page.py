import math

from pdf.models import TrafficLightReportFilter
from pdf.draw import insert_page_number
from pdf_group.traffic_light_report.draw import draw_traffic_light_report_table
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y
from pdf_group.page_funcs import block_name_


def page(pdf, lang, json):
    square_results = json['square_results']
    # questionnaire_inst = Questionnaire.objects.filter(participant__employee__email=participant_email).latest('created_at')
    pdf.set_auto_page_break(False)
    project_id = json['project_id']

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

    draw_traffic_light_report_table(pdf, lang, x, y, square_results, project_id)

    insert_page_number(pdf)

    page_traffic_light_descriptions(pdf, lang, project_id)


def page_traffic_light_descriptions_title(pdf, lang):
    x = 12
    y = 12
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    # pdf.set_font("RalewayLight", "", 9)
    if lang == 'ru':
        pdf.cell(0, 0, 'Определение компетенций')
    else:
        pdf.cell(0, 0, 'Short conclusions')
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + 5, x + 220, y + 5)


def page_traffic_light_descriptions(pdf, lang, project_id):
    pdf.add_page()
    pdf.set_auto_page_break(False)

    x = 12
    page_traffic_light_descriptions_title(pdf, lang)

    traffic_light_filters = TrafficLightReportFilter.objects.filter(project_id=project_id)
    if not traffic_light_filters.exists():
        traffic_light_filters = TrafficLightReportFilter.objects.filter(project=None)

    y = pdf.get_y() + 5
    pdf.set_xy(x, y)

    for traffic_light_filter in traffic_light_filters:
        name = traffic_light_filter.name
        description = traffic_light_filter.description
        if description:
            if pdf.get_y() >= 250:
                insert_page_number(pdf)
                pdf.add_page()
                page_traffic_light_descriptions_title(pdf, lang)
                y = pdf.get_y() + 5
            else:
                y = pdf.get_y() + 5
            pdf.set_xy(x, y)

            block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, str(name).upper())
            pdf.set_text_color(0, 0, 0)

            y = pdf.get_y() + 10
            pdf.set_xy(x, y)
            pdf.multi_cell(0, 4, description, align='J')
    insert_page_number(pdf)

