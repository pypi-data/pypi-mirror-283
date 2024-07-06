from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .teaser_line_leg import TeaserLineLeg

class TeaserLinesResponseStatus(Enum):
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
        return list(map(lambda x: x.value, TeaserLinesResponseStatus._member_map_.values()))


class TeaserLinesResponseErrorCode(Enum):
    """An enumeration representing different categories.

:cvar INVALID_LEGS: "INVALID_LEGS"
:vartype INVALID_LEGS: str
:cvar SAME_EVENT_ONLY_REQUIRED: "SAME_EVENT_ONLY_REQUIRED"
:vartype SAME_EVENT_ONLY_REQUIRED: str
:cvar TEASER_DISABLED: "TEASER_DISABLED"
:vartype TEASER_DISABLED: str
:cvar TEASER_DOES_NOT_EXIST: "TEASER_DOES_NOT_EXIST"
:vartype TEASER_DOES_NOT_EXIST: str
:cvar TOO_FEW_LEGS: "TOO_FEW_LEGS"
:vartype TOO_FEW_LEGS: str
:cvar TOO_MANY_LEGS: "TOO_MANY_LEGS"
:vartype TOO_MANY_LEGS: str
:cvar UNKNOWN: "UNKNOWN"
:vartype UNKNOWN: str
"""
    INVALID_LEGS = "INVALID_LEGS"
    SAME_EVENT_ONLY_REQUIRED = "SAME_EVENT_ONLY_REQUIRED"
    TEASER_DISABLED = "TEASER_DISABLED"
    TEASER_DOES_NOT_EXIST = "TEASER_DOES_NOT_EXIST"
    TOO_FEW_LEGS = "TOO_FEW_LEGS"
    TOO_MANY_LEGS = "TOO_MANY_LEGS"
    UNKNOWN = "UNKNOWN"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, TeaserLinesResponseErrorCode._member_map_.values()))




@JsonMap({"error_code": "errorCode","min_risk_stake": "minRiskStake","max_risk_stake": "maxRiskStake","min_win_stake": "minWinStake","max_win_stake": "maxWinStake"})
class TeaserLinesResponse(BaseModel):
    """TeaserLinesResponse

:param status: Status of the request. [VALID = Teaser is valid, PROCESSED_WITH_ERROR = Teaser contains one or more errors]
:type status: TeaserLinesResponseStatus
:param error_code: When Status is PROCESSED_WITH_ERROR, provides a code indicating the specific problem.  <br>   <br>  INVALID_LEGS = One or more of the legs is invalid,<br>  SAME_EVENT_ONLY_REQUIRED = Teaser specified requires that all legs are from the same event,  <br>  TEASER_DISABLED = Teaser has been disabled and cannot be bet on,  <br>  TEASER_DOES_NOT_EXIST = The teaser identifier could not be found,  <br>  TOO_FEW_LEGS = You do not meet the minimum number of legs requirement for the teaser specified,  <br>  TOO_MANY_LEGS = You are above the maximum number of legs for the teaser specified,  <br>  UNKNOWN = An unknown error has occurred  <br>, defaults to None
:type error_code: TeaserLinesResponseErrorCode, optional
:param price: Price for the bet., defaults to None
:type price: float, optional
:param min_risk_stake: Minimum bet amount for WIN_RISK_TYPE.RISK., defaults to None
:type min_risk_stake: float, optional
:param max_risk_stake: Maximum bet amount for WIN_RISK_TYPE.RISK., defaults to None
:type max_risk_stake: float, optional
:param min_win_stake: Minimum bet amount for WIN_RISK_TYPE.WIN., defaults to None
:type min_win_stake: float, optional
:param max_win_stake: Maximum bet amount for WIN_RISK_TYPE.WIN., defaults to None
:type max_win_stake: float, optional
:param legs: Collection of Teaser Legs from the request.
:type legs: List[TeaserLineLeg]
"""
    def __init__(self, status: TeaserLinesResponseStatus, legs: List[TeaserLineLeg], error_code: TeaserLinesResponseErrorCode = None, price: float = None, min_risk_stake: float = None, max_risk_stake: float = None, min_win_stake: float = None, max_win_stake: float = None):
        self.status = self._enum_matching(status,TeaserLinesResponseStatus.list(),"status")
        if error_code is not None:
            self.error_code = self._enum_matching(error_code,TeaserLinesResponseErrorCode.list(),"error_code")
        if price is not None:
            self.price = price
        if min_risk_stake is not None:
            self.min_risk_stake = min_risk_stake
        if max_risk_stake is not None:
            self.max_risk_stake = max_risk_stake
        if min_win_stake is not None:
            self.min_win_stake = min_win_stake
        if max_win_stake is not None:
            self.max_win_stake = max_win_stake
        self.legs = self._define_list(legs, TeaserLineLeg)



