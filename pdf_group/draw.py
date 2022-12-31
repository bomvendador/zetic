from pdf.models import Report, ReportData
import math


def draw_arrow(pdf, startX, startY, r, g, b, data_by_points):
    pdf.set_draw_color(r, g, b)
    pdf.set_fill_color(r, g, b)
    # отрисовка прямоугольника
    rect_width = 140
    rect_height = 4
    pdf.rect(startX, startY, rect_width, rect_height, 'FD')
    # отрисовка треугольника
    triangle_width = 7
    point1 = (startX + rect_width, startY - rect_height/2)
    point2 = (startX + rect_width + triangle_width, startY - rect_height/2 + rect_height)
    point3 = (startX + rect_width, startY - rect_height/2 + rect_height * 2)
    pdf.polygon(point_list=[point1, point2, point3, point1], style="FD")
    pdf.set_font("NotoSansDisplayMedium", "", 8)
    section_qnt = 10
    section_width = rect_width / section_qnt

    line_x_start = startX

    for cur_section in range(section_qnt):

        if cur_section == 0:
            cur_section_width = section_width / 2
        else:
            cur_section_width = section_width

        # # отрисовка прямоугольника на шкале
        # if (cur_section % 2) != 0:
        #     new_r = r + 50
        #     new_g = g + 50
        #     new_b = b + 50
        #     if new_r > 255:
        #         new_r = 255
        #     if new_g > 255:
        #         new_g = 255
        #     if new_b > 255:
        #         new_b = 255
        #     pdf.set_draw_color(new_r, new_g, new_b)
        #     pdf.set_fill_color(new_r, new_g, new_b)
        #     # pdf.rect(line_x_start - cur_section_width / 2, startY + rect_height + 1.3, section_width - 0.17, 15, 'FD')
        #     pdf.rect(line_x_start - cur_section_width / 2, startY - rect_height/2 + 1, section_width - 0.17, 15, 'FD')
        #
        # pdf.set_draw_color(r, g, b)
        # pdf.set_fill_color(r, g, b)

        # отрисовка линий
        pdf.line(line_x_start + cur_section_width, startY - rect_height/2 + 1, line_x_start + cur_section_width, startY + rect_height + rect_height/2 - 1)
        pdf.set_text_color(105, 105, 105)
        # цифры текст на шкале
        if cur_section + 1 == 10:
            pdf.text(line_x_start + cur_section_width - 1.5, startY + 3, str(cur_section + 1))
        else:
            pdf.text(line_x_start + cur_section_width - 0.75, startY + 3, str(cur_section + 1))
        line_x_start = line_x_start + cur_section_width
    total_points = 0
    total_participants_qnt = 0

    for key, value in data_by_points.items():

        if len(value) > 0:
            circles_placed_cnt = 0

            col_qnt = len(value)
            first_item_x = 0
            if col_qnt > 4:
                col_qnt = 4

            cur_col = 1
            delta_y = 0

            for scale_number_data in value:
                total_points = total_points + scale_number_data[1]
                circles_placed_cnt = circles_placed_cnt + 1

                if cur_col > col_qnt:
                    delta_y = delta_y + 3.5
                    cur_col = 1
                    first_item_x = 0

                scale_number_x = startX + scale_number_data[1] * section_width - section_width / 2  # x позиция черты на шкале
                draw_single_circle_arrow(pdf, scale_number_x - 1.75 * col_qnt + first_item_x, startY + 5.5 + delta_y, scale_number_data[2])
                first_item_x = first_item_x + 3.5
                cur_col = cur_col + 1

            total_participants_qnt = total_participants_qnt + circles_placed_cnt

    #треугольник СРЕДНЕЕ
    if total_participants_qnt > 0:
        average_number_x = startX + (total_points // total_participants_qnt) * section_width - section_width / 2
        # print(f'{total_points} / {total_participants_qnt} = {total_points // total_participants_qnt}')

        pdf.set_draw_color(r, g, b)
        pdf.set_text_color(105, 105, 105)
        point1 = (average_number_x - 5, startY - 3)
        point2 = (average_number_x + 5, startY - 3)
        point3 = (average_number_x, startY-1.5)
        pdf.polygon(point_list=[point1, point2, point3, point1], style="FD")
        pdf.text(average_number_x - 4.5, startY - 3.5, 'СРЕДНЕЕ')


def draw_single_circle_arrow(pdf, x, y, number):
    # print(f'start - {pdf.get_y()}')
    pdf.set_draw_color(0, 0, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("NotoSansDisplayMedium", "", 6)
    pdf.circle(x, y, r=3.4)
    if number < 10:
        pdf.text(x + 1.1, y + 2.5, str(number))
    else:
        if 10 <= number < 20:
            pdf.text(x + 0.5, y + 2.5, str(number))
        else:
            pdf.text(x + 0.6, y + 2.5, str(number))
    print(f'start - {pdf.get_y()}')


def draw_squares(pdf, square_results):
    startX = 15
    startY = 25
    width = 90
    pdf.set_draw_color(255, 240, 193)
    pdf.set_fill_color(255, 240, 193)
    pdf.rect(startX, startY, width, width, 'FD')

    pdf.set_draw_color(253, 219, 246)
    pdf.set_fill_color(253, 219, 246)
    pdf.rect(startX + width, startY, width, width, 'FD')

    pdf.set_draw_color(217, 245, 251)
    pdf.set_fill_color(217, 245, 251)
    pdf.rect(startX, startY + width, width, width, 'FD')

    pdf.set_draw_color(226, 239, 218)
    pdf.set_fill_color(226, 239, 218)
    pdf.rect(startX + width, startY + width, width, width, 'FD')

    pdf.set_draw_color(255, 255, 255)
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(startX + width / 2 - 0.3, startY, 0.6, startY + width * 2, 'FD')

    pdf.rect(startX + width + width / 2 - 0.3, startY, 0.6, startY + width * 2, 'FD')

    pdf.rect(startX, startY + width / 2 - 0.3, startY + width * 2, 0.6, 'FD')

    pdf.rect(startX, startY + width + width / 2 - 0.3, startY + width * 2, 0.6, 'FD')

    pdf.set_font("RalewayLight", "", 10)

    pdf.rect(startX + width / 2 - 17, startY + width / 2 - 5, 34, 10, 'FD')
    pdf.text(startX + width / 2 - 15 + 4, startY + width / 2 + 1, 'Интеграторы')

    pdf.rect(startX + width + width / 2 - 17, startY + width / 2 - 5, 34, 10, 'FD')
    pdf.text(startX + width + width / 2 - 15 + 4.5, startY + width / 2 + 1, 'Инноваторы')

    pdf.rect(startX + width / 2 - 17, startY + width + width / 2 - 5, 34, 10, 'FD')
    pdf.text(startX + width / 2 - 15 + 0.5, startY + width + width / 2 + 1, 'Администраторы')

    pdf.rect(startX + width + width / 2 - 17, startY + width + width / 2 - 5, 34, 10, 'FD')
    pdf.text(startX + width + width / 2 - 15 + 5, startY + width + width / 2 + 1, 'Продюсеры')

    # названия квадратов
    pdf.set_font("RalewayRegular", "", 8)

    pdf.text(startX + width / 2 - 13, startY - 2.5, 'Фокус на процесс')
    pdf.text(startX + width / 2 + width - 13.5, startY - 2.5, 'Фокус на результат')
    with pdf.rotation(90, 12, startY + width / 2 + 10):
        pdf.text(0, startY + width / 2 + 10, "Неструктурированный подход")
    with pdf.rotation(270, startX + width * 2 + 3, startY + width / 2 - 18):
        pdf.text(startX + width * 2 + 3, startY + width / 2 - 18, "Концептуальные решения")
    with pdf.rotation(90, 12, startY + width / 2 + 7 + width):
        pdf.text(0, startY + width / 2 + 7 + width, "Структурированный подход")
    with pdf.rotation(270, startX + width * 2 + 3, startY + width / 2 - 15 + width):
        pdf.text(startX + width * 2 + 3, startY + width / 2 - 15 + width, "Локальные решения")

    pdf.set_font("RalewayLight", "", 8)

    pdf.text(startX + width / 4 - 3, startY + 4, 'ESFJ')
    pdf.text(startX + width / 4 - 13, startY + 7, 'Массовик-затейник')

    pdf.text(startX + width * (3/4) - 3, startY + 4, 'ENFJ')
    pdf.text(startX + width * (3/4) - 13, startY + 7, 'Идеалист-харизматик')

    pdf.text(startX + width + width / 4 - 3, startY + 4, 'ESTJ')
    pdf.text(startX + width + width / 4 - 14, startY + 7, 'Контролер по жизни')

    pdf.text(startX + width + width * (3/4) - 3, startY + 4, 'ENTJ')
    pdf.text(startX + width + width * (3/4) - 11, startY + 7, 'Предприниматель')

    pdf.text(startX + width / 4 - 3, startY + width - 6, 'ESFP')
    pdf.text(startX + width / 4 - 18.5, startY + width - 3, 'Спонтанный коммуникатор')

    pdf.text(startX + width * (3/4) - 3, startY + width - 6, 'ENFP')
    pdf.text(startX + width * (3/4) - 7, startY + width - 3, 'Инициатор')

    pdf.text(startX + width + width / 4 - 3, startY + width - 6, 'ESTP')
    pdf.text(startX + width + width / 4 - 10, startY + width - 3, 'Ультра-реалист')

    pdf.text(startX + width + width * (3/4) - 3, startY + width - 6, 'ENTP')
    pdf.text(startX + width + width * (3/4) - 9, startY + width - 3, 'Изобретатель')

    pdf.text(startX + width / 4 - 3, startY + width + 4, 'ISFJ')
    pdf.text(startX + width / 4 - 7, startY + width + 7, 'Хранитель')

    pdf.text(startX + width * (3/4) - 3, startY + width + 4, 'INFJ')
    pdf.text(startX + width * (3/4) - 9, startY + width + 7, 'Вдохновитель')

    pdf.text(startX + width + width / 4 - 3, startY + width + 4, 'ISTJ')
    pdf.text(startX + width + width / 4 - 8, startY + width + 7, 'Организатор')

    pdf.text(startX + width + width * (3/4) - 3, startY + width + 4, 'INTJ')
    pdf.text(startX + width + width * (3/4) - 14, startY + width + 7, 'Любитель улучшений')

    pdf.text(startX + width / 4 - 3, startY + width + width - 6, 'ISFP')
    pdf.text(startX + width / 4 - 7, startY + width + width - 3, 'Посредник')

    pdf.text(startX + width * (3/4) - 3, startY + width + width - 6, 'INFP')
    pdf.text(startX + width * (3/4) - 16, startY + width + width - 3, 'Благородный служитель')

    pdf.text(startX + width + width / 4 - 3, startY + width + width - 6, 'ISTP')
    pdf.text(startX + width + width / 4 - 12, startY + width + width - 3, 'Экспериментатор')

    pdf.text(startX + width + width * (3/4) - 3, startY + width + width - 6, 'INTP')
    pdf.text(startX + width + width * (3/4) - 12, startY + width + width - 3, 'Решатель проблем')

    pdf.set_line_width(0.5)
    pdf.set_draw_color(240)
    pdf.set_font("NotoSansDisplayMedium", "", 10)

    text_y_delta = 5.2
    text_x_delta = 3

    square_x_cnt = {
        'ESFJ - Массовик-затейник': {
            'circle_coords': [startX + 5, startY + 10],
            'text_coords': [startX + 5 + text_x_delta, startY + 10 + text_y_delta],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'ENFJ - Идеалист-харизматик': {
            'circle_coords': [startX + 5 + width / 2, startY + 10],
            'text_coords': [startX + 5 + text_x_delta + width / 2, startY + 10 + text_y_delta],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'ESFP - Спонтанный коммуникатор': {
            'circle_coords': [startX + 5, startY + 10 + width / 2 - 2],
            'text_coords': [startX + 5 + text_x_delta, startY + 10 + text_y_delta + width / 2 - 2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'ENFP - Инициатор': {
            'circle_coords': [startX + 5 + width / 2, startY + 10 + width / 2 - 2],
            'text_coords': [startX + 5 + text_x_delta + width / 2, startY + 10 + text_y_delta + width / 2 - 2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'ESTJ - Контролер по жизни': {
            'circle_coords': [startX + 5 + width, startY + 10],
            'text_coords': [startX + 5 + text_x_delta + width, startY + 10 + text_y_delta],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'ENTJ - Предприниматель': {
            'circle_coords': [startX + 5 + width + width / 2, startY + 10],
            'text_coords': [startX + 5 + text_x_delta + width  + width / 2, startY + 10 + text_y_delta],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'ESTP - Ультра-реалист': {
            'circle_coords': [startX + 5 + width, startY + 10 + width / 2 - 2],
            'text_coords': [startX + 5 + text_x_delta + width, startY + 10 + text_y_delta + width / 2 - 2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'ENTP - Изобретатель': {
            'circle_coords': [startX + 5 + width + width / 2, startY + 10 + width / 2 - 2],
            'text_coords': [startX + 5 + text_x_delta + width + width / 2, startY + 10 + text_y_delta + width / 2 - 2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'ISFJ - Хранитель': {
            'circle_coords': [startX + 5, startY + 10 + width],
            'text_coords': [startX + 5 + text_x_delta, startY + 10 + text_y_delta + width],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'INFJ - Вдохновитель': {
            'circle_coords': [startX + 5 + width / 2, startY + 10 + width],
            'text_coords': [startX + 5 + text_x_delta + width / 2, startY + 10 + text_y_delta + width],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'ISFP - Посредник': {
            'circle_coords': [startX + 5, startY + 10 + width / 2 + width - 2],
            'text_coords': [startX + 5 + text_x_delta, startY + 10 + text_y_delta + width / 2 + width - 2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'INFP - Благородный служитель': {
            'circle_coords': [startX + 5 + width / 2, startY + 10 + width / 2 + width - 2],
            'text_coords': [startX + 5 + text_x_delta + width / 2, startY + 10 + text_y_delta + width / 2 + width - 2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},

        'ISTJ - Организатор': {
            'circle_coords': [startX + 5 + width, startY + 10 + width],
            'text_coords': [startX + 5 + text_x_delta + width, startY + 10 + text_y_delta + width],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'INTJ - Любитель улучшений': {
            'circle_coords': [startX + 5 + width + width / 2, startY + 10 + width],
            'text_coords': [startX + 5 + text_x_delta + width + width / 2, startY + 10 + text_y_delta + width],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'ISTP - Экспериментатор': {
            'circle_coords': [startX + 5 + width, startY + 10 + width / 2 + width - 2],
            'text_coords': [startX + 5 + text_x_delta + width, startY + 10 + text_y_delta + width / 2 + width - 2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'INTP - Решатель проблем': {
            'circle_coords': [startX + 5 + width + width / 2, startY + 10 + width / 2 + width - 2],
            'text_coords': [startX + 5 + text_x_delta + width + width / 2, startY + 10 + text_y_delta + width / 2 + width - 2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
    }
    cnt = 0

    for square_data in square_results:
        cnt = cnt + 1
        draw_single_circle_squares(square_data, pdf, square_x_cnt, cnt)


def draw_single_circle_squares(square_data, pdf, square_x_cnt, cnt):
    square_name = square_data[0]
    email = square_data[1]
    participant_name = square_data[2]
    report = Report.objects.filter(participant__employee__email=email).latest('added')
    report_data = ReportData.objects.filter(report=report, section_code='3')
    section_1 = 0
    section_2 = 0
    section_3 = 0

    for report_data_item in report_data:
        split = report_data_item.category.name.split('_')
        if int(split[0]) <= 4:
            section_1 = section_1 + report_data_item.points
        elif 5 <= int(split[0]) <= 8:
            section_2 = section_2 + report_data_item.points
        elif int(split[0]) >= 9:
            section_3 = section_3 + report_data_item.points
    if section_1 > 18 or section_2 > 18 or section_3 > 18 or section_2 >= 7:
        pdf.set_fill_color(241, 151, 15)
    else:
        pdf.set_fill_color(255, 255, 255)
    # print(f'participant_name - {participant_name} - секция 1 - {section_1} секция 2 - {section_2} секция 3 - {section_3}')
        # section_points_sum = section_points_sum + report_data_item['points']
    # print(participant_name + ' - ' + str(section_points_sum))

    pdf.circle(square_x_cnt[square_name]['circle_coords'][0] + 9 * square_x_cnt[square_name]['cur_X_pos'], square_x_cnt[square_name]['circle_coords'][1] + 9 * square_x_cnt[square_name]['cur_Y_pos'], 8, style="FD")
    if cnt <= 9:
        pdf.text(square_x_cnt[square_name]['text_coords'][0] + 9 * square_x_cnt[square_name]['cur_X_pos'], square_x_cnt[square_name]['text_coords'][1] + 9 * square_x_cnt[square_name]['cur_Y_pos'], str(cnt))
    else:
        pdf.text(square_x_cnt[square_name]['text_coords'][0] - 1.1 + 9 * square_x_cnt[square_name]['cur_X_pos'], square_x_cnt[square_name]['text_coords'][1] + 9 * square_x_cnt[square_name]['cur_Y_pos'], str(cnt))

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
    for square_data_item in square_data:
        report = Report.objects.filter(participant__employee__email=square_data_item[1]).latest('added')
        if report.lie_points > 4:
            pdf.set_text_color(255, 0, 0)
        else:
            pdf.set_text_color(0, 0, 0)

        pdf.multi_cell(7, line_height, str(cnt), border=1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
        pdf.multi_cell(width - 7, line_height, square_data_item[2], border=1, new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
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
                y = start_y
                x = x + width

        pdf.set_xy(x, y)

    if all_participants_qnt // 2 != all_participants_qnt / 2:
        # y = y + line_height
        pdf.multi_cell(7, line_height, '', border=1, align='C', new_x='RIGHT', new_y='TOP',
                       max_line_height=pdf.font_size)
        pdf.multi_cell(width - 7, line_height, '', border=1, new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)

