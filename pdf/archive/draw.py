from .extract_data import extract_categories
from pdf_group.page_funcs import BLOCK_R, BLOCK_G, BLOCK_B


def draw_scale(pdf, x, y, w, h, points, img_link):
    # pdf.set_draw_color(color)
    pdf.set_line_width(0.3)
    pdf.set_fill_color(230, 230, 230)

    pdf.rect(x, y, w, h, "F")
    # print(f"point - {points}")
    for i in range(points):
        # pdf.rect(x+1, y+1, 5.9, h-2, 'F', round_corners=True, corner_radius=0.5)
        pdf.image(img_link, x=x + 1, y=y + 1, w=5.9)

        x += 5.9 + 1


def draw_full_scale(
    pdf,
    scale_name,
    x,
    y,
    scale_name_y,
    json_section,
    section_name,
    scale_element_file,
    lang,
    participant_info,
):
    points_with_description = extract_categories(
        json_section, section_name, lang, participant_info
    )
    pdf.set_xy(x, scale_name_y - 2)
    pdf.set_font("RalewayLight", "", 9)
    pdf.multi_cell(0, 4, scale_name)
    pdf.set_xy(x + 110, y - 6)
    pdf.cell(10, h=12, txt=str(points_with_description["points"]), ln=0, align="C")
    pdf.set_font("RalewayLight", "", 8)
    pdf.multi_cell(0, h=4, txt=points_with_description["point_description"], align="L")

    draw_scale(
        pdf,
        x + 40,
        y - 5,
        70,
        10,
        points_with_description["points"],
        scale_element_file,
    )


def insert_page_number(pdf):
    pdf.set_fill_color(BLOCK_R, BLOCK_G, BLOCK_B)
    pdf.set_draw_color(BLOCK_R, BLOCK_G, BLOCK_B)
    rect_width = 20
    rect_height = 6
    pdf.set_xy(200, 290)

    pdf.rect(197, 287, rect_width, rect_height, "FD")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("RalewayLight", "", 10)
    pdf.set_xy(200, 290)
    pdf.cell(0, 0, txt=str(pdf.page_no()))