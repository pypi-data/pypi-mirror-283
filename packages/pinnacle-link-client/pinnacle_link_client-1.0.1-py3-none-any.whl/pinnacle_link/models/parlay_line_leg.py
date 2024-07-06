from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel

class ParlayLineLegStatus(Enum):
    """An enumeration representing different categories.

:cvar VALID: "VALID"
:vartype VALID: str
:cvar PROCESSED_WITH_ERROR: "PROCESSED_WITH_ERROR"
:vartype PROCESSED_WITH_ERROR: str
"""
    VALID = "VALID"
    PROCESSED_WITH_ERROR = "PROCESSED_WITH_ERROR"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ParlayLineLegStatus._member_map_.values()))


class ParlayLineLegErrorCode(Enum):
    """An enumeration representing different categories.

:cvar CORRELATED: "CORRELATED"
:vartype CORRELATED: str
:cvar CANNOT_PARLAY_LIVE_GAME: "CANNOT_PARLAY_LIVE_GAME"
:vartype CANNOT_PARLAY_LIVE_GAME: str
:cvar EVENT_NO_LONGER_AVAILABLE_FOR_BETTING: "EVENT_NO_LONGER_AVAILABLE_FOR_BETTING"
:vartype EVENT_NO_LONGER_AVAILABLE_FOR_BETTING: str
:cvar EVENT_NOT_OFFERED_FOR_PARLAY: "EVENT_NOT_OFFERED_FOR_PARLAY"
:vartype EVENT_NOT_OFFERED_FOR_PARLAY: str
:cvar LINE_DOES_NOT_BELONG_TO_EVENT: "LINE_DOES_NOT_BELONG_TO_EVENT"
:vartype LINE_DOES_NOT_BELONG_TO_EVENT: str
:cvar WAGER_TYPE_NO_LONGER_AVAILABLE_FOR_BETTING: "WAGER_TYPE_NO_LONGER_AVAILABLE_FOR_BETTING"
:vartype WAGER_TYPE_NO_LONGER_AVAILABLE_FOR_BETTING: str
:cvar WAGER_TYPE_NOT_VALID_FOR_PARLAY: "WAGER_TYPE_NOT_VALID_FOR_PARLAY"
:vartype WAGER_TYPE_NOT_VALID_FOR_PARLAY: str
:cvar WAGER_TYPE_CONFLICTS_WITH_OTHER_LEG: "WAGER_TYPE_CONFLICTS_WITH_OTHER_LEG"
:vartype WAGER_TYPE_CONFLICTS_WITH_OTHER_LEG: str
:cvar SAME_EVENT_PERIODS_ARE_DISALLOWED: "SAME_EVENT_PERIODS_ARE_DISALLOWED"
:vartype SAME_EVENT_PERIODS_ARE_DISALLOWED: str
"""
    CORRELATED = "CORRELATED"
    CANNOT_PARLAY_LIVE_GAME = "CANNOT_PARLAY_LIVE_GAME"
    EVENT_NO_LONGER_AVAILABLE_FOR_BETTING = "EVENT_NO_LONGER_AVAILABLE_FOR_BETTING"
    EVENT_NOT_OFFERED_FOR_PARLAY = "EVENT_NOT_OFFERED_FOR_PARLAY"
    LINE_DOES_NOT_BELONG_TO_EVENT = "LINE_DOES_NOT_BELONG_TO_EVENT"
    WAGER_TYPE_NO_LONGER_AVAILABLE_FOR_BETTING = "WAGER_TYPE_NO_LONGER_AVAILABLE_FOR_BETTING"
    WAGER_TYPE_NOT_VALID_FOR_PARLAY = "WAGER_TYPE_NOT_VALID_FOR_PARLAY"
    WAGER_TYPE_CONFLICTS_WITH_OTHER_LEG = "WAGER_TYPE_CONFLICTS_WITH_OTHER_LEG"
    SAME_EVENT_PERIODS_ARE_DISALLOWED = "SAME_EVENT_PERIODS_ARE_DISALLOWED"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ParlayLineLegErrorCode._member_map_.values()))




@JsonMap({"error_code": "errorCode","leg_id": "legId","line_id": "lineId","alt_line_id": "altLineId","correlated_legs": "correlatedLegs"})
class ParlayLineLeg(BaseModel):
    """ParlayLineLeg

:param status: Status of the request. [VALID = Valid leg, PROCESSED_WITH_ERROR = Processed with error]
:type status: ParlayLineLegStatus
:param error_code: When Status is PROCESSED_WITH_ERROR, provides a code indicating the specific problem. <br><br>  CORRELATED - The leg is correlated with another one,  <br>  CANNOT_PARLAY_LIVE_GAME - The wager is placed on Live game,   <br>  EVENT_NO_LONGER_AVAILABLE_FOR_BETTING - The event is no longer offered for Parlays,  <br>  EVENT_NOT_OFFERED_FOR_PARLAY - The event is not offered for Parlays,  <br>  LINE_DOES_NOT_BELONG_TO_EVENT - LineId does not match the EventId specified in the request,  <br>  WAGER_TYPE_NO_LONGER_AVAILABLE_FOR_BETTING - Wager Type no longer available for betting, <br>  WAGER_TYPE_NOT_VALID_FOR_PARLAY -  Wager Type not valid for parlay,  <br>  WAGER_TYPE_CONFLICTS_WITH_OTHER_LEG - Wager Type conflicts with other leg<br>  SAME_EVENT_PERIODS_ARE_DISALLOWED - It's not allowed to parlay selected periods of the same event.<br>, defaults to None
:type error_code: ParlayLineLegErrorCode, optional
:param leg_id: Echo of the legId from the request.
:type leg_id: str
:param line_id: Line identification., defaults to None
:type line_id: int, optional
:param alt_line_id: If alternate Line was requested, the Id of that line will be returned., defaults to None
:type alt_line_id: int, optional
:param price: Price, defaults to None
:type price: float, optional
:param correlated_legs: If errorCode is CORRELATED will contain legIds of all correlated legs., defaults to None
:type correlated_legs: List[str], optional
"""
    def __init__(self, status: ParlayLineLegStatus, leg_id: str, error_code: ParlayLineLegErrorCode = None, line_id: int = None, alt_line_id: int = None, price: float = None, correlated_legs: List[str] = None):
        self.status = self._enum_matching(status,ParlayLineLegStatus.list(),"status")
        if error_code is not None:
            self.error_code = self._enum_matching(error_code,ParlayLineLegErrorCode.list(),"error_code")
        self.leg_id = leg_id
        if line_id is not None:
            self.line_id = line_id
        if alt_line_id is not None:
            self.alt_line_id = alt_line_id
        if price is not None:
            self.price = price
        if correlated_legs is not None:
            self.correlated_legs = correlated_legs



