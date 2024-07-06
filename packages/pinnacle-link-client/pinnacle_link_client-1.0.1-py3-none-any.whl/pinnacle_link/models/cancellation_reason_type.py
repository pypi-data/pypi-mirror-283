from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .cancellation_reason_details_type import CancellationReasonDetailsType



@JsonMap({})
class CancellationReasonType(BaseModel):
    """CancellationReasonType

:param code: Cancellation Reason Code, defaults to None
:type code: str, optional
:param details: details, defaults to None
:type details: CancellationReasonDetailsType, optional
"""
    def __init__(self, code: str = None, details: CancellationReasonDetailsType = None):
        if code is not None:
            self.code = code
        if details is not None:
            self.details = self._define_object(details, CancellationReasonDetailsType)



