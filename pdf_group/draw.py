from pdf.models import Report, ReportData, ReportGroup, ReportGroupSquare, IntegralReportFilter, \
    IntegralReportFilterCategory, ReportDataByCategories

from django.db.models import Q

import math


def draw_arrow(pdf, startX, startY, r, g, b, data_by_points):
    # print(f'data_by_points - {data_by_points}')
    pdf.set_draw_color(r, g, b)
    pdf.set_fill_color(r, g, b)
    # отрисовка прямоугольника
    rect_width = 140 + 10
    rect_height = 4
    pdf.rect(startX, startY, rect_width, rect_height, 'FD')
    # отрисовка треугольника
    triangle_width = 7
    point1 = (startX + rect_width, startY - rect_height/2)
    point2 = (startX + rect_width + triangle_width, startY - rect_height/2 + rect_height)
    point3 = (startX + rect_width, startY - rect_height/2 + rect_height * 2)
    pdf.polygon(point_list=[point1, point2, point3, point1], style="FD")
    pdf.set_font("NotoSansDisplayMedium", "", 8)
    section_qnt = 11
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
        if cur_section + 1 == section_qnt:
            pdf.text(line_x_start + cur_section_width - 1.5, startY + 3, str(cur_section))
        else:
            pdf.text(line_x_start + cur_section_width - 0.75, startY + 3, str(cur_section))
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
                group_color = scale_number_data[3]
                email = scale_number_data[4]
                total_points = total_points + scale_number_data[1]
                bold = scale_number_data[5]
                circles_placed_cnt = circles_placed_cnt + 1

                if cur_col > col_qnt:
                    delta_y = delta_y + 3.5
                    cur_col = 1
                    first_item_x = 0

                scale_number_x = startX + scale_number_data[1] * section_width - section_width / 2 + section_width  # x позиция черты на шкале
                draw_single_circle_arrow(pdf, scale_number_x - 1.75 * col_qnt + first_item_x, startY + 5.5 + delta_y, scale_number_data[2], group_color, email, bold)
                first_item_x = first_item_x + 3.5
                cur_col = cur_col + 1

            total_participants_qnt = total_participants_qnt + circles_placed_cnt

    #треугольник СРЕДНЕЕ
    if total_participants_qnt > 0:
        average_number_x = (startX + section_width) + (total_points // total_participants_qnt) * section_width - section_width / 2
        # print(f'{total_points} / {total_participants_qnt} = {total_points // total_participants_qnt}')

        pdf.set_draw_color(r, g, b)
        pdf.set_fill_color(r=r, g=g, b=b)
        pdf.set_text_color(105, 105, 105)
        point1 = (average_number_x - 5, startY - 3)
        point2 = (average_number_x + 5, startY - 3)
        point3 = (average_number_x, startY-1.5)
        pdf.polygon(point_list=[point1, point2, point3, point1], style="FD")
        pdf.text(average_number_x - 4.5, startY - 3.5, 'СРЕДНЕЕ')


def draw_single_circle_arrow(pdf, x, y, number, group_color, email, bold):
    # print(f'start - {pdf.get_y()}')
    # print(f'bold - {bold}')
    if bold == 1:
        pdf.set_line_width(0.5)
    else:
        pdf.set_line_width(0.2)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("NotoSansDisplayMedium", "", 6)
    if is_orange_color(email):
        pdf.set_fill_color(241, 151, 15)
    else:
        if not group_color == 'rgba(0, 0, 0, 0)':
            color_r = int(group_color[group_color.find('(') + len('('):group_color.rfind(')')].split(',')[0])
            color_g = int(group_color[group_color.find('(') + len('('):group_color.rfind(')')].split(',')[1].strip())
            color_b = int(group_color[group_color.find('(') + len('('):group_color.rfind(')')].split(',')[2].strip())
            pdf.set_fill_color(color_r, color_g, color_b)
        else:
            pdf.set_fill_color(255, 255, 255)
    pdf.circle(x, y, r=3.4, style="FD")
    if number < 10:
        pdf.text(x + 1.1, y + 2.5, str(number))
    else:
        if 10 <= number < 20:
            pdf.text(x + 0.5, y + 2.5, str(number))
        else:
            pdf.text(x + 0.6, y + 2.5, str(number))
    # print(f'start - {pdf.get_y()}')
    pdf.set_line_width(0.2)


def draw_squares(pdf, square_results):
    startX = 15
    startY = 25 + 8
    width = 90

    ESFJ_1_1 = 0
    ENFJ_1_2 = 0
    ESFP_1_3 = 0
    ENFP_1_4 = 0
    ESTJ_2_1 = 0
    ENTJ_2_2 = 0
    ESTP_2_3 = 0
    ENTP_2_4 = 0
    ISFJ_3_1 = 0
    INFJ_3_2 = 0
    ISFP_3_3 = 0
    INFP_3_4 = 0
    ISTJ_4_1 = 0
    INTJ_4_2 = 0
    ISTP_4_3 = 0
    INTP_4_4 = 0
    top_1_max_qnt = 0
    top_2_max_qnt = 0
    bottom_1_max_qnt = 0
    bottom_2_max_qnt = 0
    delta_y_1 = 0
    delta_y_2 = 0
    delta_y_3 = 0
    delta_y_4 = 0

    for square_result in square_results:
        # print(f'square_result - {square_result}')
        square_name = square_result[0]
        if square_name == 'Магнит':
            ESFJ_1_1 = ESFJ_1_1 + 1
        if square_name == 'Фасилитатор':
            ENFJ_1_2 = ENFJ_1_2 + 1
        if square_name == 'Переговорщик':
            ESFP_1_3 = ESFP_1_3 + 1
        if square_name == 'Коннектор':
            ENFP_1_4 = ENFP_1_4 + 1
        if square_name == 'Визионер':
            ESTJ_2_1 = ESTJ_2_1 + 1
        if square_name == 'Авантюрист':
            ENTJ_2_2 = ENTJ_2_2 + 1
        if square_name == 'Искатель ресурсов':
            ESTP_2_3 = ESTP_2_3 + 1
        if square_name == 'Изобретатель':
            ENTP_2_4 = ENTP_2_4 + 1
        if square_name == 'Хранитель':
            ISFJ_3_1 = ISFJ_3_1 + 1
        if square_name == 'Вдохновитель':
            INFJ_3_2 = INFJ_3_2 + 1
        if square_name == 'Контролер':
            ISFP_3_3 = ISFP_3_3 + 1
        if square_name == 'Благородный служитель':
            INFP_3_4 = INFP_3_4 + 1
        if square_name == 'Организатор':
            ISTJ_4_1 = ISTJ_4_1 + 1
        if square_name == 'Любитель улучшений':
            INTJ_4_2 = INTJ_4_2 + 1
        if square_name == 'Реализатор':
            ISTP_4_3 = ISTP_4_3 + 1
        if square_name == 'Решатель проблем':
            INTP_4_4 = INTP_4_4 + 1


        # match square_result[0]:
            # case 'Магнит':
            #     ESFJ_1_1 = ESFJ_1_1 + 1
            # case 'ENFJ - Идеалист-харизматик':
            #     ENFJ_1_2 = ENFJ_1_2 + 1
            # case 'ESFP - Спонтанный коммуникатор':
            #     ESFP_1_3 = ESFP_1_3 + 1
            # case 'ENFP - Инициатор':
            #     ENFP_1_4 = ENFP_1_4 + 1
            # case 'Визионер по жизни':
            #     ESTJ_2_1 = ESTJ_2_1 + 1
            # case 'ENTJ - Предприниматель':
            #     ENTJ_2_2 = ENTJ_2_2 + 1
            # case 'ESTP - Ультра-реалист':
            #     ESTP_2_3 = ESTP_2_3 + 1
            # case 'Изобретатель':
            #     ENTP_2_4 = ENTP_2_4 + 1
            # case 'Хранитель':
            #     ISFJ_3_1 = ISFJ_3_1 + 1
            # case 'Вдохновитель':
            #     INFJ_3_2 = INFJ_3_2 + 1
            # case 'ISFP - Посредник':
            #     ISFP_3_3 = ISFP_3_3 + 1
            # case 'Благородный служитель':
            #     INFP_3_4 = INFP_3_4 + 1
            # case 'Организатор':
            #     ISTJ_4_1 = ISTJ_4_1 + 1
            # case 'Любитель улучшений':
            #     INTJ_4_2 = INTJ_4_2 + 1
            # case 'ISTP - Экспериментатор':
            #     ISTP_4_3 = ISTP_4_3 + 1
            # case 'Решатель проблем':
            #     INTP_4_4 = INTP_4_4 + 1

    top_1_max_qnt = max(ESFJ_1_1, ENFJ_1_2, ESTJ_2_1, ENTJ_2_2)
    top_2_max_qnt = max(ESFP_1_3, ENFP_1_4, ESTP_2_3, ENTP_2_4)
    bottom_1_max_qnt = max(ISFJ_3_1, INFJ_3_2, ISTJ_4_1, INTJ_4_2)
    bottom_2_max_qnt = max(ISFP_3_3, INFP_3_4, ISTP_4_3, INTP_4_4)
    rows_max_qnt_1 = math.ceil(top_1_max_qnt / 4)
    rows_max_qnt_2 = math.ceil(top_2_max_qnt / 4)
    rows_max_qnt_3 = math.ceil(bottom_1_max_qnt / 4)
    rows_max_qnt_4 = math.ceil(bottom_2_max_qnt / 4)

    if rows_max_qnt_1 >= 4:
        delta_y_1 = (rows_max_qnt_1 - 3) * 9
    if rows_max_qnt_2 >= 4:
        delta_y_2 = (rows_max_qnt_2 - 3) * 9
    if rows_max_qnt_3 >= 4:
        delta_y_3 = (rows_max_qnt_3 - 3) * 9
    if rows_max_qnt_4 >= 4:
        delta_y_4 = (rows_max_qnt_4 - 3) * 9

    # print(f'top_1_max_qnt - {top_1_max_qnt} top_2_max_qnt - {top_2_max_qnt} bottom_1_max_qnt - {bottom_1_max_qnt} bottom_2_max_qnt - {bottom_2_max_qnt}')
    #1
    pdf.set_draw_color(255, 240, 193)
    pdf.set_fill_color(255, 240, 193)
    # pdf.rect(startX, startY, width, width + delta_y_1 + delta_y_2, 'FD')
    pdf.rect(startX, startY, width, 120, 'FD')
    #2
    pdf.set_draw_color(253, 219, 246)
    pdf.set_fill_color(253, 219, 246)
    # pdf.rect(startX + width, startY, width, width + delta_y_1 + delta_y_2, 'FD')
    pdf.rect(startX + width, startY, width, 120, 'FD')
    #3
    pdf.set_draw_color(217, 245, 251)
    pdf.set_fill_color(217, 245, 251)
    # pdf.rect(startX, startY + width, width, width + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'FD')
    pdf.rect(startX, startY + width + 30, width, 120, 'FD')
    #4
    pdf.set_draw_color(226, 239, 218)
    pdf.set_fill_color(226, 239, 218)
    # pdf.rect(startX + width, startY + width, width, width + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'FD')
    pdf.rect(startX + width, startY + width + 30, width, 120, 'FD')

    pdf.set_draw_color(255, 255, 255)
    pdf.set_fill_color(255, 255, 255)
    # белый вертикальный разделитель первый
    # pdf.rect(startX + width / 2 - 0.3, startY, 0.6, startY + width * 2 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4 , 'FD')
    pdf.rect(startX + width / 2 - 0.3, startY, 0.6, startY + 240, 'FD')
    # белый вертикальный разделитель второй
    # pdf.rect(startX + width + width / 2 - 0.3, startY, 0.6, startY + width * 2 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'FD')
    pdf.rect(startX + width + width / 2 - 0.3, startY, 0.6, startY + 240, 'FD')
    # белый горизонтальный разделитель первый
    # pdf.rect(startX, startY + width / 2 - 0.3 + delta_y_1, startY + width * 2, 0.6, 'FD')
    pdf.rect(startX, startY + width / 2 - 0.3 + 15, startY + width * 2, 0.6, 'FD')
    # белый горизонтальный разделитель второй
    # pdf.rect(startX, startY + width + width / 2 - 0.3 + delta_y_1 + delta_y_2 + delta_y_3, startY + width * 2, 0.6, 'FD')
    pdf.rect(startX, startY + width + width / 2 - 0.3 + 45, startY + width * 2, 0.6, 'FD')

    pdf.set_font("RalewayRegular", "", 10)

    delta_1_y_text = 3 + 6
    pdf.rect(startX + width / 2 - 17 - 2, startY + width / 2 + 1, 34 + 4, 10 + 18, 'FD')
    pdf.text(startX + width / 2 - 15 + 4, startY + width / 2 + delta_1_y_text, 'Интеграторы')

    delta_Y_between_lines_in_square_name = 3
    first_line_description_delta_y = 5
    cur_delta_Y_between_lines_in_square_name = first_line_description_delta_y
    pdf.set_font("RalewayLight", "", 9)

    pdf.text(startX + width / 2 - 9, startY + width / 2 + delta_1_y_text + cur_delta_Y_between_lines_in_square_name, 'Cтремятся к')

    cur_delta_Y_between_lines_in_square_name = cur_delta_Y_between_lines_in_square_name + delta_Y_between_lines_in_square_name
    pdf.text(startX + width / 2 - 1 - 12, startY + width / 2 + delta_1_y_text + cur_delta_Y_between_lines_in_square_name, 'передаче знаний')

    cur_delta_Y_between_lines_in_square_name = cur_delta_Y_between_lines_in_square_name + delta_Y_between_lines_in_square_name
    pdf.text(startX + width / 2 - 11, startY + width / 2 + delta_1_y_text + cur_delta_Y_between_lines_in_square_name, 'и целостности')

    cur_delta_Y_between_lines_in_square_name = cur_delta_Y_between_lines_in_square_name + delta_Y_between_lines_in_square_name
    pdf.text(startX + width / 2 - 7, startY + width / 2 + delta_1_y_text + cur_delta_Y_between_lines_in_square_name, 'культуры')


    pdf.set_font("RalewayRegular", "", 10)

    pdf.rect(startX + width + width / 2 - 17 - 2, startY + width / 2 + 1, 34 + 4, 10 + 18, 'FD')
    pdf.text(startX + width + width / 2 - 15.5, startY + width / 2 + delta_1_y_text, 'Предприниматели')

    delta_Y_between_lines_in_square_name = 3
    cur_delta_Y_between_lines_in_square_name = first_line_description_delta_y
    pdf.set_font("RalewayLight", "", 9)

    pdf.text(startX + width + width / 2 - 9, startY + width / 2 + delta_1_y_text + cur_delta_Y_between_lines_in_square_name, 'Cтремятся к')

    cur_delta_Y_between_lines_in_square_name = cur_delta_Y_between_lines_in_square_name + delta_Y_between_lines_in_square_name
    pdf.text(startX + width + width / 2 - 1 - 6, startY + width / 2 + delta_1_y_text + cur_delta_Y_between_lines_in_square_name, 'развитию')

    cur_delta_Y_between_lines_in_square_name = cur_delta_Y_between_lines_in_square_name + delta_Y_between_lines_in_square_name
    pdf.text(startX + width + width / 2 - 1 - 5, startY + width / 2 + delta_1_y_text + cur_delta_Y_between_lines_in_square_name, 'бизнеса')

    # pdf.rect(startX + width / 2 - 17, startY + width + width / 2 - 5 + delta_y_1 + delta_y_2 + delta_y_3, 34, 10, 'FD')
    # pdf.text(startX + width / 2 - 15 + 0.5, startY + width + width / 2 + 1 + delta_y_1 + delta_y_2 + delta_y_3, 'Администраторы')
    #
    # pdf.rect(startX + width + width / 2 - 17, startY + width + width / 2 - 5 + delta_y_1 + delta_y_2 + delta_y_3, 34, 10, 'FD')
    # pdf.text(startX + width + width / 2 - 15 + 2, startY + width + width / 2 + 1 + delta_y_1 + delta_y_2 + delta_y_3, 'Производители')

    pdf.set_font("RalewayRegular", "", 10)

    pdf.rect(startX + width / 2 - 17 - 2, startY + width + width / 2 + 1 + 30, 34 + 4, 10 + 18, 'FD')
    pdf.text(startX + width / 2 - 15 + 0.5, startY + width + width / 2 + delta_1_y_text + 30, 'Администраторы')

    delta_Y_between_lines_in_square_name = 3
    cur_delta_Y_between_lines_in_square_name = first_line_description_delta_y
    pdf.set_font("RalewayLight", "", 9)

    pdf.text(startX + width / 2 - 9, startY + width + width / 2 + delta_1_y_text + 30 + cur_delta_Y_between_lines_in_square_name, 'Cтремятся к')

    cur_delta_Y_between_lines_in_square_name = cur_delta_Y_between_lines_in_square_name + delta_Y_between_lines_in_square_name
    pdf.text(startX + width / 2 - 1 - 10, startY + width + width / 2 + delta_1_y_text + 30 + cur_delta_Y_between_lines_in_square_name, 'прозрачности и')

    cur_delta_Y_between_lines_in_square_name = cur_delta_Y_between_lines_in_square_name + delta_Y_between_lines_in_square_name
    pdf.text(startX + width / 2 - 11, startY + width + width / 2 + delta_1_y_text + 30 + cur_delta_Y_between_lines_in_square_name, 'эффективности')

    cur_delta_Y_between_lines_in_square_name = cur_delta_Y_between_lines_in_square_name + delta_Y_between_lines_in_square_name
    pdf.text(startX + width / 2 - 5, startY + width + width / 2 + delta_1_y_text + 30 + cur_delta_Y_between_lines_in_square_name, 'работы')

    pdf.set_font("RalewayRegular", "", 10)

    pdf.rect(startX + width + width / 2 - 17 - 2, startY + width + width / 2 + 1 + 30, 34 + 4, 10 + 18, 'FD')
    pdf.text(startX + width + width / 2 - 15 + 2, startY + width + width / 2 + delta_1_y_text + 30, 'Производители')

    delta_Y_between_lines_in_square_name = 3
    cur_delta_Y_between_lines_in_square_name = first_line_description_delta_y
    pdf.set_font("RalewayLight", "", 9)

    pdf.text(startX + width + width / 2 - 10, startY + width + width / 2 + delta_1_y_text + 30 + cur_delta_Y_between_lines_in_square_name, 'Нацелены на')

    cur_delta_Y_between_lines_in_square_name = cur_delta_Y_between_lines_in_square_name + delta_Y_between_lines_in_square_name
    pdf.text(startX + width + width / 2 - 1 - 8, startY + width + width / 2 + delta_1_y_text + 30 + cur_delta_Y_between_lines_in_square_name, 'выполнение')

    cur_delta_Y_between_lines_in_square_name = cur_delta_Y_between_lines_in_square_name + delta_Y_between_lines_in_square_name
    pdf.text(startX + width + width / 2 - 1 - 6, startY + width + width / 2 + delta_1_y_text + 30 + cur_delta_Y_between_lines_in_square_name, 'планов и')

    cur_delta_Y_between_lines_in_square_name = cur_delta_Y_between_lines_in_square_name + delta_Y_between_lines_in_square_name
    pdf.text(startX + width + width / 2 - 12, startY + width + width / 2 + delta_1_y_text + 30 + cur_delta_Y_between_lines_in_square_name, 'продуктивность')

    # названия квадратов
    pdf.set_font("RalewayRegular", "", 8)

    pdf.text(startX + width / 2 - 13, startY - 2.5, 'Фокус на процесс')
    pdf.text(startX + width / 2 + width - 13.5, startY - 2.5, 'Фокус на результат')
    with pdf.rotation(90, 12, startY + width / 2 + 10 + 15):
        pdf.text(0, startY + width / 2 + 10 + 15, "Неструктурированный подход")
    with pdf.rotation(270, startX + width * 2 + 3, startY + width / 2 - 18 + 15):
        pdf.text(startX + width * 2 + 3, startY + width / 2 - 18 + 15, "Концептуальные решения")
    with pdf.rotation(90, 12, startY + width / 2 + 7 + width + 45):
        pdf.text(0, startY + width / 2 + 7 + width + 45, "Структурированный подход")
    with pdf.rotation(270, startX + width * 2 + 3, startY + width / 2 - 15 + width + 45):
        pdf.text(startX + width * 2 + 3, startY + width / 2 - 15 + width + 45, "Локальные решения")
    # with pdf.rotation(90, 12, startY + width / 2 + 10 + delta_y_1):
    #     pdf.text(0, startY + width / 2 + 10 + delta_y_1, "Неструктурированный подход")
    # with pdf.rotation(270, startX + width * 2 + 3, startY + width / 2 - 18 + delta_y_1):
    #     pdf.text(startX + width * 2 + 3, startY + width / 2 - 18 + delta_y_1, "Концептуальные решения")
    # with pdf.rotation(90, 12, startY + width / 2 + 7 + width + delta_y_1 + delta_y_2 + delta_y_3):
    #     pdf.text(0, startY + width / 2 + 7 + width + delta_y_1 + delta_y_2 + delta_y_3, "Структурированный подход")
    # with pdf.rotation(270, startX + width * 2 + 3, startY + width / 2 - 15 + width + delta_y_1 + delta_y_2 + delta_y_3):
    #     pdf.text(startX + width * 2 + 3, startY + width / 2 - 15 + width + delta_y_1 + delta_y_2 + delta_y_3, "Локальные решения")

    pdf.set_font("RalewayLight", "", 8)

    # pdf.text(startX + width / 4 - 3, startY + 4, 'ESFJ')
    # pdf.text(startX + width / 4 - 13, startY + 7, 'Массовик-затейник')
    pdf.text(startX + width / 4 - 4, startY + 4, 'Магнит')

    # pdf.text(startX + width * (3/4) - 3, startY + 4, 'ENFJ')
    # pdf.text(startX + width * (3/4) - 13, startY + 7, 'Идеалист-харизматик')
    pdf.text(startX + width * (3/4) - 9, startY + 4, 'Фасилитатор')

    # pdf.text(startX + width + width / 4 - 3, startY + 4, 'ESTJ')
    # pdf.text(startX + width + width / 4 - 14, startY + 7, 'Контролер по жизни')
    pdf.text(startX + width + width / 4 - 7, startY + 4, 'Визионер')

    # pdf.text(startX + width + width * (3/4) - 3, startY + 4, 'ENTJ')
    # pdf.text(startX + width + width * (3/4) - 11, startY + 7, 'Предприниматель')
    pdf.text(startX + width + width * (3/4) - 7, startY + 4, 'Авантюрист')

    # pdf.text(startX + width / 4 - 3, startY + width - 6 + delta_y_1 + delta_y_2, 'ESFP')
    # pdf.text(startX + width / 4 - 18.5, startY + width - 3 + delta_y_1 + delta_y_2, 'Спонтанный коммуникатор')
    pdf.text(startX + width / 4 - 10, startY + width - 3 + 30, 'Переговорщик')

    # pdf.text(startX + width * (3/4) - 3, startY + width - 6 + delta_y_1 + delta_y_2, 'ENFP')
    # pdf.text(startX + width * (3/4) - 7, startY + width - 3 + delta_y_1 + delta_y_2, 'Инициатор')
    pdf.text(startX + width * (3/4) - 7, startY + width - 3 + 30, 'Коннектор')

    # pdf.text(startX + width + width / 4 - 3, startY + width - 6 + delta_y_1 + delta_y_2, 'ESTP')
    # pdf.text(startX + width + width / 4 - 10, startY + width - 3 + delta_y_1 + delta_y_2, 'Ультра-реалист')
    pdf.text(startX + width + width / 4 - 12, startY + width - 3 + 30, 'Искатель ресурсов')

    # pdf.text(startX + width + width * (3/4) - 3, startY + width - 6 + delta_y_1 + delta_y_2, 'ENTP')
    pdf.text(startX + width + width * (3/4) - 9, startY + width - 3 + 30, 'Изобретатель')

    # pdf.text(startX + width / 4 - 3, startY + width + 4 + delta_y_1 + delta_y_2, 'ISFJ')
    # pdf.text(startX + width / 4 - 7, startY + width + 7 + delta_y_1 + delta_y_2, 'Хранитель')
    pdf.text(startX + width / 4 - 7, startY + width + 4 + 30, 'Хранитель')

    # pdf.text(startX + width * (3/4) - 3, startY + width + 4 + delta_y_1 + delta_y_2, 'INFJ')
    # pdf.text(startX + width * (3/4) - 9, startY + width + 7 + delta_y_1 + delta_y_2, 'Вдохновитель')
    pdf.text(startX + width * (3/4) - 9, startY + width + 4 + 30, 'Вдохновитель')

    # pdf.text(startX + width + width / 4 - 3, startY + width + 4 + delta_y_1 + delta_y_2, 'ISTJ')
    # pdf.text(startX + width + width / 4 - 8, startY + width + 7 + delta_y_1 + delta_y_2, 'Организатор')
    pdf.text(startX + width + width / 4 - 7, startY + width + 4 + 30, 'Организатор')

    # pdf.text(startX + width + width * (3/4) - 3, startY + width + 4 + delta_y_1 + delta_y_2, 'INTJ')
    # pdf.text(startX + width + width * (3/4) - 14, startY + width + 7 + delta_y_1 + delta_y_2, 'Любитель улучшений')
    pdf.text(startX + width + width * (3/4) - 14, startY + width + 4 + 30, 'Любитель улучшений')

    # pdf.text(startX + width / 4 - 3, startY + width + width - 6 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'ISFP')
    # pdf.text(startX + width / 4 - 7, startY + width + width - 3 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'Посредник')
    pdf.text(startX + width / 4 - 7, startY + width + width - 3 + 60, 'Контролер')

    # pdf.text(startX + width * (3/4) - 3, startY + width + width - 6 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'INFP')
    pdf.text(startX + width * (3/4) - 16, startY + width + width - 3 + 60, 'Благородный служитель')

    # pdf.text(startX + width + width / 4 - 3, startY + width + width - 6 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'ISTP')
    # pdf.text(startX + width + width / 4 - 12, startY + width + width - 3 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'Экспериментатор')
    pdf.text(startX + width + width / 4 - 8, startY + width + width - 3 + 60, 'Реализатор')

    # pdf.text(startX + width + width * (3/4) - 3, startY + width + width - 6 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'INTP')
    pdf.text(startX + width + width * (3/4) - 12, startY + width + width - 3 + 60, 'Решатель проблем')

    pdf.set_line_width(0.5)
    pdf.set_draw_color(240)
    pdf.set_font("NotoSansDisplayMedium", "", 10)

    text_y_delta = 5.2
    text_x_delta = 3

    square_x_cnt = {
        'Магнит': {
            'circle_coords': [startX + 5, startY + 10],
            'text_coords': [startX + 5 + text_x_delta, startY + 10 + text_y_delta],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Фасилитатор': {
            'circle_coords': [startX + 5 + width / 2, startY + 10],
            'text_coords': [startX + 5 + text_x_delta + width / 2, startY + 10 + text_y_delta],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Переговорщик': {
            'circle_coords': [startX + 5, startY + 10 + width / 2 - 2 + 26],
            'text_coords': [startX + 5 + text_x_delta, startY + 10 + text_y_delta + width / 2 - 2 + 26],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Коннектор': {
            'circle_coords': [startX + 5 + width / 2, startY + 10 + width / 2 - 2 + 26],
            'text_coords': [startX + 5 + text_x_delta + width / 2, startY + 10 + text_y_delta + width / 2 - 2 + 26],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Визионер': {
            'circle_coords': [startX + 5 + width, startY + 10],
            'text_coords': [startX + 5 + text_x_delta + width, startY + 10 + text_y_delta],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Авантюрист': {
            'circle_coords': [startX + 5 + width + width / 2, startY + 10],
            'text_coords': [startX + 5 + text_x_delta + width + width / 2, startY + 10 + text_y_delta],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Искатель ресурсов': {
            'circle_coords': [startX + 5 + width, startY + 10 + width / 2 - 2 + 26],
            'text_coords': [startX + 5 + text_x_delta + width, startY + 10 + text_y_delta + width / 2 - 2 + 26],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Изобретатель': {
            'circle_coords': [startX + 5 + width + width / 2, startY + 10 + width / 2 - 2 + 26],
            'text_coords': [startX + 5 + text_x_delta + width + width / 2, startY + 10 + text_y_delta + width / 2 - 2 + 26],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Хранитель': {
            'circle_coords': [startX + 5, startY + 10 + width + 30],
            'text_coords': [startX + 5 + text_x_delta, startY + 10 + text_y_delta + width + 30],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Вдохновитель': {
            'circle_coords': [startX + 5 + width / 2, startY + 10 + width + 30],
            'text_coords': [startX + 5 + text_x_delta + width / 2, startY + 10 + text_y_delta + width + 30],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Контролер': {
            'circle_coords': [startX + 5, startY + 10 + width / 2 + width - 2 + 56],
            'text_coords': [startX + 5 + text_x_delta, startY + 10 + text_y_delta + width / 2 + width - 2 + 56],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Благородный служитель': {
            'circle_coords': [startX + 5 + width / 2, startY + 10 + width / 2 + width - 2 + 56],
            'text_coords': [startX + 5 + text_x_delta + width / 2, startY + 10 + text_y_delta + width / 2 + width - 2 + 56],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},

        'Организатор': {
            'circle_coords': [startX + 5 + width, startY + 10 + width + 30],
            'text_coords': [startX + 5 + text_x_delta + width, startY + 10 + text_y_delta + width + 30],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Любитель улучшений': {
            'circle_coords': [startX + 5 + width + width / 2, startY + 10 + width + 30],
            'text_coords': [startX + 5 + text_x_delta + width + width / 2, startY + 10 + text_y_delta + width + 30],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Реализатор': {
            'circle_coords': [startX + 5 + width, startY + 10 + width / 2 + width - 2 + 56],
            'text_coords': [startX + 5 + text_x_delta + width, startY + 10 + text_y_delta + width / 2 + width - 2 + 56],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Решатель проблем': {
            'circle_coords': [startX + 5 + width + width / 2, startY + 10 + width / 2 + width - 2 + 56],
            'text_coords': [startX + 5 + text_x_delta + width + width / 2, startY + 10 + text_y_delta + width / 2 + width - 2 + 56],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
    }
    cnt = 0

    for square_data in square_results:
        cnt = cnt + 1
        draw_single_circle_squares(square_data, pdf, square_x_cnt, cnt)


def is_orange_color(email):
    report = Report.objects.filter(participant__employee__email=email).latest('added')
    report_data = ReportData.objects.filter(report=report, section_code='3')
    section_1 = 0
    section_2 = 0
    section_3 = 0

    for report_data_item in report_data:
        split = report_data_item.category_code.split('_')
        if int(split[1]) <= 4:
            section_1 = section_1 + report_data_item.points
        elif 5 <= int(split[1]) <= 8:
            section_2 = section_2 + report_data_item.points
        elif int(split[1]) >= 9:
            section_3 = section_3 + report_data_item.points
    if section_1 > 18 or section_2 > 18 or section_3 > 18 or section_2 >= 7:
        return True
    else:
        return False


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

    pdf.set_line_width(0.1)
    pdf.line(start_X, start_Y + total_height / 2 / 2, start_X + total_width, start_Y + total_height / 2 / 2) #горизонтальная линия 1/4
    pdf.line(start_X, start_Y + total_height * (3/4), start_X + total_width, start_Y + total_height * (3/4)) #горизонтальная линия 3/4
    pdf.line(start_X + total_width / 2 / 2, start_Y, start_X + total_width / 2 / 2,  start_Y + total_height) #вертикальная линия 1/4
    pdf.line(start_X + total_width * (3/4), start_Y, start_X + total_width * (3/4), start_Y + total_height) #вертикальная линия 3/4

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
    text = u'Данная мтарица отражает группы характеристик, определеюящие рабочее поведение участников. ' \
           u'Матрица построена на основе двух осей:\n' \
           u'• яркость проявления (насколкь развита данная характеристика у большинства участников)\n' \
           u'• согласованность результатов (насколько похоже проявляют характеристику большинство участников)\n \n' \
           u'В зеленый квадрат попадают характеристики, которые ярко проявляются у большиснмтва участников. В данном квадрате ' \
           u'размещены ключевые ресурсы, за счет которых участники выполняют работу и добиваются результатов.\n \n' \
           u'В красный квадрат попадают характеристики, которые слабо проявляются у большиснмтва участников. В данном квадрате ' \
           u'размещены ключевые ресурсы, за счет которых участники выполняют работу и добиваются результатов.'

    pdf.multi_cell(0, 4, text)

    draw_integral_report_items(pdf, start_X, start_Y, end_X, end_Y, square_results)


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
            print(f'++++{integral_report_filter.name}++++')
            print(categories_t_points)
            for category_points in categories_t_points:
                average_category_t_points = math.floor((sum(category_points) / len(category_points)) * 10) / 10
                points_variance_from_average_in_category = []
                for point in category_points:
                    points_variance_from_average_in_category.append(abs(average_category_t_points - point))
                # print('---points_variance_from_average_in_category---')
                # print(points_variance_from_average_in_category)
                # print('---')
                variance_from_average.append(math.floor((sum(points_variance_from_average_in_category) / len(
                    points_variance_from_average_in_category)) * 10) / 10)
                # variance_from_average.append(math.floor((sum(points_variance_from_average_in_category) / 3) * 10) / 10)
            # print('---variance_from_average---')
            # print(variance_from_average)
            # print('----')
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
    print(integral_report_data)
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



