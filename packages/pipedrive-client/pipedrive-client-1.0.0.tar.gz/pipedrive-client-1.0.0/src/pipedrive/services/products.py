from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_product_request import UpdateProductRequest
from ..models.update_product_ok_response import UpdateProductOkResponse
from ..models.search_products_ok_response import SearchProductsOkResponse
from ..models.search_products_include_fields import SearchProductsIncludeFields
from ..models.search_products_fields import SearchProductsFields
from ..models.get_products_ok_response import GetProductsOkResponse
from ..models.get_product_users_ok_response import GetProductUsersOkResponse
from ..models.get_product_ok_response import GetProductOkResponse
from ..models.get_product_followers_ok_response import GetProductFollowersOkResponse
from ..models.get_product_files_ok_response import GetProductFilesOkResponse
from ..models.get_product_deals_status import GetProductDealsStatus
from ..models.get_product_deals_ok_response import GetProductDealsOkResponse
from ..models.delete_product_ok_response import DeleteProductOkResponse
from ..models.delete_product_follower_ok_response import DeleteProductFollowerOkResponse
from ..models.add_product_request import AddProductRequest
from ..models.add_product_follower_request import AddProductFollowerRequest
from ..models.add_product_follower_created_response import (
    AddProductFollowerCreatedResponse,
)
from ..models.add_product_created_response import AddProductCreatedResponse


class ProductsService(BaseService):

    @cast_models
    def get_products(
        self,
        user_id: int = None,
        filter_id: int = None,
        ids: List[int] = None,
        first_char: str = None,
        get_summary: bool = None,
        start: int = None,
        limit: int = None,
    ) -> GetProductsOkResponse:
        """Returns data about all products.

        :param user_id: If supplied, only products owned by the given user will be returned, defaults to None
        :type user_id: int, optional
        :param filter_id: The ID of the filter to use, defaults to None
        :type filter_id: int, optional
        :param ids: An array of integers with the IDs of the products that should be returned in the response, defaults to None
        :type ids: List[int], optional
        :param first_char: If supplied, only products whose name starts with the specified letter will be returned (case-insensitive), defaults to None
        :type first_char: str, optional
        :param get_summary: If supplied, the response will return the total numbers of products in the `additional_data.summary.total_count` property, defaults to None
        :type get_summary: bool, optional
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List of products
        :rtype: GetProductsOkResponse
        """

        Validator(int).is_optional().validate(user_id)
        Validator(int).is_optional().validate(filter_id)
        Validator(int).is_array().is_optional().validate(ids)
        Validator(str).is_optional().validate(first_char)
        Validator(bool).is_optional().validate(get_summary)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/products", self.get_default_headers())
            .add_query("user_id", user_id)
            .add_query("filter_id", filter_id)
            .add_query("ids", ids)
            .add_query("first_char", first_char)
            .add_query("get_summary", get_summary)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProductsOkResponse._unmap(response)

    @cast_models
    def add_product(
        self, request_body: AddProductRequest = None
    ) -> AddProductCreatedResponse:
        """Adds a new product to the Products inventory. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/adding-a-product" target="_blank" rel="noopener noreferrer">adding a product</a>.

        :param request_body: The request body., defaults to None
        :type request_body: AddProductRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add product data
        :rtype: AddProductCreatedResponse
        """

        Validator(AddProductRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/products", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddProductCreatedResponse._unmap(response)

    @cast_models
    def search_products(
        self,
        term: str,
        fields: SearchProductsFields = None,
        exact_match: bool = None,
        include_fields: SearchProductsIncludeFields = None,
        start: int = None,
        limit: int = None,
    ) -> SearchProductsOkResponse:
        """Searches all products by name, code and/or custom fields. This endpoint is a wrapper of <a href="https://developers.pipedrive.com/docs/api/v1/ItemSearch#searchItem">/v1/itemSearch</a> with a narrower OAuth scope.

        :param term: The search term to look for. Minimum 2 characters (or 1 if using `exact_match`). Please note that the search term has to be URL encoded.
        :type term: str
        :param fields: A comma-separated string array. The fields to perform the search from. Defaults to all of them. Only the following custom field types are searchable: `address`, `varchar`, `text`, `varchar_auto`, `double`, `monetary` and `phone`. Read more about searching by custom fields <a href="https://support.pipedrive.com/en/article/search-finding-what-you-need#searching-by-custom-fields" target="_blank" rel="noopener noreferrer">here</a>., defaults to None
        :type fields: SearchProductsFields, optional
        :param exact_match: When enabled, only full exact matches against the given term are returned. It is <b>not</b> case sensitive., defaults to None
        :type exact_match: bool, optional
        :param include_fields: Supports including optional fields in the results which are not provided by default, defaults to None
        :type include_fields: SearchProductsIncludeFields, optional
        :param start: Pagination start. Note that the pagination is based on main results and does not include related items when using `search_for_related_items` parameter., defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: SearchProductsOkResponse
        """

        Validator(str).validate(term)
        Validator(SearchProductsFields).is_optional().validate(fields)
        Validator(bool).is_optional().validate(exact_match)
        Validator(SearchProductsIncludeFields).is_optional().validate(include_fields)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/products/search", self.get_default_headers())
            .add_query("term", term)
            .add_query("fields", fields)
            .add_query("exact_match", exact_match)
            .add_query("include_fields", include_fields)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return SearchProductsOkResponse._unmap(response)

    @cast_models
    def get_product(self, id_: int) -> GetProductOkResponse:
        """Returns data about a specific product.

        :param id_: The ID of the product
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get product information by id
        :rtype: GetProductOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/products/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProductOkResponse._unmap(response)

    @cast_models
    def update_product(
        self, id_: int, request_body: UpdateProductRequest = None
    ) -> UpdateProductOkResponse:
        """Updates product data.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateProductRequest, optional
        :param id_: The ID of the product
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Updates product data
        :rtype: UpdateProductOkResponse
        """

        Validator(UpdateProductRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/products/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateProductOkResponse._unmap(response)

    @cast_models
    def delete_product(self, id_: int) -> DeleteProductOkResponse:
        """Marks a product as deleted. After 30 days, the product will be permanently deleted.

        :param id_: The ID of the product
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Deletes a product
        :rtype: DeleteProductOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/products/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteProductOkResponse._unmap(response)

    @cast_models
    def get_product_deals(
        self,
        id_: int,
        start: int = None,
        limit: int = None,
        status: GetProductDealsStatus = None,
    ) -> GetProductDealsOkResponse:
        """Returns data about deals that have a product attached to it.

        :param id_: The ID of the product
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param status: Only fetch deals with a specific status. If omitted, all not deleted deals are returned. If set to deleted, deals that have been deleted up to 30 days ago will be included., defaults to None
        :type status: GetProductDealsStatus, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The data of deals that have a product attached
        :rtype: GetProductDealsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(GetProductDealsStatus).is_optional().validate(status)

        serialized_request = (
            Serializer(
                f"{self.base_url}/products/{{id}}/deals", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("status", status)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProductDealsOkResponse._unmap(response)

    @cast_models
    def get_product_files(
        self, id_: int, start: int = None, limit: int = None, sort: str = None
    ) -> GetProductFilesOkResponse:
        """Lists files associated with a product.

        :param id_: The ID of the product
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param sort: The field name and sorting mode (`field_name_1 ASC` or `field_name_1 DESC`). Supported fields: `update_time`, `id`., defaults to None
        :type sort: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetProductFilesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(sort)

        serialized_request = (
            Serializer(
                f"{self.base_url}/products/{{id}}/files", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("sort", sort)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProductFilesOkResponse._unmap(response)

    @cast_models
    def get_product_followers(
        self, id_: int, start: int = None, limit: int = None
    ) -> GetProductFollowersOkResponse:
        """Lists the followers of a product.

        :param id_: The ID of the product
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Lists the followers of a product
        :rtype: GetProductFollowersOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/products/{{id}}/followers", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProductFollowersOkResponse._unmap(response)

    @cast_models
    def add_product_follower(
        self, id_: int, request_body: AddProductFollowerRequest = None
    ) -> AddProductFollowerCreatedResponse:
        """Adds a follower to a product.

        :param request_body: The request body., defaults to None
        :type request_body: AddProductFollowerRequest, optional
        :param id_: The ID of the product
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Adds a follower to a product
        :rtype: AddProductFollowerCreatedResponse
        """

        Validator(AddProductFollowerRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/products/{{id}}/followers", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddProductFollowerCreatedResponse._unmap(response)

    @cast_models
    def delete_product_follower(
        self, id_: int, follower_id: int
    ) -> DeleteProductFollowerOkResponse:
        """Deletes a follower from a product.

        :param id_: The ID of the product
        :type id_: int
        :param follower_id: The ID of the relationship between the follower and the product
        :type follower_id: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Deletes a follower from a product
        :rtype: DeleteProductFollowerOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).validate(follower_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/products/{{id}}/followers/{{follower_id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("follower_id", follower_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteProductFollowerOkResponse._unmap(response)

    @cast_models
    def get_product_users(self, id_: int) -> GetProductUsersOkResponse:
        """Lists users permitted to access a product.

        :param id_: The ID of the product
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Lists users permitted to access a product
        :rtype: GetProductUsersOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/products/{{id}}/permittedUsers",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProductUsersOkResponse._unmap(response)
