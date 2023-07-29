from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict


class AgeGroup(Enum):
    MAYOR = "Mayor"
    JOVEN = "Joven"

    @staticmethod
    def from_age(year: int):
        if year < 1991:
            return AgeGroup.MAYOR
        else:
            return AgeGroup.JOVEN


class RawToTPointMapper:
    def __init__(
        self,
        gender: str,
        age: AgeGroup,
        points_mapper: Dict[str, Dict[str, Dict[int, int]]],
    ):
        self._gender = gender
        self._age = age
        self._points = points_mapper

    def map_to_t_points(self, section: str, category: str, points: int):
        return self._points[section][category][points]
