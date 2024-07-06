from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_product_field_request import UpdateProductFieldRequest
from ..models.update_product_field_ok_response import UpdateProductFieldOkResponse
from ..models.get_product_fields_ok_response import GetProductFieldsOkResponse
from ..models.get_product_field_ok_response import GetProductFieldOkResponse
from ..models.delete_product_fields_ok_response import DeleteProductFieldsOkResponse
from ..models.delete_product_field_ok_response import DeleteProductFieldOkResponse
from ..models.add_product_field_request import AddProductFieldRequest
from ..models.add_product_field_created_response import AddProductFieldCreatedResponse


class ProductFieldsService(BaseService):

    @cast_models
    def get_product_fields(
        self, start: int = None, limit: int = None
    ) -> GetProductFieldsOkResponse:
        """Returns data about all product fields.

        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get data about all product fields
        :rtype: GetProductFieldsOkResponse
        """

        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/productFields", self.get_default_headers())
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProductFieldsOkResponse._unmap(response)

    @cast_models
    def add_product_field(
        self, request_body: AddProductFieldRequest = None
    ) -> AddProductFieldCreatedResponse:
        """Adds a new product field. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/adding-a-new-custom-field" target="_blank" rel="noopener noreferrer">adding a new custom field</a>.

        :param request_body: The request body., defaults to None
        :type request_body: AddProductFieldRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get the data for a single product field
        :rtype: AddProductFieldCreatedResponse
        """

        Validator(AddProductFieldRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/productFields", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddProductFieldCreatedResponse._unmap(response)

    @cast_models
    def delete_product_fields(self, ids: str) -> DeleteProductFieldsOkResponse:
        """Marks multiple fields as deleted.

        :param ids: The comma-separated field IDs to delete
        :type ids: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Mark multiple product fields as deleted
        :rtype: DeleteProductFieldsOkResponse
        """

        Validator(str).validate(ids)

        serialized_request = (
            Serializer(f"{self.base_url}/productFields", self.get_default_headers())
            .add_query("ids", ids)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteProductFieldsOkResponse._unmap(response)

    @cast_models
    def get_product_field(self, id_: int) -> GetProductFieldOkResponse:
        """Returns data about a specific product field.

        :param id_: The ID of the product field
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get the data for a single product field
        :rtype: GetProductFieldOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/productFields/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProductFieldOkResponse._unmap(response)

    @cast_models
    def update_product_field(
        self, id_: int, request_body: UpdateProductFieldRequest = None
    ) -> UpdateProductFieldOkResponse:
        """Updates a product field. For more information, see the tutorial for <a href=" https://pipedrive.readme.io/docs/updating-custom-field-value " target="_blank" rel="noopener noreferrer">updating custom fields' values</a>.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateProductFieldRequest, optional
        :param id_: The ID of the product field
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get the data for a single product field
        :rtype: UpdateProductFieldOkResponse
        """

        Validator(UpdateProductFieldRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/productFields/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateProductFieldOkResponse._unmap(response)

    @cast_models
    def delete_product_field(self, id_: int) -> DeleteProductFieldOkResponse:
        """Marks a product field as deleted. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/deleting-a-custom-field" target="_blank" rel="noopener noreferrer">deleting a custom field</a>.

        :param id_: The ID of the product field
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete a product field
        :rtype: DeleteProductFieldOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/productFields/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteProductFieldOkResponse._unmap(response)
