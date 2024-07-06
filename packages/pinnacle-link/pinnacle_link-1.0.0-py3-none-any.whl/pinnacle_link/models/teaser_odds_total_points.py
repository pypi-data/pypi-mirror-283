from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({"max_bet": "maxBet","over_points": "overPoints","under_points": "underPoints"})
class TeaserOddsTotalPoints(BaseModel):
    """TeaserOddsTotalPoints

:param max_bet: Maximum bet amount volume. See [How to calculate max risk from the max volume](https://github.com/pinnacleapi/pinnacleapi-documentation/blob/master/FAQ.md#how-to-calculate-max-risk-from-the-max-volume-limits-in-odds), defaults to None
:type max_bet: float, optional
:param over_points: Over points., defaults to None
:type over_points: float, optional
:param under_points: Under points., defaults to None
:type under_points: float, optional
"""
    def __init__(self, max_bet: float = None, over_points: float = None, under_points: float = None):
        if max_bet is not None:
            self.max_bet = max_bet
        if over_points is not None:
            self.over_points = over_points
        if under_points is not None:
            self.under_points = under_points



