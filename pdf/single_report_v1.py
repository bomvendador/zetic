from typing import Dict

from pdf.single_report import SingleReport


class SingleReportV1(SingleReport):
    def __init__(self, scale_points_description: Dict[str, str]):
        super().__init__()
        self._scale_points_description = scale_points_description

    def _get_scale_points_description(self, scale: str, points: int) -> str:
        description = self._scale_points_description.get(scale)
        if description is None:
            print(f"No description for scale {scale} for points {points}")
            return ""
        return description
