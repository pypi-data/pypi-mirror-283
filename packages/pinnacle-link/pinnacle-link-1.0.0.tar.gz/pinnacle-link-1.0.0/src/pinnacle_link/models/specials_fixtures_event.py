from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({"id_": "id","period_number": "periodNumber"})
class SpecialsFixturesEvent(BaseModel):
    """Optional event asscoaited with the special.

:param id_: Event Id, defaults to None
:type id_: int, optional
:param period_number: The period of the match., defaults to None
:type period_number: int, optional
:param home: Home team name., defaults to None
:type home: str, optional
:param away: Away team name., defaults to None
:type away: str, optional
"""
    def __init__(self, id_: int = None, period_number: int = None, home: str = None, away: str = None):
        if id_ is not None:
            self.id_ = id_
        if period_number is not None:
            self.period_number = period_number
        if home is not None:
            self.home = home
        if away is not None:
            self.away = away



