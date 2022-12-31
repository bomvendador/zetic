from pdf_group.draw import draw_arrow,draw_squares, draw_table
from pdf.draw import insert_page_number


def page2(pdf, square_results, table_y):
    pdf.set_auto_page_break(False)

    x = 20
    y = 12
    pdf.set_xy(x,y)
    pdf.set_font("RalewayBold", "", 10)

    # if lang == 'ru':
    pdf.cell(0, 0, 'Командный профиль: распределение ролей по модели PAEI И. Адизеса и Майерс-Бриггс (MBTI)')
    # else:
    #     pdf.cell(0, 0, 'Section C')

    # draw_arrow(pdf, startX=40, startY=20, rgb1=34, rgb2=170, rgb3=245)
    draw_squares(pdf, square_results)
    # draw_table(square_results, pdf, width=90, x=15, y=table_y)

    insert_page_number(pdf)