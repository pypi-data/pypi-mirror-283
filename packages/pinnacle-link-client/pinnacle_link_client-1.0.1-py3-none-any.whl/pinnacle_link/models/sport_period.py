from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({"short_description": "shortDescription","spread_description": "spreadDescription","moneyline_description": "moneylineDescription","total_description": "totalDescription","team1_total_description": "team1TotalDescription","team2_total_description": "team2TotalDescription","spread_short_description": "spreadShortDescription","moneyline_short_description": "moneylineShortDescription","total_short_description": "totalShortDescription","team1_total_short_description": "team1TotalShortDescription","team2_total_short_description": "team2TotalShortDescription"})
class SportPeriod(BaseModel):
    """SportPeriod

:param number: Period Number, defaults to None
:type number: int, optional
:param description: Description for the period, defaults to None
:type description: str, optional
:param short_description: Short description for the period, defaults to None
:type short_description: str, optional
:param spread_description: Description for the Spread, defaults to None
:type spread_description: str, optional
:param moneyline_description: Description for the Moneyline, defaults to None
:type moneyline_description: str, optional
:param total_description: Description for the Totals, defaults to None
:type total_description: str, optional
:param team1_total_description: Description for Team1 Totals, defaults to None
:type team1_total_description: str, optional
:param team2_total_description: Description for Team2 Totals, defaults to None
:type team2_total_description: str, optional
:param spread_short_description: Short description for the Spread, defaults to None
:type spread_short_description: str, optional
:param moneyline_short_description: Short description for the Moneyline, defaults to None
:type moneyline_short_description: str, optional
:param total_short_description: Short description for the Totals, defaults to None
:type total_short_description: str, optional
:param team1_total_short_description: Short description for Team1 Totals, defaults to None
:type team1_total_short_description: str, optional
:param team2_total_short_description: Short description for Team2 Totals, defaults to None
:type team2_total_short_description: str, optional
"""
    def __init__(self, number: int = None, description: str = None, short_description: str = None, spread_description: str = None, moneyline_description: str = None, total_description: str = None, team1_total_description: str = None, team2_total_description: str = None, spread_short_description: str = None, moneyline_short_description: str = None, total_short_description: str = None, team1_total_short_description: str = None, team2_total_short_description: str = None):
        if number is not None:
            self.number = number
        if description is not None:
            self.description = description
        if short_description is not None:
            self.short_description = short_description
        if spread_description is not None:
            self.spread_description = spread_description
        if moneyline_description is not None:
            self.moneyline_description = moneyline_description
        if total_description is not None:
            self.total_description = total_description
        if team1_total_description is not None:
            self.team1_total_description = team1_total_description
        if team2_total_description is not None:
            self.team2_total_description = team2_total_description
        if spread_short_description is not None:
            self.spread_short_description = spread_short_description
        if moneyline_short_description is not None:
            self.moneyline_short_description = moneyline_short_description
        if total_short_description is not None:
            self.total_short_description = total_short_description
        if team1_total_short_description is not None:
            self.team1_total_short_description = team1_total_short_description
        if team2_total_short_description is not None:
            self.team2_total_short_description = team2_total_short_description



