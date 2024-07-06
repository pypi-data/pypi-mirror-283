from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .in_running_sport import InRunningSport



@JsonMap({})
class InRunningResponse(BaseModel):
    """InRunningResponse

:param sports: Sports container, defaults to None
:type sports: List[InRunningSport], optional
"""
    def __init__(self, sports: List[InRunningSport] = None):
        if sports is not None:
            self.sports = self._define_list(sports, InRunningSport)



