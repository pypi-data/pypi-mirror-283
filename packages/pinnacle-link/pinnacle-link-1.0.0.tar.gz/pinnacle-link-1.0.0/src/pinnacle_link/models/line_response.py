from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel

class LineResponseStatus(Enum):
    """An enumeration representing different categories.

:cvar SUCCESS: "SUCCESS"
:vartype SUCCESS: str
:cvar NOT_EXISTS: "NOT_EXISTS"
:vartype NOT_EXISTS: str
"""
    SUCCESS = "SUCCESS"
    NOT_EXISTS = "NOT_EXISTS"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, LineResponseStatus._member_map_.values()))




@JsonMap({"line_id": "lineId","alt_line_id": "altLineId","team1_score": "team1Score","team2_score": "team2Score","team1_red_cards": "team1RedCards","team2_red_cards": "team2RedCards","max_risk_stake": "maxRiskStake","min_risk_stake": "minRiskStake","max_win_stake": "maxWinStake","min_win_stake": "minWinStake","effective_as_of": "effectiveAsOf","period_team1_score": "periodTeam1Score","period_team2_score": "periodTeam2Score","period_team1_red_cards": "periodTeam1RedCards","period_team2_red_cards": "periodTeam2RedCards"})
class LineResponse(BaseModel):
    """LineResponse

:param status: If the value is NOT_EXISTS, than this will be the only parameter in the response. All other params would be empty. [SUCCESS = OK, NOT_EXISTS = Line not offered anymore], defaults to None
:type status: LineResponseStatus, optional
:param price: Latest price., defaults to None
:type price: float, optional
:param line_id: Line identification needed to place a bet., defaults to None
:type line_id: int, optional
:param alt_line_id: This would be needed to place the bet if the handicap is on alternate line, otherwise it will not be populated in the response., defaults to None
:type alt_line_id: int, optional
:param team1_score: Team 1 score for the period 0. Applicable to soccer only., defaults to None
:type team1_score: int, optional
:param team2_score: Team 2 score for the period 0. Applicable to soccer only., defaults to None
:type team2_score: int, optional
:param team1_red_cards: Team 1 red cards for the period 0. Applicable to soccer only., defaults to None
:type team1_red_cards: int, optional
:param team2_red_cards: Team 2 red cards for the period 0. Applicable to soccer only., defaults to None
:type team2_red_cards: int, optional
:param max_risk_stake: Maximum bettable risk amount., defaults to None
:type max_risk_stake: float, optional
:param min_risk_stake: Minimum bettable risk amount., defaults to None
:type min_risk_stake: float, optional
:param max_win_stake: Maximum bettable win amount., defaults to None
:type max_win_stake: float, optional
:param min_win_stake: Minimum bettable win amount., defaults to None
:type min_win_stake: float, optional
:param effective_as_of: Line is effective as of this date and time in UTC., defaults to None
:type effective_as_of: str, optional
:param period_team1_score: Team 1 score for the supported periods. Applicable to soccer only., defaults to None
:type period_team1_score: int, optional
:param period_team2_score: Team 2 score for the supported periods. Applicable to soccer only., defaults to None
:type period_team2_score: int, optional
:param period_team1_red_cards: Team 1 red cards for the supported periods. Applicable to soccer only., defaults to None
:type period_team1_red_cards: int, optional
:param period_team2_red_cards: Team 2 red cards for the supported periods. Applicable to soccer only., defaults to None
:type period_team2_red_cards: int, optional
"""
    def __init__(self, status: LineResponseStatus = None, price: float = None, line_id: int = None, alt_line_id: int = None, team1_score: int = None, team2_score: int = None, team1_red_cards: int = None, team2_red_cards: int = None, max_risk_stake: float = None, min_risk_stake: float = None, max_win_stake: float = None, min_win_stake: float = None, effective_as_of: str = None, period_team1_score: int = None, period_team2_score: int = None, period_team1_red_cards: int = None, period_team2_red_cards: int = None):
        if status is not None:
            self.status = self._enum_matching(status,LineResponseStatus.list(),"status")
        if price is not None:
            self.price = price
        if line_id is not None:
            self.line_id = line_id
        if alt_line_id is not None:
            self.alt_line_id = alt_line_id
        if team1_score is not None:
            self.team1_score = team1_score
        if team2_score is not None:
            self.team2_score = team2_score
        if team1_red_cards is not None:
            self.team1_red_cards = team1_red_cards
        if team2_red_cards is not None:
            self.team2_red_cards = team2_red_cards
        if max_risk_stake is not None:
            self.max_risk_stake = max_risk_stake
        if min_risk_stake is not None:
            self.min_risk_stake = min_risk_stake
        if max_win_stake is not None:
            self.max_win_stake = max_win_stake
        if min_win_stake is not None:
            self.min_win_stake = min_win_stake
        if effective_as_of is not None:
            self.effective_as_of = effective_as_of
        if period_team1_score is not None:
            self.period_team1_score = period_team1_score
        if period_team2_score is not None:
            self.period_team2_score = period_team2_score
        if period_team1_red_cards is not None:
            self.period_team1_red_cards = period_team1_red_cards
        if period_team2_red_cards is not None:
            self.period_team2_red_cards = period_team2_red_cards



