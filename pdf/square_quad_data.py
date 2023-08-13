from dataclasses import dataclass
from typing import Tuple, List

from pdf.zetic_group_pdf import SquareQuadId


@dataclass
class LiePoint:
    fio: str
    email: str
    lie_points: int
    role_name: str
    position: str


@dataclass
class ParticipantData:
    fio: str
    email: str
    section_code: str
    category_code: str
    points: int


@dataclass
class ReportParticipantsResponse:
    data: List[ParticipantData]
    lie_points: List[LiePoint]


@dataclass
class RuleConfiguration:
    square_quad_id: SquareQuadId
    rules: List[Tuple[str, int, int]]
    pass


RULE_1_1 = RuleConfiguration(
    SquareQuadId.ESFJ_1_1,
    [
        ("1_7", 6, 10),
        ("1_6", 6, 10),
        ("1_5", 5, 10),
        ("1_8", 1, 5),
        ("4_1", 5, 10),
        ("4_3", 5, 10),
        ("4_4", 5, 10),
    ],
)

RULE_1_2 = RuleConfiguration(
    SquareQuadId.ENFJ_1_2,
    [
        ("1_7", 6, 10),
        ("1_6", 6, 10),
        ("1_4", 5, 10),
        ("1_8", 5, 10),
        ("1_12", 5, 10),
        ("4_1", 5, 10),
        ("4_4", 5, 10),
        ("4_10", 5, 10),
    ],
)

RULE_1_3 = RuleConfiguration(
    SquareQuadId.ESFP_1_3,
    [
        ("1_7", 6, 10),
        ("1_6", 6, 10),
        ("1_4", 5, 10),
        ("1_10", 0, 5),
        ("1_11", 0, 5),
        ("1_14", 5, 10),
        ("1_13", 0, 5),
        ("1_12", 0, 5),
        ("4_1", 5, 10),
        ("4_3", 5, 10),
    ],
)

RULE_1_4 = RuleConfiguration(
    SquareQuadId.ENFP_1_4,
    [
        ("1_7", 6, 10),
        ("1_6", 6, 10),
        ("1_4", 5, 10),
        ("1_8", 0, 5),
        ("1_11", 0, 5),
        ("1_14", 5, 10),
        ("1_13", 0, 5),
        ("1_12", 5, 10),
        ("4_1", 5, 10),
        ("4_3", 5, 10),
        ("4_10", 5, 10),
    ],
)

RULE_2_1 = RuleConfiguration(
    SquareQuadId.ESTJ_2_1,
    [
        ("1_7", 6, 10),
        ("1_6", 0, 5),
        ("1_8", 0, 5),
        ("1_11", 6, 10),
        ("1_10", 6, 10),
        ("1_4", 0, 5),
        ("1_13", 6, 10),
        ("4_9", 5, 10),
        ("4_2", 5, 10),
        ("4_4", 5, 10),
    ],
)

RULE_2_2 = RuleConfiguration(
    SquareQuadId.ENTJ_2_2,
    [
        ("1_7", 6, 10),
        ("1_6", 0, 5),
        ("1_8", 6, 10),
        ("1_11", 5, 10),
        ("1_10", 5, 10),
        ("1_4", 0, 5),
        ("1_15", 4, 10),
        ("1_12", 5, 10),
        ("4_9", 5, 10),
        ("4_2", 5, 10),
        ("4_4", 5, 10),
        ("4_10", 5, 10),
    ],
)

RULE_2_3 = RuleConfiguration(
    SquareQuadId.ESFJ_1_1,
    [
        ("1_7", 6, 10),
        ("1_6", 0, 5),
        ("1_11", 0, 5),
        ("1_10", 0, 5),
        ("1_4", 5, 10),
        ("4_3", 5, 10),
    ],
)

RULE_2_4 = RuleConfiguration(
    SquareQuadId.ENTP_2_4,
    [
        ("1_7", 6, 10),
        ("1_6", 0, 5),
        ("1_8", 6, 10),
        ("1_11", 0, 5),
        ("1_10", 0, 5),
        ("1_15", 5, 10),
        ("1_12", 5, 10),
        ("1_14", 5, 10),
        ("4_7", 5, 10),
        ("4_10", 5, 10),
    ],
)

RULE_3_1 = RuleConfiguration(
    SquareQuadId.ISFJ_3_1,
    [
        ("1_7", 1, 5),
        ("1_6", 6, 10),
        ("1_11", 5, 10),
        ("1_10", 5, 10),
        ("1_9", 0, 5),
        ("1_13", 6, 10),
        ("1_8", 0, 5),
        ("4_1", 5, 10),
        ("4_9", 5, 10),
        ("4_2", 5, 10),
        ("4_4", 5, 10),
        ("4_10", 5, 10),
        ("1_1", 0, 6),
    ],
)

RULE_3_2 = RuleConfiguration(
    SquareQuadId.INFJ_3_2,
    [
        ("1_7", 1, 5),
        ("1_6", 6, 10),
        ("1_11", 5, 10),
        ("1_10", 5, 10),
        ("1_9", 0, 5),
        ("4_1", 5, 10),
        ("4_9", 5, 10),
        ("4_2", 5, 10),
        ("4_5", 5, 10),
        ("4_4", 5, 10),
        ("4_10", 5, 10),
    ],
)

RULE_3_3 = RuleConfiguration(
    SquareQuadId.ISFP_3_3,
    [
        ("1_1", 0, 6),
        ("1_7", 1, 5),
        ("1_6", 6, 10),
        ("1_10", 0, 5),
        ("1_5", 5, 10),
        ("1_11", 0, 5),
        ("1_9", 0, 5),
        ("1_13", 6, 10),
        ("4_1", 5, 10),
        ("4_5", 5, 10),
    ],
)

RULE_3_4 = RuleConfiguration(
    SquareQuadId.INFP_3_4,
    [
        ("1_7", 1, 5),
        ("1_6", 6, 10),
        ("1_11", 5, 10),
        ("1_10", 5, 10),
        ("1_9", 0, 5),
        ("4_1", 5, 10),
        ("4_9", 5, 10),
        ("4_2", 5, 10),
        ("1_15", 0, 5),
        ("4_3", 0, 5),
        ("4_10", 5, 10),
    ],
)

RULE_4_1 = RuleConfiguration(
    SquareQuadId.ISTJ_4_1,
    [
        ("1_7", 0, 5),
        ("1_6", 0, 5),
        ("1_11", 5, 10),
        ("1_10", 5, 10),
        ("1_8", 0, 5),
        ("1_13", 5, 10),
        ("4_9", 5, 10),
        ("4_2", 5, 10),
        ("4_4", 5, 10),
        ("4_7", 5, 10),
    ],
)

RULE_4_2 = RuleConfiguration(
    SquareQuadId.INTJ_4_2,
    [
        ("1_7", 0, 5),
        ("1_6", 0, 5),
        ("1_11", 5, 10),
        ("1_10", 5, 10),
        ("1_8", 5, 10),
        ("1_12", 5, 10),
        ("1_13", 5, 10),
        ("4_9", 5, 10),
        ("4_10", 5, 10),
        ("4_4", 5, 10),
    ],
)

RULE_4_3 = RuleConfiguration(
    SquareQuadId.ISTP_4_3,
    [
        ("1_14", 6, 10),
        ("1_7", 1, 5),
        ("1_8", 6, 10),
        ("1_6", 1, 5),
        ("1_14", 6, 10),
        ("1_11", 0, 5),
        ("1_10", 0, 5),
    ],
)

RULE_4_4 = RuleConfiguration(
    SquareQuadId.INTP_4_4,
    [
        ("1_7", 0, 5),
        ("1_6", 0, 5),
        ("1_11", 0, 5),
        ("1_10", 0, 5),
        ("1_8", 5, 10),
        ("1_12", 5, 10),
        ("4_2", 0, 5),
        ("4_10", 5, 10),
    ],
)

RULES = [
    RULE_1_1,
    RULE_1_2,
    RULE_1_3,
    RULE_1_4,
    RULE_2_1,
    RULE_2_2,
    RULE_2_3,
    RULE_2_4,
    RULE_3_1,
    RULE_3_2,
    RULE_3_3,
    RULE_3_4,
    RULE_4_1,
    RULE_4_2,
    RULE_4_3,
    RULE_4_4,
]
