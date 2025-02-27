from pdf.models import PotentialMatrix, ReportDataByCategories, Report, ConditionGroupCategoryPotentialMatrix, \
    ConditionGroup, ConditionGroupOfGroups, ConditionGroupPotentialMatrix
from django.db.models import Sum, Q,Max



def draw_potential_matrix_squares(pdf, lang, start_x, request_json):
    print('матрица потенциала square_results')
    # print(square_results)
    print('==================================')
    start_X = start_x
    start_Y = 25 + 3
    end_X = 190
    total_width = end_X - start_X
    end_Y = start_Y + total_width
    total_height = end_Y - start_Y

    # 1.3 (зеленый квадрат)
    pdf.set_fill_color(226, 239, 218)
    pdf.rect(start_X + total_width / 3 * 2, start_Y, total_width / 3, total_height / 3, 'F')

    # 3.3 красный квадрат
    pdf.set_fill_color(255, 200, 200)
    pdf.rect(start_X, start_Y + total_height / 3 * 2, total_width / 3, total_height / 3, 'F')

    print(f'total_width - {total_width}')
    pdf.set_line_width(0.4)
    pdf.set_draw_color(r=135, g=135, b=135)
    pdf.rect(start_X, start_Y, total_width, total_height, 'D') #обводка

    pdf.set_line_width(0.1)
    pdf.line(start_X, start_Y + total_height / 3, start_X + total_width, start_Y + total_height / 3) #вертикальная линия 1
    pdf.line(start_X, start_Y + total_height / 3 * 2, start_X + total_width, start_Y + total_height / 3 * 2) #вертикальная линия 2

    pdf.line(start_X + total_width / 3, start_Y, start_X + total_width / 3, start_Y + total_height) #вертикальная линия 1
    pdf.line(start_X + total_width / 3 * 2, start_Y, start_X + total_width / 3 * 2, start_Y + total_height) #вертикальная линия 1

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
    pdf.rect(start_X, start_Y + total_height + 0.5, 20, 4, 'FD')
    pdf.text(start_X + 5, start_Y + total_height + 3.5, 'Низко')

    pdf.rect(start_X + total_width - 20, start_Y + total_height + 0.5, 20 + 4 + 0.5, 4, 'FD')
    pdf.text(start_X + total_width - 15, start_Y + total_height + 3.5, 'Высоко')

    # pdf.set_text_color(r=135, g=135, b=135)
    # pdf.text(start_X + total_width / 2 / 2 - 2, start_Y + total_height + 3, '25%')
    # pdf.text(start_X + total_width / 2 - 2, start_Y + total_height + 3, '50%')
    # pdf.text(start_X + total_width * (3/4) - 2, start_Y + total_height + 3, '75%')

    # вертикальная ось
    pdf.set_text_color(118, 134, 146)

    pdf.rect(start_X + total_width + 0.5, start_Y + total_height - 20, 4, 21, 'FD')
    with pdf.rotation(90, start_X + total_width + 3.5, start_Y + total_height - 5):
        pdf.text(start_X + total_width + 3.5, start_Y + total_height - 5, 'Низко')

    pdf.rect(start_X + total_width + 0.5, start_Y, 4, 20, 'FD')
    with pdf.rotation(90, start_X + total_width + 3.5, start_Y + 15):
        pdf.text(start_X + total_width + 3.5, start_Y + 15, 'Высоко')

    # pdf.text(start_X + total_width - 37, start_Y + total_height + 3, 'Высокая проявленность')

    # pdf.set_text_color(r=135, g=135, b=135)
    #
    # with pdf.rotation(90, start_X + total_width + 3, start_Y + total_height * (3 / 4) + 2):
    #     pdf.text(start_X + total_width + 3, start_Y + total_height * (3 / 4) + 2, '25%')
    # with pdf.rotation(90, start_X + total_width + 3, start_Y + total_height / 2 + 2):
    #     pdf.text(start_X + total_width + 3, start_Y + total_height / 2 + 2, '50%')
    # with pdf.rotation(90, start_X + total_width + 3, start_Y + total_height / 2 / 2 + 2):
    #     pdf.text(start_X + total_width + 3, start_Y + total_height / 2 / 2 + 2, '75%')

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
    pdf.rect((start_X + total_width) / 2 - 20, start_Y + total_height + delta_Y_for_horizontal_arrow - 2, total_width / 3 - 6, 6, 'FD')

    pdf.set_font("RalewayLight", "", 12)
    pdf.text((start_X + total_width) / 2 - 17, start_Y + total_height + delta_Y_for_horizontal_arrow + 2, 'Менеджерские навыки')

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
    pdf.rect(start_X + total_width + delta_Y_for_horizontal_arrow - 2, (start_Y + total_height) / 2 - 2, 6, 30, 'FD')

    pdf.set_font("RalewayLight", "", 12)
    with pdf.rotation(90, start_X + total_width + delta_Y_for_horizontal_arrow + 2, start_Y + total_height / 2 + 10):
        pdf.text(start_X + total_width + delta_Y_for_horizontal_arrow + 2, start_Y + total_height / 2 + 10, 'Потенциал')

    # pdf.text((start_X + total_width) / 2 - 30, start_Y + total_height + delta_Y_for_horizontal_arrow + 2, 'Согласованность ответов участников')

    # описание матрицы
    y = start_Y + total_height + delta_Y_for_horizontal_arrow + 8

    pdf.set_fill_color(r=230, g=230, b=227)
    pdf.set_draw_color(r=230, g=230, b=227)

    pdf.rect(0, y, 4, 60, 'FD')

    pdf.set_text_color(r=0, g=0, b=0)
    pdf.set_font("RalewayLight", "", 10)
    pdf.set_xy(start_X, y)
    text = u'Данная матрица отражает соотношение потенциала к развитию и менеджерских компетенций, определяющие рабочее поведение участников. ' \
           u'Матрица построена на основе двух осей:\n\n' \
           u'• Потенциал к развитию – способность к трансформации мышления и наличие внутренних ресурсов для адаптации к изменениям, ' \
           u'усложнению и преобразованию работы, при сохранении продуктивности и гармоничных отношений со средой.\n' \
           u'• Менеджерские компетенции – это комбинация характеристик руководителя, которые позволяют эффективно управлять командой, ресурсами и процессами внутри организации.\n \n' \
           u'В зеленую зону попадают сотрудники, обладающие высоким потенциалом к развитию и проявляющие развитые менеджерские компетенции. В данном квадрате размещается кадровый резерв и потенциальные преемники на управленческие роли.\n \n' \
           u'В красную зону попадают сотрудники, обладающие низким потенциалом к развитию и проявляющие неразвитые менеджерские компетенции. Данным сотрудникам необходимо уделить дополнительное внимание.'

    pdf.multi_cell(0, 4, text)
    draw_potential_matrix_participants(pdf, total_width, total_height, lang, request_json)


def draw_potential_matrix_participants(pdf, total_width, total_height, lang, request_json):
    project_id = request_json['project_id']
    square_results = request_json['square_results']
    startX = 15
    startY = 25 + 8

    pdf.set_draw_color(r=0, g=0, b=0)

    potential_matrices = PotentialMatrix.objects.filter(project=None)
    if PotentialMatrix.objects.filter(project_id=project_id).exists():
        potential_matrices = PotentialMatrix.objects.filter(project_id=project_id)

    pdf.set_line_width(0.5)
    # pdf.set_draw_color(240)
    pdf.set_font("NotoSansDisplayMedium", "", 10)

    text_y_delta = 5.2
    text_x_delta = 3

    square_x_cnt = {
        '1_1': {
            'circle_coords': [startX + 5, startY],
            'text_coords': [startX + 5 + text_x_delta, startY + text_y_delta],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        '1_2': {
            'circle_coords': [startX + 5 + total_width / 3, startY],
            'text_coords': [startX + 5 + text_x_delta + total_width / 3, startY + text_y_delta],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        '1_3': {
            'circle_coords': [startX + 5 + total_width / 3 * 2, startY],
            'text_coords': [startX + 5 + text_x_delta + total_width / 3 * 2, startY + text_y_delta],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        '2_1': {
            'circle_coords': [startX + 5, startY + total_height / 3],
            'text_coords': [startX + 5 + text_x_delta, startY + text_y_delta + total_height / 3],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        '2_2': {
            'circle_coords': [startX + 5 + total_width / 3, startY + total_height / 3],
            'text_coords': [startX + 5 + text_x_delta + total_width / 3, startY + text_y_delta + total_height / 3],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        '2_3': {
            'circle_coords': [startX + 5 + total_width / 3 * 2, startY + total_height / 3],
            'text_coords': [startX + 5 + text_x_delta + total_width / 3 * 2, startY + text_y_delta + total_height / 3],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        '3_1': {
            'circle_coords': [startX + 5, startY + total_height / 3 * 2],
            'text_coords': [startX + 5 + text_x_delta, startY + text_y_delta + total_height / 3 * 2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        '3_2': {
            'circle_coords': [startX + 5 + total_width / 3, startY + total_height / 3 * 2],
            'text_coords': [startX + 5 + text_x_delta + total_width / 3, startY + text_y_delta + total_height / 3 * 2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},
        '3_3': {
            'circle_coords': [startX + 5 + total_width / 3 * 2, startY + total_height / 3 * 2],
            'text_coords': [startX + 5 + text_x_delta + total_width / 3 * 2, startY + text_y_delta + total_height / 3 * 2],
            'cur_X_pos': 0,
            'cur_Y_pos': 0,
            'cnt': 0},

    }
    cnt = 0

    for square_data in square_results:
        participant_id = square_data[8]
        print('===========================================================================================================')
        print(f'participant_number = {participant_id}')
        report = Report.objects.filter(participant_id=participant_id).latest('added')
        # print()
        for matrix in potential_matrices:

            add_to_squares = True
            print(f'участник - {report.participant.employee.email} матрица - {matrix.code}')
            potential_matrix_groups_max_level = ConditionGroupPotentialMatrix.objects.filter(matrix=matrix).aggregate(Max('level'))['level__max']
            print(f'potential_matrix_groups_max_level = {potential_matrix_groups_max_level}')
            matrix_check_result = True
            all_matrix_groups_check_results = []
            levels_check_result = []
            final_child_groups_check_result = []
            for level in reversed(range(potential_matrix_groups_max_level + 1)):
                print(f'level = {level}')
                if level > 0: #если группа НЕ корневая
                    potential_matrix_groups = ConditionGroupPotentialMatrix.objects.filter(Q(matrix=matrix) &
                                                                                           Q(level=level))
                    parent_group_of_level = ConditionGroupOfGroups.objects.get(group=potential_matrix_groups[0].group).parent_group
                    parent_group_of_level_type = parent_group_of_level.type
                    child_groups_check_result = []

                    for matrix_group in potential_matrix_groups:

                        group_type = matrix_group.group.type

                        matrix_categories = ConditionGroupCategoryPotentialMatrix.objects.filter(group=matrix_group.group)
                        if matrix_categories:
                            categories_check_result = []
                            for matrix_category in matrix_categories:
                                print(f'++++ category check - {matrix_category.category.code}. {matrix_category.category.name}')

                                code = matrix_category.category.code
                                points_from = matrix_category.points_from
                                points_to = matrix_category.points_to
                                t_points_sum = ReportDataByCategories.objects.filter(Q(report=report) &
                                                                                     Q(category_code=code)).aggregate(Sum('t_points'))['t_points__sum']
                                if not t_points_sum:
                                    categories_check_result.append(False)
                                    # add_to_squares = False
                                else:
                                    if not points_from <= t_points_sum <= points_to:
                                        categories_check_result.append(False)
                                    else:
                                        categories_check_result.append(True)
                                        # add_to_squares = False
                            if group_type == 'and':
                                if False in categories_check_result:
                                    child_groups_check_result.append(False)
                                    group_check_result = False
                                else:
                                    child_groups_check_result.append(True)
                                    group_check_result = True
                            else:
                                if True in categories_check_result:
                                    child_groups_check_result.append(True)
                                    group_check_result = True
                                else:
                                    child_groups_check_result.append(False)
                                    group_check_result = False
                            all_matrix_groups_check_results.append({
                                'group_id': matrix_group.id,
                                'result': group_check_result
                            })
                            print('---categories_check_result---')
                            print(categories_check_result)
                            print('------------------------')
                        else: # есть только группы в группе, нет категорий
                            groups_of_group = ConditionGroupOfGroups.objects.filter(Q(parent_group=matrix_group.group))
                            if groups_of_group:
                                group_of_group_type = groups_of_group[0].group.type
                                parent_groups_of_group_results = []
                                for group_of_group in groups_of_group:
                                    for group_result in all_matrix_groups_check_results:
                                        if group_result['group_id'] == group_of_group.group.id:
                                            parent_groups_of_group_results.append(group_result['result'])

                                if group_of_group_type == 'and':
                                    if False in parent_groups_of_group_results:
                                        child_groups_check_result.append(False)
                                    else:
                                        child_groups_check_result.append(True)
                                else:
                                    if True in parent_groups_of_group_results:
                                        child_groups_check_result.append(True)
                                    else:
                                        child_groups_check_result.append(False)
                # else:
                #     final_child_groups_check_result = child_groups_check_result


                    print('---child_groups_check_result---')
                    print(child_groups_check_result)
                    print('------------------------')

                    # if parent_group_of_level_type == 'and':
                    #     if False in child_groups_check_result:
                    #         levels_check_result.append(False)
                    #     else:
                    #         levels_check_result.append(True)
                    # else:
                    #     if True in child_groups_check_result:
                    #         levels_check_result.append(True)
                    #     else:
                    #         levels_check_result.append(False)

            # print('---level_check_result---')
            # print(levels_check_result)
            # print('-------------------')
            root_group = ConditionGroupPotentialMatrix.objects.get(Q(matrix=matrix) &
                                                                   Q(level=0))

            print('---final child_groups_check_result---')
            print(child_groups_check_result)
            print('------------------------')

            print(f'root_group type = {root_group.group.type}')
            if root_group.group.type == 'and':
                if False not in child_groups_check_result:
                    print('...........1 вствить...................')
                    draw_single_circle_potential_matrix_squares(square_data, pdf, square_x_cnt, cnt, matrix.code)
                else:
                    print('...........1 НЕ вствить...................')
            else:
                if True in child_groups_check_result:
                    print('...........2 вствить...................')
                    draw_single_circle_potential_matrix_squares(square_data, pdf, square_x_cnt, cnt, matrix.code)
                else:
                    print('...........2 НЕ вствить...................')

            print('***************all_matrix_groups_check_results*******************')
            print(all_matrix_groups_check_results)
            print('************************************************************')
        print('===========================================================================================================')


def draw_single_circle_potential_matrix_squares(square_data, pdf, square_x_cnt, cnt, matrix_code):
    square_name = matrix_code
    participant_number = square_data[7]
    group_color = square_data[5]
    bold = square_data[3]

    if group_color != 'rgba(0, 0, 0, 0)':
        color_r = int(group_color[group_color.find('(')+len('('):group_color.rfind(')')].split(',')[0])
        color_g = int(group_color[group_color.find('(')+len('('):group_color.rfind(')')].split(',')[1].strip())
        color_b = int(group_color[group_color.find('(')+len('('):group_color.rfind(')')].split(',')[2].strip())
        pdf.set_fill_color(color_r, color_g, color_b)
    else:
        pdf.set_fill_color(255, 255, 255)
    if bold == 1:
        pdf.set_draw_color(r=0, g=0, b=0)
    else:
        pdf.set_line_width(0.1)
        pdf.set_draw_color(r=135, g=135, b=135)
    pdf.circle(square_x_cnt[square_name]['circle_coords'][0] + 9 * square_x_cnt[square_name]['cur_X_pos'], square_x_cnt[square_name]['circle_coords'][1] + 9 * square_x_cnt[square_name]['cur_Y_pos'], 8, style="FD")
    if cnt <= 9:
        pdf.text(square_x_cnt[square_name]['text_coords'][0] + 9 * square_x_cnt[square_name]['cur_X_pos'], square_x_cnt[square_name]['text_coords'][1] + 9 * square_x_cnt[square_name]['cur_Y_pos'], str(participant_number))
    else:
        pdf.text(square_x_cnt[square_name]['text_coords'][0] - 1.1 + 9 * square_x_cnt[square_name]['cur_X_pos'], square_x_cnt[square_name]['text_coords'][1] + 9 * square_x_cnt[square_name]['cur_Y_pos'], str(participant_number))

    cur_X_cnt = square_x_cnt[square_name]['cur_X_pos']
    if cur_X_cnt < 4:
        square_x_cnt[square_name]['cur_X_pos'] = square_x_cnt[square_name]['cur_X_pos'] + 1
    else:
        square_x_cnt[square_name]['cur_X_pos'] = 0
        square_x_cnt[square_name]['cur_Y_pos'] = square_x_cnt[square_name]['cur_Y_pos'] + 1
    square_x_cnt[square_name]['cnt'] = square_x_cnt[square_name]['cnt'] + 1
    pdf.set_line_width(0.5)

