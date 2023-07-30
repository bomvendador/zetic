import json
import os
from typing import Dict, List

from django.test import TestCase

from pdf.report_sections_configuration import (
    CATTELL_CATEGORIES,
    COPING_CATEGORIES_V1,
    BOYKO_CATEGORIES_V1,
    VALUES_CATEGORIES_V1,
)
from pdf.single_report import (
    SingleReport,
    SingleReportData,
    SectionData,
    PDF_MODULE_BASE_DIR,
)
from pdf.single_report import IncomingSingleReportData

cattel_example = SectionData(
    {
        "1_1": 1,
        "1_2": 2,
        "1_3": 3,
        "1_4": 4,
        "1_5": 5,
        "1_6": 6,
        "1_7": 7,
        "1_8": 8,
        "1_9": 9,
        "1_10": 10,
        "1_11": 1,
        "1_12": 2,
        "1_13": 3,
        "1_14": 4,
        "1_15": 5,
    }
)
coping_example = SectionData(
    {
        "2_1": 1,
        "2_2": 2,
        "2_3": 3,
        "2_4": 4,
        "2_5": 5,
        "2_6": 6,
        "2_7": 7,
        "2_8": 8,
        "2_9": 9,
        "2_10": 10,
        "2_11": 1,
        "2_12": 2,
        "2_13": 3,
        "2_14": 4,
        "2_15": 5,
        "2_16": 6,
        "2_17": 7,
        "2_18": 8,
        "2_19": 9,
        "2_20": 10,
    }
)

boyko_example = SectionData(
    {
        "3_1": 1,
        "3_2": 2,
        "3_3": 3,
        "3_4": 4,
        "3_5": 5,
        "3_6": 6,
        "3_7": 7,
        "3_8": 8,
        "3_9": 9,
        "3_10": 10,
        "3_11": 1,
        "3_12": 2,
        "3_13": 3,
        "3_14": 4,
        "3_15": 5,
        "3_16": 6,
        "3_17": 7,
        "3_18": 8,
    }
)

values_example = SectionData(
    {
        "4_1": 1,
        "4_2": 2,
        "4_3": 3,
        "4_4": 4,
        "4_5": 5,
        "4_6": 6,
        "4_7": 7,
        "4_8": 8,
        "4_9": 9,
        "4_10": 10,
    }
)


class SingleReportWithDummyData(SingleReport):
    def _get_scale_points_description(self, scale: str, points: int) -> str:
        return f"{scale} {points}"

    def _get_section_scales(self, section: str) -> Dict[str, List[str]]:
        match section:
            case "1":
                return CATTELL_CATEGORIES
            case "2":
                return COPING_CATEGORIES_V1
            case "3":
                return BOYKO_CATEGORIES_V1
            case "4":
                return VALUES_CATEGORIES_V1
            case _:
                raise Exception(f"Unknown section {section}")
        pass


class SingleReportTest(TestCase):
    def test_single_report(self):
        single_report = SingleReportWithDummyData()
        single_report.generate_pdf(
            SingleReportData(
                participant_name="Pablo",
                lang="en",
                cattell_data=cattel_example,
                coping_data=coping_example,
                boyko_data=boyko_example,
                values_data=values_example,
            ),
            path="test",
        )
        single_report = SingleReportWithDummyData()
        single_report.generate_pdf(
            SingleReportData(
                participant_name="Павел",
                lang="ru",
                cattell_data=cattel_example,
                coping_data=coping_example,
                boyko_data=boyko_example,
                values_data=values_example,
            ),
            path="test",
        )

    def test_incoming_report_data(self):
        path_to_json = os.path.join(os.path.dirname(PDF_MODULE_BASE_DIR), "report.json")
        with open(path_to_json, "r") as f:
            parsed_data = json.load(f)

        incoming_data = IncomingSingleReportData.from_dict(parsed_data)
        assert incoming_data.participant_info.name == "Попов Артем Юрьевич "

    def test_real_data(self):
        path_to_json = os.path.join(
            os.path.dirname(PDF_MODULE_BASE_DIR), "report-velle.json"
        )
        with open(path_to_json, "r") as f:
            parsed_data = json.load(f)

        incoming_data = IncomingSingleReportData.from_dict(parsed_data)
        report_data = incoming_data.to_single_report_data()
        single_report = SingleReportWithDummyData()
        single_report.generate_pdf(
            report_data,
            path="test-real-data-velle",
        )
        report_data.lang = "en"
        single_report = SingleReportWithDummyData()
        single_report.generate_pdf(
            report_data,
            path="test-real-data-velle",
        )
