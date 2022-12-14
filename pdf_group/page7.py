from pdf.draw import insert_page_number
from pdf_group.draw import draw_arrow, draw_table
from pdf_group.page_funcs import proceed_scale, block_name
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B


def page7(pdf, square_results, lang):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    x = 8
    y = 5
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    # pdf.line(x + 1, y + 5, x + 220, y + 5)

    # y = y + 10

    start_block_name_y = y

    scale_name = u'''
Агрессия
                '''
    scale_discription = '''
Пребывание в состоянии
сопротивления, нарушения
личного эмоционального баланса
и устойчивости, ярость/агрессия
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Копинги', 'Агрессия',
                  description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=107, arrow_color_g=196, arrow_color_b=38)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y + 3, "", end_y_delta=25, end_y_text_delta=45)

    draw_table(square_results, pdf, width=90, x=14, y=230)
    insert_page_number(pdf)
