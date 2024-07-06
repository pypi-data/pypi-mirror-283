from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .teaser_groups_payout import TeaserGroupsPayout
from .teaser_groups_league import TeaserGroupsLeague



@JsonMap({"id_": "id","sport_id": "sportId","min_legs": "minLegs","max_legs": "maxLegs","same_event_only": "sameEventOnly"})
class TeaserGroupsTeaser(BaseModel):
    """TeaserGroupsTeaser

:param id_: Unique identifier., defaults to None
:type id_: int, optional
:param description: Description for the Teaser., defaults to None
:type description: str, optional
:param sport_id: Unique Sport identifier. Sport details can be retrieved from a call to v2/sports endpoint., defaults to None
:type sport_id: int, optional
:param min_legs: Minimum number of legs that must be selected., defaults to None
:type min_legs: int, optional
:param max_legs: Maximum number of legs that can be selected., defaults to None
:type max_legs: int, optional
:param same_event_only: If 'true' then all legs must be from the same event, otherwise legs can be from different events., defaults to None
:type same_event_only: bool, optional
:param payouts: A collection of Payout indicating all possible payout combinations., defaults to None
:type payouts: List[TeaserGroupsPayout], optional
:param leagues: A collection of Leagues available to the teaser., defaults to None
:type leagues: List[TeaserGroupsLeague], optional
"""
    def __init__(self, id_: int = None, description: str = None, sport_id: int = None, min_legs: int = None, max_legs: int = None, same_event_only: bool = None, payouts: List[TeaserGroupsPayout] = None, leagues: List[TeaserGroupsLeague] = None):
        if id_ is not None:
            self.id_ = id_
        if description is not None:
            self.description = description
        if sport_id is not None:
            self.sport_id = sport_id
        if min_legs is not None:
            self.min_legs = min_legs
        if max_legs is not None:
            self.max_legs = max_legs
        if same_event_only is not None:
            self.same_event_only = same_event_only
        if payouts is not None:
            self.payouts = self._define_list(payouts, TeaserGroupsPayout)
        if leagues is not None:
            self.leagues = self._define_list(leagues, TeaserGroupsLeague)



