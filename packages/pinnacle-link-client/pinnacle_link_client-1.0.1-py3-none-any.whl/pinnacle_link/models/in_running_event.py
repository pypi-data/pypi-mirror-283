from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel

class State(Enum):
    """An enumeration representing different categories.

:cvar _1: 1
:vartype _1: str
:cvar _2: 2
:vartype _2: str
:cvar _3: 3
:vartype _3: str
:cvar _4: 4
:vartype _4: str
:cvar _5: 5
:vartype _5: str
:cvar _6: 6
:vartype _6: str
:cvar _7: 7
:vartype _7: str
:cvar _8: 8
:vartype _8: str
:cvar _9: 9
:vartype _9: str
:cvar _10: 10
:vartype _10: str
:cvar _11: 11
:vartype _11: str
"""
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _9 = 9
    _10 = 10
    _11 = 11

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, State._member_map_.values()))




@JsonMap({"id_": "id"})
class InRunningEvent(BaseModel):
    """InRunningEvent

:param id_: Game Id, defaults to None
:type id_: int, optional
:param state: State of the game.<br><br>1 = First half in progress, <br>2 = Half time in progress, <br>3 = Second half in progress, <br>4 = End of regular time,<br>5 = First half extra time in progress, <br>6 = Extra time half time in progress, <br>7 = Second half extra time in progress, <br>8 = End of extra time, <br>9 = End of Game, <br>10 = Game is temporary suspended, <br>11 = Penalties in progress<br>, defaults to None
:type state: State, optional
:param elapsed: Elapsed minutes, defaults to None
:type elapsed: int, optional
"""
    def __init__(self, id_: int = None, state: State = None, elapsed: int = None):
        if id_ is not None:
            self.id_ = id_
        if state is not None:
            self.state = self._enum_matching(state,State.list(),"state")
        if elapsed is not None:
            self.elapsed = elapsed



