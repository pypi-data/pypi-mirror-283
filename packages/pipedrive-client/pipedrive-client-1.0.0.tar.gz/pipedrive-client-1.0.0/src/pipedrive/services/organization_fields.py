from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_organization_field_request import UpdateOrganizationFieldRequest
from ..models.update_organization_field_ok_response import (
    UpdateOrganizationFieldOkResponse,
)
from ..models.get_organization_fields_ok_response import GetOrganizationFieldsOkResponse
from ..models.get_organization_field_ok_response import GetOrganizationFieldOkResponse
from ..models.delete_organization_fields_ok_response import (
    DeleteOrganizationFieldsOkResponse,
)
from ..models.delete_organization_field_ok_response import (
    DeleteOrganizationFieldOkResponse,
)
from ..models.add_organization_field_request import AddOrganizationFieldRequest
from ..models.add_organization_field_ok_response import AddOrganizationFieldOkResponse


class OrganizationFieldsService(BaseService):

    @cast_models
    def get_organization_fields(
        self, start: int = None, limit: int = None
    ) -> GetOrganizationFieldsOkResponse:
        """Returns data about all organization fields.

        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationFieldsOkResponse
        """

        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizationFields", self.get_default_headers()
            )
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationFieldsOkResponse._unmap(response)

    @cast_models
    def add_organization_field(
        self, request_body: AddOrganizationFieldRequest = None
    ) -> AddOrganizationFieldOkResponse:
        """Adds a new organization field. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/adding-a-new-custom-field" target="_blank" rel="noopener noreferrer">adding a new custom field</a>.

        :param request_body: The request body., defaults to None
        :type request_body: AddOrganizationFieldRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: AddOrganizationFieldOkResponse
        """

        Validator(AddOrganizationFieldRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizationFields", self.get_default_headers()
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddOrganizationFieldOkResponse._unmap(response)

    @cast_models
    def delete_organization_fields(
        self, ids: str
    ) -> DeleteOrganizationFieldsOkResponse:
        """Marks multiple fields as deleted.

        :param ids: The comma-separated field IDs to delete
        :type ids: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteOrganizationFieldsOkResponse
        """

        Validator(str).validate(ids)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizationFields", self.get_default_headers()
            )
            .add_query("ids", ids)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteOrganizationFieldsOkResponse._unmap(response)

    @cast_models
    def get_organization_field(self, id_: int) -> GetOrganizationFieldOkResponse:
        """Returns data about a specific organization field.

        :param id_: The ID of the field
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationFieldOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizationFields/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationFieldOkResponse._unmap(response)

    @cast_models
    def update_organization_field(
        self, id_: int, request_body: UpdateOrganizationFieldRequest = None
    ) -> UpdateOrganizationFieldOkResponse:
        """Updates an organization field. For more information, see the tutorial for <a href=" https://pipedrive.readme.io/docs/updating-custom-field-value " target="_blank" rel="noopener noreferrer">updating custom fields' values</a>.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateOrganizationFieldRequest, optional
        :param id_: The ID of the field
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateOrganizationFieldOkResponse
        """

        Validator(UpdateOrganizationFieldRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizationFields/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateOrganizationFieldOkResponse._unmap(response)

    @cast_models
    def delete_organization_field(self, id_: int) -> DeleteOrganizationFieldOkResponse:
        """Marks a field as deleted. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/deleting-a-custom-field" target="_blank" rel="noopener noreferrer">deleting a custom field</a>.

        :param id_: The ID of the field
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteOrganizationFieldOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizationFields/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteOrganizationFieldOkResponse._unmap(response)
