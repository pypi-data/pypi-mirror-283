from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .special_odds_league import SpecialOddsLeague



@JsonMap({"sport_id": "sportId"})
class SpecialOddsResponse(BaseModel):
    """SpecialOddsResponse

:param sport_id: Id of a sport for which to retrieve the odds., defaults to None
:type sport_id: int, optional
:param last: Used for retrieving changes only on subsequent requests. Provide this value as the Since paramter in subsequent calls to only retrieve changes., defaults to None
:type last: int, optional
:param leagues: Contains a list of Leagues., defaults to None
:type leagues: List[SpecialOddsLeague], optional
"""
    def __init__(self, sport_id: int = None, last: int = None, leagues: List[SpecialOddsLeague] = None):
        if sport_id is not None:
            self.sport_id = sport_id
        if last is not None:
            self.last = last
        if leagues is not None:
            self.leagues = self._define_list(leagues, SpecialOddsLeague)



