from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({})
class OddsMoneyline(BaseModel):
    """OddsMoneyline

:param home: Away team price, defaults to None
:type home: float, optional
:param away: Away team price., defaults to None
:type away: float, optional
:param draw: Draw price. This is present only for events we offer price for draw., defaults to None
:type draw: float, optional
"""
    def __init__(self, home: float = None, away: float = None, draw: float = None):
        if home is not None:
            self.home = home
        if away is not None:
            self.away = away
        if draw is not None:
            self.draw = draw



