from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .settled_fixtures_period import SettledFixturesPeriod



@JsonMap({"id_": "id"})
class SettledFixturesEvent(BaseModel):
    """SettledFixturesEvent

:param id_: Event Id., defaults to None
:type id_: int, optional
:param periods: Contains a list of periods., defaults to None
:type periods: List[SettledFixturesPeriod], optional
"""
    def __init__(self, id_: int = None, periods: List[SettledFixturesPeriod] = None):
        if id_ is not None:
            self.id_ = id_
        if periods is not None:
            self.periods = self._define_list(periods, SettledFixturesPeriod)



