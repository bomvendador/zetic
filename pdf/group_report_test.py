import math
import os
import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Tuple, List
from unittest import TestCase

from PIL import ImageColor

from pdf.group_report import (
    GroupReport,
    GroupReportData,
    GroupData,
    ParticipantData,
)
from pdf.single_report import SingleReportData, SectionData
from pdf.zetic_group_pdf import SquareId


def rgb_to_hex(r: int, g: int, b: int):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


class GroupReportDataGenerator:
    def __init__(self, color_step: float = 25.5):
        self.color_max = math.ceil(255 / color_step)
        self.color_step = 255 / math.ceil(255 / color_step)
        pass

    def generate_section_data(
        self, start: int, end: int, section_format: str
    ) -> SectionData:
        section_data: Dict[str, int] = {}
        for i in range(start, end):
            section_data[section_format.format(i)] = random.randint(0, 10)

        return SectionData(section_data)
        pass

    def generate_group_report_data(
        self,
        project_name: str = "Project Name",
        lang: str = "ru",
        group_count: int = 5,
        participant_per_group: int = 20,
    ) -> GroupReportData:
        group_data = {}
        participant_data = {}
        cattell_data: Dict[str, SectionData] = {}
        coping_data: Dict[str, SectionData] = {}
        boyko_data: Dict[str, SectionData] = {}
        values_data: Dict[str, SectionData] = {}

        max_participant_count = group_count * participant_per_group

        for i in range(group_count):
            group_name = f"Group {i}"
            group_data[group_name] = self.generate_group_data(group_name, i)

        for i in range(max_participant_count):
            participant_name = f"Participant {i}"
            participant_email = f"participan-{i}@group.pdf"
            group_id = i % group_count
            participant_id = i
            participant_data[participant_email] = self.generate_participant_data(
                participant_id, participant_name, participant_email, group_id
            )
            cattell_data[participant_email] = self.generate_section_data(1, 15, "1_{}")
            coping_data[participant_email] = self.generate_section_data(1, 20, "2_{}")
            boyko_data[participant_email] = self.generate_section_data(1, 18, "3_{}")
            values_data[participant_email] = self.generate_section_data(1, 10, "4_{}")

        def map_participant_to_square(
            participant: ParticipantData,
        ) -> Tuple[SquareId, int]:
            return random.choice(list(SquareId)), participant.id

        output_dict = map(map_participant_to_square, participant_data.values())
        transformed_dict: Dict[SquareId, List[int]] = defaultdict(list)
        for square_id, participant_id in output_dict:
            transformed_dict[square_id].append(participant_id)

        return GroupReportData(
            lang=lang,
            project_name=f"{project_name} {lang} - {group_count} groups ({participant_per_group}), {max_participant_count} participants",
            group_data=group_data,
            participant_data=participant_data,
            square_results=transformed_dict,
            cattell_data=cattell_data,
            coping_data=coping_data,
            boyko_data=boyko_data,
            values_data=values_data,
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
            crown=int(random.randint(0, 100) < 30),
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
            31,
        )

        bytes = group_report.generate_pdf(data)
        with open(f"test-{group_report.data.lang}-group.pdf", "wb") as f:
            f.write(bytes)

        pass
