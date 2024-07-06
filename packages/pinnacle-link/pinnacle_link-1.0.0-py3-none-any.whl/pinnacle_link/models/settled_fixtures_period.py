from __future__ import annotations
from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel
from .cancellation_reason_type import CancellationReasonType

class SettledFixturesPeriodStatus(Enum):
    """An enumeration representing different categories.

:cvar _1: 1
:vartype _1: str
:cvar _2: 2
:vartype _2: str
:cvar _3: 3
:vartype _3: str
:cvar _4: 4
:vartype _4: str
:cvar _5: 5
:vartype _5: str
"""
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SettledFixturesPeriodStatus._member_map_.values()))




@JsonMap({"settlement_id": "settlementId","settled_at": "settledAt","team1_score": "team1Score","team2_score": "team2Score","team1_score_sets": "team1ScoreSets","team2_score_sets": "team2ScoreSets","cancellation_reason": "cancellationReason"})
class SettledFixturesPeriod(BaseModel):
    """SettledFixturesPeriod

:param number: This represents the period of the match. , defaults to None
:type number: int, optional
:param status: Period settlement status. <br><br>1 = Event period is settled, <br>2 = Event period is re-settled, <br>3 = Event period is cancelled, <br>4 = Event period is re-settled as cancelled, <br>5 = Event is deleted<br>, defaults to None
:type status: SettledFixturesPeriodStatus, optional
:param settlement_id: Unique id of the settlement. In case of a re-settlement, a new settlementId and settledAt will be generated., defaults to None
:type settlement_id: int, optional
:param settled_at: Date and time in UTC when the period was settled., defaults to None
:type settled_at: str, optional
:param team1_score: Team1 score., defaults to None
:type team1_score: int, optional
:param team2_score: Team2 score., defaults to None
:type team2_score: int, optional
:param team1_score_sets: Team1 sets score. Supported for tennis only., defaults to None
:type team1_score_sets: int, optional
:param team2_score_sets: Team2 sets score. Supported for tennis only., defaults to None
:type team2_score_sets: int, optional
:param cancellation_reason: cancellation_reason, defaults to None
:type cancellation_reason: CancellationReasonType, optional
"""
    def __init__(self, number: int = None, status: SettledFixturesPeriodStatus = None, settlement_id: int = None, settled_at: str = None, team1_score: int = None, team2_score: int = None, team1_score_sets: int = None, team2_score_sets: int = None, cancellation_reason: CancellationReasonType = None):
        if number is not None:
            self.number = number
        if status is not None:
            self.status = self._enum_matching(status,SettledFixturesPeriodStatus.list(),"status")
        if settlement_id is not None:
            self.settlement_id = settlement_id
        if settled_at is not None:
            self.settled_at = settled_at
        if team1_score is not None:
            self.team1_score = team1_score
        if team2_score is not None:
            self.team2_score = team2_score
        if team1_score_sets is not None:
            self.team1_score_sets = team1_score_sets
        if team2_score_sets is not None:
            self.team2_score_sets = team2_score_sets
        if cancellation_reason is not None:
            self.cancellation_reason = self._define_object(cancellation_reason, CancellationReasonType)



