from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .special_odds_contestant_line import SpecialOddsContestantLine



@JsonMap({"id_": "id","max_bet": "maxBet","contestant_lines": "contestantLines"})
class SpecialOddsSpecial(BaseModel):
    """SpecialOddsSpecial

:param id_: Special Id., defaults to None
:type id_: int, optional
:param max_bet: Maximum bet volume amount. See [How to calculate max risk from the max volume](https://github.com/pinnacleapi/pinnacleapi-documentation/blob/master/FAQ.md#how-to-calculate-max-risk-from-the-max-volume-limits-in-odds), defaults to None
:type max_bet: float, optional
:param contestant_lines: ContestantLines available for wagering on., defaults to None
:type contestant_lines: List[SpecialOddsContestantLine], optional
"""
    def __init__(self, id_: int = None, max_bet: float = None, contestant_lines: List[SpecialOddsContestantLine] = None):
        if id_ is not None:
            self.id_ = id_
        if max_bet is not None:
            self.max_bet = max_bet
        if contestant_lines is not None:
            self.contestant_lines = self._define_list(contestant_lines, SpecialOddsContestantLine)



