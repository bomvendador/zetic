import os
from dataclasses import dataclass
from typing import Dict
from unittest import TestCase

from pdf.group_report import (
    GroupReport,
    GroupReportData,
    SquareResult,
    GroupData,
    ParticipantData,
)
from pdf.single_report import SingleReportData
from pdf.translations import TRANSLATIONS_DICT
from pdf.zetic_pdf import ZeticPDF, BLOCK_R, BLOCK_G, BLOCK_B, PDF_MODULE_BASE_DIR


class GroupReportTest(TestCase):
    def test_single_report(self):
        group_report = GroupReport()

        groups: Dict[str, GroupData] = {
            "test": GroupData(
                id=1,
                name="test",
                color="#004422",
            )
        }
        participants: Dict[str, ParticipantData] = {
            "@@@": ParticipantData(
                id=1,
                name="Participant name",
                email="@@@",
            )
        }

        data = GroupReportData(
            lang="ru",
            project_name="Project name",
            group_data=groups,
            participant_data=participants,
            square_results=[
                SquareResult.from_client_list(
                    ["@@@", "@@@", "@@@", "@@@", "test"],
                    groups,
                    participants,
                    SingleReportData(),
                )
            ],
        )
        bytes = group_report.generate_pdf(data)
        with open(f"test-{group_report.data.lang}-group.pdf", "wb") as f:
            f.write(bytes)

        pass
