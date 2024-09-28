import datetime

def title_page(pdf, participant, lang):
    pdf.image('media/images/page_img.png', x=0, y=0, w=210)

    pdf.set_font("Cambria", "", 18)

    y = 150
    pdf.set_xy(20, y)
    if lang == 'ru':
        pdf.cell(0, 0, 'Индивидуальный отчетдддд')
    else:
        pdf.cell(0, 0, 'Personal report')
    pdf.line(x1=21, y1=y+6, x2=250, y2=y+6)

    pdf.set_font("Cambria-Bold", "", 12)

    y = y + 16
    pdf.set_xy(20, y)
    if lang == 'ru':
        pdf.cell(0, 0, 'Опросник Zetic 4S', ln=1)
    else:
        pdf.cell(0, 0, 'Zetic 4S Questionnaire', ln=1)

    pdf.set_font("Cambria", "", 12)

    y = y + 8
    pdf.set_xy(20, y)
    if lang == 'ru':
        pdf.cell(20, 0, 'Дата и время создания отчета:', ln=0)
        now = datetime.datetime.now()
        # pdf.write(0, now.strftime("%d.%m.%Y %H:%M:%S"))
        pdf.set_font("Cambria-Bold", "", 12)
        pdf.set_xy(80, y)
        pdf.cell(20, 0, now.strftime("%d.%m.%Y %H:%M:%S"), ln=0)

    else:
        pdf.cell(0, 0, 'Zetic 4S Questionnaire', ln=1)

    y = y + 20
    # pdf.ln(10)
    pdf.set_font("Cambria", "", 12)
    pdf.set_xy(20, y)

    if lang == 'ru':
        pdf.cell(20, 0, 'Участник:', ln=0)
        pdf.set_font("Cambria-Bold", "", 12)
        pdf.write(0, participant)
    else:
        pdf.cell(20, 0, 'Participant:', ln=0)
        pdf.set_font("Cambria-Bold", "", 12)
        pdf.set_xy(42, y)
        pdf.cell(42, 0, participant, ln=0)





