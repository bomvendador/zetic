from pdf.draw import insert_page_number

from pdf.models import ConsultantForm, ConsultantFormResources, ConsultantFormResourcesComments, \
    ConsultantFormGrowthZone, ConsultantFormGrowthZoneComments
from django.db.models import Q

from pdf_group.page_funcs import block_name_
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B, MIN_SCALE_DELTA_Y, MAX_Y, START_Y


def page(pdf, lang, consultant_form_id):
    pdf.set_auto_page_break(False)

    x = 12
    y = 12
    pdf.set_xy(x,y)
    # pdf.set_font("RalewayBold", "", 10)
    pdf.set_font("Cambria-Bold", "", 11)
    if lang == 'ru':
        pdf.cell(0, 0, 'Выводы эксперта')
    else:
        pdf.cell(0, 0, 'Expert conclusions')

    pdf.set_draw_color(0, 0, 0)
    pdf.line(x + 1, y + 5, x + 220, y + 5)

    consultant_form = ConsultantForm.objects.get(id=consultant_form_id)
    # карьерный трек
    if consultant_form.career_track != '':
        y = y + 10
        pdf.set_xy(x, y)
        block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, str('Карьерный трек').upper())
        pdf.set_text_color(0, 0, 0)

    y = y + 10
    pdf.set_xy(x, y)
    pdf.set_font("Cambria", "", 10)
    pdf.multi_cell(0, 4, consultant_form.career_track)

    # ресурсы
    y = pdf.get_y()
    consultant_form_resources = ConsultantFormResources.objects.filter(consultant_form=consultant_form)
    if consultant_form_resources.exists():
        resource_cnt = 0
        y = y + 5
        block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, str('Ресурсы').upper())
        pdf.set_text_color(0, 0, 0)

        y = y + 10
        for consultant_form_resource in consultant_form_resources:
            resource_cnt = resource_cnt + 1
            resource_name = consultant_form_resource.name
            pdf.set_font("Cambria-Bold", "", 11)
            pdf.set_xy(x, y)
            pdf.multi_cell(0, 4, str(resource_cnt) + '. ')
            pdf.set_xy(x + 5, y)
            pdf.multi_cell(0, 4, str(resource_name))
            consultant_form_resource_comments = ConsultantFormResourcesComments.objects.filter(consultant_form_resource=consultant_form_resource)
            y = y + 5
            for consultant_form_resource_comment in consultant_form_resource_comments:
                # y = y + 5
                pdf.set_xy(x + 5, y)
                pdf.set_font("Cambria", "", 20)
                pdf.multi_cell(0, 4, '·')

                pdf.set_font("Cambria", "", 10)
                pdf.set_xy(x + 10, y)
                pdf.multi_cell(0, 4, consultant_form_resource_comment.text)
                y = pdf.get_y() + 2
            y = pdf.get_y() + 2
    # ресурсы

    y = pdf.get_y()
    consultant_form_growth_zones = ConsultantFormGrowthZone.objects.filter(consultant_form=consultant_form)
    if consultant_form_growth_zones.exists():
        growth_zone_cnt = 0
        y = y + 5
        block_name_(pdf, BLOCK_R, BLOCK_G, BLOCK_B, y, x, str('Зоны роста').upper())
        pdf.set_text_color(0, 0, 0)

        y = y + 10
        for consultant_form_growth_zone in consultant_form_growth_zones:
            growth_zone_cnt = growth_zone_cnt + 1
            growth_zone_name = consultant_form_growth_zone.name
            pdf.set_font("Cambria-Bold", "", 11)
            pdf.set_xy(x, y)
            pdf.multi_cell(0, 4, str(growth_zone_cnt) + '. ')
            pdf.set_xy(x + 5, y)
            pdf.multi_cell(0, 4, str(growth_zone_name))
            consultant_form_growth_zone_comments = ConsultantFormGrowthZoneComments.objects.filter(consultant_form_growth_zone=consultant_form_growth_zone)
            y = y + 5
            for consultant_form_growth_zone_comment in consultant_form_growth_zone_comments:
                # y = y + 5
                pdf.set_xy(x + 5, y)
                pdf.set_font("Cambria", "", 20)
                pdf.multi_cell(0, 4, '·')

                pdf.set_font("Cambria", "", 10)
                pdf.set_xy(x + 10, y)
                pdf.multi_cell(0, 4, consultant_form_growth_zone_comment.text)
                y = pdf.get_y() + 2
            y = pdf.get_y() + 2
        insert_page_number(pdf)

