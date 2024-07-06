from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .teaser_groups_bet_type import TeaserGroupsBetType



@JsonMap({"id_": "id"})
class TeaserGroupsLeague(BaseModel):
    """TeaserGroupsLeague

:param id_: Unique identifier. League details can be retrieved from a call to v2/leagues endpoint., defaults to None
:type id_: int, optional
:param spread: spread, defaults to None
:type spread: TeaserGroupsBetType, optional
:param total: total, defaults to None
:type total: TeaserGroupsBetType, optional
"""
    def __init__(self, id_: int = None, spread: TeaserGroupsBetType = None, total: TeaserGroupsBetType = None):
        if id_ is not None:
            self.id_ = id_
        if spread is not None:
            self.spread = self._define_object(spread, TeaserGroupsBetType)
        if total is not None:
            self.total = self._define_object(total, TeaserGroupsBetType)



