from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .fixture import Fixture



@JsonMap({"id_": "id"})
class FixturesLeague(BaseModel):
    """FixturesLeague

:param id_: League ID., defaults to None
:type id_: int, optional
:param name: League Name., defaults to None
:type name: str, optional
:param events: Contains a list of events., defaults to None
:type events: List[Fixture], optional
"""
    def __init__(self, id_: int = None, name: str = None, events: List[Fixture] = None):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if events is not None:
            self.events = self._define_list(events, Fixture)



