from pdf.draw import insert_page_number
from pdf.models import Questionnaire, QuestionnaireQuestionAnswers, QuestionAnswers, Employee, RawToTPointsType, \
    Category, IndividualReportPointsDescriptionFilter, IndividualReportPointsDescriptionFilterCategory, Report, \
    ReportDataByCategories, IndividualReportPointsDescriptionFilterText
from . import raw_to_t_point
from django.db.models import Q

from pdf_group.page_funcs import block_name_
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y


def page(pdf, questionnaire_id, lang, report_id):
    pdf.set_auto_page_break(False)

    x = 12
    y = 12
    pdf.set_xy(x,y)
    # pdf.set_font("RalewayBold", "", 10)
    pdf.set_font("Cambria-Bold", "", 11)
    if lang == 'ru':
        pdf.cell(0, 0, 'Краткие выводы')
    else:
        pdf.cell(0, 0, 'Short conclusions')

    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + 5, x + 220, y + 5)

    # 17
    # pdf.set_font("RalewayLight", "", 9)
    pdf.set_font("Cambria", "", 10)

    conclusions_arr = []
    questionnaire_inst = Questionnaire.objects.get(id=questionnaire_id)
    participant_inst = questionnaire_inst.participant
    # report_data_by_categories = ReportDataByCategories.objects.filter(report=report)

    # categories_inst = Category.objects.all()

    # questionnaire_question_answers = QuestionnaireQuestionAnswers.objects.filter(questionnaire=questionnaire_inst)

    individual_report_points_description_filter_inst = IndividualReportPointsDescriptionFilter.objects.all()

    report_exists = False
    if not report_id == '':
        report = Report.objects.filter(participant=participant_inst).latest('added')
        report_exists = True

    for description_filter in individual_report_points_description_filter_inst:
        filter_categories = IndividualReportPointsDescriptionFilterCategory.objects.filter(filter=description_filter)
        filter_categories_qnt = len(filter_categories)
        questionnaire_categories_fits_filter_qnt = 0
        for filter_category in filter_categories:
            if report_exists:
                # print(f'report_id = {report_id} report id = {report.id} filter_category.category.code = {filter_category.category.code}')
                if ReportDataByCategories.objects.filter(Q(report=report) & Q(category_code=filter_category.category.code)).exists():
                    print(f'report_exists - {report_exists}')
                    t_points = ReportDataByCategories.objects.filter(Q(report=report) & Q(category_code=filter_category.category.code)).latest('created_at').t_points
            else:
                questionnaire_question_answers = QuestionnaireQuestionAnswers.objects.filter(
                    Q(questionnaire=questionnaire_inst) & Q(question__category=filter_category.category))

                if len(questionnaire_question_answers) > 0:
                    raw_points = 0
                    for answer in questionnaire_question_answers:
                        raw_points = raw_points + answer.answer.raw_point
                    t_points = raw_to_t_point.filter_raw_points_to_t_points(raw_points, questionnaire_inst.participant.employee_id, filter_category.category.id)
            # print(f't_point = {t_points}')
            if filter_category.points_from <= t_points <= filter_category.points_to:
                questionnaire_categories_fits_filter_qnt = questionnaire_categories_fits_filter_qnt + 1
        if filter_categories_qnt == questionnaire_categories_fits_filter_qnt:
            filter_texts = IndividualReportPointsDescriptionFilterText.objects.filter(filter=description_filter)
            texts = []
            for text in filter_texts:
                texts.append(text.text)
            conclusions_arr.append({
                'title': description_filter.name,
                'texts': texts,
            })
    cnt = 0
    for conclusion in conclusions_arr:
        cnt = cnt + 1
        if cnt == 1:
            y = y + 10
        # else:
        #     y = y + 2
        x = 12
        pdf.set_xy(x, y)

        block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, conclusion['title'].upper())
        pdf.set_text_color(0, 0, 0)

        y = y + 10
        x = 17
        pdf.set_xy(x, y)

        for conclusion_text in conclusion['texts']:
            pdf.set_xy(x - 5, y)
            pdf.set_font("Cambria", "", 20)
            pdf.multi_cell(0, 4, '·')

            pdf.set_font("Cambria", "", 10)
            pdf.set_xy(x, y)
            pdf.multi_cell(0, 4, conclusion_text)
            y = pdf.get_y()
            y = y + 2
            pdf.set_xy(x, y)

    insert_page_number(pdf)

