from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .teaser_odds_league import TeaserOddsLeague



@JsonMap({"teaser_id": "teaserId","sport_id": "sportId"})
class TeaserOddsResponse(BaseModel):
    """TeaserOddsResponse

:param teaser_id: Unique identifier. Teaser details can be retrieved from a call to Get Teaser Groups endpoint., defaults to None
:type teaser_id: int, optional
:param sport_id: Unique identifier. Sport details can be retrieved from a call to Get Sports endpoint., defaults to None
:type sport_id: int, optional
:param leagues: A collection of League., defaults to None
:type leagues: List[TeaserOddsLeague], optional
"""
    def __init__(self, teaser_id: int = None, sport_id: int = None, leagues: List[TeaserOddsLeague] = None):
        if teaser_id is not None:
            self.teaser_id = teaser_id
        if sport_id is not None:
            self.sport_id = sport_id
        if leagues is not None:
            self.leagues = self._define_list(leagues, TeaserOddsLeague)



