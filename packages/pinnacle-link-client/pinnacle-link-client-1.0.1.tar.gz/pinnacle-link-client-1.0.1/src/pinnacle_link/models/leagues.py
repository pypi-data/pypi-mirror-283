from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .league import League



@JsonMap({})
class Leagues(BaseModel):
    """Leagues

:param leagues: Leagues container, defaults to None
:type leagues: List[League], optional
"""
    def __init__(self, leagues: List[League] = None):
        if leagues is not None:
            self.leagues = self._define_list(leagues, League)



