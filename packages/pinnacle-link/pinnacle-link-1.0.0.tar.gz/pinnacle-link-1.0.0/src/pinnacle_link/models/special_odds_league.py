from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .special_odds_special import SpecialOddsSpecial



@JsonMap({"id_": "id"})
class SpecialOddsLeague(BaseModel):
    """SpecialOddsLeague

:param id_: League id., defaults to None
:type id_: int, optional
:param specials: A collection of FixturesSpecial., defaults to None
:type specials: List[SpecialOddsSpecial], optional
"""
    def __init__(self, id_: int = None, specials: List[SpecialOddsSpecial] = None):
        if id_ is not None:
            self.id_ = id_
        if specials is not None:
            self.specials = self._define_list(specials, SpecialOddsSpecial)



