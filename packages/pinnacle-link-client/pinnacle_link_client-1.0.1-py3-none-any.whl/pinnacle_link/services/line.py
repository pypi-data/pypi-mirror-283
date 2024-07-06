from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.teaser_lines_response import TeaserLinesResponse
from ..models.special_line_response import SpecialLineResponse
from ..models.parlay_lines_response_v2 import ParlayLinesResponseV2
from ..models.parlay_lines_request import ParlayLinesRequest
from ..models.lines_request_teaser import LinesRequestTeaser
from ..models.line_straight_v1_get_team import LineStraightV1GetTeam
from ..models.line_straight_v1_get_side import LineStraightV1GetSide
from ..models.line_straight_v1_get_odds_format import LineStraightV1GetOddsFormat
from ..models.line_straight_v1_get_bet_type import LineStraightV1GetBetType
from ..models.line_special_v1_get_odds_format import LineSpecialV1GetOddsFormat
from ..models.line_response import LineResponse


class LineService(BaseService):
    
    @cast_models
    def line_straight_v1_get(self,league_id: int,handicap: float,odds_format: LineStraightV1GetOddsFormat,sport_id: int,event_id: int,period_number: int,bet_type: LineStraightV1GetBetType,team: LineStraightV1GetTeam = None,side: LineStraightV1GetSide = None) -> LineResponse:
        """Returns latest line.

:param league_id: League Id.
:type league_id: int
:param handicap: This is needed for SPREAD, TOTAL_POINTS and TEAM_TOTAL_POINTS bet types
:type handicap: float
:param odds_format: Format in which we return the odds. Default is American.
:type odds_format: LineStraightV1GetOddsFormat
:param sport_id: Sport identification
:type sport_id: int
:param event_id: Event identification
:type event_id: int
:param period_number: This represents the period of the match. Please check Get Periods endpoint for the list of currently supported periods per sport.
:type period_number: int
:param bet_type: Bet Type
:type bet_type: LineStraightV1GetBetType
:param team: Chosen team type. This is needed only for SPREAD, MONEYLINE and TEAM_TOTAL_POINTS bet types, defaults to None
:type team: LineStraightV1GetTeam, optional
:param side: Chosen side. This is needed only for TOTAL_POINTS and TEAM_TOTAL_POINTS, defaults to None
:type side: LineStraightV1GetSide, optional
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: LineResponse
"""

        Validator(int).validate(league_id)
        Validator(float).validate(handicap)
        Validator(LineStraightV1GetOddsFormat).validate(odds_format)
        Validator(int).validate(sport_id)
        Validator(int).validate(event_id)
        Validator(int).validate(period_number)
        Validator(LineStraightV1GetBetType).validate(bet_type)
        Validator(LineStraightV1GetTeam).is_optional().validate(team)
        Validator(LineStraightV1GetSide).is_optional().validate(side)

        serialized_request = Serializer(f"{self.base_url}/v1/line", self.get_default_headers()).add_query("leagueId", league_id   ).add_query("handicap", handicap   ).add_query("oddsFormat", odds_format   ).add_query("sportId", sport_id   ).add_query("eventId", event_id   ).add_query("periodNumber", period_number   ).add_query("betType", bet_type   ).add_query("team", team   ).add_query("side", side   ).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return LineResponse._unmap(response)
    
    @cast_models
    def line_parlay_v2_post(self,request_body: ParlayLinesRequest) -> ParlayLinesResponseV2:
        """Returns parlay lines and calculate odds. For placing round robin bets, must be used with /v2/bets/parlay.

:param request_body: The request body.
:type request_body: ParlayLinesRequest
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: ParlayLinesResponseV2
"""

        Validator(ParlayLinesRequest).validate(request_body)

        serialized_request = Serializer(f"{self.base_url}/v2/line/parlay", self.get_default_headers()).serialize().set_method("POST").set_body(request_body)

        response = self.send_request(serialized_request)

        return ParlayLinesResponseV2._unmap(response)
    
    @cast_models
    def line_teaser_v1_post(self,request_body: LinesRequestTeaser) -> TeaserLinesResponse:
        """Validates a teaser bet prior to submission. Returns bet limit and price on success.

:param request_body: The request body.
:type request_body: LinesRequestTeaser
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: TeaserLinesResponse
"""

        Validator(LinesRequestTeaser).validate(request_body)

        serialized_request = Serializer(f"{self.base_url}/v1/line/teaser", self.get_default_headers()).serialize().set_method("POST").set_body(request_body)

        response = self.send_request(serialized_request)

        return TeaserLinesResponse._unmap(response)
    
    @cast_models
    def line_special_v1_get(self,odds_format: LineSpecialV1GetOddsFormat,special_id: int,contestant_id: int,handicap: int = None) -> SpecialLineResponse:
        """Returns special lines and calculate odds.

:param odds_format: Format the odds are returned in. [American, Decimal, HongKong, Indonesian, Malay]
:type odds_format: LineSpecialV1GetOddsFormat
:param special_id: Id of the special.
:type special_id: int
:param contestant_id: Id of the contestant.
:type contestant_id: int
:param handicap: handicap of the contestant. As contestant's handicap is a mutable property, it may happened that line/special returns status:SUCCESS, but with the different handicap from the one that client had at the moment of calling the line/special. One can specify handicap parameter in the request and if the contestant's handicap changed, it would return status:NOT_EXISTS. This way line/special is more aligned to how /line works., defaults to None
:type handicap: int, optional
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: SpecialLineResponse
"""

        Validator(LineSpecialV1GetOddsFormat).validate(odds_format)
        Validator(int).validate(special_id)
        Validator(int).validate(contestant_id)
        Validator(int).is_optional().validate(handicap)

        serialized_request = Serializer(f"{self.base_url}/v1/line/special", self.get_default_headers()).add_query("oddsFormat", odds_format   ).add_query("specialId", special_id   ).add_query("contestantId", contestant_id   ).add_query("handicap", handicap   ).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return SpecialLineResponse._unmap(response)
