from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_filter_request import UpdateFilterRequest
from ..models.update_filter_ok_response import UpdateFilterOkResponse
from ..models.get_filters_type import GetFiltersType
from ..models.get_filters_ok_response import GetFiltersOkResponse
from ..models.get_filter_ok_response import GetFilterOkResponse
from ..models.delete_filters_ok_response import DeleteFiltersOkResponse
from ..models.delete_filter_ok_response import DeleteFilterOkResponse
from ..models.add_filter_request import AddFilterRequest
from ..models.add_filter_ok_response import AddFilterOkResponse


class FiltersService(BaseService):

    @cast_models
    def get_filters(self, type_: GetFiltersType = None) -> GetFiltersOkResponse:
        """Returns data about all filters.

        :param type_: The types of filters to fetch, defaults to None
        :type type_: GetFiltersType, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetFiltersOkResponse
        """

        Validator(GetFiltersType).is_optional().validate(type_)

        serialized_request = (
            Serializer(f"{self.base_url}/filters", self.get_default_headers())
            .add_query("type", type_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetFiltersOkResponse._unmap(response)

    @cast_models
    def add_filter(self, request_body: AddFilterRequest = None) -> AddFilterOkResponse:
        """Adds a new filter, returns the ID upon success. Note that in the conditions JSON object only one first-level condition group is supported, and it must be glued with 'AND', and only two second level condition groups are supported of which one must be glued with 'AND' and the second with 'OR'. Other combinations do not work (yet) but the syntax supports introducing them in future. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/adding-a-filter" target="_blank" rel="noopener noreferrer">adding a filter</a>.

        :param request_body: The request body., defaults to None
        :type request_body: AddFilterRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: AddFilterOkResponse
        """

        Validator(AddFilterRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/filters", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddFilterOkResponse._unmap(response)

    @cast_models
    def delete_filters(self, ids: str) -> DeleteFiltersOkResponse:
        """Marks multiple filters as deleted.

        :param ids: The comma-separated filter IDs to delete
        :type ids: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteFiltersOkResponse
        """

        Validator(str).validate(ids)

        serialized_request = (
            Serializer(f"{self.base_url}/filters", self.get_default_headers())
            .add_query("ids", ids)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteFiltersOkResponse._unmap(response)

    @cast_models
    def get_filter_helpers(self) -> dict:
        """Returns all supported filter helpers. It helps to know what conditions and helpers are available when you want to <a href="/docs/api/v1/Filters#addFilter">add</a> or <a href="/docs/api/v1/Filters#updateFilter">update</a> filters. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/adding-a-filter" target="_blank" rel="noopener noreferrer">adding a filter</a>.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: dict
        """

        serialized_request = (
            Serializer(f"{self.base_url}/filters/helpers", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def get_filter(self, id_: int) -> GetFilterOkResponse:
        """Returns data about a specific filter. Note that this also returns the condition lines of the filter.

        :param id_: The ID of the filter
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetFilterOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/filters/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetFilterOkResponse._unmap(response)

    @cast_models
    def update_filter(
        self, id_: int, request_body: UpdateFilterRequest = None
    ) -> UpdateFilterOkResponse:
        """Updates an existing filter.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateFilterRequest, optional
        :param id_: The ID of the filter
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateFilterOkResponse
        """

        Validator(UpdateFilterRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/filters/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateFilterOkResponse._unmap(response)

    @cast_models
    def delete_filter(self, id_: int) -> DeleteFilterOkResponse:
        """Marks a filter as deleted.

        :param id_: The ID of the filter
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteFilterOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/filters/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteFilterOkResponse._unmap(response)
