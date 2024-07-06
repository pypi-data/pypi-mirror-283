from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .teaser_odds_event import TeaserOddsEvent



@JsonMap({"id_": "id"})
class TeaserOddsLeague(BaseModel):
    """TeaserOddsLeague

:param id_: Unique identifier. League details can be retrieved from a call to Get Leagues endpoint., defaults to None
:type id_: int, optional
:param events: A collection of Event., defaults to None
:type events: List[TeaserOddsEvent], optional
"""
    def __init__(self, id_: int = None, events: List[TeaserOddsEvent] = None):
        if id_ is not None:
            self.id_ = id_
        if events is not None:
            self.events = self._define_list(events, TeaserOddsEvent)



