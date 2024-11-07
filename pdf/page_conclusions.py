from pdf.draw import insert_page_number
from pdf.models import Questionnaire, QuestionnaireQuestionAnswers, QuestionAnswers, Employee, RawToTPointsType, \
    Category, IndividualReportPointsDescriptionFilter, IndividualReportPointsDescriptionFilterCategory, Report, \
    ReportDataByCategories, IndividualReportPointsDescriptionFilterText, IndividualReportPointsDescriptionFilterTextRecommendations
from . import raw_to_t_point
from django.db.models import Q

from pdf_group.page_funcs import block_name_
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y

from celery.utils.log import get_task_logger
import logging

logger = get_task_logger(__name__)

logger2 = logging.getLogger(__name__)


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
            t_points_exists = False
            if report_exists:
                # print(f'report_id = {report_id} report id = {report.id} filter_category.category.code = {filter_category.category.code}')
                if ReportDataByCategories.objects.filter(Q(report=report) & Q(category_code=filter_category.category.code)).exists():
                    # print(f'report_exists - {report_exists}')
                    t_points = ReportDataByCategories.objects.filter(Q(report=report) & Q(category_code=filter_category.category.code)).latest('created_at').t_points
                    t_points_exists = True
            else:
                # print(f'report_exists - {report_exists}')
                questionnaire_question_answers = QuestionnaireQuestionAnswers.objects.filter(
                    Q(questionnaire=questionnaire_inst) & Q(question__category=filter_category.category))
                # print(f'questionnaire_id = {questionnaire_inst.id}')
                # print(f'participant = {questionnaire_inst.participant.employee.name}')
                # print(f'filter_category = {filter_category.category.code}. {filter_category.category.name}')
                # print(f'questionnaire_question_answers = {len(questionnaire_question_answers)}')

                if questionnaire_question_answers.exists():
                    raw_points = 0
                    for answer in questionnaire_question_answers:
                        raw_points = raw_points + answer.answer.raw_point
                    t_points = raw_to_t_point.filter_raw_points_to_t_points(raw_points, questionnaire_inst.participant.employee_id, filter_category.category.id)
                    t_points_exists = True
            # print(f't_point = {t_points}')
            if t_points_exists:
                if filter_category.points_from <= t_points <= filter_category.points_to:
                    questionnaire_categories_fits_filter_qnt = questionnaire_categories_fits_filter_qnt + 1
        if filter_categories_qnt == questionnaire_categories_fits_filter_qnt and not filter_categories_qnt == 0:
            filter_texts = IndividualReportPointsDescriptionFilterText.objects.filter(filter=description_filter)
            texts = []
            for text in filter_texts:
                recommendations = []
                recommendations_inst = IndividualReportPointsDescriptionFilterTextRecommendations.objects.filter(filter_text=text)
                for recommendation in recommendations_inst:
                    recommendations.append(recommendation.text)
                texts.append({
                    'text': text.text,
                    'recommendations': recommendations,
                })
            conclusions_arr.append({
                'title': description_filter.name,
                'texts': texts,
            })
    cnt = 0
    # print('---conclusions_arr---')
    # print(conclusions_arr)
    # logger.info(conclusions_arr)
    # print('-------------------')
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
        pdf.set_draw_color(192, 192, 195)

        for conclusion_text in conclusion['texts']:
            pdf.set_xy(x - 5, y)
            pdf.set_font("Cambria", "", 20)
            pdf.multi_cell(0, 4, '·')

            pdf.set_font("Cambria", "", 10)
            pdf.set_xy(x, y)
            pdf.multi_cell(0, 4, conclusion_text['text'])
            y = pdf.get_y()
            print('======================')
            print(conclusion_text['text'])
            print(f'y = {y}')
            print('=======================')
            logger.info(f'y = {y}')
            logger2.info(f'y = {y}')
            if y > MAX_Y and conclusion_text['recommendations']:
                insert_page_number(pdf)
                pdf.add_page()
                y = 12
            if conclusion_text['recommendations']:
                start_y_recommendation_block = y + 2
                # отрисовка шапки Рекомендаций
                y = draw_recommendations_table_header(pdf, x, y, start_y_recommendation_block)
                # -------------------------------
                y = y + 2
                pdf.set_font("Cambria", "", 10)
                cnt = 0
                for recommendation_text in conclusion_text['recommendations']:
                    if y > MAX_Y:
                        pdf.rect(x - 7, start_y_recommendation_block, x + 176, y - start_y_recommendation_block, 'D')
                        insert_page_number(pdf)
                        pdf.add_page()
                        y = 14
                        start_y_recommendation_block = 12
                        pdf.set_font("Cambria", "", 10)
                        pdf.set_draw_color(192, 192, 195)

                    cnt = cnt + 1
                    pdf.set_xy(x - 5, y)
                    # pdf.set_font("Cambria", "", 20)
                    pdf.multi_cell(0, 4, str(cnt) + '.')

                    pdf.set_font("Cambria", "", 10)
                    pdf.set_xy(x, y)
                    pdf.multi_cell(0, 4, recommendation_text)
                    y = pdf.get_y()
                    y = y + 2
                    pdf.set_xy(x, y)
                pdf.rect(x - 7, start_y_recommendation_block, x + 176, y - start_y_recommendation_block, 'D')
                print('====recommendations=======')
                print(f'y = {y}')
                print('=======================')
                logger.info(f'rec y = {y}')
            y = y + 4
            pdf.set_xy(x, y)

    insert_page_number(pdf)


def draw_recommendations_table_header(pdf, x, y, start_y_recommendation_block):
    y = y + 4
    pdf.set_xy(x, y)
    pdf.set_font("Cambria-Bold", "", 10)
    pdf.multi_cell(0, 4, 'Рекомендации')
    y = pdf.get_y()
    y = y + 2
    pdf.rect(x - 7, start_y_recommendation_block, x + 176, y - start_y_recommendation_block, 'D')
    return y
