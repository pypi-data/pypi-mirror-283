from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .teaser_groups_teaser import TeaserGroupsTeaser



@JsonMap({"id_": "id"})
class TeaserGroups(BaseModel):
    """TeaserGroups

:param id_: Unique identifier., defaults to None
:type id_: int, optional
:param name: Friendly name for the Teaser Group, defaults to None
:type name: str, optional
:param teasers: A collection of Teaser., defaults to None
:type teasers: List[TeaserGroupsTeaser], optional
"""
    def __init__(self, id_: int = None, name: str = None, teasers: List[TeaserGroupsTeaser] = None):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if teasers is not None:
            self.teasers = self._define_list(teasers, TeaserGroupsTeaser)



