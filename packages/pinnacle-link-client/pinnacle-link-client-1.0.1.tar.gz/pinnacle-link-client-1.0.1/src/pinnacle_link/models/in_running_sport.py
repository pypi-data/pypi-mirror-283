from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .in_running_league import InRunningLeague



@JsonMap({"id_": "id"})
class InRunningSport(BaseModel):
    """InRunningSport

:param id_: Sport Id, defaults to None
:type id_: int, optional
:param leagues: Leagues container, defaults to None
:type leagues: List[InRunningLeague], optional
"""
    def __init__(self, id_: int = None, leagues: List[InRunningLeague] = None):
        if id_ is not None:
            self.id_ = id_
        if leagues is not None:
            self.leagues = self._define_list(leagues, InRunningLeague)



