from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({})
class CancellationReason(BaseModel):
    """Cancellation Data

:param code: Cancellation code assigned by the server, defaults to None
:type code: str, optional
:param description: Text description for the cancellation reason, defaults to None
:type description: str, optional
"""
    def __init__(self, code: str = None, description: str = None):
        if code is not None:
            self.code = code
        if description is not None:
            self.description = description



