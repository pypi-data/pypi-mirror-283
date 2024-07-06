from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_lead_request import UpdateLeadRequest
from ..models.update_lead_ok_response import UpdateLeadOkResponse
from ..models.sort import Sort
from ..models.search_leads_ok_response import SearchLeadsOkResponse
from ..models.search_leads_include_fields import SearchLeadsIncludeFields
from ..models.search_leads_fields import SearchLeadsFields
from ..models.get_leads_ok_response import GetLeadsOkResponse
from ..models.get_lead_users_ok_response import GetLeadUsersOkResponse
from ..models.get_lead_ok_response import GetLeadOkResponse
from ..models.delete_lead_ok_response import DeleteLeadOkResponse
from ..models.archived_status import ArchivedStatus
from ..models.add_lead_request import AddLeadRequest
from ..models.add_lead_created_response import AddLeadCreatedResponse


class LeadsService(BaseService):

    @cast_models
    def get_leads(
        self,
        limit: int = None,
        start: int = None,
        archived_status: ArchivedStatus = None,
        owner_id: int = None,
        person_id: int = None,
        organization_id: int = None,
        filter_id: int = None,
        sort: Sort = None,
    ) -> GetLeadsOkResponse:
        """Returns multiple leads. Leads are sorted by the time they were created, from oldest to newest. Pagination can be controlled using `limit` and `start` query parameters. If a lead contains custom fields, the fields' values will be included in the response in the same format as with the `Deals` endpoints. If a custom field's value hasn't been set for the lead, it won't appear in the response. Please note that leads do not have a separate set of custom fields, instead they inherit the custom fields' structure from deals.

        :param limit: For pagination, the limit of entries to be returned. If not provided, 100 items will be returned., defaults to None
        :type limit: int, optional
        :param start: For pagination, the position that represents the first result for the page, defaults to None
        :type start: int, optional
        :param archived_status: Filtering based on the archived status of a lead. If not provided, `All` is used., defaults to None
        :type archived_status: ArchivedStatus, optional
        :param owner_id: If supplied, only leads matching the given user will be returned. However, `filter_id` takes precedence over `owner_id` when supplied., defaults to None
        :type owner_id: int, optional
        :param person_id: If supplied, only leads matching the given person will be returned. However, `filter_id` takes precedence over `person_id` when supplied., defaults to None
        :type person_id: int, optional
        :param organization_id: If supplied, only leads matching the given organization will be returned. However, `filter_id` takes precedence over `organization_id` when supplied., defaults to None
        :type organization_id: int, optional
        :param filter_id: The ID of the filter to use, defaults to None
        :type filter_id: int, optional
        :param sort: The field names and sorting mode separated by a comma (`field_name_1 ASC`, `field_name_2 DESC`). Only first-level field keys are supported (no nested keys)., defaults to None
        :type sort: Sort, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response containing payload in the `data` field
        :rtype: GetLeadsOkResponse
        """

        Validator(int).is_optional().validate(limit)
        Validator(int).is_optional().validate(start)
        Validator(ArchivedStatus).is_optional().validate(archived_status)
        Validator(int).is_optional().validate(owner_id)
        Validator(int).is_optional().validate(person_id)
        Validator(int).is_optional().validate(organization_id)
        Validator(int).is_optional().validate(filter_id)
        Validator(Sort).is_optional().validate(sort)

        serialized_request = (
            Serializer(f"{self.base_url}/leads", self.get_default_headers())
            .add_query("limit", limit)
            .add_query("start", start)
            .add_query("archived_status", archived_status)
            .add_query("owner_id", owner_id)
            .add_query("person_id", person_id)
            .add_query("organization_id", organization_id)
            .add_query("filter_id", filter_id)
            .add_query("sort", sort)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetLeadsOkResponse._unmap(response)

    @cast_models
    def add_lead(self, request_body: AddLeadRequest = None) -> AddLeadCreatedResponse:
        """Creates a lead. A lead always has to be linked to a person or an organization or both. All leads created through the Pipedrive API will have a lead source and origin set to `API`. Here's the tutorial for <a href="https://pipedrive.readme.io/docs/adding-a-lead" target="_blank" rel="noopener noreferrer">adding a lead</a>. If a lead contains custom fields, the fields' values will be included in the response in the same format as with the `Deals` endpoints. If a custom field's value hasn't been set for the lead, it won't appear in the response. Please note that leads do not have a separate set of custom fields, instead they inherit the custom fields' structure from deals. See an example given in the <a href="https://pipedrive.readme.io/docs/updating-custom-field-value" target="_blank" rel="noopener noreferrer">updating custom fields' values tutorial</a>.

        :param request_body: The request body., defaults to None
        :type request_body: AddLeadRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response containing payload in the `data` field
        :rtype: AddLeadCreatedResponse
        """

        Validator(AddLeadRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/leads", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddLeadCreatedResponse._unmap(response)

    @cast_models
    def get_lead(self, id_: str) -> GetLeadOkResponse:
        """Returns details of a specific lead. If a lead contains custom fields, the fields' values will be included in the response in the same format as with the `Deals` endpoints. If a custom field's value hasn't been set for the lead, it won't appear in the response. Please note that leads do not have a separate set of custom fields, instead they inherit the custom fields’ structure from deals.

        :param id_: The ID of the lead
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response containing payload in the `data` field
        :rtype: GetLeadOkResponse
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/leads/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetLeadOkResponse._unmap(response)

    @cast_models
    def update_lead(
        self, id_: str, request_body: UpdateLeadRequest = None
    ) -> UpdateLeadOkResponse:
        """Updates one or more properties of a lead. Only properties included in the request will be updated. Send `null` to unset a property (applicable for example for `value`, `person_id` or `organization_id`). If a lead contains custom fields, the fields' values will be included in the response in the same format as with the `Deals` endpoints. If a custom field's value hasn't been set for the lead, it won't appear in the response. Please note that leads do not have a separate set of custom fields, instead they inherit the custom fields’ structure from deals. See an example given in the <a href="https://pipedrive.readme.io/docs/updating-custom-field-value" target="_blank" rel="noopener noreferrer">updating custom fields’ values tutorial</a>.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateLeadRequest, optional
        :param id_: The ID of the lead
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response containing payload in the `data` field
        :rtype: UpdateLeadOkResponse
        """

        Validator(UpdateLeadRequest).is_optional().validate(request_body)
        Validator(str).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/leads/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PATCH")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateLeadOkResponse._unmap(response)

    @cast_models
    def delete_lead(self, id_: str) -> DeleteLeadOkResponse:
        """Deletes a specific lead.

        :param id_: The ID of the lead
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response with id value only. Used in DELETE calls.
        :rtype: DeleteLeadOkResponse
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/leads/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteLeadOkResponse._unmap(response)

    @cast_models
    def get_lead_users(self, id_: str) -> GetLeadUsersOkResponse:
        """Lists the users permitted to access a lead.

        :param id_: The ID of the lead
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Lists users permitted to access a lead
        :rtype: GetLeadUsersOkResponse
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/leads/{{id}}/permittedUsers",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetLeadUsersOkResponse._unmap(response)

    @cast_models
    def search_leads(
        self,
        term: str,
        fields: SearchLeadsFields = None,
        exact_match: bool = None,
        person_id: int = None,
        organization_id: int = None,
        include_fields: SearchLeadsIncludeFields = None,
        start: int = None,
        limit: int = None,
    ) -> SearchLeadsOkResponse:
        """Searches all leads by title, notes and/or custom fields. This endpoint is a wrapper of <a href="https://developers.pipedrive.com/docs/api/v1/ItemSearch#searchItem">/v1/itemSearch</a> with a narrower OAuth scope. Found leads can be filtered by the person ID and the organization ID.

        :param term: The search term to look for. Minimum 2 characters (or 1 if using `exact_match`). Please note that the search term has to be URL encoded.
        :type term: str
        :param fields: A comma-separated string array. The fields to perform the search from. Defaults to all of them., defaults to None
        :type fields: SearchLeadsFields, optional
        :param exact_match: When enabled, only full exact matches against the given term are returned. It is <b>not</b> case sensitive., defaults to None
        :type exact_match: bool, optional
        :param person_id: Will filter leads by the provided person ID. The upper limit of found leads associated with the person is 2000., defaults to None
        :type person_id: int, optional
        :param organization_id: Will filter leads by the provided organization ID. The upper limit of found leads associated with the organization is 2000., defaults to None
        :type organization_id: int, optional
        :param include_fields: Supports including optional fields in the results which are not provided by default, defaults to None
        :type include_fields: SearchLeadsIncludeFields, optional
        :param start: Pagination start. Note that the pagination is based on main results and does not include related items when using `search_for_related_items` parameter., defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: SearchLeadsOkResponse
        """

        Validator(str).validate(term)
        Validator(SearchLeadsFields).is_optional().validate(fields)
        Validator(bool).is_optional().validate(exact_match)
        Validator(int).is_optional().validate(person_id)
        Validator(int).is_optional().validate(organization_id)
        Validator(SearchLeadsIncludeFields).is_optional().validate(include_fields)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/leads/search", self.get_default_headers())
            .add_query("term", term)
            .add_query("fields", fields)
            .add_query("exact_match", exact_match)
            .add_query("person_id", person_id)
            .add_query("organization_id", organization_id)
            .add_query("include_fields", include_fields)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return SearchLeadsOkResponse._unmap(response)
