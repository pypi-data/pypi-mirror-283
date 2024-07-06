from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.teaser_groups_v1_get_odds_format import TeaserGroupsV1GetOddsFormat
from ..models.teaser_groups_response import TeaserGroupsResponse
from ..models.successful_currencies_response import SuccessfulCurrenciesResponse
from ..models.sports_response import SportsResponse
from ..models.sport_period import SportPeriod
from ..models.leagues import Leagues
from ..models.in_running_response import InRunningResponse
from ..models.cancellation_reason_response import CancellationReasonResponse


class OthersService(BaseService):
    
    @cast_models
    def sports_v2_get(self) -> SportsResponse:
        """Returns all sports with the status whether they currently have lines or not.

...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: SportsResponse
"""


        serialized_request = Serializer(f"{self.base_url}/v2/sports", self.get_default_headers()).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return SportsResponse._unmap(response)
    
    @cast_models
    def leagues_v2_get(self,sport_id: str) -> Leagues:
        """Returns all sports leagues with the status whether they currently have lines or not.

:param sport_id: Sport id for which the leagues are requested.
:type sport_id: str
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: Leagues
"""

        Validator(str).validate(sport_id)

        serialized_request = Serializer(f"{self.base_url}/v2/leagues", self.get_default_headers()).add_query("sportId", sport_id   ).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return Leagues._unmap(response)
    
    @cast_models
    def periods_v1_get(self,sport_id: str) -> SportPeriod:
        """Returns all periods for a given sport.

:param sport_id: sport_id
:type sport_id: str
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: SportPeriod
"""

        Validator(str).validate(sport_id)

        serialized_request = Serializer(f"{self.base_url}/v1/periods", self.get_default_headers()).add_query("sportId", sport_id   ).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return SportPeriod._unmap(response)
    
    @cast_models
    def in_running_v1_get(self) -> InRunningResponse:
        """Returns all live soccer events that have a status that indicates the event is in progress.

...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: InRunningResponse
"""


        serialized_request = Serializer(f"{self.base_url}/v1/inrunning", self.get_default_headers()).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return InRunningResponse._unmap(response)
    
    @cast_models
    def teaser_groups_v1_get(self,odds_format: TeaserGroupsV1GetOddsFormat) -> TeaserGroupsResponse:
        """Returns all teaser groups.

:param odds_format: Format the odds are returned in. [American, Decimal, HongKong, Indonesian, Malay]
:type odds_format: TeaserGroupsV1GetOddsFormat
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: TeaserGroupsResponse
"""

        Validator(TeaserGroupsV1GetOddsFormat).validate(odds_format)

        serialized_request = Serializer(f"{self.base_url}/v1/teaser/groups", self.get_default_headers()).add_query("oddsFormat", odds_format   ).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return TeaserGroupsResponse._unmap(response)
    
    @cast_models
    def cancellation_reasons_v1_get(self) -> CancellationReasonResponse:
        """Lookup for all the cancellation reasons

...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: CancellationReasonResponse
"""


        serialized_request = Serializer(f"{self.base_url}/v1/cancellationreasons", self.get_default_headers()).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return CancellationReasonResponse._unmap(response)
    
    @cast_models
    def currencies_v2_get(self) -> SuccessfulCurrenciesResponse:
        """Returns the list of supported currencies

...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: SuccessfulCurrenciesResponse
"""


        serialized_request = Serializer(f"{self.base_url}/v2/currencies", self.get_default_headers()).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return SuccessfulCurrenciesResponse._unmap(response)
