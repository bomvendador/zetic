from pdf.draw import insert_page_number

from pdf.models import Participant, Company, TrafficLightReportFilter, TrafficLightReportFilterCategory, Questionnaire, \
    Report, ReportDataByCategories, QuestionnaireQuestionAnswers, QuestionAnswers
from django.db.models import Q

from numpy import arange, array, cos, log, pi, sin, sqrt

from bokeh.models import ColumnDataSource, Legend, LegendItem
from bokeh.plotting import figure, show, save, output_file
from bokeh.io import export_png, export_svg
from bokeh.io.export import get_screenshot_as_png

from bokeh.sampledata.antibiotics import data as df
from bokeh import sampledata
import pandas as pd
import chromedriver_binary
import time
from .raw_to_t_point import get_t_point, filter_raw_points_to_t_points
from .page2_file import draw_lie_scale

from webdriver_manager.chrome import ChromeDriverManager
import os
from reports.settings import DEBUG
from pdf_group.page_funcs import block_name_
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y


# from selenium.webdriver import Chrome, ChromeOptions
#
# options = ChromeOptions()
#
# options.add_argument('--headless')
# options.add_argument("--window-size=2000x2000")
# metrics = { "deviceMetrics": { "pixelRatio": 1.0 } }
# options.add_experimental_option("mobileEmulation", metrics)
# web_driver = Chrome(chrome_options=options)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


if DEBUG == 0:
#     # driver_path = ChromeDriverManager().install()
#     # os.environ["BOKEH_CHROMEDRIVER_PATH"] = driver_path
#     os.environ["BOKEH_CHROMEDRIVER_PATH"] = '/usr/bin/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    web_driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)


def page_circle_diagram_descriptions(pdf, lang):
    pdf.add_page()
    pdf.set_auto_page_break(False)

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
    traffic_light_filters = TrafficLightReportFilter.objects.filter(project=None).order_by('position')

    y = pdf.get_y() + 10
    pdf.set_xy(x, y)

    for traffic_light_filter in traffic_light_filters:
        name = traffic_light_filter.name
        description = traffic_light_filter.description
        if description:
            y = pdf.get_y() + 5
            pdf.set_xy(x, y)

            block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, str(name).upper())
            pdf.set_text_color(0, 0, 0)

            y = pdf.get_y() + 12
            pdf.set_xy(x, y)

            pdf.multi_cell(0, 4, description, align='J')
    insert_page_number(pdf)


def page_circle_diagram(pdf, questionnaire_id, report_id, lang):
    pdf.set_auto_page_break(False)

    x = 12
    y = 12
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    # pdf.set_font("RalewayLight", "", 9)
    if lang == 'ru':
        pdf.cell(0, 0, 'Круговая диаграмма')
    else:
        pdf.cell(0, 0, 'Short conclusions')

    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + 5, x + 220, y + 5)
    questionnaire = Questionnaire.objects.get(id=questionnaire_id)
    traffic_light_report_filter = TrafficLightReportFilter.objects.filter(project=None).order_by('position')
    potential_indicator = 0
    potential_text = 0
    data_for_circle = []
    for traffic_light_filter in traffic_light_report_filter:
        total_t_points = 0


        traffic_light_report_filter_categories = TrafficLightReportFilterCategory.objects.filter(filter=traffic_light_filter)
        for filter_category in traffic_light_report_filter_categories:
            if report_id != '':
                report = Report.objects.get(id=report_id)
                report_data_by_categories_inst = ReportDataByCategories.objects.filter(Q(report=report) & Q(category_code=filter_category.category.code))
                if report_data_by_categories_inst:
                    report_data_by_categories_inst = report_data_by_categories_inst.latest('created_at')
                    # report_data_by_categories_inst = ReportDataByCategories.objects.filter(Q(report=report) & Q(category_code=filter_category.category.code)).latest('created_at')
                    t_point = report_data_by_categories_inst.t_points
                    total_t_points = total_t_points + t_point
            else:
                raw_points = 0
                questionnaire = Questionnaire.objects.get(id=questionnaire_id)
                questionnaire_question_answers = QuestionnaireQuestionAnswers.objects.filter(Q(questionnaire=questionnaire) &
                                                                                             Q(question__category__code=filter_category.category.code))

                for questionnaire_question_answer in questionnaire_question_answers:
                    raw_points = raw_points + questionnaire_question_answer.answer.raw_point
                t_point = filter_raw_points_to_t_points(raw_points, questionnaire.participant.employee.id, filter_category.category.id)
                # t_point = get_t_point(raw_points, filter_category.category.code, questionnaire.participant.employee.sex.name_ru, questionnaire.participant.employee.birth_year)
                total_t_points = total_t_points + int(t_point)
        average_t_points = round(total_t_points / len(traffic_light_report_filter_categories))
        if traffic_light_filter.for_circle_diagram:
            potential_indicator = average_t_points
            if traffic_light_filter.points_from_red <= int(average_t_points) <= traffic_light_filter.points_to_red:
                potential_text = traffic_light_filter.circle_diagram_description_red
            if traffic_light_filter.points_from_yellow <= int(average_t_points) <= traffic_light_filter.points_to_yellow:
                potential_text = traffic_light_filter.circle_diagram_description_yellow
            if traffic_light_filter.points_from_green <= int(average_t_points) <= traffic_light_filter.points_to_green:
                potential_text = traffic_light_filter.circle_diagram_description_green

        data_for_circle.append({
            'average_t_points': average_t_points,
            'filter_name': traffic_light_filter.name,
        })
    print(data_for_circle)
    draw_circle_diagram(pdf, data_for_circle)
    print(f'y = {y}')
    y = y + pdf.epw
    pdf.set_xy(x, y)
    pdf.cell(0, 0, 'Индикатор потенциала')
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + 5, x + 220, y + 5)
    text = u'Потенциал - совокупность особых способностей и личностных качеств, позвлояющих эффективно справляться с рабочими ' \
           u'задачами и прогнозировать успех человека в ситуации изменений '

    # text = '''
    # Потенциал - совокупность особых способностей и лисночтных качеств, позвлояющих эффективно справляться с рабочими задачами и прогнозировать успех челоовека
    # в ситуации изменений
    # '''

    pdf.set_font("RalewayLight", "", 9)
    y = pdf.get_y()
    pdf.set_xy(x, y + 10)
    pdf.multi_cell(190, 4, text)

    y = pdf.get_y() + 10
    pdf.set_xy(x, y)
    draw_potential_scale(pdf, x + 2, y + 1, 70, 10, potential_indicator, 'media/images/kettel_page3.png')
    text = u'Уровень потенциала отражается на шкале от 0 до 10. ' \
           u'Зелеными рамками выделены средние показатели потенциала' \
           u' на рынке труда для данной категории персонала'

    pdf.set_font("RalewayBold", "", 11)
    pdf.set_xy(x + 78, y)
    pdf.cell(5, 12, str(potential_indicator), ln=0)

    pdf.set_font("RalewayLight", "", 9)
    pdf.set_xy(x + 90, y)
    # pdf.cell(60, 12, text, ln=0)
    pdf.multi_cell(100, 4, text)

    y = pdf.get_y() + 15
    pdf.set_xy(x, y)
    pdf.multi_cell(190, 4, str(potential_text))

    insert_page_number(pdf)

    page_circle_diagram_descriptions(pdf, lang)


def draw_circle_diagram(pdf, data_for_circle):
    wedges_names = []
    t_points = []
    indexes = []
    cnt = 0
    wedges_names_colors = []
    for data in data_for_circle:
        indexes.append(cnt)
        cnt = cnt + 1
        wedges_names.append(data['filter_name'])
        t_points.append(data['average_t_points'])
        wedges_names_colors.append('negative')
    print(indexes)
    print(wedges_names)
    print(wedges_names_colors)
    print(t_points)
    # DRUGS = ("penicillin", "streptomycin")
    # DRUGS = ("Баллы")
    COLORS = ("#0d3362", "#c64737", "#000000")
    GRAM = dict([
        ("negative", "#00a5ff"),
        ("positive", "#aeaeb8"),
    ])

    # print(type(df.bacteria))

    # d = {
    #     'bacteria': ['Вовлеченность, выгорание', 'Гибкость', 'Достижение результатов', 'Обучаемость, потенциал',
    #                  'Переговорные навыки', 'Принятие решений', 'Развитие бизнеса', 'Сотрудничество', 'Стратегичность',
    #                  'Устойчивость', 'Эффективное управление'],
    #     't_points': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    #     # 'streptomycin': [5, 0.8, 0.1, 1.2],
    #     'gram': ['negative', 'negative', 'negative', 'negative', 'negative', 'negative', 'negative', 'negative', 'negative',
    #              'negative', 'negative'],
    # }
    d = {
        'wedges_names': wedges_names,
        't_points': t_points,
        # 'streptomycin': [5, 0.8, 0.1, 1.2],
        'gram': wedges_names_colors,
    }
    # index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    index = indexes

    df = pd.DataFrame(data=d, index=index)

    # print(df)
    # for row in df.bacteria:
    #     print(row)

    big_angle = 2 * pi / (len(df))
    angles = pi / 2 - 3 * big_angle / 2 - array(df.index) * big_angle

    # print(f'angles')
    # print(angles)
    # print(f'big_angle')
    # print(big_angle)

    df["start"] = angles
    df["end"] = angles + big_angle
    df["colors"] = [GRAM[gram] for gram in df.gram]

    source = ColumnDataSource(df)

    print(source)
    # Burtin's unusual inverted radial sqrt-log scale
    micmin = sqrt(log(.001 * 1E4))
    micmax = sqrt(log(1000 * 1E4))


    # def scale(mic):
    #     return - sqrt(log(mic * 1E4)) + (micmin + micmax)
    #

    p = figure(
        width=1000, height=1000, title=None, tools="", toolbar_location=None,
        x_axis_type=None, y_axis_type=None, match_aspect=True,
        min_border=0, outline_line_color=None, background_fill_color="#ffffff",


    )

    # large wedges for bacteria
    br = p.annular_wedge(0, 0, micmax, micmin, "start", "end", fill_color="colors", line_color="#ffffff", source=source)

    # circular axes and labels
    # radii = scale(10.0 ** arange(-3, 4))
    # print(radii)
    step = 0.25
    start_radius = 4
    radii = []
    for r in range(1, 11):
        radii.append(start_radius - (r * step))
    # radii = [, , 3, 2.5, 2, 1.5]
    p.circle(0, 0, radius=radii, fill_color=None, line_color="#ffffff")
    # p.text(
    #     0, radii, ["10", "9", "8", "7", "6", "5", "4", "3", "2", "1"],
    #     text_font_size="12px", anchor="center",
    # )

    # small wedges for drugs
    # определяет размер и положение шкал внутри круга
    small_angle = big_angle / 30
    # for i, drug in enumerate(DRUGS):
    start = angles + (5) * small_angle
    end = angles + (25) * small_angle
    t_points = d['t_points']
    t_points_for_diagram = []
    colors_for_diagram = []
    start_radius = 1.5
    for t_point in t_points:
        t_points_for_diagram.append(start_radius + (t_point * step))
        if t_point == 0:
            colors_for_diagram.append('#fffff')
        else:
            colors_for_diagram.append('#0d3362')
    p.annular_wedge(
        0, 0, micmin, t_points_for_diagram, start, end,
        color=colors_for_diagram, line_color='#ffffff'
    )
    # p.annular_wedge(
    #     0, 0, micmin, scale(df[DRUGS]), start, end,
    #     color="#0d3362", line_color=None, legend_label=DRUGS,
    # )

    # bacteria labels
    # подписи секторов круга
    r = radii[0] * 1.35
    xr = r * cos(angles + big_angle / 2)
    yr = r * sin(angles + big_angle / 2)
    p.text(
        xr, yr, ["\n".join(x.split()) for x in df.wedges_names],
        text_font_size="22px", anchor="center", text_align='center'
    )

    # p.legend.location = "center"
    # p.legend.background_fill_alpha = 0
    # p.legend.glyph_width = 45
    # p.legend.glyph_height = 20

    p.x_range.range_padding = 0.3
    p.y_range.range_padding = 0.3

    p.grid.grid_line_color = '#ffffff'

    # legend = Legend(items=[
    #     LegendItem(label="Gram-positive", renderers=[br], index=10),
    #     LegendItem(label="Gram-negative", renderers=[br], index=0),
    # ], location="bottom", orientation="horizontal", background_fill_alpha=0)
    # p.add_layout(legend, 'center')

    # driver = webdriver.Firefox(service=FirefoxService(
    #     r'C:/Users/Алексей/AppData/Local/Programs/Python/Python310/geckodriver.exe')
    # )
    # save(p, '2/eeeee.html')
    name = 'pdf/images/plot' + str(time.time()) + '.png'
    # export_png(p, filename=name, scale_factor=1, width=500, height=500)
    if DEBUG == 0:
        export_png(p, filename=name, webdriver=web_driver)
    else:
        # driver = webdriver.Firefox(executable_path=r'D:\projects\bokeh\geckodriver.exe')

        options = Firefox_Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        cap = DesiredCapabilities().FIREFOX
        cap["marionette"] = False
        driver = webdriver.Firefox(capabilities=cap, executable_path=r'D:\projects\bokeh\geckodriver.exe', options=options)

        export_png(p, filename=name, webdriver=driver)

    pdf.image(name, x=20, y=18, h=pdf.epw*0.9)


def draw_potential_scale(pdf, x, y, w, h, lie_points, img_link):
    pdf.set_line_width(0.3)
    pdf.set_fill_color(230, 230, 230)

    pdf.rect(x, y, w, h, 'F')

    pdf.set_draw_color(146, 208, 80)
    pdf.rect(x-1+29.1-6.9, y-1, 6.9*4, h+2)

    # pdf.set_draw_color(255, 0, 0)
    # pdf.rect(x-1+29.1, y-1, 43, h+2)

    for i in range(lie_points):
        pdf.image(img_link, x=x+1, y=y+1, w=5.9)
        x += 5.9 + 1
