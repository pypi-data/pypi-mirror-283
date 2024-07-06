from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .odds_spread import OddsSpread
from .odds_moneyline import OddsMoneyline
from .odds_total import OddsTotal
from .odds_team_totals import OddsTeamTotals



@JsonMap({"line_id": "lineId","max_spread": "maxSpread","max_moneyline": "maxMoneyline","max_total": "maxTotal","max_team_total": "maxTeamTotal","moneyline_updated_at": "moneylineUpdatedAt","spread_updated_at": "spreadUpdatedAt","total_updated_at": "totalUpdatedAt","team_total_updated_at": "teamTotalUpdatedAt","team_total": "teamTotal","away_score": "awayScore","home_score": "homeScore","away_red_cards": "awayRedCards","home_red_cards": "homeRedCards"})
class OddsPeriod(BaseModel):
    """OddsPeriod

:param line_id: Line Id., defaults to None
:type line_id: int, optional
:param number: This represents the period of the match., defaults to None
:type number: int, optional
:param cutoff: Period’s wagering cut-off date in UTC., defaults to None
:type cutoff: str, optional
:param status: 1 - online, period is open for betting <br>2 - offline, period is not open for betting<br>, defaults to None
:type status: int, optional
:param max_spread: Maximum spread bet volume. See [How to calculate max risk from the max volume](https://github.com/pinnacleapi/pinnacleapi-documentation/blob/master/FAQ.md#how-to-calculate-max-risk-from-the-max-volume-limits-in-odds), defaults to None
:type max_spread: float, optional
:param max_moneyline: Maximum moneyline bet volume. See [How to calculate max risk from the max volume](https://github.com/pinnacleapi/pinnacleapi-documentation/blob/master/FAQ.md#how-to-calculate-max-risk-from-the-max-volume-limits-in-odds), defaults to None
:type max_moneyline: float, optional
:param max_total: Maximum total points bet volume. See [How to calculate max risk from the max volume](https://github.com/pinnacleapi/pinnacleapi-documentation/blob/master/FAQ.md#how-to-calculate-max-risk-from-the-max-volume-limits-in-odds), defaults to None
:type max_total: float, optional
:param max_team_total: Maximum team total points bet volume. See [How to calculate max risk from the max volume](https://github.com/pinnacleapi/pinnacleapi-documentation/blob/master/FAQ.md#how-to-calculate-max-risk-from-the-max-volume-limits-in-odds), defaults to None
:type max_team_total: float, optional
:param moneyline_updated_at: Date time of the last moneyline update., defaults to None
:type moneyline_updated_at: str, optional
:param spread_updated_at: Date time of the last spread update., defaults to None
:type spread_updated_at: str, optional
:param total_updated_at: Date time of the last total update., defaults to None
:type total_updated_at: str, optional
:param team_total_updated_at: Date time of the last team total update., defaults to None
:type team_total_updated_at: str, optional
:param spreads: Container for spread odds., defaults to None
:type spreads: List[OddsSpread], optional
:param moneyline: moneyline, defaults to None
:type moneyline: OddsMoneyline, optional
:param totals: Container for team total points., defaults to None
:type totals: List[OddsTotal], optional
:param team_total: team_total, defaults to None
:type team_total: OddsTeamTotals, optional
:param away_score: Period away team score. Only for live soccer events. Supported only for Match (number=0) and Extra Time (number=3)., defaults to None
:type away_score: float, optional
:param home_score: Period home team score. Only for live soccer events. Supported only for Match (number=0) and Extra Time (number=3)., defaults to None
:type home_score: float, optional
:param away_red_cards: Period away team red cards. Only for live soccer events. Supported only for  Match (number=0) and Extra Time (number=3)., defaults to None
:type away_red_cards: int, optional
:param home_red_cards: Period home team red cards. Only for live soccer events. Supported only for Match (number=0) and Extra Time number=3)., defaults to None
:type home_red_cards: int, optional
"""
    def __init__(self, line_id: int = None, number: int = None, cutoff: str = None, status: int = None, max_spread: float = None, max_moneyline: float = None, max_total: float = None, max_team_total: float = None, moneyline_updated_at: str = None, spread_updated_at: str = None, total_updated_at: str = None, team_total_updated_at: str = None, spreads: List[OddsSpread] = None, moneyline: OddsMoneyline = None, totals: List[OddsTotal] = None, team_total: OddsTeamTotals = None, away_score: float = None, home_score: float = None, away_red_cards: int = None, home_red_cards: int = None):
        if line_id is not None:
            self.line_id = line_id
        if number is not None:
            self.number = number
        if cutoff is not None:
            self.cutoff = cutoff
        if status is not None:
            self.status = status
        if max_spread is not None:
            self.max_spread = max_spread
        if max_moneyline is not None:
            self.max_moneyline = max_moneyline
        if max_total is not None:
            self.max_total = max_total
        if max_team_total is not None:
            self.max_team_total = max_team_total
        if moneyline_updated_at is not None:
            self.moneyline_updated_at = moneyline_updated_at
        if spread_updated_at is not None:
            self.spread_updated_at = spread_updated_at
        if total_updated_at is not None:
            self.total_updated_at = total_updated_at
        if team_total_updated_at is not None:
            self.team_total_updated_at = team_total_updated_at
        if spreads is not None:
            self.spreads = self._define_list(spreads, OddsSpread)
        if moneyline is not None:
            self.moneyline = self._define_object(moneyline, OddsMoneyline)
        if totals is not None:
            self.totals = self._define_list(totals, OddsTotal)
        if team_total is not None:
            self.team_total = self._define_object(team_total, OddsTeamTotals)
        if away_score is not None:
            self.away_score = away_score
        if home_score is not None:
            self.home_score = home_score
        if away_red_cards is not None:
            self.away_red_cards = away_red_cards
        if home_red_cards is not None:
            self.home_red_cards = home_red_cards



