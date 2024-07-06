from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel

class FixtureLiveStatus(Enum):
    """An enumeration representing different categories.

:cvar _0: 0
:vartype _0: str
:cvar _1: 1
:vartype _1: str
:cvar _2: 2
:vartype _2: str
"""
    _0 = 0
    _1 = 1
    _2 = 2

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, FixtureLiveStatus._member_map_.values()))


class FixtureStatus(Enum):
    """An enumeration representing different categories.

:cvar O: "O"
:vartype O: str
:cvar H: "H"
:vartype H: str
:cvar I: "I"
:vartype I: str
"""
    O = "O"
    H = "H"
    I = "I"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, FixtureStatus._member_map_.values()))


class ParlayRestriction(Enum):
    """An enumeration representing different categories.

:cvar _0: 0
:vartype _0: str
:cvar _1: 1
:vartype _1: str
:cvar _2: 2
:vartype _2: str
"""
    _0 = 0
    _1 = 1
    _2 = 2

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ParlayRestriction._member_map_.values()))




@JsonMap({"id_": "id","parent_id": "parentId","rot_num": "rotNum","live_status": "liveStatus","parlay_restriction": "parlayRestriction","alt_teaser": "altTeaser","resulting_unit": "resultingUnit","same_event_parlay_periods_enabled": "sameEventParlayPeriodsEnabled"})
class Fixture(BaseModel):
    """Fixture

:param id_: Event id., defaults to None
:type id_: int, optional
:param parent_id: If event is linked to another event, parentId will be populated.  Live event would have pre game event as parent id., defaults to None
:type parent_id: int, optional
:param starts: Start time of the event in UTC., defaults to None
:type starts: str, optional
:param home: Home team name., defaults to None
:type home: str, optional
:param away: Away team name., defaults to None
:type away: str, optional
:param rot_num: Team1 rotation number. Please note that in the next version of /fixtures, rotNum property will be decommissioned. ParentId can be used instead to group the related events., defaults to None
:type rot_num: str, optional
:param live_status: Indicates live status of the event. <br><br>0 = No live betting will be offered on this event, <br>1 = Live betting event, <br>2 = Live betting will be offered on this match, but on a different event. Please note that [pre-game and live events are different](https://github.com/pinnacleapi/pinnacleapi-documentation/blob/master/FAQ.md#how-to-find-associated-events) .<br>, defaults to None
:type live_status: FixtureLiveStatus, optional
:param status: This is deprecated parameter, please check period's `status` in the<br>`/odds` endpoint to see if it's open for betting.<br><br><br>O = This is the starting status of a game.  <br><br>H = This status indicates that the lines are temporarily unavailable<br>for betting, <br><br>I = This status indicates that one or more lines have a red circle<br>(lower maximum bet amount).<br>, defaults to None
:type status: FixtureStatus, optional
:param parlay_restriction: <br>Parlay status of the event. <br><br>0 = Allowed to parlay, without restrictions, <br>1 = Not allowed to parlay this event, <br>2 = Allowed to parlay with the restrictions. You cannot have more than one leg from the same event in the parlay. All events with the same rotation number are treated as same event.<br>, defaults to None
:type parlay_restriction: ParlayRestriction, optional
:param alt_teaser: Whether an event is offer with alternative teaser points. Events with alternative teaser points may vary from teaser definition., defaults to None
:type alt_teaser: bool, optional
:param resulting_unit: Specifies based on what the event will be resulted, e.g. Corners, Bookings <br>, defaults to None
:type resulting_unit: str, optional
:param version: Fixture version, goes up when there is a change in the fixture. <br>, defaults to None
:type version: float, optional
:param same_event_parlay_periods_enabled: Contains a list of period numbers that are allowed to be parlayed together., defaults to None
:type same_event_parlay_periods_enabled: List[int], optional
"""
    def __init__(self, id_: int = None, parent_id: int = None, starts: str = None, home: str = None, away: str = None, rot_num: str = None, live_status: FixtureLiveStatus = None, status: FixtureStatus = None, parlay_restriction: ParlayRestriction = None, alt_teaser: bool = None, resulting_unit: str = None, version: float = None, same_event_parlay_periods_enabled: List[int] = None):
        if id_ is not None:
            self.id_ = id_
        if parent_id is not None:
            self.parent_id = parent_id
        if starts is not None:
            self.starts = starts
        if home is not None:
            self.home = home
        if away is not None:
            self.away = away
        if rot_num is not None:
            self.rot_num = rot_num
        if live_status is not None:
            self.live_status = self._enum_matching(live_status,FixtureLiveStatus.list(),"live_status")
        if status is not None:
            self.status = self._enum_matching(status,FixtureStatus.list(),"status")
        if parlay_restriction is not None:
            self.parlay_restriction = self._enum_matching(parlay_restriction,ParlayRestriction.list(),"parlay_restriction")
        if alt_teaser is not None:
            self.alt_teaser = alt_teaser
        if resulting_unit is not None:
            self.resulting_unit = resulting_unit
        if version is not None:
            self.version = version
        if same_event_parlay_periods_enabled is not None:
            self.same_event_parlay_periods_enabled = same_event_parlay_periods_enabled



