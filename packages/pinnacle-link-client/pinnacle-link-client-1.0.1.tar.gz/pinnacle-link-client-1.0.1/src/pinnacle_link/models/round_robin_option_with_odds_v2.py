from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel

class RoundRobinOption(Enum):
    """An enumeration representing different categories.

:cvar PARLAY: "Parlay"
:vartype PARLAY: str
:cvar TWOLEGROUNDROBIN: "TwoLegRoundRobin"
:vartype TWOLEGROUNDROBIN: str
:cvar THREELEGROUNDROBIN: "ThreeLegRoundRobin"
:vartype THREELEGROUNDROBIN: str
:cvar FOURLEGROUNDROBIN: "FourLegRoundRobin"
:vartype FOURLEGROUNDROBIN: str
:cvar FIVELEGROUNDROBIN: "FiveLegRoundRobin"
:vartype FIVELEGROUNDROBIN: str
:cvar SIXLEGROUNDROBIN: "SixLegRoundRobin"
:vartype SIXLEGROUNDROBIN: str
:cvar SEVENLEGROUNDROBIN: "SevenLegRoundRobin"
:vartype SEVENLEGROUNDROBIN: str
:cvar EIGHTLEGROUNDROBIN: "EightLegRoundRobin"
:vartype EIGHTLEGROUNDROBIN: str
"""
    PARLAY = "Parlay"
    TWOLEGROUNDROBIN = "TwoLegRoundRobin"
    THREELEGROUNDROBIN = "ThreeLegRoundRobin"
    FOURLEGROUNDROBIN = "FourLegRoundRobin"
    FIVELEGROUNDROBIN = "FiveLegRoundRobin"
    SIXLEGROUNDROBIN = "SixLegRoundRobin"
    SEVENLEGROUNDROBIN = "SevenLegRoundRobin"
    EIGHTLEGROUNDROBIN = "EightLegRoundRobin"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, RoundRobinOption._member_map_.values()))




@JsonMap({"round_robin_option": "roundRobinOption","unrounded_decimal_odds": "unroundedDecimalOdds","number_of_bets": "numberOfBets"})
class RoundRobinOptionWithOddsV2(BaseModel):
    """RoundRobinOptionWithOddsV2

:param round_robin_option: RoundRobinOptions  <br>  <br>  Parlay = Single parlay that include all wagers (No Round Robin),  <br>  TwoLegRoundRobin = Multiple parlays having 2 wagers each (round robin style),  <br>  ThreeLegRoundRobin = Multiple parlays having 3 wagers each (round robin style),  <br>  FourLegRoundRobin = Multiple parlays having 4 wagers each (round robin style),  <br>  FiveLegRoundRobin = Multiple parlays having 5 wagers each (round robin style),  <br>  SixLegRoundRobin = Multiple parlays having 6 wagers each (round robin style),  <br>  SevenLegRoundRobin = Multiple parlays having 7 wagers each (round robin style),   <br>  EightLegRoundRobin = Multiple parlays having 8 wagers each (round robin style)  <br>
:type round_robin_option: RoundRobinOption
:param odds: Parlay odds for this option.
:type odds: float
:param unrounded_decimal_odds: Unrounded parlay odds in decimal format to be used for calculations only
:type unrounded_decimal_odds: float
:param number_of_bets: Number of bets in the roundRobinOption., defaults to None
:type number_of_bets: float, optional
"""
    def __init__(self, round_robin_option: RoundRobinOption, odds: float, unrounded_decimal_odds: float, number_of_bets: float = None):
        self.round_robin_option = self._enum_matching(round_robin_option,RoundRobinOption.list(),"round_robin_option")
        self.odds = odds
        self.unrounded_decimal_odds = unrounded_decimal_odds
        if number_of_bets is not None:
            self.number_of_bets = number_of_bets



