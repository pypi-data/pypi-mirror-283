from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({"id_": "id","home_team_type": "homeTeamType","has_offerings": "hasOfferings","allow_round_robins": "allowRoundRobins","league_specials_count": "leagueSpecialsCount","event_specials_count": "eventSpecialsCount","event_count": "eventCount"})
class League(BaseModel):
    """League

:param id_: League Id., defaults to None
:type id_: int, optional
:param name: Name of the league., defaults to None
:type name: str, optional
:param home_team_type: Specifies whether the home team is team1 or team2. You need this information to place a bet., defaults to None
:type home_team_type: str, optional
:param has_offerings: Whether the league currently has events or specials., defaults to None
:type has_offerings: bool, optional
:param container: Represents grouping for the league, usually a region/country, defaults to None
:type container: str, optional
:param allow_round_robins: Specifies whether you can place parlay round robins on events in this league., defaults to None
:type allow_round_robins: bool, optional
:param league_specials_count: Indicates how many specials are in the given league., defaults to None
:type league_specials_count: int, optional
:param event_specials_count: Indicates how many game specials are in the given league., defaults to None
:type event_specials_count: int, optional
:param event_count: Indicates how many events are in the given league., defaults to None
:type event_count: int, optional
"""
    def __init__(self, id_: int = None, name: str = None, home_team_type: str = None, has_offerings: bool = None, container: str = None, allow_round_robins: bool = None, league_specials_count: int = None, event_specials_count: int = None, event_count: int = None):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if home_team_type is not None:
            self.home_team_type = home_team_type
        if has_offerings is not None:
            self.has_offerings = has_offerings
        if container is not None:
            self.container = container
        if allow_round_robins is not None:
            self.allow_round_robins = allow_round_robins
        if league_specials_count is not None:
            self.league_specials_count = league_specials_count
        if event_specials_count is not None:
            self.event_specials_count = event_specials_count
        if event_count is not None:
            self.event_count = event_count



