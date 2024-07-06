from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .teaser_odds_spread import TeaserOddsSpread
from .teaser_odds_total_points import TeaserOddsTotalPoints



@JsonMap({"line_id": "lineId","spread_updated_at": "spreadUpdatedAt","total_updated_at": "totalUpdatedAt"})
class TeaserOddsPeriod(BaseModel):
    """TeaserOddsPeriod

:param number: Period of the match that the request is for. Refer to v1/periods endpoint to retrieve all valid periods for a sport., defaults to None
:type number: int, optional
:param line_id: Unique identifier., defaults to None
:type line_id: int, optional
:param spread_updated_at: Date time of the last spread update., defaults to None
:type spread_updated_at: str, optional
:param total_updated_at: Date time of the last total update., defaults to None
:type total_updated_at: str, optional
:param spread: spread, defaults to None
:type spread: TeaserOddsSpread, optional
:param total: total, defaults to None
:type total: TeaserOddsTotalPoints, optional
"""
    def __init__(self, number: int = None, line_id: int = None, spread_updated_at: str = None, total_updated_at: str = None, spread: TeaserOddsSpread = None, total: TeaserOddsTotalPoints = None):
        if number is not None:
            self.number = number
        if line_id is not None:
            self.line_id = line_id
        if spread_updated_at is not None:
            self.spread_updated_at = spread_updated_at
        if total_updated_at is not None:
            self.total_updated_at = total_updated_at
        if spread is not None:
            self.spread = self._define_object(spread, TeaserOddsSpread)
        if total is not None:
            self.total = self._define_object(total, TeaserOddsTotalPoints)



