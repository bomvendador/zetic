import datetime

def title_page(pdf, client_name, lang):
    pdf.image('media/images/page_img.png', x=0, y=0, w=210)

    pdf.set_font("RalewayRegular", "", 18)

    y = 150

    pdf.set_xy(20, y)
    if lang == 'ru':
        pdf.cell(0, 0, 'Командный отчет')
    else:
        pdf.cell(0, 0, 'Team report')
    pdf.line(x1=21, y1=y+6, x2=250, y2=y+6)

    pdf.set_font("RalewayLight", "", 12)

    y = y + 16
    pdf.set_xy(20, y)

    if lang == 'ru':
        pdf.cell(20, 0, 'Дата и время создания отчета:', ln=0)
        now = datetime.datetime.now()
        # pdf.write(0, now.strftime("%d.%m.%Y %H:%M:%S"))
        pdf.set_xy(83, y)
        pdf.set_font("RalewayRegular", "", 12)

        pdf.cell(20, 0, now.strftime("%d.%m.%Y %H:%M:%S"), ln=0)
    else:
        pdf.cell(20, 0, 'Project:', ln=0)
        pdf.set_font("RalewayRegular", "", 12)
        pdf.set_xy(42, y)
        pdf.cell(42, 0, client_name, ln=0)

    y = y + 10
    pdf.set_xy(20, y)

    pdf.set_font("RalewayLight", "", 12)

    if lang == 'ru':
        pdf.cell(20, 0, 'Проект:', ln=0)
        pdf.set_font("RalewayRegular", "", 12)
        pdf.set_xy(37, y)
        pdf.cell(42, 0, client_name, ln=0)
    else:
        pdf.cell(20, 0, 'Project:', ln=0)
        pdf.set_font("RalewayRegular", "", 12)
        pdf.set_xy(42, y)
        pdf.cell(42, 0, client_name, ln=0)

    y = y + 7

    pdf.set_xy(20, y)
    if lang == 'ru':
        pdf.cell(0, 0, 'Опросник Zetic 4S', ln=1)
    else:
        pdf.cell(0, 0, 'Zetic 4S Questionnaire', ln=1)




