from pdf.models import Report, ReportData, ReportGroup, ReportGroupSquare, IntegralReportFilter, \
    IntegralReportFilterCategory, ReportDataByCategories, TrafficLightReportFilter, TrafficLightReportFilterCategory, \
    Participant

from django.db.models import Q

import math

from pdf.draw import insert_page_number



def draw_single_circle_squares(square_data, pdf, square_x_cnt, cnt):
    square_name = square_data[0]
    email = square_data[1]
    participant_name = square_data[2]
    participant_number = square_data[7]
    group_color = square_data[5]
    bold = square_data[3]

    orange_color = is_orange_color(email)

    if orange_color:
        pdf.set_fill_color(241, 151, 15)
    else:
        if not group_color == 'rgba(0, 0, 0, 0)':
            color_r = int(group_color[group_color.find('(')+len('('):group_color.rfind(')')].split(',')[0])
            color_g = int(group_color[group_color.find('(')+len('('):group_color.rfind(')')].split(',')[1].strip())
            color_b = int(group_color[group_color.find('(')+len('('):group_color.rfind(')')].split(',')[2].strip())
            pdf.set_fill_color(color_r, color_g, color_b)
        else:
            pdf.set_fill_color(255, 255, 255)
    if bold == 1:
        pdf.set_draw_color(r=0, g=0, b=0)
    else:
        pdf.set_draw_color(240)
    # print(f'participant_name - {participant_name} - секция 1 - {section_1} секция 2 - {section_2} секция 3 - {section_3}')
        # section_points_sum = section_points_sum + report_data_item['points']
    # print(participant_name + ' - ' + str(section_points_sum))

    pdf.circle(square_x_cnt[square_name]['circle_coords'][0] + 9 * square_x_cnt[square_name]['cur_X_pos'], square_x_cnt[square_name]['circle_coords'][1] + 9 * square_x_cnt[square_name]['cur_Y_pos'], 8, style="FD")
    # pdf.text_annotation(square_x_cnt[square_name]['circle_coords'][0] + 9 * square_x_cnt[square_name]['cur_X_pos'] + 3, square_x_cnt[square_name]['circle_coords'][1] + 9 * square_x_cnt[square_name]['cur_Y_pos'] - 3, 'Фамилия', 3, 3, flags=('NO_VIEW',))
    if cnt <= 9:
        pdf.text(square_x_cnt[square_name]['text_coords'][0] + 9 * square_x_cnt[square_name]['cur_X_pos'], square_x_cnt[square_name]['text_coords'][1] + 9 * square_x_cnt[square_name]['cur_Y_pos'], str(participant_number))
    else:
        pdf.text(square_x_cnt[square_name]['text_coords'][0] - 1.1 + 9 * square_x_cnt[square_name]['cur_X_pos'], square_x_cnt[square_name]['text_coords'][1] + 9 * square_x_cnt[square_name]['cur_Y_pos'], str(participant_number))

    cur_X_cnt = square_x_cnt[square_name]['cur_X_pos']
    if cur_X_cnt < 3:
        square_x_cnt[square_name]['cur_X_pos'] = square_x_cnt[square_name]['cur_X_pos'] + 1
    else:
        square_x_cnt[square_name]['cur_X_pos'] = 0
        square_x_cnt[square_name]['cur_Y_pos'] = square_x_cnt[square_name]['cur_Y_pos'] + 1
    square_x_cnt[square_name]['cnt'] = square_x_cnt[square_name]['cnt'] + 1


def draw_table(square_data, pdf, width, x, y):
    # new_line_cnt = 5
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 8)
    pdf.set_line_width(0.1)
    pdf.set_draw_color(230, 230, 227)
    line_height = pdf.font_size * 2
    start_y = y
    cnt = 1
    new_column_added = False
    all_participants_qnt = len(square_data)

    pdf.multi_cell(7, line_height, '#', border=1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
    pdf.multi_cell((width - 10) - 7, line_height, 'Имя', border=1, new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
    pdf.multi_cell(10, line_height, 'Цвет', border=1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
    pdf.ln(line_height)

    pdf.set_xy(x + width, y)

    pdf.multi_cell(7, line_height, '#', border=1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
    pdf.multi_cell((width - 10) - 7, line_height, 'Имя', border=1, new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
    pdf.multi_cell(10, line_height, 'Цвет', border=1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
    pdf.ln(line_height)

    y = y + line_height
    pdf.set_xy(x, y)

    for square_data_item in square_data:
        participant_name = square_data_item[2]
        group_name = square_data_item[4]
        group_color = square_data_item[5]
        bold = square_data_item[3]
        email = square_data_item[1]
        print(email)
        report = Report.objects.filter(participant__employee__email=square_data_item[1]).latest('added')
        if report.lie_points > 4:
            pdf.set_text_color(255, 0, 0)
        else:
            pdf.set_text_color(0, 0, 0)

        # pdf.multi_cell(7, line_height, str(cnt), border=1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
        pdf.multi_cell(7, line_height, str(square_data_item[7]), border=1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
        pdf.multi_cell((width - 10) - 7, line_height, participant_name, border=1, new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
        pdf.multi_cell(10, line_height, '', border=1, new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)

        orange_color = is_orange_color(email)

        if orange_color:
            pdf.set_fill_color(241, 151, 15)
        else:
            if not group_color == 'rgba(0, 0, 0, 0)':
                color_r = int(group_color[group_color.find('(')+len('('):group_color.rfind(')')].split(',')[0])
                color_g = int(group_color[group_color.find('(')+len('('):group_color.rfind(')')].split(',')[1].strip())
                color_b = int(group_color[group_color.find('(')+len('('):group_color.rfind(')')].split(',')[2].strip())
                pdf.set_fill_color(color_r, color_g, color_b)
                pdf.set_draw_color(color_r, color_g, color_b)
            else:
                pdf.set_fill_color(r=255, g=255, b=255)
        if bold == 1:
            pdf.set_draw_color(r=0, g=0, b=0)
            pdf.set_line_width(0.6)
        else:
            pdf.set_draw_color(r=255, g=255, b=255)

        pdf.circle(x=x + width - line_height / 2 - 4, y=y + line_height / 2 - 2, r=4, style="FD")

        pdf.set_line_width(0.1)
        pdf.set_draw_color(230, 230, 227)

        pdf.ln(line_height)
        cnt = cnt + 1
        y = y + line_height

        new_line_cnt = all_participants_qnt // 2
        if all_participants_qnt / 2 == new_line_cnt:
            new_line_cnt = all_participants_qnt / 2
        else:
            new_line_cnt = new_line_cnt + 1
        if cnt > new_line_cnt:
            if not new_column_added:
                new_column_added = True
                y = start_y + line_height
                x = x + width

        pdf.set_xy(x, y)

    if all_participants_qnt // 2 != all_participants_qnt / 2:
        # y = y + line_height
        pdf.multi_cell(7, line_height, '', border=1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
        pdf.multi_cell((width - 10) - 7, line_height, '', border=1, new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
        pdf.multi_cell(10, line_height, '', border=1, new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)


def draw_(pdf, lang, start_x, start_y, square_results):
    start_X = start_x
    start_Y = start_y
    end_X = 190
    total_width = end_X - start_X
    end_Y = 220
    total_height = end_Y - start_Y


def draw_traffic_light_report_legend(pdf, lang, start_x, start_y, color, item_marker_width):
    red = color['red']
    yellow = color['yellow']
    green = color['green']
    interval_between = item_marker_width + 2
    text_y = start_y + item_marker_width / 2 + 1
    square_y = start_y

    pdf.set_line_width(0.1)
    pdf.set_draw_color(r=135, g=135, b=135)

    #красный
    pdf.set_fill_color(r=red['r'], g=red['g'], b=red['b'])
    # pdf.set_draw_color(r=red['r'], g=red['g'], b=red['b'])
    pdf.rect(x=start_x, y=square_y, w=item_marker_width, h=item_marker_width, style="FD")
    pdf.text(start_x + item_marker_width + 2, text_y, '- Слабое проявление характеристики')

    # pdf.set_xy(100, start_y)
    # text = u'Данная таблица визуально отражает результаты оценки участников по ключевым шкалам. Формат «светофора» ' \
    #        u'обозначает наиболее слабые и наиболее сильные компетенции у участников. Данные формируются автоматически ' \
    #        u'на основе результатов заполнения опросника.'
    # pdf.multi_cell(0, 4, text)


    text_y = text_y + interval_between
    square_y = square_y + interval_between
    #желтый
    pdf.set_fill_color(r=yellow['r'], g=yellow['g'], b=yellow['b'])
    # pdf.set_draw_color(r=yellow['r'], g=yellow['g'], b=yellow['b'])
    pdf.rect(x=start_x, y=square_y, w=item_marker_width, h=item_marker_width, style="FD")
    pdf.text(start_x + item_marker_width + 2, text_y, '- Проявление характеристики с ограничениями')

    text_y = text_y + interval_between
    square_y = square_y + interval_between
    #зеленый
    pdf.set_fill_color(r=green['r'], g=green['g'], b=green['b'])
    # pdf.set_draw_color(r=green['r'], g=green['g'], b=green['b'])
    pdf.rect(x=start_x, y=square_y, w=item_marker_width, h=item_marker_width, style="FD")
    pdf.text(start_x + item_marker_width + 2, text_y, '- Яркое проявление характеристики')


def draw_traffic_light_report_border(pdf, lang, start_x, start_y, end_x, end_y):
    start_Y_items_table = start_y
    start_X_items_table = start_x
    pdf.set_line_width(0.1)
    pdf.set_draw_color(r=135, g=135, b=135)
    pdf.rect(start_X_items_table, start_Y_items_table, end_x - start_X_items_table, end_y - start_Y_items_table, 'D') #обводка


def draw_traffic_light_report_table(pdf, lang, start_x, start_y, square_results):
    color = {
        'red': {
            'r': 250,
            'g': 121,
            'b': 121,
        },
        'yellow': {
            'r': 235,
            'g': 235,
            'b': 60,
        },
        'green': {
            'r': 110,
            'g': 212,
            'b': 110,
        },
    }
    item_marker_width = 6

    start_X = start_x
    start_Y = pdf.get_y() + 2
    end_X = 200
    total_width = end_X - start_X
    end_Y = 255
    total_height = end_Y - start_Y
    interval_between_rows = 2

    # start_Y_items_table = start_Y + 30
    # start_X_items_table = start_X + 30
    # pdf.set_line_width(0.1)
    # pdf.set_draw_color(r=135, g=135, b=135)
    # pdf.rect(start_X_items_table, start_Y_items_table, end_X - start_X_items_table, end_Y - start_Y_items_table, 'D') #обводка

    letter_interval = 1.5
    letter_interval_participant_name = 1.9
    text_size_for_name = 10
    text_size_for_filters = 8
    interval_between_description_and_filters_name = 4

    # print('-- square results ---')
    # print(square_results)
    # print('-------')

    traffic_light_report_inst = TrafficLightReportFilter.objects.all().order_by('position')

    max_name_length = 0
    for report in traffic_light_report_inst:
        name_length = len(report.name)
        if name_length > max_name_length:
            max_name_length = name_length
        # print(f'{report.name} - {len(report.name)}')
    columns_max_y_length = max_name_length * letter_interval

    start_y_border = start_Y + columns_max_y_length + 4 + interval_between_description_and_filters_name

    name_max_length = 0
    participant_name_y = start_y_border + interval_between_rows + item_marker_width
    pdf.set_font("RalewayLight", "", text_size_for_name)

    # for data in square_results:
    # items_colors_arr = []
    data_items = []

    for data in square_results:
        participant_id = int(data[8])
        participant_number = data[7]
        category_code = data[6]
        participant_inst = Participant.objects.get(id=participant_id)
        print(f'277 - participant_name - {participant_inst.employee.name} participant_email - {participant_inst.employee.email}')
        report_inst = Report.objects.get(participant=participant_inst)
        name = participant_inst.employee.name
        name_with_number = str(participant_number) + '. ' + name
        participant_name_length = len(name_with_number)
        if participant_name_length > name_max_length:
            name_max_length = participant_name_length
        colors_for_participant = []
        # pdf.text(start_X, participant_name_y + interval_between_description_and_filters_name, name_with_number)
        for traffic_light_report in traffic_light_report_inst:
            # filter_colors_arr = []
            color_obj = {}
            total_t_points = 0
            traffic_light_report_categories_inst = TrafficLightReportFilterCategory.objects.filter(filter=traffic_light_report)
            for traffic_light_report_category in traffic_light_report_categories_inst:
                report_data_by_categories_inst = ReportDataByCategories.objects.get(Q(report=report_inst) & Q(category_code=traffic_light_report_category.category.code))
                t_point = report_data_by_categories_inst.t_points
                total_t_points = total_t_points + t_point
                # print(f'traffic_light_report - {traffic_light_report.name} code - {report_data_by_categories_inst.category_code} t_points - {t_point}')

            average_t_points = total_t_points / len(traffic_light_report_categories_inst)
            if traffic_light_report.points_from_red <= int(average_t_points) <= traffic_light_report.points_to_red:
                color_obj = {
                    'r': color['red']['r'],
                    'g': color['red']['g'],
                    'b': color['red']['b'],
                }
            if traffic_light_report.points_from_yellow <= int(average_t_points) <= traffic_light_report.points_to_yellow:
                color_obj = {
                    'r': color['yellow']['r'],
                    'g': color['yellow']['g'],
                    'b': color['yellow']['b'],
                }
            if traffic_light_report.points_from_green <= int(average_t_points) <= traffic_light_report.points_to_green:
                color_obj = {
                    'r': color['green']['r'],
                    'g': color['green']['g'],
                    'b': color['green']['b'],
                }
            colors_for_participant.append(color_obj)

        # items_colors_arr.append(colors_for_participant)
        data_items.append({
            'colors': colors_for_participant,
            'name': name_with_number
        })

    participant_name_ends_x = start_X + name_max_length * letter_interval_participant_name

    start_x_border = participant_name_ends_x + 2

    border_width = end_X - start_x_border

    columns_qnt = len(traffic_light_report_inst)
    # print(f'border_width = {border_width} columns_qnt = {columns_qnt}')
    interval_between_columns = border_width / (columns_qnt + 1)

    column_item_start_x = start_x_border + interval_between_columns
    pdf.set_font("RalewayLight", "", 8)
    # cnt = 0
    # print(f'items_colors_arr len - {len(items_colors_arr)}')
    for report in traffic_light_report_inst:
        # item_start_y = start_y_border + interval_between_rows + item_marker_width
        # print('--------')
        with pdf.rotation(90, column_item_start_x, start_Y + columns_max_y_length + 2 + interval_between_description_and_filters_name):
            pdf.text(column_item_start_x, start_Y + columns_max_y_length + 2 + interval_between_description_and_filters_name, report.name)
        column_item_start_x = column_item_start_x + interval_between_columns
        # print('--------')
        # cnt = cnt + 1

    draw_traffic_light_report_border(pdf, lang, start_x_border, start_y_border, end_X, end_Y)

    draw_traffic_light_report_legend(pdf, lang, start_x_border, end_Y + 10, color, item_marker_width)

    item_start_y = start_y_border + interval_between_rows + item_marker_width
    for data_item in data_items:
        if item_start_y > (end_Y - item_marker_width):
            pdf.add_page()
            insert_page_number(pdf)
            init_interval_for_new_page = 15
            start_y_border = init_interval_for_new_page + columns_max_y_length + 4
            participant_name_y = start_y_border + interval_between_rows + item_marker_width
            item_start_y = start_y_border + interval_between_rows + item_marker_width
            column_item_start_x = start_x_border + interval_between_columns
            new_start_Y = init_interval_for_new_page
            pdf.set_font("RalewayLight", "", text_size_for_filters)

            for report in traffic_light_report_inst:
                # item_start_y = start_y_border + interval_between_rows + item_marker_width
                # print('--------')
                with pdf.rotation(90, column_item_start_x,
                                  new_start_Y + columns_max_y_length + 2):
                    pdf.text(column_item_start_x,
                             new_start_Y + columns_max_y_length + 2,
                             report.name)
                column_item_start_x = column_item_start_x + interval_between_columns

            draw_traffic_light_report_border(pdf, lang, start_x_border, start_y_border, end_X, end_Y)
            draw_traffic_light_report_legend(pdf, lang, start_x_border, end_Y + 10, color, item_marker_width)

        pdf.set_font("RalewayLight", "", text_size_for_name)
        pdf.text(start_X, participant_name_y + interval_between_description_and_filters_name, data_item['name'])
        participant_name_y = participant_name_y + item_marker_width + interval_between_rows
        column_item_start_x = start_x_border + interval_between_columns
        # print(f'item_start_y = {item_start_y} name - {data_item["name"]}')

        for item_color in data_item['colors']:
            pdf.set_fill_color(r=item_color['r'], g=item_color['g'], b=item_color['b'])
            pdf.set_draw_color(r=item_color['r'], g=item_color['g'], b=item_color['b'])
            pdf.set_line_width(0.1)
            pdf.set_draw_color(r=135, g=135, b=135)

            pdf.rect(x=column_item_start_x - item_marker_width / 2, y=item_start_y, w=item_marker_width, h=item_marker_width, style="FD")

            column_item_start_x = column_item_start_x + interval_between_columns
        # item_start_y = item_start_y + interval_between_rows + item_marker_width
        item_start_y = item_start_y + interval_between_rows + item_marker_width


    # print(f'total_width - {total_width}')
    # pdf.set_line_width(0.4)
    # pdf.set_draw_color(r=135, g=135, b=135)
    # pdf.rect(start_X, start_Y, total_width, total_height, 'D') #обводка
    #
    # pdf.set_line_width(0.2)
    # pdf.line(start_X, start_Y + total_height / 2, start_X + total_width, start_Y + total_height / 2) #центральная горизонтальная линия
    # pdf.line(start_X + total_width / 2, start_Y, start_X + total_width / 2,  start_Y + total_height) #центральная вертикальная линия
    #
    # pdf.set_line_width(0.1)
    # pdf.line(start_X, start_Y + total_height / 2 / 2, start_X + total_width, start_Y + total_height / 2 / 2) #горизонтальная линия 1/4
    # pdf.line(start_X, start_Y + total_height * (3/4), start_X + total_width, start_Y + total_height * (3/4)) #горизонтальная линия 3/4
    # pdf.line(start_X + total_width / 2 / 2, start_Y, start_X + total_width / 2 / 2,  start_Y + total_height) #вертикальная линия 1/4
    # pdf.line(start_X + total_width * (3/4), start_Y, start_X + total_width * (3/4), start_Y + total_height) #вертикальная линия 3/4
    #
    # pdf.set_font("RalewayLight", "", 8)
    #
    # # pdf.set_text_color(r=255, g=255, b=255)
    # # pdf.set_text_color(r=135, g=135, b=135)
    # pdf.set_text_color(118, 134, 146)
    # pdf.set_fill_color(r=230, g=230, b=227)
    # pdf.set_draw_color(r=230, g=230, b=227)
    #
    # pdf.set_line_width(0.4)
    #
    # # горизонтальная ось
    # pdf.rect(start_X, start_Y + total_height + 0.4, 40, 4, 'FD')
    # pdf.text(start_X + 3, start_Y + total_height + 3, 'Низкая согласованность')
    #
    # pdf.rect(start_X + total_width - 40, start_Y + total_height + 0.4, 40 + 4 + 0.4, 4, 'FD')
    # pdf.text(start_X + total_width - 37, start_Y + total_height + 3, 'Высокая согласованность')
    #
    # pdf.set_text_color(r=135, g=135, b=135)
    # pdf.text(start_X + total_width / 2 / 2 - 2, start_Y + total_height + 3, '25%')
    # pdf.text(start_X + total_width / 2 - 2, start_Y + total_height + 3, '50%')
    # pdf.text(start_X + total_width * (3/4) - 2, start_Y + total_height + 3, '75%')
    #
    # # вертикальная ось
    # pdf.set_text_color(118, 134, 146)
    #
    # pdf.rect(start_X + total_width + 0.4, start_Y + total_height - 40, 4, 40, 'FD')
    # with pdf.rotation(90, start_X + total_width + 3, start_Y + total_height - 5):
    #     pdf.text(start_X + total_width + 3, start_Y + total_height - 5, 'Низкая проявленность')
    #
    # pdf.rect(start_X + total_width + 0.4, start_Y, 4, 40, 'FD')
    # with pdf.rotation(90, start_X + total_width + 3, start_Y + 40 - 4):
    #     pdf.text(start_X + total_width + 3, start_Y + 40 - 4, 'Высокая проявленность')
    #
    # # pdf.text(start_X + total_width - 37, start_Y + total_height + 3, 'Высокая проявленность')
    #
    # pdf.set_text_color(r=135, g=135, b=135)
    #
    # with pdf.rotation(90, start_X + total_width + 3, start_Y + total_height * (3 / 4) + 2):
    #     pdf.text(start_X + total_width + 3, start_Y + total_height * (3 / 4) + 2, '25%')
    # with pdf.rotation(90, start_X + total_width + 3, start_Y + total_height / 2 + 2):
    #     pdf.text(start_X + total_width + 3, start_Y + total_height / 2 + 2, '50%')
    # with pdf.rotation(90, start_X + total_width + 3, start_Y + total_height / 2 / 2 + 2):
    #     pdf.text(start_X + total_width + 3, start_Y + total_height / 2 / 2 + 2, '75%')
    #
    # # вертикальная ось (стрелка)
    # rect_width = total_width
    # rect_height = 1
    # delta_Y_for_horizontal_arrow = 10
    # pdf.rect(start_X, start_Y + total_height + delta_Y_for_horizontal_arrow, rect_width, rect_height, 'FD')
    # # отрисовка треугольника
    # triangle_width = 2
    # point1 = (start_X + rect_width, start_Y + total_height + delta_Y_for_horizontal_arrow - rect_height/2)
    # point2 = (start_X + rect_width + triangle_width, start_Y + total_height + delta_Y_for_horizontal_arrow + rect_height / 2)
    # point3 = (start_X + rect_width, start_Y + total_height + delta_Y_for_horizontal_arrow + rect_height + rect_height / 2)
    # pdf.polygon(point_list=[point1, point2, point3, point1], style="FD")
    #
    # pdf.set_fill_color(r=255, g=255, b=255)
    # pdf.set_draw_color(r=255, g=255, b=255)
    # pdf.rect((start_X + total_width) / 2 - 32, start_Y + total_height + delta_Y_for_horizontal_arrow - 2, 80, 6, 'FD')
    #
    # pdf.set_font("RalewayLight", "", 12)
    # pdf.text((start_X + total_width) / 2 - 30, start_Y + total_height + delta_Y_for_horizontal_arrow + 2, 'Согласованность ответов участников')
    #
    # # горизонтальная ось (стрелка)
    # pdf.set_fill_color(r=230, g=230, b=227)
    # pdf.set_draw_color(r=230, g=230, b=227)
    #
    # pdf.rect(start_X + total_width + delta_Y_for_horizontal_arrow, start_Y + triangle_width, rect_height, rect_width, 'FD')
    # # отрисовка треугольника
    # point1 = (start_X + total_width + delta_Y_for_horizontal_arrow - rect_height / 2, start_Y + triangle_width)
    # point2 = (start_X + total_width + delta_Y_for_horizontal_arrow + rect_height * 1.5, start_Y + triangle_width)
    # point3 = (start_X + total_width + delta_Y_for_horizontal_arrow + rect_height / 2, start_Y)
    # pdf.polygon(point_list=[point1, point2, point3, point1], style="FD")
    #
    # pdf.set_fill_color(r=255, g=255, b=255)
    # pdf.set_draw_color(r=255, g=255, b=255)
    # pdf.rect(start_X + total_width + delta_Y_for_horizontal_arrow - 2, (start_Y + total_height) / 2 - 40, 6, 110, 'FD')
    #
    # pdf.set_font("RalewayLight", "", 12)
    # with pdf.rotation(90, start_X + total_width + delta_Y_for_horizontal_arrow + 2, start_Y + total_height / 2 + 53):
    #     pdf.text(start_X + total_width + delta_Y_for_horizontal_arrow + 2, start_Y + total_height / 2 + 53, 'Проявленность компетенций в сравнении с рынком')
    #
    # # pdf.text((start_X + total_width) / 2 - 30, start_Y + total_height + delta_Y_for_horizontal_arrow + 2, 'Согласованность ответов участников')
    #
    # # описание матрицы
    # y = start_Y + total_height + delta_Y_for_horizontal_arrow + 15
    #
    # pdf.set_fill_color(r=230, g=230, b=227)
    # pdf.set_draw_color(r=230, g=230, b=227)
    #
    # pdf.rect(0, y, 4, 48, 'FD')
    #
    # pdf.set_text_color(r=0, g=0, b=0)
    # pdf.set_font("RalewayLight", "", 10)
    # pdf.set_xy(start_X, y)
    # text = u'Данная мтарица отражает группы характеристик, определеюящие рабочее поведение участников. ' \
    #        u'Матрица построена на основе двух осей:\n' \
    #        u'• яркость проявления (насколкь развита данная характеристика у большинства участников)\n' \
    #        u'• согласованность результатов (насколько похоже проявляют характеристику большинство участников)\n \n' \
    #        u'В зеленый квадрат попадают характеристики, которые ярко проявляются у большиснмтва участников. В данном квадрате ' \
    #        u'размещены ключевые ресурсы, за счет которых участники выполняют работу и добиваются результатов.\n \n' \
    #        u'В красный квадрат попадают характеристики, которые слабо проявляются у большиснмтва участников. В данном квадрате ' \
    #        u'размещены ключевые ресурсы, за счет которых участники выполняют работу и добиваются результатов.'
    #
    # pdf.multi_cell(0, 4, text)
    #
    # draw_integral_report_items(pdf, start_X, start_Y, end_X, end_Y, square_results)


def draw_integral_report_items(pdf, start_x, start_y, end_x, end_y, square_results):
    # ['Переговорщик', 'mariya.lyushakova@rt.ru', 'Люшакова Мария Олеговна', 0, '', 'rgba(0, 0, 0, 0)', '1_3', 1]
    matrix_height = end_y - start_y
    matrix_width = end_x - start_x
    # group_report = ReportGroup.objects.get(id=group_report_id)
    # report_group_squares = ReportGroupSquare.objects.filter(report_group=group_report)

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
                        t_points = ReportDataByCategories.objects.get(Q(report=report) & Q(category_code=category_code)).t_points
                        category_points_cnt = category_points_cnt + 1
                        category_points_sum = category_points_sum + t_points
                        category_t_points.append(t_points)
                if len(category_t_points) > 0:
                    categories_t_points.append(category_t_points)

            # average_category_t_point = math.floor((category_points_sum / category_points_cnt) * 10) / 10



                # for report_group_square in report_group_squares:
                #     report = report_group_square.report
                #     report_data_by_categories = ReportDataByCategories.objects.filter(Q(report=report) & Q(category_code=category_code))
                #     if report_data_by_categories.exists():
                #         category_points_cnt = category_points_cnt + 1
                #         category_points_sum = category_points_sum + report_data_by_categories[0].t_points
            variance_from_average = []
            # print(f'categories_t_points')
            # print(categories_t_points)
            for category_points in categories_t_points:
                average_category_t_points = math.floor((sum(category_points) / len(category_points)) * 10) / 10
                points_variance_from_average_in_category = []
                for point in category_points:
                    points_variance_from_average_in_category.append(abs(average_category_t_points - point))
                print('---points_variance_from_average_in_category---')
                print(points_variance_from_average_in_category)
                print('---')
                variance_from_average.append(math.floor((sum(points_variance_from_average_in_category) / len(
                    points_variance_from_average_in_category)) * 10) / 10)
                # variance_from_average.append(math.floor((sum(points_variance_from_average_in_category) / 3) * 10) / 10)
            print('---variance_from_average---')
            print(variance_from_average)
            print('----')
            if len(variance_from_average) > 0:
                x = 10 - math.floor((sum(variance_from_average) / len(variance_from_average)) * 10) / 10
            else:
                x = 0
            # x = 10 - math.floor((sum(variance_from_average) / 3) * 10) / 10
            if category_points_cnt > 0:
                integral_report_data.append({
                    'name': integral_report_filter.name,
                    'y': round((category_points_sum / category_points_cnt), 1),
                    'x': x,
                    'category_points_sum': category_points_sum,
                    'category_points_cnt': category_points_cnt,
                })
    # print(integral_report_data)
    # print(categories_t_points)
    circle_radius = 3
    if len(integral_report_data) > 0:
        pdf.set_fill_color(r=85, g=85, b=200)
        pdf.set_draw_color(r=255, g=255, b=255)
        pdf.set_font("RalewayLight", "", 11)
        letter_width = 1.9
        matrix_interval_width = matrix_width / 10
        matrix_interval_height = matrix_height / 10
        for data in integral_report_data:
            x = start_x + matrix_interval_width * data['x']
            y = end_y - matrix_interval_height * data['y']
            pdf.circle(x - circle_radius / 2, y, circle_radius, style="FD")
            name_length = len(data['name'])
            pdf.text(x - (name_length * letter_width) / 2 - circle_radius / 2, y - 1, data['name'])



