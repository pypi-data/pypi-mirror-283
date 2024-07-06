from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.specials_fixtures_response import SpecialsFixturesResponse
from ..models.settled_specials_response import SettledSpecialsResponse
from ..models.settled_fixtures_sport import SettledFixturesSport
from ..models.fixtures_response import FixturesResponse


class FixturesService(BaseService):
    
    @cast_models
    def fixtures_v1_get(self,sport_id: int,league_ids: List[int] = None,is_live: bool = None,since: int = None,event_ids: List[int] = None) -> FixturesResponse:
        """Returns all **non-settled** events for the given sport. Please note that it is possible that the event is in Get Fixtures response but not in Get Odds. This happens when the odds are not currently available for wagering. Please note that it is possible to receive the same exact response when using **since** parameter. This is rare and can be caused by internal updates of event properties.

:param sport_id: The sport id to retrieve the fixtures for.
:type sport_id: int
:param league_ids: The leagueIds array may contain a list of comma separated league ids., defaults to None
:type league_ids: List[int], optional
:param is_live: To retrieve ONLY live events set the value to 1 (isLive=1). Missing or any other value will result in retrieval of events regardless of their Live status., defaults to None
:type is_live: bool, optional
:param since: This is used to receive incremental updates. Use the value of last from previous fixtures response. When since parameter is not provided, the fixtures are delayed up to 1 minute to encourage the use of the parameter., defaults to None
:type since: int, optional
:param event_ids: Comma separated list of event ids to filter by, defaults to None
:type event_ids: List[int], optional
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: FixturesResponse
"""

        Validator(int).validate(sport_id)
        Validator(int).is_array().is_optional().validate(league_ids)
        Validator(bool).is_optional().validate(is_live)
        Validator(int).is_optional().validate(since)
        Validator(int).is_array().is_optional().validate(event_ids)

        serialized_request = Serializer(f"{self.base_url}/v1/fixtures", self.get_default_headers()).add_query("sportId", sport_id   ).add_query("leagueIds", league_ids   ).add_query("isLive", is_live   ).add_query("since", since   ).add_query("eventIds", event_ids   ).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return FixturesResponse._unmap(response)
    
    @cast_models
    def fixtures_special_v1_get(self,sport_id: int,league_ids: List[int] = None,since: int = None,category: str = None,event_id: int = None,special_id: int = None) -> SpecialsFixturesResponse:
        """Returns all **non-settled** specials for the given sport.

:param sport_id: Id of a sport for which to retrieve the specials.
:type sport_id: int
:param league_ids: The leagueIds array may contain a list of comma separated league ids., defaults to None
:type league_ids: List[int], optional
:param since: This is used to receive incremental updates. Use the value of last field from the previous response. When since parameter is not provided, the fixtures are delayed up to 1 min to encourage the use of the parameter., defaults to None
:type since: int, optional
:param category: The category the special falls under., defaults to None
:type category: str, optional
:param event_id: Id of an event associated with a special., defaults to None
:type event_id: int, optional
:param special_id: Id of the special., defaults to None
:type special_id: int, optional
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: SpecialsFixturesResponse
"""

        Validator(int).validate(sport_id)
        Validator(int).is_array().is_optional().validate(league_ids)
        Validator(int).is_optional().validate(since)
        Validator(str).is_optional().validate(category)
        Validator(int).is_optional().validate(event_id)
        Validator(int).is_optional().validate(special_id)

        serialized_request = Serializer(f"{self.base_url}/v1/fixtures/special", self.get_default_headers()).add_query("sportId", sport_id   ).add_query("leagueIds", league_ids   ).add_query("since", since   ).add_query("category", category   ).add_query("eventId", event_id   ).add_query("specialId", special_id   ).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return SpecialsFixturesResponse._unmap(response)
    
    @cast_models
    def fixtures_settled_v1_get(self,sport_id: int,league_ids: List[int] = None,since: int = None) -> SettledFixturesSport:
        """Returns fixtures settled in the last 24 hours for the given sport.

:param sport_id: sport_id
:type sport_id: int
:param league_ids: league_ids, defaults to None
:type league_ids: List[int], optional
:param since: since, defaults to None
:type since: int, optional
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: SettledFixturesSport
"""

        Validator(int).validate(sport_id)
        Validator(int).is_array().is_optional().validate(league_ids)
        Validator(int).is_optional().validate(since)

        serialized_request = Serializer(f"{self.base_url}/v1/fixtures/settled", self.get_default_headers()).add_query("sportId", sport_id   ).add_query("leagueIds", league_ids   ).add_query("since", since   ).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return SettledFixturesSport._unmap(response)
    
    @cast_models
    def fixtures_specials_settled_v1_get(self,sport_id: int,league_ids: List[int] = None,since: int = None) -> SettledSpecialsResponse:
        """Returns all specials which are settled in the last 24 hours for the given Sport.

:param sport_id: Id of the sport for which to retrieve the settled specials.
:type sport_id: int
:param league_ids: Array of leagueIds. This is optional parameter., defaults to None
:type league_ids: List[int], optional
:param since: This is used to receive incremental updates. Use the value of last from previous response., defaults to None
:type since: int, optional
...
:raises RequestError: Raised when a request fails, with optional HTTP status code and details.
...
:return: OK
:rtype: SettledSpecialsResponse
"""

        Validator(int).validate(sport_id)
        Validator(int).is_array().is_optional().validate(league_ids)
        Validator(int).is_optional().validate(since)

        serialized_request = Serializer(f"{self.base_url}/v1/fixtures/special/settled", self.get_default_headers()).add_query("sportId", sport_id   ).add_query("leagueIds", league_ids   ).add_query("since", since   ).serialize().set_method("GET")

        response = self.send_request(serialized_request)

        return SettledSpecialsResponse._unmap(response)
