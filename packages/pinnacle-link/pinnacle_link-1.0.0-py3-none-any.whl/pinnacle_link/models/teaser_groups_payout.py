from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({"number_of_legs": "numberOfLegs"})
class TeaserGroupsPayout(BaseModel):
    """TeaserGroupsPayout

:param number_of_legs: Number of legs that must be bet and won to get the associated price., defaults to None
:type number_of_legs: int, optional
:param price: Price of the bet given the specified number of legs., defaults to None
:type price: float, optional
"""
    def __init__(self, number_of_legs: int = None, price: float = None):
        if number_of_legs is not None:
            self.number_of_legs = number_of_legs
        if price is not None:
            self.price = price



