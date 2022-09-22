def title_page(pdf, participant):
    pdf.image('media/images/page_img.png', x=0, y=0, w=210)

    pdf.set_font("RalewayRegular", "", 18)

    pdf.set_xy(20,150)
    pdf.cell(0, 0, 'Индивидуальный отчет')
    # pdf.ln(10)
    pdf.set_xy(20,170)
    pdf.set_font("RalewayLight", "", 12)
    pdf.cell(20, 0, 'Участник:', ln=0)
    pdf.set_font("RalewayRegular", "", 12)
    pdf.write(0, participant)
    pdf.set_xy(20,180)
    pdf.cell(0, 0, 'Опросник Zetic 4S', ln=1)



