def title_page(pdf, participant, lang):
    pdf.image("media/images/page_img.png", x=0, y=0, w=210)

    pdf.set_font("RalewayRegular", "", 18)

    pdf.set_xy(20, 150)
    if lang == "ru":
        pdf.cell(0, 0, "Индивидуальный отчет")
    else:
        pdf.cell(0, 0, "Personal report")

    # pdf.ln(10)
    pdf.set_font("RalewayLight", "", 12)
    pdf.set_xy(20, 170)

    if lang == "ru":
        pdf.cell(20, 0, "Участник:", ln=0)
        pdf.set_font("RalewayRegular", "", 12)
        pdf.write(0, participant)
    else:
        pdf.cell(20, 0, "Participant:", ln=0)
        pdf.set_font("RalewayRegular", "", 12)
        pdf.set_xy(42, 170)
        pdf.cell(42, 0, participant, ln=0)

    pdf.set_xy(20, 180)
    if lang == "ru":
        pdf.cell(0, 0, "Опросник Zetic 4S", ln=1)
    else:
        pdf.cell(0, 0, "Zetic 4S Questionnaire", ln=1)
