from pdf.extract_data import extract_categories
from pdf.draw import draw_scale, insert_page_number
import time


def page3(pdf, json_section):
    t1 = time.perf_counter()
    pdf.set_margins(top=15, left=0, right=5)
    pdf.set_auto_page_break(False)
    pdf.image('media/images/page3.png', x=0, y=0, w=210)

    x = 10
    y = 10
    pdf.set_xy(x, y)
    pdf.set_font("RalewayBold", "", 10)
    pdf.cell(0, 0, 'Базовые черты личности')
    y = y + 5
    # 17
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    text = u'Приведенные ниже результаты исследования отражают фундаментальные черты личности, определяющие стиль ' \
           u'деятельности и взаимоотношения с окружением. Обнаружив эти черты, Вы можете осознанно усиливать или ослаблять их'
    pdf.multi_cell(0, 4, text, align='J')

    y += 10
    x += 3
    scale_name = u'''
    Шкала С
    Эмоциональная
    стабильность
    '''
    points_with_description = extract_categories(json_section, 'Шкала C')
    scale_legend_left = u'''
    Следование эмоциям,
    Утомляемость
    '''
    scale_legend_right = u'''
    Стабильность, Зрелость,
    Работоспособность
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала O
    Тревожность
    '''
    points_with_description = extract_categories(json_section, 'Шкала O')
    scale_legend_left = u'''
    Безмятежность,
    Энергичность
    '''
    scale_legend_right = u'''
    Чувство вины, Тревожность,
    Впечатлительность
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала Q4
    Внутренний комфорт
    '''
    points_with_description = extract_categories(json_section, 'Шкала Q4')
    scale_legend_left = u'''
    Расслабленность,  
    Низкая мотивация
    '''
    scale_legend_right = u'''
    Собранность, Напряженность, 
    Раздражительность
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала F
    Импульсивность
    '''
    points_with_description = extract_categories(json_section, 'Шкала F')
    scale_legend_left = u'''
    Молчаливость, 
    Расчетливость
    '''
    scale_legend_right = u'''
    Беззаботность, Беспечность,
    Экспрессивность
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала N
    Дипломатичность
    '''
    points_with_description = extract_categories(json_section, 'Шкала N')
    scale_legend_left = u'''
    Прямолинейность, 
    Бестактность
    '''
    scale_legend_right = u'''
    Влияние, Хитрость
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала I
    Дипломатичность
    '''
    points_with_description = extract_categories(json_section, 'Шкала I')
    scale_legend_left = u'''
    Рассудительность, Циничность,
    Ответственность
    '''
    scale_legend_right = u'''
    Эмпатичность,
    Интуитивность
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала A
    Открытость
    '''
    points_with_description = extract_categories(json_section, 'Шкала A')
    scale_legend_left = u'''
    Замкнутость, Холодность,
    Безучастность, Строгость
    '''
    scale_legend_right = u'''
    Общительность,
    Открытость
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала M
    Восторженность
    '''
    points_with_description = extract_categories(json_section, 'Шкала M')
    scale_legend_left = u'''
    Практичность, Принципиальность
    Реалистичность, Прозаичность
    '''
    scale_legend_right = u'''
    Восторженность,
    Воображение
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала Q2
    Самостоятельность
    '''
    points_with_description = extract_categories(json_section, 'Шкала Q2')
    scale_legend_left = u'''
    Зависимость от группы,
    Разделение ответственности
    '''
    scale_legend_right = u'''
    Самостоятельность,
    Независимость
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала G
    Ответственность
    '''
    points_with_description = extract_categories(json_section, 'Шкала G')
    scale_legend_left = u'''
    Непостоянство, Ненадежность
    '''
    scale_legend_right = u'''
    Настойчивость,
    Дисциплина, Долг
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала Q3
    Самоконтроль
    '''
    points_with_description = extract_categories(json_section, 'Шкала Q3')
    scale_legend_left = u'''
    Конфликтность,
    Невнимательность
    '''
    scale_legend_right = u'''
    Самоконтроль,
    Сильная воля, Точность
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала Q1
    Критичность
    '''
    points_with_description = extract_categories(json_section, 'Шкала Q1')
    scale_legend_left = u'''
    Консерватизм, 
    Неприятие перемен
    '''
    scale_legend_right = u'''
    Критичность, Анализ информации,
    Оптимизация работы 
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала L
    Осторожность
    '''
    points_with_description = extract_categories(json_section, 'Шкала L')
    scale_legend_left = u'''
    Доверчивость, Терпимость,
    Откровенность
    '''
    scale_legend_right = u'''
    Подозрительность,
    Осторожность
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала H
    Смелость
    '''
    points_with_description = extract_categories(json_section, 'Шкала H')
    scale_legend_left = u'''
    Робость, Деликатность
    '''
    scale_legend_right = u'''
    Смелость, Авантюрность
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    y += 17
    scale_name = u'''
    Шкала E
    Независимость
    '''
    points_with_description = extract_categories(json_section, 'Шкала E')
    scale_legend_left = u'''
    Мягкость, Тактичность, 
    Уступчивость
    '''
    scale_legend_right = u'''
    Напористость, Властность,
    Самоуверенность
    '''
    draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points_with_description['points'], points_with_description['point_description'])

    insert_page_number(pdf)
    t2 = time.perf_counter()
    print(f'стр 3 - {round(t2-t1,2)}')

def draw_scale_page3(pdf, x, y, scale_name, scale_legend_left, scale_legend_right, points, points_description):
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 9)
    pdf.multi_cell(0, 4, scale_name)
    pdf.set_xy(x+110, y+2)
    pdf.cell(10, h=12, txt=str(points), ln=0, align='C')
    pdf.set_font("RalewayLight", "", 8)
    pdf.multi_cell(0, h=4, txt=points_description, align='L')

    y += 10
    x += 35
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(0, 3, scale_legend_left)

    draw_scale(pdf, x+3, y-7, 70, 10, points, 'media/images/kettel_page3.png')

    x += 24
    pdf.set_xy(x, y)
    pdf.set_font("RalewayLight", "", 6)
    pdf.multi_cell(50, 3, scale_legend_right, align='R')
