from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .parlay_line_request import ParlayLineRequest

class ParlayLinesRequestOddsFormat(Enum):
    """An enumeration representing different categories.

:cvar AMERICAN: "American"
:vartype AMERICAN: str
:cvar DECIMAL: "Decimal"
:vartype DECIMAL: str
:cvar HONGKONG: "HongKong"
:vartype HONGKONG: str
:cvar INDONESIAN: "Indonesian"
:vartype INDONESIAN: str
:cvar MALAY: "Malay"
:vartype MALAY: str
"""
    AMERICAN = "American"
    DECIMAL = "Decimal"
    HONGKONG = "HongKong"
    INDONESIAN = "Indonesian"
    MALAY = "Malay"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ParlayLinesRequestOddsFormat._member_map_.values()))




@JsonMap({"odds_format": "oddsFormat"})
class ParlayLinesRequest(BaseModel):
    """ParlayLinesRequest

:param odds_format: Odds in the response will be in this format. [American, Decimal, HongKong, Indonesian, Malay], defaults to None
:type odds_format: ParlayLinesRequestOddsFormat, optional
:param legs: This is a collection of legs, defaults to None
:type legs: List[ParlayLineRequest], optional
"""
    def __init__(self, odds_format: ParlayLinesRequestOddsFormat = None, legs: List[ParlayLineRequest] = None):
        if odds_format is not None:
            self.odds_format = self._enum_matching(odds_format,ParlayLinesRequestOddsFormat.list(),"odds_format")
        if legs is not None:
            self.legs = self._define_list(legs, ParlayLineRequest)



