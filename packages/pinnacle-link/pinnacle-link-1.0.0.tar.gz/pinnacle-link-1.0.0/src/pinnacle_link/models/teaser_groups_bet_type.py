from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({})
class TeaserGroupsBetType(BaseModel):
    """TeaserGroupsBetType

:param points: Number of points the line will be teased for the given league., defaults to None
:type points: float, optional
"""
    def __init__(self, points: float = None):
        if points is not None:
            self.points = points



