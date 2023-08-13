from collections import defaultdict
from dataclasses import dataclass
from typing import List, Tuple, Dict

from pdf.square_quad_data import RuleConfiguration
from pdf.zetic_group_pdf import SquareQuadId


@dataclass
class RuleValidationResult:
    square_quad_id: SquareQuadId
    possible_scales: List[str]


class RuleValidator:
    def __init__(self, rule: RuleConfiguration):
        self.rule = rule
        pass

    def validate(self, answers: Dict[str, int]) -> RuleValidationResult:
        possible_scales = []
        for rule in self.rule.rules:
            in_range = rule[1] <= answers[rule[0]] <= rule[2]
            if in_range:
                pass
            else:
                print(
                    f"NOT IN RANGE[{self.rule.square_quad_id}] rule: {rule} { answers[rule[0]]}= {in_range}"
                )
                possible_scales.append(rule[0])
                break

        # print(
        #     f"Rule {self.rule.square_quad_id} matched: {all_matched}  {possible_scales}"
        # )

        return RuleValidationResult(
            square_quad_id=self.rule.square_quad_id,
            possible_scales=possible_scales,
        )
        pass


@dataclass
class PossibleRule:
    square_quad_id: SquareQuadId
    possible_scales: List[str]


@dataclass
class SquareQuadResult:
    square_quad_id: SquareQuadId
    possible_rules: List[str]


class SquareQuadCalculator:
    def __init__(self, possible_rules: List[RuleConfiguration]):
        self.rules_validator = list(
            map(lambda rule: RuleValidator(rule), possible_rules)
        )
        pass

    def calculate(self, participant_data: Dict[str, int]) -> SquareQuadResult:
        validation_results: List[PossibleRule] = []

        for rule_validator in self.rules_validator:
            rule_result: RuleValidationResult = rule_validator.validate(
                participant_data
            )
            # print(
            #     f"Valid: {rule_result.square_quad_id}  {rule_result.possible_scales} {len(result)}"
            # )

            validation_results.append(
                PossibleRule(
                    rule_validator.rule.square_quad_id, rule_result.possible_scales
                )
            )

        possible_mismatched_scales_n = 2

        def find_accepted_rule(result: PossibleRule) -> bool:
            return len(result.possible_scales) <= possible_mismatched_scales_n

        def find_exact_match(result: PossibleRule) -> bool:
            return len(result.possible_scales) == 0

        passed_rules = list(filter(find_accepted_rule, validation_results))
        print(f"Passed rules: {len(passed_rules)} of {len(validation_results)}")

        passed_rules_n = len(passed_rules)
        exact_match = list(filter(find_exact_match, passed_rules))
        exact_match_n = len(exact_match)
        square_quad: SquareQuadResult
        if passed_rules_n == 0:
            print(f"Fail to distribute points: {validation_results}")
            square_quad = SquareQuadResult(SquareQuadId.ESFJ_1_1, ["X_X"])
        elif exact_match_n == 1:
            square_quad = SquareQuadResult(
                exact_match[0].square_quad_id, exact_match[0].possible_scales
            )
        else:
            square_quad = SquareQuadResult(
                passed_rules[len(validation_results) - 1].square_quad_id,
                passed_rules[len(validation_results) - 1].possible_scales,
            )

        print(f"Square quad: {square_quad}")
        return square_quad
        pass
