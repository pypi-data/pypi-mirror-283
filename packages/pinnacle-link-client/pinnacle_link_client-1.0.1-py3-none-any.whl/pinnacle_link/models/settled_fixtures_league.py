from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .settled_fixtures_event import SettledFixturesEvent



@JsonMap({"id_": "id"})
class SettledFixturesLeague(BaseModel):
    """SettledFixturesLeague

:param id_: League Id., defaults to None
:type id_: int, optional
:param events: Contains a list of events., defaults to None
:type events: List[SettledFixturesEvent], optional
"""
    def __init__(self, id_: int = None, events: List[SettledFixturesEvent] = None):
        if id_ is not None:
            self.id_ = id_
        if events is not None:
            self.events = self._define_list(events, SettledFixturesEvent)



