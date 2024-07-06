from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .cancellation_reason import CancellationReason



@JsonMap({"cancellation_reasons": "cancellationReasons"})
class CancellationReasonResponse(BaseModel):
    """Cancellation Response Data

:param cancellation_reasons: Contains a list of Cancellation Reasons., defaults to None
:type cancellation_reasons: List[CancellationReason], optional
"""
    def __init__(self, cancellation_reasons: List[CancellationReason] = None):
        if cancellation_reasons is not None:
            self.cancellation_reasons = self._define_list(cancellation_reasons, CancellationReason)



