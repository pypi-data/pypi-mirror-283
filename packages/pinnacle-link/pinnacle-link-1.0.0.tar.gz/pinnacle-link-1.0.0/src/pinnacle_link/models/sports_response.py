from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .sport import Sport



@JsonMap({})
class SportsResponse(BaseModel):
    """SportsResponse

:param sports: Sports container., defaults to None
:type sports: List[Sport], optional
"""
    def __init__(self, sports: List[Sport] = None):
        if sports is not None:
            self.sports = self._define_list(sports, Sport)



