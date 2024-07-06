from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .teaser_line_request import TeaserLineRequest

class LinesRequestTeaserOddsFormat(Enum):
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
        return list(map(lambda x: x.value, LinesRequestTeaserOddsFormat._member_map_.values()))




@JsonMap({"teaser_id": "teaserId","odds_format": "oddsFormat"})
class LinesRequestTeaser(BaseModel):
    """LinesRequestTeaser

:param teaser_id: Unique identifier. Teaser details can be retrieved from a call to v1/teaser/groups endpoint.
:type teaser_id: int
:param odds_format: Format the odds are returned in.. = [American, Decimal, HongKong, Indonesian, Malay]
:type odds_format: LinesRequestTeaserOddsFormat
:param legs: Collection of Teaser Legs.
:type legs: List[TeaserLineRequest]
"""
    def __init__(self, teaser_id: int, odds_format: LinesRequestTeaserOddsFormat, legs: List[TeaserLineRequest]):
        self.teaser_id = teaser_id
        self.odds_format = self._enum_matching(odds_format,LinesRequestTeaserOddsFormat.list(),"odds_format")
        self.legs = self._define_list(legs, TeaserLineRequest)



