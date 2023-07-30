from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Union


class GenderGroup(Enum):
    MUJER = "mujer"
    HOMBRE = "hombre"

    @staticmethod
    def from_sex(sex: str):
        match sex.lower().strip():
            case "hombre" | "мужской":
                return GenderGroup.HOMBRE
            case "mujer" | "женский":
                return GenderGroup.MUJER
            case _:
                return None


class AgeGroup(Enum):
    MAYOR = "Mayor"
    JOVEN = "Joven"

    @staticmethod
    def from_year(year: int):
        if year < 1991:
            return AgeGroup.MAYOR
        else:
            return AgeGroup.JOVEN


class RawToTPointMapper:
    def __init__(
        self,
        gender: GenderGroup,
        age: AgeGroup,
        points_mapper: Dict[str, Dict[str, Union[Dict[str, int], int]]],
    ):
        self._gender = gender
        self._age = age
        self._points = points_mapper

    def map_to_t_points(self, section: str, category: str, points: int):
        try:
            wtf = self._points[section][category]
            if isinstance(wtf, int):
                return round(points / wtf * 10)
            else:
                return self._points[section][category][str(points)]
        except Exception as e:
            print(f"Exception: {section} {category} {points}")
            raise e
