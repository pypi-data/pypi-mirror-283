from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_organization_request import UpdateOrganizationRequest
from ..models.update_organization_ok_response import UpdateOrganizationOkResponse
from ..models.search_organization_ok_response import SearchOrganizationOkResponse
from ..models.search_organization_fields import SearchOrganizationFields
from ..models.only_primary_association import OnlyPrimaryAssociation
from ..models.merge_organizations_request import MergeOrganizationsRequest
from ..models.merge_organizations_ok_response import MergeOrganizationsOkResponse
from ..models.get_organizations_ok_response import GetOrganizationsOkResponse
from ..models.get_organizations_collection_ok_response import (
    GetOrganizationsCollectionOkResponse,
)
from ..models.get_organization_users_ok_response import GetOrganizationUsersOkResponse
from ..models.get_organization_updates_ok_response import (
    GetOrganizationUpdatesOkResponse,
)
from ..models.get_organization_persons_ok_response import (
    GetOrganizationPersonsOkResponse,
)
from ..models.get_organization_ok_response import GetOrganizationOkResponse
from ..models.get_organization_mail_messages_ok_response import (
    GetOrganizationMailMessagesOkResponse,
)
from ..models.get_organization_followers_ok_response import (
    GetOrganizationFollowersOkResponse,
)
from ..models.get_organization_files_ok_response import GetOrganizationFilesOkResponse
from ..models.get_organization_deals_status import GetOrganizationDealsStatus
from ..models.get_organization_deals_ok_response import GetOrganizationDealsOkResponse
from ..models.get_organization_changelog_ok_response import (
    GetOrganizationChangelogOkResponse,
)
from ..models.get_organization_activities_ok_response import (
    GetOrganizationActivitiesOkResponse,
)
from ..models.get_organization_activities_done import GetOrganizationActivitiesDone
from ..models.delete_organizations_ok_response import DeleteOrganizationsOkResponse
from ..models.delete_organization_ok_response import DeleteOrganizationOkResponse
from ..models.delete_organization_follower_ok_response import (
    DeleteOrganizationFollowerOkResponse,
)
from ..models.add_organization_request import AddOrganizationRequest
from ..models.add_organization_follower_request import AddOrganizationFollowerRequest
from ..models.add_organization_follower_ok_response import (
    AddOrganizationFollowerOkResponse,
)
from ..models.add_organization_created_response import AddOrganizationCreatedResponse


class OrganizationsService(BaseService):

    @cast_models
    def get_organizations(
        self,
        user_id: int = None,
        filter_id: int = None,
        first_char: str = None,
        start: int = None,
        limit: int = None,
        sort: str = None,
    ) -> GetOrganizationsOkResponse:
        """Returns all organizations.

        :param user_id: If supplied, only organizations owned by the given user will be returned. However, `filter_id` takes precedence over `user_id` when both are supplied., defaults to None
        :type user_id: int, optional
        :param filter_id: The ID of the filter to use, defaults to None
        :type filter_id: int, optional
        :param first_char: If supplied, only organizations whose name starts with the specified letter will be returned (case-insensitive), defaults to None
        :type first_char: str, optional
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param sort: The field names and sorting mode separated by a comma (`field_name_1 ASC`, `field_name_2 DESC`). Only first-level field keys are supported (no nested keys)., defaults to None
        :type sort: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationsOkResponse
        """

        Validator(int).is_optional().validate(user_id)
        Validator(int).is_optional().validate(filter_id)
        Validator(str).is_optional().validate(first_char)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(sort)

        serialized_request = (
            Serializer(f"{self.base_url}/organizations", self.get_default_headers())
            .add_query("user_id", user_id)
            .add_query("filter_id", filter_id)
            .add_query("first_char", first_char)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("sort", sort)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationsOkResponse._unmap(response)

    @cast_models
    def add_organization(
        self, request_body: AddOrganizationRequest = None
    ) -> AddOrganizationCreatedResponse:
        """Adds a new organization. Note that you can supply additional custom fields along with the request that are not described here. These custom fields are different for each Pipedrive account and can be recognized by long hashes as keys. To determine which custom fields exists, fetch the organizationFields and look for `key` values. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/adding-an-organization" target="_blank" rel="noopener noreferrer">adding an organization</a>.

        :param request_body: The request body., defaults to None
        :type request_body: AddOrganizationRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: AddOrganizationCreatedResponse
        """

        Validator(AddOrganizationRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/organizations", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddOrganizationCreatedResponse._unmap(response)

    @cast_models
    def delete_organizations(self, ids: str) -> DeleteOrganizationsOkResponse:
        """Marks multiple organizations as deleted. After 30 days, the organizations will be permanently deleted.

        :param ids: The comma-separated IDs that will be deleted
        :type ids: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteOrganizationsOkResponse
        """

        Validator(str).validate(ids)

        serialized_request = (
            Serializer(f"{self.base_url}/organizations", self.get_default_headers())
            .add_query("ids", ids)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteOrganizationsOkResponse._unmap(response)

    @cast_models
    def get_organizations_collection(
        self,
        cursor: str = None,
        limit: int = None,
        since: str = None,
        until: str = None,
        owner_id: int = None,
        first_char: str = None,
    ) -> GetOrganizationsCollectionOkResponse:
        """Returns all organizations. This is a cursor-paginated endpoint that is currently in BETA. For more information, please refer to our documentation on <a href="https://pipedrive.readme.io/docs/core-api-concepts-pagination" target="_blank" rel="noopener noreferrer">pagination</a>. Please note that only global admins (those with global permissions) can access these endpoints. Users with regular permissions will receive a 403 response. Read more about global permissions <a href="https://support.pipedrive.com/en/article/global-user-management" target="_blank" rel="noopener noreferrer">here</a>.

        :param cursor: For pagination, the marker (an opaque string value) representing the first item on the next page, defaults to None
        :type cursor: str, optional
        :param limit: For pagination, the limit of entries to be returned. If not provided, 100 items will be returned. Please note that a maximum value of 500 is allowed., defaults to None
        :type limit: int, optional
        :param since: The time boundary that points to the start of the range of data. Datetime in ISO 8601 format. E.g. 2022-11-01 08:55:59. Operates on the `update_time` field., defaults to None
        :type since: str, optional
        :param until: The time boundary that points to the end of the range of data. Datetime in ISO 8601 format. E.g. 2022-11-01 08:55:59. Operates on the `update_time` field., defaults to None
        :type until: str, optional
        :param owner_id: If supplied, only organizations owned by the given user will be returned, defaults to None
        :type owner_id: int, optional
        :param first_char: If supplied, only organizations whose name starts with the specified letter will be returned (case-insensitive), defaults to None
        :type first_char: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationsCollectionOkResponse
        """

        Validator(str).is_optional().validate(cursor)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(since)
        Validator(str).is_optional().validate(until)
        Validator(int).is_optional().validate(owner_id)
        Validator(str).is_optional().validate(first_char)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/collection", self.get_default_headers()
            )
            .add_query("cursor", cursor)
            .add_query("limit", limit)
            .add_query("since", since)
            .add_query("until", until)
            .add_query("owner_id", owner_id)
            .add_query("first_char", first_char)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationsCollectionOkResponse._unmap(response)

    @cast_models
    def search_organization(
        self,
        term: str,
        fields: SearchOrganizationFields = None,
        exact_match: bool = None,
        start: int = None,
        limit: int = None,
    ) -> SearchOrganizationOkResponse:
        """Searches all organizations by name, address, notes and/or custom fields. This endpoint is a wrapper of <a href="https://developers.pipedrive.com/docs/api/v1/ItemSearch#searchItem">/v1/itemSearch</a> with a narrower OAuth scope.

        :param term: The search term to look for. Minimum 2 characters (or 1 if using `exact_match`). Please note that the search term has to be URL encoded.
        :type term: str
        :param fields: A comma-separated string array. The fields to perform the search from. Defaults to all of them. Only the following custom field types are searchable: `address`, `varchar`, `text`, `varchar_auto`, `double`, `monetary` and `phone`. Read more about searching by custom fields <a href="https://support.pipedrive.com/en/article/search-finding-what-you-need#searching-by-custom-fields" target="_blank" rel="noopener noreferrer">here</a>., defaults to None
        :type fields: SearchOrganizationFields, optional
        :param exact_match: When enabled, only full exact matches against the given term are returned. It is <b>not</b> case sensitive., defaults to None
        :type exact_match: bool, optional
        :param start: Pagination start. Note that the pagination is based on main results and does not include related items when using `search_for_related_items` parameter., defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: SearchOrganizationOkResponse
        """

        Validator(str).validate(term)
        Validator(SearchOrganizationFields).is_optional().validate(fields)
        Validator(bool).is_optional().validate(exact_match)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/search", self.get_default_headers()
            )
            .add_query("term", term)
            .add_query("fields", fields)
            .add_query("exact_match", exact_match)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return SearchOrganizationOkResponse._unmap(response)

    @cast_models
    def get_organization(self, id_: int) -> GetOrganizationOkResponse:
        """Returns the details of an organization. Note that this also returns some additional fields which are not present when asking for all organizations. Also note that custom fields appear as long hashes in the resulting data. These hashes can be mapped against the `key` value of organizationFields.

        :param id_: The ID of the organization
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationOkResponse._unmap(response)

    @cast_models
    def update_organization(
        self, id_: int, request_body: UpdateOrganizationRequest = None
    ) -> UpdateOrganizationOkResponse:
        """Updates the properties of an organization.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateOrganizationRequest, optional
        :param id_: The ID of the organization
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateOrganizationOkResponse
        """

        Validator(UpdateOrganizationRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateOrganizationOkResponse._unmap(response)

    @cast_models
    def delete_organization(self, id_: int) -> DeleteOrganizationOkResponse:
        """Marks an organization as deleted. After 30 days, the organization will be permanently deleted.

        :param id_: The ID of the organization
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteOrganizationOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteOrganizationOkResponse._unmap(response)

    @cast_models
    def get_organization_activities(
        self,
        id_: int,
        start: int = None,
        limit: int = None,
        done: GetOrganizationActivitiesDone = None,
        exclude: str = None,
    ) -> GetOrganizationActivitiesOkResponse:
        """Lists activities associated with an organization.

        :param id_: The ID of the organization
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param done: Whether the activity is done or not. 0 = Not done, 1 = Done. If omitted returns both Done and Not done activities., defaults to None
        :type done: GetOrganizationActivitiesDone, optional
        :param exclude: A comma-separated string of activity IDs to exclude from result, defaults to None
        :type exclude: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationActivitiesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(GetOrganizationActivitiesDone).is_optional().validate(done)
        Validator(str).is_optional().validate(exclude)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}/activities",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("done", done)
            .add_query("exclude", exclude)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationActivitiesOkResponse._unmap(response)

    @cast_models
    def get_organization_changelog(
        self, id_: int, cursor: str = None, limit: int = None
    ) -> GetOrganizationChangelogOkResponse:
        """Lists updates about field values of an organization.

        :param id_: The ID of the organization
        :type id_: int
        :param cursor: For pagination, the marker (an opaque string value) representing the first item on the next page, defaults to None
        :type cursor: str, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get changelog of an organization
        :rtype: GetOrganizationChangelogOkResponse
        """

        Validator(int).validate(id_)
        Validator(str).is_optional().validate(cursor)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}/changelog",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("cursor", cursor)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationChangelogOkResponse._unmap(response)

    @cast_models
    def get_organization_deals(
        self,
        id_: int,
        start: int = None,
        limit: int = None,
        status: GetOrganizationDealsStatus = None,
        sort: str = None,
        only_primary_association: OnlyPrimaryAssociation = None,
    ) -> GetOrganizationDealsOkResponse:
        """Lists deals associated with an organization.

        :param id_: The ID of the organization
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param status: Only fetch deals with a specific status. If omitted, all not deleted deals are returned. If set to deleted, deals that have been deleted up to 30 days ago will be included., defaults to None
        :type status: GetOrganizationDealsStatus, optional
        :param sort: The field names and sorting mode separated by a comma (`field_name_1 ASC`, `field_name_2 DESC`). Only first-level field keys are supported (no nested keys)., defaults to None
        :type sort: str, optional
        :param only_primary_association: If set, only deals that are directly associated to the organization are fetched. If not set (default), all deals are fetched that are either directly or indirectly related to the organization. Indirect relations include relations through custom, organization-type fields and through persons of the given organization., defaults to None
        :type only_primary_association: OnlyPrimaryAssociation, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationDealsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(GetOrganizationDealsStatus).is_optional().validate(status)
        Validator(str).is_optional().validate(sort)
        Validator(OnlyPrimaryAssociation).is_optional().validate(
            only_primary_association
        )

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}/deals",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("status", status)
            .add_query("sort", sort)
            .add_query("only_primary_association", only_primary_association)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationDealsOkResponse._unmap(response)

    @cast_models
    def get_organization_files(
        self, id_: int, start: int = None, limit: int = None, sort: str = None
    ) -> GetOrganizationFilesOkResponse:
        """Lists files associated with an organization.

        :param id_: The ID of the organization
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param sort: The field names and sorting mode separated by a comma (`field_name_1 ASC`, `field_name_2 DESC`). Only first-level field keys are supported (no nested keys). Supported fields: `id`, `user_id`, `deal_id`, `person_id`, `org_id`, `product_id`, `add_time`, `update_time`, `file_name`, `file_type`, `file_size`, `comment`., defaults to None
        :type sort: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationFilesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(sort)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}/files",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("sort", sort)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationFilesOkResponse._unmap(response)

    @cast_models
    def get_organization_updates(
        self,
        id_: int,
        start: int = None,
        limit: int = None,
        all_changes: str = None,
        items: str = None,
    ) -> GetOrganizationUpdatesOkResponse:
        """Lists updates about an organization.

        :param id_: The ID of the organization
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param all_changes: Whether to show custom field updates or not. 1 = Include custom field changes. If omitted, returns changes without custom field updates., defaults to None
        :type all_changes: str, optional
        :param items: A comma-separated string for filtering out item specific updates. (Possible values - activity, plannedActivity, note, file, change, deal, follower, participant, mailMessage, mailMessageWithAttachment, invoice, activityFile, document)., defaults to None
        :type items: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get the organization updates
        :rtype: GetOrganizationUpdatesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(all_changes)
        Validator(str).is_optional().validate(items)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}/flow", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("all_changes", all_changes)
            .add_query("items", items)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationUpdatesOkResponse._unmap(response)

    @cast_models
    def get_organization_followers(
        self, id_: int
    ) -> GetOrganizationFollowersOkResponse:
        """Lists the followers of an organization.

        :param id_: The ID of the organization
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationFollowersOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}/followers",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationFollowersOkResponse._unmap(response)

    @cast_models
    def add_organization_follower(
        self, id_: int, request_body: AddOrganizationFollowerRequest = None
    ) -> AddOrganizationFollowerOkResponse:
        """Adds a follower to an organization.

        :param request_body: The request body., defaults to None
        :type request_body: AddOrganizationFollowerRequest, optional
        :param id_: The ID of the organization
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: AddOrganizationFollowerOkResponse
        """

        Validator(AddOrganizationFollowerRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}/followers",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddOrganizationFollowerOkResponse._unmap(response)

    @cast_models
    def delete_organization_follower(
        self, id_: int, follower_id: int
    ) -> DeleteOrganizationFollowerOkResponse:
        """Deletes a follower from an organization. You can retrieve the `follower_id` from the <a href="https://developers.pipedrive.com/docs/api/v1/Organizations#getOrganizationFollowers">List followers of an organization</a> endpoint.

        :param id_: The ID of the organization
        :type id_: int
        :param follower_id: The ID of the follower
        :type follower_id: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteOrganizationFollowerOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).validate(follower_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}/followers/{{follower_id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("follower_id", follower_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteOrganizationFollowerOkResponse._unmap(response)

    @cast_models
    def get_organization_mail_messages(
        self, id_: int, start: int = None, limit: int = None
    ) -> GetOrganizationMailMessagesOkResponse:
        """Lists mail messages associated with an organization.

        :param id_: The ID of the organization
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationMailMessagesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}/mailMessages",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationMailMessagesOkResponse._unmap(response)

    @cast_models
    def merge_organizations(
        self, id_: int, request_body: MergeOrganizationsRequest = None
    ) -> MergeOrganizationsOkResponse:
        """Merges an organization with another organization. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/merging-two-organizations" target="_blank" rel="noopener noreferrer">merging two organizations</a>.

        :param request_body: The request body., defaults to None
        :type request_body: MergeOrganizationsRequest, optional
        :param id_: The ID of the organization
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: MergeOrganizationsOkResponse
        """

        Validator(MergeOrganizationsRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}/merge",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return MergeOrganizationsOkResponse._unmap(response)

    @cast_models
    def get_organization_users(self, id_: int) -> GetOrganizationUsersOkResponse:
        """List users permitted to access an organization.

        :param id_: The ID of the organization
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationUsersOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}/permittedUsers",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationUsersOkResponse._unmap(response)

    @cast_models
    def get_organization_persons(
        self, id_: int, start: int = None, limit: int = None
    ) -> GetOrganizationPersonsOkResponse:
        """Lists persons associated with an organization.<br>If a company uses the [Campaigns product](https://pipedrive.readme.io/docs/campaigns-in-pipedrive-api), then this endpoint will also return the `data.marketing_status` field.

        :param id_: The ID of the organization
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationPersonsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizations/{{id}}/persons",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationPersonsOkResponse._unmap(response)
