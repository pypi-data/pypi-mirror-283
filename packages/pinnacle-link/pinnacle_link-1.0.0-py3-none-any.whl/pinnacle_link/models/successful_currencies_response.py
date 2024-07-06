from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .currency import Currency



@JsonMap({})
class SuccessfulCurrenciesResponse(BaseModel):
    """SuccessfulCurrenciesResponse

:param currencies: Currencies container., defaults to None
:type currencies: List[Currency], optional
"""
    def __init__(self, currencies: List[Currency] = None):
        if currencies is not None:
            self.currencies = self._define_list(currencies, Currency)



