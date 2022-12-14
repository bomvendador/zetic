from pdf.draw import insert_page_number
from pdf_group.draw import draw_arrow, draw_table
from pdf_group.page_funcs import proceed_scale, block_name
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B


def page9(pdf, square_results, lang):
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)

    delta_x_between_scales = 28

    x = 8
    y = 5
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)

    start_block_name_y = y

    scale_name = u'''
Эмпатическая усталость
                '''
    scale_discription = '''
Попытки облегчить или
сократить обязанности,
требующие эмоциональных
затрат или эмоционального
вовлечения 
       '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Выгорание Бойко', 'Сопротивление_Эмпатическая усталость', description_delta_y=5, line_delta_y=3.5,
                  arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y + 3, "", end_y_delta=28, end_y_text_delta=45)

    y = y + delta_x_between_scales

    start_block_name_y = y + 3

    scale_name = u'''
Эмоциональная 
опустошенность
            '''
    scale_discription = '''
Избегание эмоционального
ответа на важные ситуации
и коммуникации
        '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Выгорание Бойко', 'Истощение_Эмоциональная опустошенность', description_delta_y=9, line_delta_y=3.5,
                  arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    y = y + delta_x_between_scales

    scale_name = u'''
Эмоциональная 
отстраненность
            '''
    scale_discription = '''
Сокращение эмоционального
отклика на рабочие ситуации,
неготовность активно
общаться с другими 
       '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Выгорание Бойко', 'Истощение_Эмоциональная отстраненность', description_delta_y=9, line_delta_y=3.5,
                  arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    y = y + delta_x_between_scales

    scale_name = u'''
Личностная 
отстраненность
            '''
    scale_discription = '''
Обесценивание рабочих задач,
агрессия на стандартные
рабочие ситуации ("ненавижу",
"не выношу", "не хочу") 
       '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Выгорание Бойко', 'Истощение_Личностная отстраненность', description_delta_y=9, line_delta_y=3.5,
                  arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    y = y + delta_x_between_scales

    scale_name = u'''
Психосоматика
            '''
    scale_discription = '''
Телесные неприятные
состояния, плохое
самочувствие, отсутствие
сил/энергии 
      '''

    proceed_scale(pdf, x + 5, y, scale_name, square_results, scale_discription, 'Выгорание Бойко', 'Истощение_Психосоматика', description_delta_y=9, line_delta_y=3.5,
                  arrow_color_r=255, arrow_color_g=168, arrow_color_b=29)

    block_name(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, start_block_name_y, "ФАЗА 3. ИСТОЩЕНИЕ", end_y_delta=30, end_y_text_delta=50)

    draw_table(square_results, pdf, width=90, x=14, y=230)
    insert_page_number(pdf)
