from enum import Enum

class LineStraightV1GetTeam(Enum):
    """An enumeration representing different categories.

:cvar TEAM1: "Team1"
:vartype TEAM1: str
:cvar TEAM2: "Team2"
:vartype TEAM2: str
:cvar DRAW: "Draw"
:vartype DRAW: str
"""
    TEAM1 = "Team1"
    TEAM2 = "Team2"
    DRAW = "Draw"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, LineStraightV1GetTeam._member_map_.values()))


