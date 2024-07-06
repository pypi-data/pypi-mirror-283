from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({"id_": "id","line_id": "lineId"})
class SpecialOddsContestantLine(BaseModel):
    """SpecialOddsContestantLine

:param id_: ContestantLine Id., defaults to None
:type id_: int, optional
:param line_id: Line identifier required for placing a bet., defaults to None
:type line_id: int, optional
:param price: Price of the line., defaults to None
:type price: float, optional
:param handicap: A number indicating the spread, over/under etc., defaults to None
:type handicap: float, optional
:param max: Maximum bet volume amount per contestant. See [How to calculate max risk from the max volume](https://github.com/pinnacleapi/pinnacleapi-documentation/blob/master/FAQ.md#how-to-calculate-max-risk-from-the-max-volume-limits-in-odds), defaults to None
:type max: any, optional
"""
    def __init__(self, id_: int = None, line_id: int = None, price: float = None, handicap: float = None, max: any = None):
        if id_ is not None:
            self.id_ = id_
        if line_id is not None:
            self.line_id = line_id
        if price is not None:
            self.price = price
        if handicap is not None:
            self.handicap = handicap
        if max is not None:
            self.max = max



