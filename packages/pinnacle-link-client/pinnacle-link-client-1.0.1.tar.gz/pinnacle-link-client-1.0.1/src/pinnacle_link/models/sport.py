from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({"id_": "id","has_offerings": "hasOfferings","league_specials_count": "leagueSpecialsCount","event_specials_count": "eventSpecialsCount","event_count": "eventCount"})
class Sport(BaseModel):
    """Sport

:param id_: Sport Id., defaults to None
:type id_: int, optional
:param name: Sport name., defaults to None
:type name: str, optional
:param has_offerings: Whether the sport currently has events or specials., defaults to None
:type has_offerings: bool, optional
:param league_specials_count: Indicates how many specials are in the given sport., defaults to None
:type league_specials_count: int, optional
:param event_specials_count: Indicates how many event specials are in the given sport., defaults to None
:type event_specials_count: int, optional
:param event_count: Indicates how many events are in the given sport., defaults to None
:type event_count: int, optional
"""
    def __init__(self, id_: int = None, name: str = None, has_offerings: bool = None, league_specials_count: int = None, event_specials_count: int = None, event_count: int = None):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if has_offerings is not None:
            self.has_offerings = has_offerings
        if league_specials_count is not None:
            self.league_specials_count = league_specials_count
        if event_specials_count is not None:
            self.event_specials_count = event_specials_count
        if event_count is not None:
            self.event_count = event_count



