import math
import os
import random
from dataclasses import dataclass
from typing import Dict
from unittest import TestCase

from PIL import ImageColor

from pdf.group_report import (
    GroupReport,
    GroupReportData,
    SquareResult,
    GroupData,
    ParticipantData,
)
from pdf.single_report import SingleReportData


def rgb_to_hex(r: int, g: int, b: int):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


class GroupReportDataGenerator:
    def __init__(self, color_step: float = 25.5):
        self.color_max = math.ceil(255 / color_step)
        self.color_step = 255 / math.ceil(255 / color_step)
        pass

    def generate_group_report_data(
        self,
        project_name: str = "Project Name",
        lang: str = "ru",
        group_count: int = 5,
        participant_count: int = 25,
    ) -> GroupReportData:
        group_data = {}
        participant_data = {}
        square_results = []
        for i in range(group_count):
            group_name = f"Group {i}"
            group_data[group_name] = self.generate_group_data(group_name, i)

        for i in range(participant_count):
            participant_name = f"Participant {i}"
            participant_email = f"participan-{i}@group.pdf"
            group_id = random.randint(0, group_count - 1)
            participant_id = i + group_id * participant_count
            participant_data[participant_email] = self.generate_participant_data(
                participant_id, participant_name, participant_email, group_id
            )

        return GroupReportData(
            lang=lang,
            project_name=f"{project_name} {lang} - {group_count} groups, {participant_count} participants",
            group_data=group_data,
            participant_data=participant_data,
            square_results=square_results,
        )
        pass

    def generate_participant_data(
        self,
        participant_id: int,
        participant_name: str,
        participant_email: str,
        group_id: int,
    ) -> ParticipantData:
        return ParticipantData(
            id=participant_id,
            name=participant_name,
            email=participant_email,
            group_id=group_id,
            burnout=int(random.randint(0, 100) < 30),
        )
        pass

    def generate_group_data(self, group_name: str, group_id: int):
        r = int(random.randint(0, self.color_max) * self.color_step)
        g = int(random.randint(0, self.color_max) * self.color_step)
        b = int(random.randint(0, self.color_max) * self.color_step)

        return GroupData(
            id=group_id,
            name=group_name,
            color=rgb_to_hex(r, g, b),
        )


class GroupReportTest(TestCase):
    def test_single_report(self):
        group_report = GroupReport()
        group_report_data_generator = GroupReportDataGenerator(color_step=50)

        data = group_report_data_generator.generate_group_report_data(
            "Project Name",
            "ru",
            9,
            200,
        )

        bytes = group_report.generate_pdf(data)
        with open(f"test-{group_report.data.lang}-group.pdf", "wb") as f:
            f.write(bytes)

        pass
