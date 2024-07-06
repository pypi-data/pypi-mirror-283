from enum import Enum

class LineStraightV1GetBetType(Enum):
    """An enumeration representing different categories.

:cvar SPREAD: "SPREAD"
:vartype SPREAD: str
:cvar MONEYLINE: "MONEYLINE"
:vartype MONEYLINE: str
:cvar TOTAL_POINTS: "TOTAL_POINTS"
:vartype TOTAL_POINTS: str
:cvar TEAM_TOTAL_POINTS: "TEAM_TOTAL_POINTS"
:vartype TEAM_TOTAL_POINTS: str
"""
    SPREAD = "SPREAD"
    MONEYLINE = "MONEYLINE"
    TOTAL_POINTS = "TOTAL_POINTS"
    TEAM_TOTAL_POINTS = "TEAM_TOTAL_POINTS"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, LineStraightV1GetBetType._member_map_.values()))


