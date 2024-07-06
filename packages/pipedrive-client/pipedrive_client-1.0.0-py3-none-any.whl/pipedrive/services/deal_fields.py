from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_deal_field_request import UpdateDealFieldRequest
from ..models.update_deal_field_ok_response import UpdateDealFieldOkResponse
from ..models.get_deal_fields_ok_response import GetDealFieldsOkResponse
from ..models.get_deal_field_ok_response import GetDealFieldOkResponse
from ..models.delete_deal_fields_ok_response import DeleteDealFieldsOkResponse
from ..models.delete_deal_field_ok_response import DeleteDealFieldOkResponse
from ..models.add_deal_field_request import AddDealFieldRequest
from ..models.add_deal_field_ok_response import AddDealFieldOkResponse


class DealFieldsService(BaseService):

    @cast_models
    def get_deal_fields(
        self, start: int = None, limit: int = None
    ) -> GetDealFieldsOkResponse:
        """Returns data about all deal fields.

        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetDealFieldsOkResponse
        """

        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/dealFields", self.get_default_headers())
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealFieldsOkResponse._unmap(response)

    @cast_models
    def add_deal_field(
        self, request_body: AddDealFieldRequest = None
    ) -> AddDealFieldOkResponse:
        """Adds a new deal field. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/adding-a-new-custom-field" target="_blank" rel="noopener noreferrer">adding a new custom field</a>.

        :param request_body: The request body., defaults to None
        :type request_body: AddDealFieldRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: AddDealFieldOkResponse
        """

        Validator(AddDealFieldRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/dealFields", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddDealFieldOkResponse._unmap(response)

    @cast_models
    def delete_deal_fields(self, ids: str) -> DeleteDealFieldsOkResponse:
        """Marks multiple deal fields as deleted.

        :param ids: The comma-separated field IDs to delete
        :type ids: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteDealFieldsOkResponse
        """

        Validator(str).validate(ids)

        serialized_request = (
            Serializer(f"{self.base_url}/dealFields", self.get_default_headers())
            .add_query("ids", ids)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteDealFieldsOkResponse._unmap(response)

    @cast_models
    def get_deal_field(self, id_: int) -> GetDealFieldOkResponse:
        """Returns data about a specific deal field.

        :param id_: The ID of the field
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetDealFieldOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/dealFields/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealFieldOkResponse._unmap(response)

    @cast_models
    def update_deal_field(
        self, id_: int, request_body: UpdateDealFieldRequest = None
    ) -> UpdateDealFieldOkResponse:
        """Updates a deal field. For more information, see the tutorial for <a href=" https://pipedrive.readme.io/docs/updating-custom-field-value " target="_blank" rel="noopener noreferrer">updating custom fields' values</a>.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateDealFieldRequest, optional
        :param id_: The ID of the field
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateDealFieldOkResponse
        """

        Validator(UpdateDealFieldRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/dealFields/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateDealFieldOkResponse._unmap(response)

    @cast_models
    def delete_deal_field(self, id_: int) -> DeleteDealFieldOkResponse:
        """Marks a field as deleted. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/deleting-a-custom-field" target="_blank" rel="noopener noreferrer">deleting a custom field</a>.

        :param id_: The ID of the field
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteDealFieldOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/dealFields/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteDealFieldOkResponse._unmap(response)
