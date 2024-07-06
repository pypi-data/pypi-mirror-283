from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .odds_event import OddsEvent



@JsonMap({"id_": "id"})
class OddsLeague(BaseModel):
    """OddsLeague

:param id_: League Id., defaults to None
:type id_: int, optional
:param events: Contains a list of events., defaults to None
:type events: List[OddsEvent], optional
"""
    def __init__(self, id_: int = None, events: List[OddsEvent] = None):
        if id_ is not None:
            self.id_ = id_
        if events is not None:
            self.events = self._define_list(events, OddsEvent)



