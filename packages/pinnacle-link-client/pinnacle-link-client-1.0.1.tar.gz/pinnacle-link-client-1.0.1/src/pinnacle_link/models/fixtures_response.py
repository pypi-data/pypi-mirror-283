from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .fixtures_league import FixturesLeague



@JsonMap({"sport_id": "sportId"})
class FixturesResponse(BaseModel):
    """FixturesResponse

:param sport_id: Same as requested sport Id., defaults to None
:type sport_id: int, optional
:param last: Use this value for the subsequent requests for since query parameter to get just the changes since previous response., defaults to None
:type last: int, optional
:param league: Contains a list of Leagues., defaults to None
:type league: List[FixturesLeague], optional
"""
    def __init__(self, sport_id: int = None, last: int = None, league: List[FixturesLeague] = None):
        if sport_id is not None:
            self.sport_id = sport_id
        if last is not None:
            self.last = last
        if league is not None:
            self.league = self._define_list(league, FixturesLeague)



