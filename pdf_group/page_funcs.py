from pdf_group.draw import draw_arrow, draw_table
from pdf.models import Report, ReportData

# цвет прямоугольника названия блока
BLOCK_R = 230
BLOCK_G = 230
BLOCK_B = 227


def proceed_scale(pdf, x, y, scale_name, square_results, scale_description, section_name, category_name, description_delta_y, line_delta_y, arrow_color_r, arrow_color_g, arrow_color_b):
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("RalewayRegular", "", 9)
    pdf.set_xy(x, y)
    pdf.multi_cell(0, 4, scale_name)
    scale_data = []
    cnt = 0
    # print(square_results)
    for square_result in square_results:
        cnt = cnt + 1
        report = Report.objects.filter(participant__employee__email=square_result[1]).latest('added')
        if ReportData.objects.filter(report=report, section__name=section_name, category__name=category_name).exists():
            report_data = ReportData.objects.get(report=report, section__name=section_name, category__name=category_name)
            print(f'участик - {report.participant.employee.name} секция - {report_data.section.name} категория - {report_data.category.name} points - {report_data.points}')
            scale_data.append([square_result[2], report_data.points, cnt])
    draw_arrow(pdf, startX=x + 45, startY=y + 4, r=arrow_color_r, g=arrow_color_g, b=arrow_color_b, scale_data=scale_data)
    pdf.set_font("RalewayRegular", "", 7)
    y = y + description_delta_y
    pdf.set_xy(x, y)

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
