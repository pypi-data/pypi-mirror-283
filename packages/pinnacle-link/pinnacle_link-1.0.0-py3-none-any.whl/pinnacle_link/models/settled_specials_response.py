from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .settled_specials_league import SettledSpecialsLeague



@JsonMap({"sport_id": "sportId"})
class SettledSpecialsResponse(BaseModel):
    """Response dto for SettledSpecials request

:param sport_id: Id of a sport for which to retrieve the odds., defaults to None
:type sport_id: int, optional
:param last: Last index for the settled fixture, defaults to None
:type last: int, optional
:param leagues: List of Leagues., defaults to None
:type leagues: List[SettledSpecialsLeague], optional
"""
    def __init__(self, sport_id: int = None, last: int = None, leagues: List[SettledSpecialsLeague] = None):
        if sport_id is not None:
            self.sport_id = sport_id
        if last is not None:
            self.last = last
        if leagues is not None:
            self.leagues = self._define_list(leagues, SettledSpecialsLeague)



