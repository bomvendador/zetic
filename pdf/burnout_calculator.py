from dataclasses import dataclass
from typing import List, Dict

from pdf.models import ReportData


@dataclass
class BurnoutRule:
    max_points: int
    category_codes: List[str]


BURNOUT_RULES: List[BurnoutRule] = [
    BurnoutRule(18, ["1_1", "1_2", "1_3", "1_4"]),
    BurnoutRule(18, ["1_5", "1_6", "1_7", "1_8"]),
    BurnoutRule(18, ["1_9", "1_10", "1_11", "1_12"]),
]


class BurnoutCalculator:
    def __init__(self, rules: List[BurnoutRule]):
        self.rules = rules
        pass

    def has_burnout(self, answers: Dict[str, ReportData]):
        for rule in self.rules:
            points = 0
            for category_code in rule.category_codes:
                if category_code in answers:
                    points += answers[category_code].points
                else:
                    print(f"Category {category_code} not found in answers")
            if points > rule.max_points:
                return True

        return False
        pass
