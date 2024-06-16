from pdf.models import Report, ReportData
import math


def draw_arrow(pdf, startX, startY, r, g, b, data_by_points):
    # print(f'data_by_points - {data_by_points}')
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
                group_color = scale_number_data[3]
                email = scale_number_data[4]
                total_points = total_points + scale_number_data[1]
                bold = scale_number_data[5]
                circles_placed_cnt = circles_placed_cnt + 1

                if cur_col > col_qnt:
                    delta_y = delta_y + 3.5
                    cur_col = 1
                    first_item_x = 0

                scale_number_x = startX + scale_number_data[1] * section_width - section_width / 2  # x позиция черты на шкале
                draw_single_circle_arrow(pdf, scale_number_x - 1.75 * col_qnt + first_item_x, startY + 5.5 + delta_y, scale_number_data[2], group_color, email, bold)
                first_item_x = first_item_x + 3.5
                cur_col = cur_col + 1

            total_participants_qnt = total_participants_qnt + circles_placed_cnt

    #треугольник СРЕДНЕЕ
    if total_participants_qnt > 0:
        average_number_x = startX + (total_points // total_participants_qnt) * section_width - section_width / 2
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
    pdf.rect(startX, startY, width, width + delta_y_1 + delta_y_2, 'FD')
    #2
    pdf.set_draw_color(253, 219, 246)
    pdf.set_fill_color(253, 219, 246)
    pdf.rect(startX + width, startY, width, width + delta_y_1 + delta_y_2, 'FD')
    #3
    pdf.set_draw_color(217, 245, 251)
    pdf.set_fill_color(217, 245, 251)
    pdf.rect(startX, startY + width, width, width + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'FD')
    #4
    pdf.set_draw_color(226, 239, 218)
    pdf.set_fill_color(226, 239, 218)
    pdf.rect(startX + width, startY + width, width, width + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'FD')

    pdf.set_draw_color(255, 255, 255)
    pdf.set_fill_color(255, 255, 255)
    # белый вертикальный разделитель первый
    pdf.rect(startX + width / 2 - 0.3, startY, 0.6, startY + width * 2 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4 , 'FD')
    # белый вертикальный разделитель второй
    pdf.rect(startX + width + width / 2 - 0.3, startY, 0.6, startY + width * 2 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'FD')
    # белый горизонтальный разделитель первый
    pdf.rect(startX, startY + width / 2 - 0.3 + delta_y_1, startY + width * 2, 0.6, 'FD')
    # белый горизонтальный разделитель второй
    pdf.rect(startX, startY + width + width / 2 - 0.3 + delta_y_1 + delta_y_2 + delta_y_3, startY + width * 2, 0.6, 'FD')

    pdf.set_font("RalewayLight", "", 10)

    pdf.rect(startX + width / 2 - 17, startY + width / 2 - 5 + delta_y_1, 34, 10, 'FD')
    pdf.text(startX + width / 2 - 15 + 4, startY + width / 2 + 1 + delta_y_1, 'Интеграторы')

    pdf.rect(startX + width + width / 2 - 17, startY + width / 2 - 5 + delta_y_1, 34, 10, 'FD')
    pdf.text(startX + width + width / 2 - 15.5, startY + width / 2 + 1 + delta_y_1, 'Предприниматели')

    pdf.rect(startX + width / 2 - 17, startY + width + width / 2 - 5 + delta_y_1 + delta_y_2 + delta_y_3, 34, 10, 'FD')
    pdf.text(startX + width / 2 - 15 + 0.5, startY + width + width / 2 + 1 + delta_y_1 + delta_y_2 + delta_y_3, 'Администраторы')

    pdf.rect(startX + width + width / 2 - 17, startY + width + width / 2 - 5 + delta_y_1 + delta_y_2 + delta_y_3, 34, 10, 'FD')
    pdf.text(startX + width + width / 2 - 15 + 2, startY + width + width / 2 + 1 + delta_y_1 + delta_y_2 + delta_y_3, 'Производители')

    # названия квадратов
    pdf.set_font("RalewayRegular", "", 8)

    pdf.text(startX + width / 2 - 13, startY - 2.5, 'Фокус на процесс')
    pdf.text(startX + width / 2 + width - 13.5, startY - 2.5, 'Фокус на результат')
    with pdf.rotation(90, 12, startY + width / 2 + 10 + delta_y_1):
        pdf.text(0, startY + width / 2 + 10 + delta_y_1, "Неструктурированный подход")
    with pdf.rotation(270, startX + width * 2 + 3, startY + width / 2 - 18 + delta_y_1):
        pdf.text(startX + width * 2 + 3, startY + width / 2 - 18 + delta_y_1, "Концептуальные решения")
    with pdf.rotation(90, 12, startY + width / 2 + 7 + width + delta_y_1 + delta_y_2 + delta_y_3):
        pdf.text(0, startY + width / 2 + 7 + width + delta_y_1 + delta_y_2 + delta_y_3, "Структурированный подход")
    with pdf.rotation(270, startX + width * 2 + 3, startY + width / 2 - 15 + width + delta_y_1 + delta_y_2 + delta_y_3):
        pdf.text(startX + width * 2 + 3, startY + width / 2 - 15 + width + delta_y_1 + delta_y_2 + delta_y_3, "Локальные решения")

    pdf.set_font("RalewayLight", "", 8)

    # pdf.text(startX + width / 4 - 3, startY + 4, 'ESFJ')
    # pdf.text(startX + width / 4 - 13, startY + 7, 'Массовик-затейник')
    pdf.text(startX + width / 4 - 13, startY + 4, 'Массовик-затейник')

    # pdf.text(startX + width * (3/4) - 3, startY + 4, 'ENFJ')
    # pdf.text(startX + width * (3/4) - 13, startY + 7, 'Идеалист-харизматик')
    pdf.text(startX + width * (3/4) - 12, startY + 4, 'Чуткий наставник')

    # pdf.text(startX + width + width / 4 - 3, startY + 4, 'ESTJ')
    # pdf.text(startX + width + width / 4 - 14, startY + 7, 'Контролер по жизни')
    pdf.text(startX + width + width / 4 - 8, startY + 4, 'Контролер')

    # pdf.text(startX + width + width * (3/4) - 3, startY + 4, 'ENTJ')
    # pdf.text(startX + width + width * (3/4) - 11, startY + 7, 'Предприниматель')
    pdf.text(startX + width + width * (3/4) - 5, startY + 4, 'Аналитик')

    # pdf.text(startX + width / 4 - 3, startY + width - 6 + delta_y_1 + delta_y_2, 'ESFP')
    # pdf.text(startX + width / 4 - 18.5, startY + width - 3 + delta_y_1 + delta_y_2, 'Спонтанный коммуникатор')
    pdf.text(startX + width / 4 - 9, startY + width - 3 + delta_y_1 + delta_y_2, 'Развлекатель')

    # pdf.text(startX + width * (3/4) - 3, startY + width - 6 + delta_y_1 + delta_y_2, 'ENFP')
    # pdf.text(startX + width * (3/4) - 7, startY + width - 3 + delta_y_1 + delta_y_2, 'Инициатор')
    pdf.text(startX + width * (3/4) - 7, startY + width - 3 + delta_y_1 + delta_y_2, 'Мотиватор')

    # pdf.text(startX + width + width / 4 - 3, startY + width - 6 + delta_y_1 + delta_y_2, 'ESTP')
    # pdf.text(startX + width + width / 4 - 10, startY + width - 3 + delta_y_1 + delta_y_2, 'Ультра-реалист')
    pdf.text(startX + width + width / 4 - 12, startY + width - 3 + delta_y_1 + delta_y_2, 'Искатель ресурсов')

    # pdf.text(startX + width + width * (3/4) - 3, startY + width - 6 + delta_y_1 + delta_y_2, 'ENTP')
    pdf.text(startX + width + width * (3/4) - 9, startY + width - 3 + delta_y_1 + delta_y_2, 'Изобретатель')

    # pdf.text(startX + width / 4 - 3, startY + width + 4 + delta_y_1 + delta_y_2, 'ISFJ')
    # pdf.text(startX + width / 4 - 7, startY + width + 7 + delta_y_1 + delta_y_2, 'Хранитель')
    pdf.text(startX + width / 4 - 7, startY + width + 4 + delta_y_1 + delta_y_2, 'Хранитель')

    # pdf.text(startX + width * (3/4) - 3, startY + width + 4 + delta_y_1 + delta_y_2, 'INFJ')
    # pdf.text(startX + width * (3/4) - 9, startY + width + 7 + delta_y_1 + delta_y_2, 'Вдохновитель')
    pdf.text(startX + width * (3/4) - 9, startY + width + 4 + delta_y_1 + delta_y_2, 'Вдохновитель')

    # pdf.text(startX + width + width / 4 - 3, startY + width + 4 + delta_y_1 + delta_y_2, 'ISTJ')
    # pdf.text(startX + width + width / 4 - 8, startY + width + 7 + delta_y_1 + delta_y_2, 'Организатор')
    pdf.text(startX + width + width / 4 - 6, startY + width + 4 + delta_y_1 + delta_y_2, 'Организатор')

    # pdf.text(startX + width + width * (3/4) - 3, startY + width + 4 + delta_y_1 + delta_y_2, 'INTJ')
    # pdf.text(startX + width + width * (3/4) - 14, startY + width + 7 + delta_y_1 + delta_y_2, 'Любитель улучшений')
    pdf.text(startX + width + width * (3/4) - 14, startY + width + 4 + delta_y_1 + delta_y_2, 'Любитель улучшений')

    # pdf.text(startX + width / 4 - 3, startY + width + width - 6 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'ISFP')
    # pdf.text(startX + width / 4 - 7, startY + width + width - 3 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'Посредник')
    pdf.text(startX + width / 4 - 5, startY + width + width - 3 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'Опекун')

    # pdf.text(startX + width * (3/4) - 3, startY + width + width - 6 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'INFP')
    pdf.text(startX + width * (3/4) - 16, startY + width + width - 3 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'Благородный служитель')

    # pdf.text(startX + width + width / 4 - 3, startY + width + width - 6 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'ISTP')
    # pdf.text(startX + width + width / 4 - 12, startY + width + width - 3 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'Экспериментатор')
    pdf.text(startX + width + width / 4 - 9, startY + width + width - 3 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'Исполнитель')

    # pdf.text(startX + width + width * (3/4) - 3, startY + width + width - 6 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'INTP')
    pdf.text(startX + width + width * (3/4) - 12, startY + width + width - 3 + delta_y_1 + delta_y_2 + delta_y_3 + delta_y_4, 'Решатель проблем')

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
            'circle_coords': [startX + 5, startY + 10 + width / 2 - 2 + delta_y_1],
            'text_coords': [startX + 5 + text_x_delta, startY + 10 + text_y_delta + width / 2 - 2 + delta_y_1],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Коннектор': {
            'circle_coords': [startX + 5 + width / 2, startY + 10 + width / 2 - 2 + delta_y_1 + delta_y_2],
            'text_coords': [startX + 5 + text_x_delta + width / 2, startY + 10 + text_y_delta + width / 2 - 2 + delta_y_1],
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
            'text_coords': [startX + 5 + text_x_delta + width  + width / 2, startY + 10 + text_y_delta],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Искатель ресурсов': {
            'circle_coords': [startX + 5 + width, startY + 10 + width / 2 - 2 + delta_y_1],
            'text_coords': [startX + 5 + text_x_delta + width, startY + 10 + text_y_delta + width / 2 - 2 + delta_y_1],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Изобретатель': {
            'circle_coords': [startX + 5 + width + width / 2, startY + 10 + width / 2 - 2 + delta_y_1],
            'text_coords': [startX + 5 + text_x_delta + width + width / 2, startY + 10 + text_y_delta + width / 2 - 2 + delta_y_1],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Хранитель': {
            'circle_coords': [startX + 5, startY + 10 + width + delta_y_1 + delta_y_2],
            'text_coords': [startX + 5 + text_x_delta, startY + 10 + text_y_delta + width + delta_y_1 + delta_y_2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Вдохновитель': {
            'circle_coords': [startX + 5 + width / 2, startY + 10 + width + delta_y_1 + delta_y_2],
            'text_coords': [startX + 5 + text_x_delta + width / 2, startY + 10 + text_y_delta + width + delta_y_1 + delta_y_2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Контролер': {
            'circle_coords': [startX + 5, startY + 10 + width / 2 + width - 2 + delta_y_1 + delta_y_2 + delta_y_3],
            'text_coords': [startX + 5 + text_x_delta, startY + 10 + text_y_delta + width / 2 + width - 2 + delta_y_1 + delta_y_2 + delta_y_3],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Благородный служитель': {
            'circle_coords': [startX + 5 + width / 2, startY + 10 + width / 2 + width - 2 + delta_y_1 + delta_y_2 + delta_y_3],
            'text_coords': [startX + 5 + text_x_delta + width / 2, startY + 10 + text_y_delta + width / 2 + width - 2 + delta_y_1 + delta_y_2 + delta_y_3],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},

        'Организатор': {
            'circle_coords': [startX + 5 + width, startY + 10 + width + delta_y_1 + delta_y_2],
            'text_coords': [startX + 5 + text_x_delta + width, startY + 10 + text_y_delta + width + delta_y_1 + delta_y_2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Любитель улучшений': {
            'circle_coords': [startX + 5 + width + width / 2, startY + 10 + width + delta_y_1 + delta_y_2],
            'text_coords': [startX + 5 + text_x_delta + width + width / 2, startY + 10 + text_y_delta + width + delta_y_1 + delta_y_2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Реализатор': {
            'circle_coords': [startX + 5 + width, startY + 10 + width / 2 + width - 2 + delta_y_1 + delta_y_2 + delta_y_3],
            'text_coords': [startX + 5 + text_x_delta + width, startY + 10 + text_y_delta + width / 2 + width - 2 + delta_y_1 + delta_y_2 + delta_y_3],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        'Решатель проблем': {
            'circle_coords': [startX + 5 + width + width / 2, startY + 10 + width / 2 + width - 2 + delta_y_1 + delta_y_2 + delta_y_3],
            'text_coords': [startX + 5 + text_x_delta + width + width / 2, startY + 10 + text_y_delta + width / 2 + width - 2 + delta_y_1 + delta_y_2 + delta_y_3],
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
    pdf.text_annotation(square_x_cnt[square_name]['circle_coords'][0] + 9 * square_x_cnt[square_name]['cur_X_pos'] + 3, square_x_cnt[square_name]['circle_coords'][1] + 9 * square_x_cnt[square_name]['cur_Y_pos'] - 3, 'Фамилия', 3, 3, flags=('NO_VIEW',))
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

