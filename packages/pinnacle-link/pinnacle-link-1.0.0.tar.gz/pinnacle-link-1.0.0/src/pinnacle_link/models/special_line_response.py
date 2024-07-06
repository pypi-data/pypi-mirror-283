from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel

class SpecialLineResponseStatus(Enum):
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
        return list(map(lambda x: x.value, SpecialLineResponseStatus._member_map_.values()))




@JsonMap({"special_id": "specialId","contestant_id": "contestantId","min_risk_stake": "minRiskStake","max_risk_stake": "maxRiskStake","min_win_stake": "minWinStake","max_win_stake": "maxWinStake","line_id": "lineId"})
class SpecialLineResponse(BaseModel):
    """SpecialLineResponse

:param status: Status [SUCCESS = OK, NOT_EXISTS = Line not offered anymore], defaults to None
:type status: SpecialLineResponseStatus, optional
:param special_id: Special Id., defaults to None
:type special_id: int, optional
:param contestant_id: Contestant Id., defaults to None
:type contestant_id: int, optional
:param min_risk_stake: Minimum bettable risk amount., defaults to None
:type min_risk_stake: float, optional
:param max_risk_stake: Maximum bettable risk amount., defaults to None
:type max_risk_stake: float, optional
:param min_win_stake: Minimum bettable win amount., defaults to None
:type min_win_stake: float, optional
:param max_win_stake: Maximum bettable win amount., defaults to None
:type max_win_stake: float, optional
:param line_id: Line identification needed to place a bet., defaults to None
:type line_id: int, optional
:param price: Latest price., defaults to None
:type price: float, optional
:param handicap: Handicap., defaults to None
:type handicap: float, optional
"""
    def __init__(self, status: SpecialLineResponseStatus = None, special_id: int = None, contestant_id: int = None, min_risk_stake: float = None, max_risk_stake: float = None, min_win_stake: float = None, max_win_stake: float = None, line_id: int = None, price: float = None, handicap: float = None):
        if status is not None:
            self.status = self._enum_matching(status,SpecialLineResponseStatus.list(),"status")
        if special_id is not None:
            self.special_id = special_id
        if contestant_id is not None:
            self.contestant_id = contestant_id
        if min_risk_stake is not None:
            self.min_risk_stake = min_risk_stake
        if max_risk_stake is not None:
            self.max_risk_stake = max_risk_stake
        if min_win_stake is not None:
            self.min_win_stake = min_win_stake
        if max_win_stake is not None:
            self.max_win_stake = max_win_stake
        if line_id is not None:
            self.line_id = line_id
        if price is not None:
            self.price = price
        if handicap is not None:
            self.handicap = handicap



