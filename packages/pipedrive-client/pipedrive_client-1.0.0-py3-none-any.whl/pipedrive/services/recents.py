from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_recents_ok_response import GetRecentsOkResponse
from ..models.get_recents_items import GetRecentsItems


class RecentsService(BaseService):

    @cast_models
    def get_recents(
        self,
        since_timestamp: str,
        items: GetRecentsItems = None,
        start: int = None,
        limit: int = None,
    ) -> GetRecentsOkResponse:
        """Returns data about all recent changes occurred after the given timestamp.

        :param since_timestamp: The timestamp in UTC. Format: YYYY-MM-DD HH:MM:SS.
        :type since_timestamp: str
        :param items: Multiple selection of item types to include in the query (optional), defaults to None
        :type items: GetRecentsItems, optional
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List of items changed since "since_timestamp"
        :rtype: GetRecentsOkResponse
        """

        Validator(str).validate(since_timestamp)
        Validator(GetRecentsItems).is_optional().validate(items)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/recents", self.get_default_headers())
            .add_query("since_timestamp", since_timestamp)
            .add_query("items", items)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetRecentsOkResponse._unmap(response)
