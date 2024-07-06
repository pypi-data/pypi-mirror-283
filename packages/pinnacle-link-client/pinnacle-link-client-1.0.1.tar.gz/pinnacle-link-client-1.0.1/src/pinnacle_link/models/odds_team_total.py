from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({})
class OddsTeamTotal(BaseModel):
    """OddsTeamTotal

:param points: Total points., defaults to None
:type points: float, optional
:param over: Over price., defaults to None
:type over: float, optional
:param under: Under price., defaults to None
:type under: float, optional
"""
    def __init__(self, points: float = None, over: float = None, under: float = None):
        if points is not None:
            self.points = points
        if over is not None:
            self.over = over
        if under is not None:
            self.under = under



