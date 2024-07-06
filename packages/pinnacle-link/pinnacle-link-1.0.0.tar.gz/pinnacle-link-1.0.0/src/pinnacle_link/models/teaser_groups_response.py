from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .teaser_groups import TeaserGroups



@JsonMap({"teaser_groups": "teaserGroups"})
class TeaserGroupsResponse(BaseModel):
    """TeaserGroupsResponse

:param teaser_groups: A collection of TeaserGroups containing available teasers., defaults to None
:type teaser_groups: List[TeaserGroups], optional
"""
    def __init__(self, teaser_groups: List[TeaserGroups] = None):
        if teaser_groups is not None:
            self.teaser_groups = self._define_list(teaser_groups, TeaserGroups)



