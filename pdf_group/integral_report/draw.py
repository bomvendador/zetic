from pdf.models import Report, ReportData, ReportGroup, ReportGroupSquare, IntegralReportFilter, \
    IntegralReportFilterCategory, ReportDataByCategories

from django.db.models import Q
from operator import itemgetter

import math


def draw_integral_report_squares(pdf, lang, start_x, square_results):
    start_X = start_x
    start_Y = 25 + 3
    end_X = 190
    total_width = end_X - start_X
    end_Y = start_Y + total_width
    total_height = end_Y - start_Y

    # зеленый квадрат
    pdf.set_fill_color(226, 239, 218)
    pdf.rect(start_X + total_width / 2, start_Y, total_width / 2, total_height / 2, 'F')

    # красный квадрат
    pdf.set_fill_color(255, 200, 200)
    pdf.rect(start_X + total_width / 2, start_Y + total_height / 2, total_width / 2, total_height / 2, 'F')

    print(f'total_width - {total_width}')
    pdf.set_line_width(0.4)
    pdf.set_draw_color(r=135, g=135, b=135)
    pdf.rect(start_X, start_Y, total_width, total_height, 'D') #обводка

    pdf.set_line_width(0.2)
    pdf.line(start_X, start_Y + total_height / 2, start_X + total_width, start_Y + total_height / 2) #центральная горизонтальная линия
    pdf.line(start_X + total_width / 2, start_Y, start_X + total_width / 2,  start_Y + total_height) #центральная вертикальная линия
    print(f'X вертикальной линии - {start_X + total_width / 2}')

    # pdf.set_line_width(0.1)
    # pdf.line(start_X, start_Y + total_height / 2 / 2, start_X + total_width, start_Y + total_height / 2 / 2) #горизонтальная линия 1/4
    # pdf.line(start_X, start_Y + total_height * (3/4), start_X + total_width, start_Y + total_height * (3/4)) #горизонтальная линия 3/4
    # pdf.line(start_X + total_width / 2 / 2, start_Y, start_X + total_width / 2 / 2,  start_Y + total_height) #вертикальная линия 1/4
    # pdf.line(start_X + total_width * (3/4), start_Y, start_X + total_width * (3/4), start_Y + total_height) #вертикальная линия 3/4

    pdf.set_font("RalewayLight", "", 8)

    # pdf.set_text_color(r=255, g=255, b=255)
    # pdf.set_text_color(r=135, g=135, b=135)
    pdf.set_text_color(118, 134, 146)
    pdf.set_fill_color(r=230, g=230, b=227)
    pdf.set_draw_color(r=230, g=230, b=227)

    pdf.set_line_width(0.4)

    # горизонтальная ось
    pdf.rect(start_X, start_Y + total_height + 0.4, 40, 4, 'FD')
    pdf.text(start_X + 3, start_Y + total_height + 3, 'Низкая согласованность')

    pdf.rect(start_X + total_width - 40, start_Y + total_height + 0.4, 40 + 4 + 0.4, 4, 'FD')
    pdf.text(start_X + total_width - 37, start_Y + total_height + 3, 'Высокая согласованность')

    pdf.set_text_color(r=135, g=135, b=135)
    pdf.text(start_X + total_width / 2 / 2 - 2, start_Y + total_height + 3, '25%')
    pdf.text(start_X + total_width / 2 - 2, start_Y + total_height + 3, '50%')
    pdf.text(start_X + total_width * (3/4) - 2, start_Y + total_height + 3, '75%')

    # вертикальная ось
    pdf.set_text_color(118, 134, 146)

    pdf.rect(start_X + total_width + 0.4, start_Y + total_height - 40, 4, 40, 'FD')
    with pdf.rotation(90, start_X + total_width + 3, start_Y + total_height - 5):
        pdf.text(start_X + total_width + 3, start_Y + total_height - 5, 'Низкая проявленность')

    pdf.rect(start_X + total_width + 0.4, start_Y, 4, 40, 'FD')
    with pdf.rotation(90, start_X + total_width + 3, start_Y + 40 - 4):
        pdf.text(start_X + total_width + 3, start_Y + 40 - 4, 'Высокая проявленность')

    # pdf.text(start_X + total_width - 37, start_Y + total_height + 3, 'Высокая проявленность')

    pdf.set_text_color(r=135, g=135, b=135)

    with pdf.rotation(90, start_X + total_width + 3, start_Y + total_height * (3 / 4) + 2):
        pdf.text(start_X + total_width + 3, start_Y + total_height * (3 / 4) + 2, '25%')
    with pdf.rotation(90, start_X + total_width + 3, start_Y + total_height / 2 + 2):
        pdf.text(start_X + total_width + 3, start_Y + total_height / 2 + 2, '50%')
    with pdf.rotation(90, start_X + total_width + 3, start_Y + total_height / 2 / 2 + 2):
        pdf.text(start_X + total_width + 3, start_Y + total_height / 2 / 2 + 2, '75%')

    # вертикальная ось (стрелка)
    rect_width = total_width
    rect_height = 1
    delta_Y_for_horizontal_arrow = 10
    pdf.rect(start_X, start_Y + total_height + delta_Y_for_horizontal_arrow, rect_width, rect_height, 'FD')
    # отрисовка треугольника
    triangle_width = 2
    point1 = (start_X + rect_width, start_Y + total_height + delta_Y_for_horizontal_arrow - rect_height/2)
    point2 = (start_X + rect_width + triangle_width, start_Y + total_height + delta_Y_for_horizontal_arrow + rect_height / 2)
    point3 = (start_X + rect_width, start_Y + total_height + delta_Y_for_horizontal_arrow + rect_height + rect_height / 2)
    pdf.polygon(point_list=[point1, point2, point3, point1], style="FD")

    pdf.set_fill_color(r=255, g=255, b=255)
    pdf.set_draw_color(r=255, g=255, b=255)
    pdf.rect((start_X + total_width) / 2 - 32, start_Y + total_height + delta_Y_for_horizontal_arrow - 2, 80, 6, 'FD')

    pdf.set_font("RalewayLight", "", 12)
    pdf.text((start_X + total_width) / 2 - 30, start_Y + total_height + delta_Y_for_horizontal_arrow + 2, 'Согласованность ответов участников')

    # горизонтальная ось (стрелка)
    pdf.set_fill_color(r=230, g=230, b=227)
    pdf.set_draw_color(r=230, g=230, b=227)

    pdf.rect(start_X + total_width + delta_Y_for_horizontal_arrow, start_Y + triangle_width, rect_height, rect_width, 'FD')
    # отрисовка треугольника
    point1 = (start_X + total_width + delta_Y_for_horizontal_arrow - rect_height / 2, start_Y + triangle_width)
    point2 = (start_X + total_width + delta_Y_for_horizontal_arrow + rect_height * 1.5, start_Y + triangle_width)
    point3 = (start_X + total_width + delta_Y_for_horizontal_arrow + rect_height / 2, start_Y)
    pdf.polygon(point_list=[point1, point2, point3, point1], style="FD")

    pdf.set_fill_color(r=255, g=255, b=255)
    pdf.set_draw_color(r=255, g=255, b=255)
    pdf.rect(start_X + total_width + delta_Y_for_horizontal_arrow - 2, (start_Y + total_height) / 2 - 40, 6, 110, 'FD')

    pdf.set_font("RalewayLight", "", 12)
    with pdf.rotation(90, start_X + total_width + delta_Y_for_horizontal_arrow + 2, start_Y + total_height / 2 + 53):
        pdf.text(start_X + total_width + delta_Y_for_horizontal_arrow + 2, start_Y + total_height / 2 + 53, 'Проявленность компетенций в сравнении с рынком')

    # pdf.text((start_X + total_width) / 2 - 30, start_Y + total_height + delta_Y_for_horizontal_arrow + 2, 'Согласованность ответов участников')

    # описание матрицы
    y = start_Y + total_height + delta_Y_for_horizontal_arrow + 15

    pdf.set_fill_color(r=230, g=230, b=227)
    pdf.set_draw_color(r=230, g=230, b=227)

    pdf.rect(0, y, 4, 48, 'FD')

    pdf.set_text_color(r=0, g=0, b=0)
    pdf.set_font("RalewayLight", "", 10)
    pdf.set_xy(start_X, y)
    text = u'Данная матрица отражает группы характеристик, определяюящие рабочее поведение участников. ' \
           u'Матрица построена на основе двух осей:\n\n' \
           u'• Яркость проявления (насколько развита данная характеристика у большинства участников)\n' \
           u'• Согласованность результатов (насколько похоже проявляют характеристику большинство участников)\n \n' \
           u'В зеленый квадрат попадают характеристики, которые ярко проявляются у большинства участников. В данном квадрате ' \
           u'размещены ключевые ресурсы, за счет которых участники выполняют работу и добиваются результатов.\n \n' \
           u'В красный квадрат попадают характеристики, которые слабо проявляются у большинства участников. В данном квадрате ' \
           u'размещены ключевые ограничения группы, влияющие на выполнение работы.'

    pdf.multi_cell(0, 4, text)

    draw_integral_report_items(pdf, start_X, start_Y, end_X, end_Y, square_results)


def draw_integral_report_items(pdf, start_x, start_y, end_x, end_y, square_results):
    # ['Переговорщик', 'mariya.lyushakova@rt.ru', 'Люшакова Мария Олеговна', 0, '', 'rgba(0, 0, 0, 0)', '1_3', 1]
    pdf.set_font("RalewayLight", "", 8)
    matrix_height = end_y - start_y
    matrix_width = end_x - start_x
    middle_x = start_x + matrix_width / 2
    middle_y = start_y + matrix_height / 2

    integral_report_filters = IntegralReportFilter.objects.all()
    integral_report_data = []
    for integral_report_filter in integral_report_filters:
        integral_report_filter_categories = IntegralReportFilterCategory.objects.filter(Q(filter=integral_report_filter))
        if integral_report_filter_categories.exists():
            category_points_sum = 0
            category_points_cnt = 0
            categories_t_points = []
            for integral_report_filter_category in integral_report_filter_categories:
                category_t_points = []

                category_code = integral_report_filter_category.category.code
                for square_result in square_results:
                    report = Report.objects.filter(participant__employee__email=square_result[1]).latest('added')
                    if ReportDataByCategories.objects.filter(Q(report=report) & Q(category_code=category_code)).exists():
                        t_points = ReportDataByCategories.objects.filter(Q(report=report) & Q(category_code=category_code)).latest('created_at').t_points
                        category_points_cnt = category_points_cnt + 1
                        category_points_sum = category_points_sum + t_points
                        category_t_points.append(t_points)
                if len(category_t_points) > 0:
                    categories_t_points.append(category_t_points)
            average_categories_t_points = []
            for category_points in categories_t_points:
                average_category_t_points = math.floor((sum(category_points) / len(category_points)) * 10) / 10
                average_categories_t_points.append(average_category_t_points)

            if len(average_categories_t_points) > 0:
                x = 10 - math.floor((sum(average_categories_t_points) / len(average_categories_t_points)) * 10) / 10
            else:
                x = 0
            if category_points_cnt > 0:
                integral_report_data.append({
                    'name': integral_report_filter.name,
                    'y': round((category_points_sum / category_points_cnt), 1),
                    'x': x,
                    'category_points_sum': category_points_sum,
                    'category_points_cnt': category_points_cnt,
                })
    circle_radius = 2.5
    if len(integral_report_data) > 0:
        pdf.set_fill_color(r=85, g=85, b=200)
        pdf.set_draw_color(r=255, g=255, b=255)
        pdf.set_font("RalewayLight", "", 11)
        matrix_interval_width = matrix_width / 10
        matrix_interval_height = matrix_height / 10
        # левый верхний угол
        matrix_squares = [
        {
            'start_x': 0,
            'end_x': 5,
            'start_y': 5,
            'end_y': 10,
            'report_data': [],
            'square_id': '1'
        },
        {
            'start_x': 5,
            'end_x': 10,
            'start_y': 5,
            'end_y': 10,
            'report_data': [],
            'square_id': '2'
        },
        {
            'start_x': 0,
            'end_x': 5,
            'start_y': 0,
            'end_y': 5,
            'report_data': [],
            'square_id': '3'
        },
        {
            'start_x': 5,
            'end_x': 10,
            'start_y': 0,
            'end_y': 5,
            'report_data': [],
            'square_id': '4'
        },
        ]

        for data in integral_report_data:
            for square in matrix_squares:
                if square['start_x'] <= data['x'] < square['end_x'] and \
                        square['start_y'] <= data['y'] < square['end_y']:
                    square['report_data'].append(data)

        for square in matrix_squares:

            square_report_data = square['report_data']
            new_list_sorted_by_x = sorted(square_report_data, key=itemgetter('x'), reverse=False)

            square_id = square['square_id']
            prev_y = middle_y
            print('--------------===================++++++++++++START+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(f'square_id = {square_id}')

            if square_id == '1' or square_id == '2':
                new_list_sorted_by_y = sorted(square_report_data, key=itemgetter('y'), reverse=False)
            else:
                new_list_sorted_by_y = sorted(square_report_data, key=itemgetter('y'), reverse=True)
            print('++++++new_list_sorted_by_y+++++')
            print(new_list_sorted_by_y)
            print('+++++++++++++++++++')
            for report_data_sorted_by_y in new_list_sorted_by_y:
                item_y = end_y - report_data_sorted_by_y['y'] * matrix_interval_height
                print(f'{report_data_sorted_by_y["name"]} item_y1 = {item_y} prev_y = {prev_y}')
                if square_id == '1' or square_id == '2':
                    if item_y >= prev_y:
                        item_y = prev_y - 4
                    prev_y = item_y - 5
                else:
                    if item_y - 6 <= prev_y:
                        item_y = prev_y + 8
                    prev_y = item_y
                print(f'{report_data_sorted_by_y["name"]} item_y2 = {item_y} prev_y = {prev_y}')

                for report_data_sorted_by_x in new_list_sorted_by_x:
                    if report_data_sorted_by_x['name'] == report_data_sorted_by_y['name']:
                        report_data_sorted_by_x['y'] = item_y

            square['report_data'] = new_list_sorted_by_x
            print('----------new_list_sorted_by_x------------')
            print(new_list_sorted_by_x)
            print('-----------------------------')
            print('--------------===================++++++++++++END+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

        for matrix_square in matrix_squares:
            report_data = matrix_square['report_data']
            if len(report_data) > 0:
                cnt = 0
                for matrix_item in report_data:
                    cnt = cnt + 1
                    x = matrix_item['x'] * matrix_interval_width + start_x

                    name = f"{matrix_item['name']}"

                    name_length = pdf.get_string_width(name)
                    text_end_x = x + name_length / 2
                    text_start_x = x - name_length / 2
                    square_id = matrix_square['square_id']

                    # если текст начинается вне пределов квадрата
                    if square_id == '1' or square_id == '3':
                        if text_end_x >= middle_x:
                            x = middle_x - (name_length / 2 + 1)
                        if text_start_x <= start_x:
                            x = start_x + 1
                    else:
                        if text_end_x >= end_x:
                            x = end_x - (name_length / 2 + 1)
                        if text_start_x <= middle_x:
                            x = middle_x + name_length / 2 + 1
                    text_start_x = x - name_length / 2

                    circle_y = matrix_item['y']
                    text_y = circle_y - 1

                    pdf.circle(x - circle_radius / 2, circle_y, circle_radius, style="FD")
                    pdf.text(text_start_x, text_y, name)


