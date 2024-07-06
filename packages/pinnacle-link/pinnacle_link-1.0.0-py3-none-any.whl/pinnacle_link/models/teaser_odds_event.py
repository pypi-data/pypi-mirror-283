from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .teaser_odds_period import TeaserOddsPeriod



@JsonMap({"id_": "id"})
class TeaserOddsEvent(BaseModel):
    """TeaserOddsEvent

:param id_: Unique identifier., defaults to None
:type id_: int, optional
:param periods: A collection of periods indicating the period numbers available for betting., defaults to None
:type periods: List[TeaserOddsPeriod], optional
"""
    def __init__(self, id_: int = None, periods: List[TeaserOddsPeriod] = None):
        if id_ is not None:
            self.id_ = id_
        if periods is not None:
            self.periods = self._define_list(periods, TeaserOddsPeriod)



