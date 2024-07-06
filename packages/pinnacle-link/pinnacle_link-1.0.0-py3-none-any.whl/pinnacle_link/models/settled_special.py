from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .cancellation_reason import CancellationReason
from .settled_contestants import SettledContestants



@JsonMap({"id_": "id","settlement_id": "settlementId","settled_at": "settledAt","cancellation_reason": "cancellationReason"})
class SettledSpecial(BaseModel):
    """Settled Special

:param id_: Id for the Settled Special, defaults to None
:type id_: int, optional
:param status: Status of the settled special., defaults to None
:type status: int, optional
:param settlement_id: Id for the Settled Special, defaults to None
:type settlement_id: int, optional
:param settled_at: Settled DateTime, defaults to None
:type settled_at: str, optional
:param cancellation_reason: Cancellation Data, defaults to None
:type cancellation_reason: CancellationReason, optional
:param contestants: A collection of contestants, defaults to None
:type contestants: List[SettledContestants], optional
"""
    def __init__(self, id_: int = None, status: int = None, settlement_id: int = None, settled_at: str = None, cancellation_reason: CancellationReason = None, contestants: List[SettledContestants] = None):
        if id_ is not None:
            self.id_ = id_
        if status is not None:
            self.status = status
        if settlement_id is not None:
            self.settlement_id = settlement_id
        if settled_at is not None:
            self.settled_at = settled_at
        if cancellation_reason is not None:
            self.cancellation_reason = self._define_object(cancellation_reason, CancellationReason)
        if contestants is not None:
            self.contestants = self._define_list(contestants, SettledContestants)



