from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .settled_special import SettledSpecial



@JsonMap({"id_": "id"})
class SettledSpecialsLeague(BaseModel):
    """League Dto to hold all settled specials for the league

:param id_: League Id., defaults to None
:type id_: int, optional
:param specials: A collection of Settled Specials, defaults to None
:type specials: List[SettledSpecial], optional
"""
    def __init__(self, id_: int = None, specials: List[SettledSpecial] = None):
        if id_ is not None:
            self.id_ = id_
        if specials is not None:
            self.specials = self._define_list(specials, SettledSpecial)



