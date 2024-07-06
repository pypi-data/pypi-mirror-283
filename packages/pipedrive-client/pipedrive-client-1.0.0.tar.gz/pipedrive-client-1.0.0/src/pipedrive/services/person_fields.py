from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_person_field_request import UpdatePersonFieldRequest
from ..models.update_person_field_ok_response import UpdatePersonFieldOkResponse
from ..models.get_person_fields_ok_response import GetPersonFieldsOkResponse
from ..models.get_person_field_ok_response import GetPersonFieldOkResponse
from ..models.delete_person_fields_ok_response import DeletePersonFieldsOkResponse
from ..models.delete_person_field_ok_response import DeletePersonFieldOkResponse
from ..models.add_person_field_request import AddPersonFieldRequest
from ..models.add_person_field_ok_response import AddPersonFieldOkResponse


class PersonFieldsService(BaseService):

    @cast_models
    def get_person_fields(
        self, start: int = None, limit: int = None
    ) -> GetPersonFieldsOkResponse:
        """Returns data about all person fields.<br>If a company uses the [Campaigns product](https://pipedrive.readme.io/docs/campaigns-in-pipedrive-api), then this endpoint will also return the `data.marketing_status` field.

        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetPersonFieldsOkResponse
        """

        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/personFields", self.get_default_headers())
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPersonFieldsOkResponse._unmap(response)

    @cast_models
    def add_person_field(
        self, request_body: AddPersonFieldRequest = None
    ) -> AddPersonFieldOkResponse:
        """Adds a new person field. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/adding-a-new-custom-field" target="_blank" rel="noopener noreferrer">adding a new custom field</a>.

        :param request_body: The request body., defaults to None
        :type request_body: AddPersonFieldRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: AddPersonFieldOkResponse
        """

        Validator(AddPersonFieldRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/personFields", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddPersonFieldOkResponse._unmap(response)

    @cast_models
    def delete_person_fields(self, ids: str) -> DeletePersonFieldsOkResponse:
        """Marks multiple fields as deleted.

        :param ids: The comma-separated field IDs to delete
        :type ids: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeletePersonFieldsOkResponse
        """

        Validator(str).validate(ids)

        serialized_request = (
            Serializer(f"{self.base_url}/personFields", self.get_default_headers())
            .add_query("ids", ids)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeletePersonFieldsOkResponse._unmap(response)

    @cast_models
    def get_person_field(self, id_: int) -> GetPersonFieldOkResponse:
        """Returns data about a specific person field.

        :param id_: The ID of the field
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetPersonFieldOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/personFields/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPersonFieldOkResponse._unmap(response)

    @cast_models
    def update_person_field(
        self, id_: int, request_body: UpdatePersonFieldRequest = None
    ) -> UpdatePersonFieldOkResponse:
        """Updates a person field. For more information, see the tutorial for <a href=" https://pipedrive.readme.io/docs/updating-custom-field-value " target="_blank" rel="noopener noreferrer">updating custom fields' values</a>.

        :param request_body: The request body., defaults to None
        :type request_body: UpdatePersonFieldRequest, optional
        :param id_: The ID of the field
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdatePersonFieldOkResponse
        """

        Validator(UpdatePersonFieldRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/personFields/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdatePersonFieldOkResponse._unmap(response)

    @cast_models
    def delete_person_field(self, id_: int) -> DeletePersonFieldOkResponse:
        """Marks a field as deleted. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/deleting-a-custom-field" target="_blank" rel="noopener noreferrer">deleting a custom field</a>.

        :param id_: The ID of the field
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeletePersonFieldOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/personFields/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeletePersonFieldOkResponse._unmap(response)
