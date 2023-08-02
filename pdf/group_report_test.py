import os
from dataclasses import dataclass
from unittest import TestCase

from pdf.group_report import GroupReport, GroupReportData, SquareResult
from pdf.single_report import SingleReportData
from pdf.translations import TRANSLATIONS_DICT
from pdf.zetic_pdf import ZeticPDF, BLOCK_R, BLOCK_G, BLOCK_B, PDF_MODULE_BASE_DIR


class GroupReportTest(TestCase):
    def test_single_report(self):
        group_report = GroupReport()
        data = GroupReportData(
            lang="ru",
            project_name="Project name",
            square_results=[
                SquareResult(
                    group_name="Group name",
                    group_color="#004422",
                    name="Name",
                    email="@@@",
                    bold=True,
                    idx=1,
                    single_report_data=SingleReportData(
                        participant_name="Participant name",
                    ),
                )
            ],
        )
        bytes = group_report.generate_pdf(data)
        with open(f"test-{group_report.data.lang}-group.pdf", "wb") as f:
            f.write(bytes)

        pass
