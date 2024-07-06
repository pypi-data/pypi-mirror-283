from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({"alt_line_id": "altLineId"})
class OddsSpread(BaseModel):
    """OddsSpread

:param alt_line_id: This is present only if it’s alternative line., defaults to None
:type alt_line_id: int, optional
:param hdp: Home team handicap., defaults to None
:type hdp: float, optional
:param home: Home team price., defaults to None
:type home: float, optional
:param away: Away team price., defaults to None
:type away: float, optional
:param max: Maximum bet volume. Present only on alternative lines, if set it overides `maxSpread` market limit., defaults to None
:type max: float, optional
"""
    def __init__(self, alt_line_id: int = None, hdp: float = None, home: float = None, away: float = None, max: float = None):
        if alt_line_id is not None:
            self.alt_line_id = alt_line_id
        if hdp is not None:
            self.hdp = hdp
        if home is not None:
            self.home = home
        if away is not None:
            self.away = away
        if max is not None:
            self.max = max



