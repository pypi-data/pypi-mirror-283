from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel

class LegBetType(Enum):
    """An enumeration representing different categories.

:cvar SPREAD: "SPREAD"
:vartype SPREAD: str
:cvar MONEYLINE: "MONEYLINE"
:vartype MONEYLINE: str
:cvar TOTAL_POINTS: "TOTAL_POINTS"
:vartype TOTAL_POINTS: str
:cvar TEAM_TOTAL_POINTS: "TEAM_TOTAL_POINTS"
:vartype TEAM_TOTAL_POINTS: str
"""
    SPREAD = "SPREAD"
    MONEYLINE = "MONEYLINE"
    TOTAL_POINTS = "TOTAL_POINTS"
    TEAM_TOTAL_POINTS = "TEAM_TOTAL_POINTS"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, LegBetType._member_map_.values()))


class ParlayLineRequestTeam(Enum):
    """An enumeration representing different categories.

:cvar TEAM1: "Team1"
:vartype TEAM1: str
:cvar TEAM2: "Team2"
:vartype TEAM2: str
:cvar DRAW: "Draw"
:vartype DRAW: str
"""
    TEAM1 = "Team1"
    TEAM2 = "Team2"
    DRAW = "Draw"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ParlayLineRequestTeam._member_map_.values()))


class ParlayLineRequestSide(Enum):
    """An enumeration representing different categories.

:cvar OVER: "OVER"
:vartype OVER: str
:cvar UNDER: "UNDER"
:vartype UNDER: str
"""
    OVER = "OVER"
    UNDER = "UNDER"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ParlayLineRequestSide._member_map_.values()))




@JsonMap({"unique_leg_id": "uniqueLegId","event_id": "eventId","period_number": "periodNumber","leg_bet_type": "legBetType"})
class ParlayLineRequest(BaseModel):
    """ParlayLineRequest

:param unique_leg_id: This unique id of the leg. It used to identify and match leg in the response.
:type unique_leg_id: str
:param event_id: Id of the event.
:type event_id: int
:param period_number: This represents the period of the match. 
:type period_number: int
:param leg_bet_type: SPREAD, MONEYLINE,  TOTAL_POINTS and TEAM_TOTAL_POINTS are supported.  
:type leg_bet_type: LegBetType
:param team: Chosen team type. This is needed only for SPREAD and MONEYLINE wager types. [Team1, Team2, Draw (MONEYLINE only)], defaults to None
:type team: ParlayLineRequestTeam, optional
:param side: Chosen side. This is needed only for TOTAL_POINTS wager type.  [OVER, UNDER], defaults to None
:type side: ParlayLineRequestSide, optional
:param handicap: This is needed for SPREAD and TOTAL_POINTS bet type., defaults to None
:type handicap: float, optional
"""
    def __init__(self, unique_leg_id: str, event_id: int, period_number: int, leg_bet_type: LegBetType, team: ParlayLineRequestTeam = None, side: ParlayLineRequestSide = None, handicap: float = None):
        self.unique_leg_id = unique_leg_id
        self.event_id = event_id
        self.period_number = period_number
        self.leg_bet_type = self._enum_matching(leg_bet_type,LegBetType.list(),"leg_bet_type")
        if team is not None:
            self.team = self._enum_matching(team,ParlayLineRequestTeam.list(),"team")
        if side is not None:
            self.side = self._enum_matching(side,ParlayLineRequestSide.list(),"side")
        if handicap is not None:
            self.handicap = handicap



