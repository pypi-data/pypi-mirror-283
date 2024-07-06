from enum import Enum

class LineStraightV1GetSide(Enum):
    """An enumeration representing different categories.

:cvar OVER: "OVER"
:vartype OVER: str
:cvar UNDER: "UNDER"
:vartype UNDER: str
"""
    OVER = "OVER"
    UNDER = "UNDER"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, LineStraightV1GetSide._member_map_.values()))


