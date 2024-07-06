from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.search_item_ok_response import SearchItemOkResponse
from ..models.search_item_include_fields import SearchItemIncludeFields
from ..models.search_item_fields import SearchItemFields
from ..models.search_item_by_field_ok_response import SearchItemByFieldOkResponse
from ..models.search_item_by_field_field_type import SearchItemByFieldFieldType
from ..models.item_types import ItemTypes


class ItemSearchService(BaseService):

    @cast_models
    def search_item(
        self,
        term: str,
        item_types: ItemTypes = None,
        fields: SearchItemFields = None,
        search_for_related_items: bool = None,
        exact_match: bool = None,
        include_fields: SearchItemIncludeFields = None,
        start: int = None,
        limit: int = None,
    ) -> SearchItemOkResponse:
        """Performs a search from your choice of item types and fields.

        :param term: The search term to look for. Minimum 2 characters (or 1 if using `exact_match`). Please note that the search term has to be URL encoded.
        :type term: str
        :param item_types: A comma-separated string array. The type of items to perform the search from. Defaults to all., defaults to None
        :type item_types: ItemTypes, optional
        :param fields: A comma-separated string array. The fields to perform the search from. Defaults to all. Relevant for each item type are:<br> <table> <tr><th><b>Item type</b></th><th><b>Field</b></th></tr> <tr><td>Deal</td><td>`custom_fields`, `notes`, `title`</td></tr> <tr><td>Person</td><td>`custom_fields`, `email`, `name`, `notes`, `phone`</td></tr> <tr><td>Organization</td><td>`address`, `custom_fields`, `name`, `notes`</td></tr> <tr><td>Product</td><td>`code`, `custom_fields`, `name`</td></tr> <tr><td>Lead</td><td>`custom_fields`, `notes`, `email`, `organization_name`, `person_name`, `phone`, `title`</td></tr> <tr><td>File</td><td>`name`</td></tr> <tr><td>Mail attachment</td><td>`name`</td></tr> <tr><td>Project</td><td> `custom_fields`, `notes`, `title`, `description` </td></tr> </table> <br> Only the following custom field types are searchable: `address`, `varchar`, `text`, `varchar_auto`, `double`, `monetary` and `phone`. Read more about searching by custom fields <a href="https://support.pipedrive.com/en/article/search-finding-what-you-need#searching-by-custom-fields" target="_blank" rel="noopener noreferrer">here</a>.<br/> When searching for leads, the email, organization_name, person_name, and phone fields will return results only for leads not linked to contacts. For searching leads by person or organization values, please use `search_for_related_items`., defaults to None
        :type fields: SearchItemFields, optional
        :param search_for_related_items: When enabled, the response will include up to 100 newest related leads and 100 newest related deals for each found person and organization and up to 100 newest related persons for each found organization, defaults to None
        :type search_for_related_items: bool, optional
        :param exact_match: When enabled, only full exact matches against the given term are returned. It is <b>not</b> case sensitive., defaults to None
        :type exact_match: bool, optional
        :param include_fields: A comma-separated string array. Supports including optional fields in the results which are not provided by default., defaults to None
        :type include_fields: SearchItemIncludeFields, optional
        :param start: Pagination start. Note that the pagination is based on main results and does not include related items when using `search_for_related_items` parameter., defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: SearchItemOkResponse
        """

        Validator(str).validate(term)
        Validator(ItemTypes).is_optional().validate(item_types)
        Validator(SearchItemFields).is_optional().validate(fields)
        Validator(bool).is_optional().validate(search_for_related_items)
        Validator(bool).is_optional().validate(exact_match)
        Validator(SearchItemIncludeFields).is_optional().validate(include_fields)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/itemSearch", self.get_default_headers())
            .add_query("term", term)
            .add_query("item_types", item_types)
            .add_query("fields", fields)
            .add_query("search_for_related_items", search_for_related_items)
            .add_query("exact_match", exact_match)
            .add_query("include_fields", include_fields)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return SearchItemOkResponse._unmap(response)

    @cast_models
    def search_item_by_field(
        self,
        term: str,
        field_type: SearchItemByFieldFieldType,
        field_key: str,
        exact_match: bool = None,
        return_item_ids: bool = None,
        start: int = None,
        limit: int = None,
    ) -> SearchItemByFieldOkResponse:
        """Performs a search from the values of a specific field. Results can either be the distinct values of the field (useful for searching autocomplete field values), or the IDs of actual items (deals, leads, persons, organizations or products).

        :param term: The search term to look for. Minimum 2 characters (or 1 if using `exact_match`). Please note that the search term has to be URL encoded.
        :type term: str
        :param field_type: The type of the field to perform the search from
        :type field_type: SearchItemByFieldFieldType
        :param field_key: The key of the field to search from. The field key can be obtained by fetching the list of the fields using any of the fields' API GET methods (dealFields, personFields, etc.). Only the following custom field types are searchable: `address`, `varchar`, `text`, `varchar_auto`, `double`, `monetary` and `phone`. Read more about searching by custom fields <a href="https://support.pipedrive.com/en/article/search-finding-what-you-need#searching-by-custom-fields" target="_blank" rel="noopener noreferrer">here</a>.
        :type field_key: str
        :param exact_match: When enabled, only full exact matches against the given term are returned. The search <b>is</b> case sensitive., defaults to None
        :type exact_match: bool, optional
        :param return_item_ids: Whether to return the IDs of the matching items or not. When not set or set to `0` or `false`, only distinct values of the searched field are returned. When set to `1` or `true`, the ID of each found item is returned., defaults to None
        :type return_item_ids: bool, optional
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: SearchItemByFieldOkResponse
        """

        Validator(str).validate(term)
        Validator(SearchItemByFieldFieldType).validate(field_type)
        Validator(str).validate(field_key)
        Validator(bool).is_optional().validate(exact_match)
        Validator(bool).is_optional().validate(return_item_ids)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/itemSearch/field", self.get_default_headers())
            .add_query("term", term)
            .add_query("field_type", field_type)
            .add_query("exact_match", exact_match)
            .add_query("field_key", field_key)
            .add_query("return_item_ids", return_item_ids)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return SearchItemByFieldOkResponse._unmap(response)
