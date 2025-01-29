import math

from pdf.draw import insert_page_number
# from pdf_group.draw import draw_table
from pdf_group.potential_matrix.draw import draw_potential_matrix_squares
from pdf_group.page_funcs import proceed_scale, block_name, data_by_points, get_additional_delta_y, block_name_
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y
from pdf.models import Report, ReportData, Questionnaire, QuestionnaireQuestionAnswers, Participant, Category, ReportDataByCategories


def page(pdf, lang, square_results):
    pdf.set_auto_page_break(False)

    x = 12
    y = 12
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    # if lang == 'ru':
    pdf.cell(0, 0, 'Матрица потенциала')
    # else:
    #     pdf.cell(0, 0, 'Section K')
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.1)

    pdf.line(x + 1, y + 5, x + 220, y + 5)

    draw_potential_matrix_squares(pdf, lang, x, square_results)

    insert_page_number(pdf)
