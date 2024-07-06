from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({"max_bet": "maxBet","home_hdp": "homeHdp","away_hdp": "awayHdp","alt_hdp": "altHdp"})
class TeaserOddsSpread(BaseModel):
    """TeaserOddsSpread

:param max_bet: Maximum bet amount volume. See [How to calculate max risk from the max volume](https://github.com/pinnacleapi/pinnacleapi-documentation/blob/master/FAQ.md#how-to-calculate-max-risk-from-the-max-volume-limits-in-odds), defaults to None
:type max_bet: float, optional
:param home_hdp: Home team handicap. Refer to Get Fixtures endpoint to determine home and away teams., defaults to None
:type home_hdp: float, optional
:param away_hdp: Away team handicap. Refer to Get Fixtures endpoint to determine home and away teams., defaults to None
:type away_hdp: float, optional
:param alt_hdp: Whether the spread is offer with alterantive teaser points. Events with alternative teaser points may vary from teaser definition., defaults to None
:type alt_hdp: bool, optional
"""
    def __init__(self, max_bet: float = None, home_hdp: float = None, away_hdp: float = None, alt_hdp: bool = None):
        if max_bet is not None:
            self.max_bet = max_bet
        if home_hdp is not None:
            self.home_hdp = home_hdp
        if away_hdp is not None:
            self.away_hdp = away_hdp
        if alt_hdp is not None:
            self.alt_hdp = alt_hdp



