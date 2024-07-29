from pdf_group.draw import draw_arrow, draw_table
from pdf.models import Report, ReportData, Questionnaire, QuestionnaireQuestionAnswers, Participant, Category, ReportDataByCategories
import math
from pdf import raw_to_t_point
from django.db.models import Q


# цвет прямоугольника названия блока
BLOCK_R = 230
BLOCK_G = 230
BLOCK_B = 227

MIN_SCALE_DELTA_Y = 29
MAX_Y = 280
START_Y = 10


def proceed_scale(pdf, x, y, scale_name, section_data, scale_description, section_code, category_code, description_delta_y, line_delta_y, arrow_color_r, arrow_color_g, arrow_color_b):
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("RalewayRegular", "", 9)
    pdf.set_xy(x, y + 3)
    pdf.multi_cell(0, 4, scale_name)
    draw_arrow(pdf, startX=x + 45, startY=y + 4, r=arrow_color_r, g=arrow_color_g, b=arrow_color_b, data_by_points=section_data)
    pdf.set_font("RalewayRegular", "", 7)
    y = y + description_delta_y
    pdf.set_xy(x, y + 3)

    pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + line_delta_y, x + 39, y + line_delta_y)
    pdf.multi_cell(0, 4, scale_description)


def block_name(pdf, block_r, block_g, block_b, y, start_block_name_y, block_name, end_y_delta, end_y_text_delta):
    pdf.set_fill_color(block_r, block_g, block_b)
    pdf.set_draw_color(block_r, block_g, block_b)
    rect_width = 10
    rect_height = y - start_block_name_y + end_y_delta
    pdf.rect(0, start_block_name_y, rect_width, rect_height, 'FD')
    pdf.set_font("RalewayRegular", "", 9)
    pdf.set_text_color(118, 134, 146)
    with pdf.rotation(90, 6, start_block_name_y + rect_height - end_y_text_delta):
        pdf.text(0, start_block_name_y + rect_height - end_y_text_delta, block_name)


def block_name_(pdf, block_r, block_g, block_b, y, x, block_name_str):
    pdf.set_fill_color(block_r, block_g, block_b)
    pdf.set_draw_color(block_r, block_g, block_b)
    rect_width = 210
    rect_height = 8
    pdf.rect(0, y, rect_width, rect_height, 'FD')
    pdf.set_font("RalewayRegular", "", 9)
    pdf.set_text_color(118, 134, 146)
    # with pdf.rotation(90, 6, start_block_name_y + rect_height - end_y_text_delta):
    pdf.text(x + 1, y + 5, block_name_str)


def data_by_points(square_results, section_code, category_code):
    scale_data = []
    cnt = 0
    # print(f'square_result - {square_results}')
    for square_result in square_results:
        group_color = square_result[5]
        email = square_result[1]
        bold = square_result[3]
        cnt = cnt + 1
        report = Report.objects.filter(participant__employee__email=email).latest('added')
        # print(f'report_id = {report.id}')

        # participant_email = square_result[1]
        # questionnaire_inst = Questionnaire.objects.filter(participant__employee__email=participant_email).latest('created_at')
        # print(f'questionnaire_inst len = {questionnaire_inst.id}')

        # questionnaire_questions_answers = QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire_inst,
        #                                                                               question__category__code=category_code)
        # participant_inst = Participant.objects.get(id=questionnaire_inst.participant.id)
        # print(f'category code = {category_code}')
        # category_inst = Category.objects.get(code=category_code)

        # raw_points = 0
        # for answer in questionnaire_questions_answers:
        #     if answer.question.category.code == category_code:
        #         raw_points = raw_points + answer.answer.raw_point
        #         # print(f'raw_points = {raw_points}')
        # t_points = raw_to_t_point.filter_raw_points_to_t_points(raw_points, participant_inst.employee_id, category_inst.id)

        # print(f'участник - {report.participant.employee.name}')
        # print(f'category_code - {category_code}')
        report_data_by_categories = ReportDataByCategories.objects.filter(Q(report=report) & Q(category_code=category_code))
        if report_data_by_categories.exists():
            t_points = ReportDataByCategories.objects.get(Q(report=report) & Q(category_code=category_code)).t_points
            # print(f't_points 87 = {t_points}')
            scale_data.append([square_result[2], t_points, cnt, group_color, email, bold])


        # if ReportData.objects.filter(report=report, section_code=section_code, category_code=category_code).exists():
        #     report_data = ReportData.objects.get(report=report, section_code=section_code, category_code=category_code)
        #     # print(f'участик - {report.participant.employee.name} секция - {report_data.section_name} категория - {report_data.category_name} points - {report_data.points}')
        #     scale_data.append([square_result[2], report_data.points, cnt, group_color, email, bold])
    # print(f'scale data - {scale_data}')

    data_by_points_ = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
    }

    for data in scale_data:
        # if data[1] != 0:
        data_by_points_[data[1]].append(data)
    # print(f'data_by_points - {data_by_points_}')
    return data_by_points_


def get_additional_delta_y(section_data):
    max_rows_number = 0
    additional_delta_y = 0
    for k, v in section_data.items():
        cur_scale_rows_qnt = math.ceil(len(v)/4)
        if cur_scale_rows_qnt > max_rows_number:
            max_rows_number = cur_scale_rows_qnt
    if max_rows_number > 5:
        additional_delta_y = (max_rows_number - 5) * 3.5
    return additional_delta_y

