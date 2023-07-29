from pdf.draw import insert_page_number
from pdf_group.draw import draw_table
from pdf_group.page_funcs import START_Y


def page(pdf, square_results, lang):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    x = 8
    y = START_Y
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    if lang == "ru":
        pdf.cell(0, 0, "Состав участников исследования")
    else:
        pdf.cell(0, 0, "Study participants")
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + 5, x + 220, y + 5)

    y = y + 12

    pdf.set_xy(x, y)

    draw_table(square_results, pdf, width=90, x=14, y=y)
    insert_page_number(pdf)

    pdf.set_line_width(0.1)
