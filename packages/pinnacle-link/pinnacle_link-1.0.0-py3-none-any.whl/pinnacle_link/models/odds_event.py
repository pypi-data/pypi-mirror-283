from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .odds_period import OddsPeriod



@JsonMap({"id_": "id","away_score": "awayScore","home_score": "homeScore","away_red_cards": "awayRedCards","home_red_cards": "homeRedCards"})
class OddsEvent(BaseModel):
    """OddsEvent

:param id_: Event Id., defaults to None
:type id_: int, optional
:param away_score: Away team score. Only for live soccer events.Supported only for full match period (number=0)., defaults to None
:type away_score: float, optional
:param home_score: Home team score. Only for live soccer events.Supported only for full match period (number=0)., defaults to None
:type home_score: float, optional
:param away_red_cards: Away team red cards. Only for live soccer events. Supported only for full match period (number=0)., defaults to None
:type away_red_cards: int, optional
:param home_red_cards: Home team red cards. Only for live soccer events.Supported only for full match period (number=0)., defaults to None
:type home_red_cards: int, optional
:param periods: Contains a list of periods., defaults to None
:type periods: List[OddsPeriod], optional
"""
    def __init__(self, id_: int = None, away_score: float = None, home_score: float = None, away_red_cards: int = None, home_red_cards: int = None, periods: List[OddsPeriod] = None):
        if id_ is not None:
            self.id_ = id_
        if away_score is not None:
            self.away_score = away_score
        if home_score is not None:
            self.home_score = home_score
        if away_red_cards is not None:
            self.away_red_cards = away_red_cards
        if home_red_cards is not None:
            self.home_red_cards = home_red_cards
        if periods is not None:
            self.periods = self._define_list(periods, OddsPeriod)



