from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel

class TeaserLineRequestBetType(Enum):
    """An enumeration representing different categories.

:cvar SPREAD: "SPREAD"
:vartype SPREAD: str
:cvar TOTAL_POINTS: "TOTAL_POINTS"
:vartype TOTAL_POINTS: str
"""
    SPREAD = "SPREAD"
    TOTAL_POINTS = "TOTAL_POINTS"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, TeaserLineRequestBetType._member_map_.values()))


class TeaserLineRequestTeam(Enum):
    """An enumeration representing different categories.

:cvar TEAM1: "Team1"
:vartype TEAM1: str
:cvar TEAM2: "Team2"
:vartype TEAM2: str
"""
    TEAM1 = "Team1"
    TEAM2 = "Team2"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, TeaserLineRequestTeam._member_map_.values()))


class TeaserLineRequestSide(Enum):
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
        return list(map(lambda x: x.value, TeaserLineRequestSide._member_map_.values()))




@JsonMap({"leg_id": "legId","event_id": "eventId","period_number": "periodNumber","bet_type": "betType"})
class TeaserLineRequest(BaseModel):
    """TeaserLineRequest

:param leg_id: Client genereated GUID for uniquely identifying the leg.
:type leg_id: str
:param event_id: Unique identifier.
:type event_id: int
:param period_number: Period of the match that is being bet on. v1/periods endpoint can be used to retrieve all periods for a sport.
:type period_number: int
:param bet_type: Type of bet. Currently only SPREAD and TOTAL_POINTS are supported. [SPREAD, TOTAL_POINTS]
:type bet_type: TeaserLineRequestBetType
:param team: Team being bet on for a spread line. [Team1, Team2], defaults to None
:type team: TeaserLineRequestTeam, optional
:param side: Side of a total line being bet on. [OVER, UNDER], defaults to None
:type side: TeaserLineRequestSide, optional
:param handicap: Number of points.
:type handicap: float
"""
    def __init__(self, leg_id: str, event_id: int, period_number: int, bet_type: TeaserLineRequestBetType, handicap: float, team: TeaserLineRequestTeam = None, side: TeaserLineRequestSide = None):
        self.leg_id = leg_id
        self.event_id = event_id
        self.period_number = period_number
        self.bet_type = self._enum_matching(bet_type,TeaserLineRequestBetType.list(),"bet_type")
        if team is not None:
            self.team = self._enum_matching(team,TeaserLineRequestTeam.list(),"team")
        if side is not None:
            self.side = self._enum_matching(side,TeaserLineRequestSide.list(),"side")
        self.handicap = handicap



