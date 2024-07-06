from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel

class TeaserLineLegStatus(Enum):
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
        return list(map(lambda x: x.value, TeaserLineLegStatus._member_map_.values()))


class TeaserLineLegErrorCode(Enum):
    """An enumeration representing different categories.

:cvar EVENT_NOT_FOUND: "EVENT_NOT_FOUND"
:vartype EVENT_NOT_FOUND: str
:cvar POINTS_NO_LONGER_AVAILABLE: "POINTS_NO_LONGER_AVAILABLE"
:vartype POINTS_NO_LONGER_AVAILABLE: str
:cvar UNKNOWN: "UNKNOWN"
:vartype UNKNOWN: str
:cvar WAGER_TYPE_NOT_VALID_FOR_TEASER: "WAGER_TYPE_NOT_VALID_FOR_TEASER"
:vartype WAGER_TYPE_NOT_VALID_FOR_TEASER: str
:cvar GAME_TEASER_DISABLED: "GAME_TEASER_DISABLED"
:vartype GAME_TEASER_DISABLED: str
"""
    EVENT_NOT_FOUND = "EVENT_NOT_FOUND"
    POINTS_NO_LONGER_AVAILABLE = "POINTS_NO_LONGER_AVAILABLE"
    UNKNOWN = "UNKNOWN"
    WAGER_TYPE_NOT_VALID_FOR_TEASER = "WAGER_TYPE_NOT_VALID_FOR_TEASER"
    GAME_TEASER_DISABLED = "GAME_TEASER_DISABLED"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, TeaserLineLegErrorCode._member_map_.values()))




@JsonMap({"error_code": "errorCode","leg_id": "legId","line_id": "lineId"})
class TeaserLineLeg(BaseModel):
    """TeaserLineLeg

:param status: Status of the request. [VALID = Teaser is valid, PROCESSED_WITH_ERROR = Teaser contains error(s)]
:type status: TeaserLineLegStatus
:param error_code: When Status is PROCESSED_WITH_ERROR, provides a code indicating the specific problem.  <br>  <br>  EVENT_NOT_FOUND - The event specified could not be found,  <br>  POINTS_NO_LONGER_AVAILABLE - The points requested are no longer available. This means that the lines moved,   <br>  UNKNOWN - An unknown error has occured,  <br>  WAGER_TYPE_NOT_VALID_FOR_TEASER - The specified wager type is not valid for teasers  <br>  GAME_TEASER_DISABLED - Teasers are disabled for the event.<br>, defaults to None
:type error_code: TeaserLineLegErrorCode, optional
:param leg_id: Echo of the unique id for the leg from the request.
:type leg_id: str
:param line_id: Line identification., defaults to None
:type line_id: int, optional
"""
    def __init__(self, status: TeaserLineLegStatus, leg_id: str, error_code: TeaserLineLegErrorCode = None, line_id: int = None):
        self.status = self._enum_matching(status,TeaserLineLegStatus.list(),"status")
        if error_code is not None:
            self.error_code = self._enum_matching(error_code,TeaserLineLegErrorCode.list(),"error_code")
        self.leg_id = leg_id
        if line_id is not None:
            self.line_id = line_id



