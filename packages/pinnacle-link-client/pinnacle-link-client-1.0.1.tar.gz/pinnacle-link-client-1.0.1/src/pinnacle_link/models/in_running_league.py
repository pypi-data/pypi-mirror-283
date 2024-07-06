from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .in_running_event import InRunningEvent



@JsonMap({"id_": "id"})
class InRunningLeague(BaseModel):
    """InRunningLeague

:param id_: League Id, defaults to None
:type id_: int, optional
:param events: Events container, defaults to None
:type events: List[InRunningEvent], optional
"""
    def __init__(self, id_: int = None, events: List[InRunningEvent] = None):
        if id_ is not None:
            self.id_ = id_
        if events is not None:
            self.events = self._define_list(events, InRunningEvent)



