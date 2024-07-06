from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .round_robin_option_with_odds_v2 import RoundRobinOptionWithOddsV2
from .parlay_line_leg import ParlayLineLeg

class ParlayLinesResponseV2Status(Enum):
    """An enumeration representing different categories.

:cvar VALID: "VALID"
:vartype VALID: str
:cvar PROCESSED_WITH_ERROR: "PROCESSED_WITH_ERROR"
:vartype PROCESSED_WITH_ERROR: str
"""
    VALID = "VALID"
    PROCESSED_WITH_ERROR = "PROCESSED_WITH_ERROR"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ParlayLinesResponseV2Status._member_map_.values()))




@JsonMap({"min_risk_stake": "minRiskStake","max_parlay_risk_stake": "maxParlayRiskStake","max_round_robin_total_risk": "maxRoundRobinTotalRisk","max_round_robin_total_win": "maxRoundRobinTotalWin","round_robin_option_with_odds": "roundRobinOptionWithOdds"})
class ParlayLinesResponseV2(BaseModel):
    """ParlayLinesResponseV2

:param status: Status of the parlay [VALID = Parlay is valid, PROCESSED_WITH_ERROR = Parlay contains error(s)]
:type status: ParlayLinesResponseV2Status
:param error: INVALID_LEGS. Signifies that one or more legs are invalid. Populated only if status is PROCESSED_WITH_ERROR., defaults to None
:type error: str, optional
:param min_risk_stake: Minimum allowed stake amount., defaults to None
:type min_risk_stake: float, optional
:param max_parlay_risk_stake: Maximum allowed stake amount for parlay bets. For round robin max stake [see FAQ](https://github.com/pinnacleapi/pinnacleapi-documentation/blob/master/FAQ.md#how-to-calculate-round-robin-max-stake)., defaults to None
:type max_parlay_risk_stake: float, optional
:param max_round_robin_total_risk: Maximum allowed total stake amount for all the parlay bets in the round robin., defaults to None
:type max_round_robin_total_risk: float, optional
:param max_round_robin_total_win: Maximum allowed total win amount for all the parlay bets in the round robin., defaults to None
:type max_round_robin_total_win: float, optional
:param round_robin_option_with_odds: Provides array with all acceptable Round Robin options with parlay odds for that option., defaults to None
:type round_robin_option_with_odds: List[RoundRobinOptionWithOddsV2], optional
:param legs: The collection of legs (the format of the object is described below)., defaults to None
:type legs: List[ParlayLineLeg], optional
"""
    def __init__(self, status: ParlayLinesResponseV2Status, error: str = None, min_risk_stake: float = None, max_parlay_risk_stake: float = None, max_round_robin_total_risk: float = None, max_round_robin_total_win: float = None, round_robin_option_with_odds: List[RoundRobinOptionWithOddsV2] = None, legs: List[ParlayLineLeg] = None):
        self.status = self._enum_matching(status,ParlayLinesResponseV2Status.list(),"status")
        if error is not None:
            self.error = error
        if min_risk_stake is not None:
            self.min_risk_stake = min_risk_stake
        if max_parlay_risk_stake is not None:
            self.max_parlay_risk_stake = max_parlay_risk_stake
        if max_round_robin_total_risk is not None:
            self.max_round_robin_total_risk = max_round_robin_total_risk
        if max_round_robin_total_win is not None:
            self.max_round_robin_total_win = max_round_robin_total_win
        if round_robin_option_with_odds is not None:
            self.round_robin_option_with_odds = self._define_list(round_robin_option_with_odds, RoundRobinOptionWithOddsV2)
        if legs is not None:
            self.legs = self._define_list(legs, ParlayLineLeg)



