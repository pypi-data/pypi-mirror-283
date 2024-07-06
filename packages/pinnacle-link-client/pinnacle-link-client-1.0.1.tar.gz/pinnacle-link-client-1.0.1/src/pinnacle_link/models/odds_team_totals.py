from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .odds_team_total import OddsTeamTotal



@JsonMap({})
class OddsTeamTotals(BaseModel):
    """OddsTeamTotals

:param home: home, defaults to None
:type home: OddsTeamTotal, optional
:param away: away, defaults to None
:type away: OddsTeamTotal, optional
"""
    def __init__(self, home: OddsTeamTotal = None, away: OddsTeamTotal = None):
        if home is not None:
            self.home = self._define_object(home, OddsTeamTotal)
        if away is not None:
            self.away = self._define_object(away, OddsTeamTotal)



