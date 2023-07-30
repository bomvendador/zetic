from typing import Dict, List

from pdf.report_sections_configuration import (
    CATTELL_CATEGORIES,
    COPING_CATEGORIES_V1,
    BOYKO_CATEGORIES_V1,
    VALUES_CATEGORIES_V1,
    COPING_CATEGORIES_V2,
    BOYKO_CATEGORIES_V2,
)
from pdf.single_report import SingleReport


class SingleReportDict(SingleReport):
    def __init__(self, scale_points_description: Dict[str, str]):
        super().__init__()
        self._scale_points_description = scale_points_description

    def _get_scale_points_description(self, scale: str, points: int) -> str:
        description = self._scale_points_description.get(scale)
        if description is None:
            print(f"No description for scale {scale} for points {points}")
            return ""
        return description


class SingleReportV1(SingleReportDict):
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


class SingleReportV2(SingleReportDict):
    def _get_section_scales(self, section: str) -> Dict[str, List[str]]:
        match section:
            case "1":
                return CATTELL_CATEGORIES
            case "2":
                return COPING_CATEGORIES_V2
            case "3":
                return BOYKO_CATEGORIES_V2
            case "4":
                return VALUES_CATEGORIES_V1
            case _:
                raise Exception(f"Unknown section {section}")
        pass
