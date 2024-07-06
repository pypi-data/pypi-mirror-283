from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .odds_league import OddsLeague



@JsonMap({"sport_id": "sportId"})
class OddsResponse(BaseModel):
    """OddsResponse

:param sport_id: Same as requested sport Id., defaults to None
:type sport_id: int, optional
:param last: Use this value for the subsequent requests for since query parameter to get just the changes since previous response., defaults to None
:type last: int, optional
:param leagues: Contains a list of Leagues., defaults to None
:type leagues: List[OddsLeague], optional
"""
    def __init__(self, sport_id: int = None, last: int = None, leagues: List[OddsLeague] = None):
        if sport_id is not None:
            self.sport_id = sport_id
        if last is not None:
            self.last = last
        if leagues is not None:
            self.leagues = self._define_list(leagues, OddsLeague)



