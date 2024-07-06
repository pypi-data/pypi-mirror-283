from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({"alt_line_id": "altLineId"})
class OddsTotal(BaseModel):
    """OddsTotal

:param alt_line_id: This is present only if it’s alternative line., defaults to None
:type alt_line_id: int, optional
:param points: Total points., defaults to None
:type points: float, optional
:param over: Over price., defaults to None
:type over: float, optional
:param under: Under price., defaults to None
:type under: float, optional
:param max: Maximum bet volume. Present only on alternative lines, if set it overides `maxTotal` market limit., defaults to None
:type max: float, optional
"""
    def __init__(self, alt_line_id: int = None, points: float = None, over: float = None, under: float = None, max: float = None):
        if alt_line_id is not None:
            self.alt_line_id = alt_line_id
        if points is not None:
            self.points = points
        if over is not None:
            self.over = over
        if under is not None:
            self.under = under
        if max is not None:
            self.max = max



