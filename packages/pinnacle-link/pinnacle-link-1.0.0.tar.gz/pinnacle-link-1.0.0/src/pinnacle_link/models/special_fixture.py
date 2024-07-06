from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .specials_fixtures_event import SpecialsFixturesEvent
from .specials_fixtures_contestant import SpecialsFixturesContestant

class SpecialFixtureBetType(Enum):
    """An enumeration representing different categories.

:cvar MULTI_WAY_HEAD_TO_HEAD: "MULTI_WAY_HEAD_TO_HEAD"
:vartype MULTI_WAY_HEAD_TO_HEAD: str
:cvar SPREAD: "SPREAD"
:vartype SPREAD: str
:cvar OVER_UNDER: "OVER_UNDER"
:vartype OVER_UNDER: str
"""
    MULTI_WAY_HEAD_TO_HEAD = "MULTI_WAY_HEAD_TO_HEAD"
    SPREAD = "SPREAD"
    OVER_UNDER = "OVER_UNDER"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SpecialFixtureBetType._member_map_.values()))


class SpecialFixtureStatus(Enum):
    """An enumeration representing different categories.

:cvar O: "O"
:vartype O: str
:cvar H: "H"
:vartype H: str
:cvar I: "I"
:vartype I: str
"""
    O = "O"
    H = "H"
    I = "I"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SpecialFixtureStatus._member_map_.values()))


class SpecialFixtureLiveStatus(Enum):
    """An enumeration representing different categories.

:cvar _0: 0
:vartype _0: str
:cvar _1: 1
:vartype _1: str
:cvar _2: 2
:vartype _2: str
"""
    _0 = 0
    _1 = 1
    _2 = 2

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SpecialFixtureLiveStatus._member_map_.values()))




@JsonMap({"id_": "id","bet_type": "betType","date_": "date","live_status": "liveStatus"})
class SpecialFixture(BaseModel):
    """SpecialFixture

:param id_: Unique Id, defaults to None
:type id_: int, optional
:param bet_type: The type [MULTI_WAY_HEAD_TO_HEAD, SPREAD, OVER_UNDER], defaults to None
:type bet_type: SpecialFixtureBetType, optional
:param name: Name of the special., defaults to None
:type name: str, optional
:param date_: Date of the special in UTC., defaults to None
:type date_: str, optional
:param cutoff: Wagering cutoff date in UTC., defaults to None
:type cutoff: str, optional
:param category: The category that the special falls under., defaults to None
:type category: str, optional
:param units: Measurment in the context of the special. This is applicable to specials bet type spead and over/under. In a hockey special this could be goals., defaults to None
:type units: str, optional
:param status: Status of the Special <br><br> O = This is the starting status. It means that the lines<br> are open for betting, <br><br> H = This status indicates that the lines are temporarily unavailable<br> for betting, <br><br> I = This status indicates that one or more lines have a red circle<br> (a lower maximum bet amount)<br>, defaults to None
:type status: SpecialFixtureStatus, optional
:param event: Optional event asscoaited with the special., defaults to None
:type event: SpecialsFixturesEvent, optional
:param contestants: ContestantLines available for wagering., defaults to None
:type contestants: List[SpecialsFixturesContestant], optional
:param live_status: When a special is linked to an event, we will return live status of the event, otherwise it will be 0. <br>0 = No live betting will be offered on this event, <br>1 = Live betting event, <br>2 = Live betting will be offered on this match, but on a different event.  <br>Please note that live delay is applied when placing bets on special with LiveStatus=1 <br>, defaults to None
:type live_status: SpecialFixtureLiveStatus, optional
"""
    def __init__(self, id_: int = None, bet_type: SpecialFixtureBetType = None, name: str = None, date_: str = None, cutoff: str = None, category: str = None, units: str = None, status: SpecialFixtureStatus = None, event: SpecialsFixturesEvent = None, contestants: List[SpecialsFixturesContestant] = None, live_status: SpecialFixtureLiveStatus = None):
        if id_ is not None:
            self.id_ = id_
        if bet_type is not None:
            self.bet_type = self._enum_matching(bet_type,SpecialFixtureBetType.list(),"bet_type")
        if name is not None:
            self.name = name
        if date_ is not None:
            self.date_ = date_
        if cutoff is not None:
            self.cutoff = cutoff
        if category is not None:
            self.category = category
        if units is not None:
            self.units = units
        if status is not None:
            self.status = self._enum_matching(status,SpecialFixtureStatus.list(),"status")
        if event is not None:
            self.event = self._define_object(event, SpecialsFixturesEvent)
        if contestants is not None:
            self.contestants = self._define_list(contestants, SpecialsFixturesContestant)
        if live_status is not None:
            self.live_status = self._enum_matching(live_status,SpecialFixtureLiveStatus.list(),"live_status")



