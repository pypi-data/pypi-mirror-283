from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.teaser_odds_response import TeaserOddsResponse
from ..models.special_odds_response import SpecialOddsResponse
from ..models.odds_straight_v1_get_odds_format import OddsStraightV1GetOddsFormat
from ..models.odds_special_v1_get_odds_format import OddsSpecialV1GetOddsFormat
from ..models.odds_response import OddsResponse


class OddsService(BaseService):
    
    @cast_models
    def odds_straight_v1_get(self,sport_id: int,league_ids: List[int] = None,odds_format: OddsStraightV1GetOddsFormat = None,since: int = None,is_live: bool = None,event_ids: List[int] = None,to_currency_code: str = None) -> OddsResponse:
        """Returns straight odds for all non-settled events. Please note that it is  possible that the event is in Get Fixtures response but not in Get Odds. This happens when the odds are not currently available for wagering.

:param sport_id: The sportid for which to retrieve the odds.
:type sport_id: int
:param league_ids: The leagueIds array may contain a list of comma separated league ids., defaults to None
:type league_ids: List[int], optional
:param odds_format: Format in which we return the odds. Default is American. [American, Decimal, HongKong, Indonesian, Malay], defaults to None
:type odds_format: OddsStraightV1GetOddsFormat, optional
:param since: This is used to receive incremental updates. Use the value of last from previous odds response. When since parameter is not provided, the odds are delayed up to 1 min to encourage the use of the parameter. Please note that when using since parameter you will get in the response ONLY changed periods. If a period did not have any changes it will not be in the response., defaults to None
:type since: int, optional
:param is_live: To retrieve ONLY live odds set the value to 1 (isLive=1). Otherwise response will have all odds., defaults to None
:type is_live: bool, optional
:param event_ids: Filter by EventIds, defaults to None
:type event_ids: List[int], optional
:param to_currency_code: 3 letter currency code as in the [/currency](https://pinnacleapi.github.io/linesapi#operation/Currencies_V2_Get) response. Limits will be returned in the requested currency. Default is USD., defaults to None
:type to_currency_code: str, optional
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: OddsResponse
"""

        Validator(int).validate(sport_id)
        Validator(int).is_array().is_optional().validate(league_ids)
        Validator(OddsStraightV1GetOddsFormat).is_optional().validate(odds_format)
        Validator(int).is_optional().validate(since)
        Validator(bool).is_optional().validate(is_live)
        Validator(int).is_array().is_optional().validate(event_ids)
        Validator(str).is_optional().validate(to_currency_code)

        serialized_request = Serializer(f"{self.base_url}/v1/odds", self.get_default_headers()).add_query("sportId", sport_id   ).add_query("leagueIds", league_ids   ).add_query("oddsFormat", odds_format   ).add_query("since", since   ).add_query("isLive", is_live   ).add_query("eventIds", event_ids   ).add_query("toCurrencyCode", to_currency_code   ).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return OddsResponse._unmap(response)
    
    @cast_models
    def odds_teasers_v1_get(self,teaser_id: int) -> TeaserOddsResponse:
        """Returns odds for specified teaser.

:param teaser_id: Unique identifier.Teaser details can be retrieved from a call to Get Teaser Groups endpoint.
:type teaser_id: int
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: TeaserOddsResponse
"""

        Validator(int).validate(teaser_id)

        serialized_request = Serializer(f"{self.base_url}/v1/odds/teaser", self.get_default_headers()).add_query("teaserId", teaser_id   ).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return TeaserOddsResponse._unmap(response)
    
    @cast_models
    def odds_special_v1_get(self,sport_id: int,odds_format: OddsSpecialV1GetOddsFormat = None,league_ids: List[int] = None,since: int = None,special_id: int = None) -> SpecialOddsResponse:
        """Returns odds for specials for all non-settled events.

:param sport_id: Id of a sport for which to retrieve the specials.
:type sport_id: int
:param odds_format: Format the odds are returned in. [American, Decimal, HongKong, Indonesian, Malay], defaults to None
:type odds_format: OddsSpecialV1GetOddsFormat, optional
:param league_ids: The leagueIds array may contain a list of comma separated league ids., defaults to None
:type league_ids: List[int], optional
:param since: This is used to receive incremental updates. Use the value of last from previous response. When since parameter is not provided, the fixtures are delayed up to 1 min to encourage the use of the parameter., defaults to None
:type since: int, optional
:param special_id: Id of the special. This is an optional argument., defaults to None
:type special_id: int, optional
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: SpecialOddsResponse
"""

        Validator(int).validate(sport_id)
        Validator(OddsSpecialV1GetOddsFormat).is_optional().validate(odds_format)
        Validator(int).is_array().is_optional().validate(league_ids)
        Validator(int).is_optional().validate(since)
        Validator(int).is_optional().validate(special_id)

        serialized_request = Serializer(f"{self.base_url}/v1/odds/special", self.get_default_headers()).add_query("oddsFormat", odds_format   ).add_query("sportId", sport_id   ).add_query("leagueIds", league_ids   ).add_query("since", since   ).add_query("specialId", special_id   ).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return SpecialOddsResponse._unmap(response)
