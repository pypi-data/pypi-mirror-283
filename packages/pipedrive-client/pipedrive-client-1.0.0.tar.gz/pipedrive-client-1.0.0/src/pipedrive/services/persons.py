from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_person_request import UpdatePersonRequest
from ..models.update_person_ok_response import UpdatePersonOkResponse
from ..models.search_persons_ok_response import SearchPersonsOkResponse
from ..models.search_persons_include_fields import SearchPersonsIncludeFields
from ..models.search_persons_fields import SearchPersonsFields
from ..models.merge_persons_request import MergePersonsRequest
from ..models.merge_persons_ok_response import MergePersonsOkResponse
from ..models.get_persons_ok_response import GetPersonsOkResponse
from ..models.get_persons_collection_ok_response import GetPersonsCollectionOkResponse
from ..models.get_person_users_ok_response import GetPersonUsersOkResponse
from ..models.get_person_updates_ok_response import GetPersonUpdatesOkResponse
from ..models.get_person_products_ok_response import GetPersonProductsOkResponse
from ..models.get_person_ok_response import GetPersonOkResponse
from ..models.get_person_mail_messages_ok_response import (
    GetPersonMailMessagesOkResponse,
)
from ..models.get_person_followers_ok_response import GetPersonFollowersOkResponse
from ..models.get_person_files_ok_response import GetPersonFilesOkResponse
from ..models.get_person_deals_status import GetPersonDealsStatus
from ..models.get_person_deals_ok_response import GetPersonDealsOkResponse
from ..models.get_person_changelog_ok_response import GetPersonChangelogOkResponse
from ..models.get_person_activities_ok_response import GetPersonActivitiesOkResponse
from ..models.get_person_activities_done import GetPersonActivitiesDone
from ..models.delete_persons_ok_response import DeletePersonsOkResponse
from ..models.delete_person_picture_ok_response import DeletePersonPictureOkResponse
from ..models.delete_person_ok_response import DeletePersonOkResponse
from ..models.delete_person_follower_ok_response import DeletePersonFollowerOkResponse
from ..models.add_person_request import AddPersonRequest
from ..models.add_person_picture_request import AddPersonPictureRequest
from ..models.add_person_picture_ok_response import AddPersonPictureOkResponse
from ..models.add_person_follower_request import AddPersonFollowerRequest
from ..models.add_person_follower_ok_response import AddPersonFollowerOkResponse
from ..models.add_person_created_response import AddPersonCreatedResponse


class PersonsService(BaseService):

    @cast_models
    def get_persons(
        self,
        user_id: int = None,
        filter_id: int = None,
        first_char: str = None,
        start: int = None,
        limit: int = None,
        sort: str = None,
    ) -> GetPersonsOkResponse:
        """Returns all persons.

        :param user_id: If supplied, only persons owned by the given user will be returned. However, `filter_id` takes precedence over `user_id` when both are supplied., defaults to None
        :type user_id: int, optional
        :param filter_id: The ID of the filter to use, defaults to None
        :type filter_id: int, optional
        :param first_char: If supplied, only persons whose name starts with the specified letter will be returned (case-insensitive), defaults to None
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
        :rtype: GetPersonsOkResponse
        """

        Validator(int).is_optional().validate(user_id)
        Validator(int).is_optional().validate(filter_id)
        Validator(str).is_optional().validate(first_char)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(sort)

        serialized_request = (
            Serializer(f"{self.base_url}/persons", self.get_default_headers())
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

        return GetPersonsOkResponse._unmap(response)

    @cast_models
    def add_person(
        self, request_body: AddPersonRequest = None
    ) -> AddPersonCreatedResponse:
        """Adds a new person. Note that you can supply additional custom fields along with the request that are not described here. These custom fields are different for each Pipedrive account and can be recognized by long hashes as keys. To determine which custom fields exists, fetch the personFields and look for `key` values.<br>If a company uses the [Campaigns product](https://pipedrive.readme.io/docs/campaigns-in-pipedrive-api), then this endpoint will also accept and return the `data.marketing_status` field.

        :param request_body: The request body., defaults to None
        :type request_body: AddPersonRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: AddPersonCreatedResponse
        """

        Validator(AddPersonRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/persons", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddPersonCreatedResponse._unmap(response)

    @cast_models
    def delete_persons(self, ids: str) -> DeletePersonsOkResponse:
        """Marks multiple persons as deleted. After 30 days, the persons will be permanently deleted.

        :param ids: The comma-separated IDs that will be deleted
        :type ids: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeletePersonsOkResponse
        """

        Validator(str).validate(ids)

        serialized_request = (
            Serializer(f"{self.base_url}/persons", self.get_default_headers())
            .add_query("ids", ids)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeletePersonsOkResponse._unmap(response)

    @cast_models
    def get_persons_collection(
        self,
        cursor: str = None,
        limit: int = None,
        since: str = None,
        until: str = None,
        owner_id: int = None,
        first_char: str = None,
    ) -> GetPersonsCollectionOkResponse:
        """Returns all persons. This is a cursor-paginated endpoint that is currently in BETA. For more information, please refer to our documentation on <a href="https://pipedrive.readme.io/docs/core-api-concepts-pagination" target="_blank" rel="noopener noreferrer">pagination</a>. Please note that only global admins (those with global permissions) can access these endpoints. Users with regular permissions will receive a 403 response. Read more about global permissions <a href="https://support.pipedrive.com/en/article/global-user-management" target="_blank" rel="noopener noreferrer">here</a>.

        :param cursor: For pagination, the marker (an opaque string value) representing the first item on the next page, defaults to None
        :type cursor: str, optional
        :param limit: For pagination, the limit of entries to be returned. If not provided, 100 items will be returned. Please note that a maximum value of 500 is allowed., defaults to None
        :type limit: int, optional
        :param since: The time boundary that points to the start of the range of data. Datetime in ISO 8601 format. E.g. 2022-11-01 08:55:59. Operates on the `update_time` field., defaults to None
        :type since: str, optional
        :param until: The time boundary that points to the end of the range of data. Datetime in ISO 8601 format. E.g. 2022-11-01 08:55:59. Operates on the `update_time` field., defaults to None
        :type until: str, optional
        :param owner_id: If supplied, only persons owned by the given user will be returned, defaults to None
        :type owner_id: int, optional
        :param first_char: If supplied, only persons whose name starts with the specified letter will be returned (case-insensitive), defaults to None
        :type first_char: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetPersonsCollectionOkResponse
        """

        Validator(str).is_optional().validate(cursor)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(since)
        Validator(str).is_optional().validate(until)
        Validator(int).is_optional().validate(owner_id)
        Validator(str).is_optional().validate(first_char)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/collection", self.get_default_headers()
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

        return GetPersonsCollectionOkResponse._unmap(response)

    @cast_models
    def search_persons(
        self,
        term: str,
        fields: SearchPersonsFields = None,
        exact_match: bool = None,
        organization_id: int = None,
        include_fields: SearchPersonsIncludeFields = None,
        start: int = None,
        limit: int = None,
    ) -> SearchPersonsOkResponse:
        """Searches all persons by name, email, phone, notes and/or custom fields. This endpoint is a wrapper of <a href="https://developers.pipedrive.com/docs/api/v1/ItemSearch#searchItem">/v1/itemSearch</a> with a narrower OAuth scope. Found persons can be filtered by organization ID.

        :param term: The search term to look for. Minimum 2 characters (or 1 if using `exact_match`). Please note that the search term has to be URL encoded.
        :type term: str
        :param fields: A comma-separated string array. The fields to perform the search from. Defaults to all of them. Only the following custom field types are searchable: `address`, `varchar`, `text`, `varchar_auto`, `double`, `monetary` and `phone`. Read more about searching by custom fields <a href="https://support.pipedrive.com/en/article/search-finding-what-you-need#searching-by-custom-fields" target="_blank" rel="noopener noreferrer">here</a>., defaults to None
        :type fields: SearchPersonsFields, optional
        :param exact_match: When enabled, only full exact matches against the given term are returned. It is <b>not</b> case sensitive., defaults to None
        :type exact_match: bool, optional
        :param organization_id: Will filter persons by the provided organization ID. The upper limit of found persons associated with the organization is 2000., defaults to None
        :type organization_id: int, optional
        :param include_fields: Supports including optional fields in the results which are not provided by default, defaults to None
        :type include_fields: SearchPersonsIncludeFields, optional
        :param start: Pagination start. Note that the pagination is based on main results and does not include related items when using `search_for_related_items` parameter., defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: SearchPersonsOkResponse
        """

        Validator(str).validate(term)
        Validator(SearchPersonsFields).is_optional().validate(fields)
        Validator(bool).is_optional().validate(exact_match)
        Validator(int).is_optional().validate(organization_id)
        Validator(SearchPersonsIncludeFields).is_optional().validate(include_fields)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/persons/search", self.get_default_headers())
            .add_query("term", term)
            .add_query("fields", fields)
            .add_query("exact_match", exact_match)
            .add_query("organization_id", organization_id)
            .add_query("include_fields", include_fields)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return SearchPersonsOkResponse._unmap(response)

    @cast_models
    def get_person(self, id_: int) -> GetPersonOkResponse:
        """Returns the details of a person. Note that this also returns some additional fields which are not present when asking for all persons. Also note that custom fields appear as long hashes in the resulting data. These hashes can be mapped against the `key` value of personFields.<br>If a company uses the [Campaigns product](https://pipedrive.readme.io/docs/campaigns-in-pipedrive-api), then this endpoint will also return the `data.marketing_status` field.

        :param id_: The ID of the person
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetPersonOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/persons/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPersonOkResponse._unmap(response)

    @cast_models
    def update_person(
        self, id_: int, request_body: UpdatePersonRequest = None
    ) -> UpdatePersonOkResponse:
        """Updates the properties of a person. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/updating-a-person" target="_blank" rel="noopener noreferrer">updating a person</a>.<br>If a company uses the [Campaigns product](https://pipedrive.readme.io/docs/campaigns-in-pipedrive-api), then this endpoint will also accept and return the `data.marketing_status` field.

        :param request_body: The request body., defaults to None
        :type request_body: UpdatePersonRequest, optional
        :param id_: The ID of the person
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdatePersonOkResponse
        """

        Validator(UpdatePersonRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/persons/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdatePersonOkResponse._unmap(response)

    @cast_models
    def delete_person(self, id_: int) -> DeletePersonOkResponse:
        """Marks a person as deleted. After 30 days, the person will be permanently deleted.

        :param id_: The ID of the person
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeletePersonOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/persons/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeletePersonOkResponse._unmap(response)

    @cast_models
    def get_person_activities(
        self,
        id_: int,
        start: int = None,
        limit: int = None,
        done: GetPersonActivitiesDone = None,
        exclude: str = None,
    ) -> GetPersonActivitiesOkResponse:
        """Lists activities associated with a person.

        :param id_: The ID of the person
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param done: Whether the activity is done or not. 0 = Not done, 1 = Done. If omitted, returns both Done and Not done activities., defaults to None
        :type done: GetPersonActivitiesDone, optional
        :param exclude: A comma-separated string of activity IDs to exclude from result, defaults to None
        :type exclude: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetPersonActivitiesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(GetPersonActivitiesDone).is_optional().validate(done)
        Validator(str).is_optional().validate(exclude)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/activities", self.get_default_headers()
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

        return GetPersonActivitiesOkResponse._unmap(response)

    @cast_models
    def get_person_changelog(
        self, id_: int, cursor: str = None, limit: int = None
    ) -> GetPersonChangelogOkResponse:
        """Lists updates about field values of a person.

        :param id_: The ID of the person
        :type id_: int
        :param cursor: For pagination, the marker (an opaque string value) representing the first item on the next page, defaults to None
        :type cursor: str, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get changelog of a person
        :rtype: GetPersonChangelogOkResponse
        """

        Validator(int).validate(id_)
        Validator(str).is_optional().validate(cursor)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/changelog", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("cursor", cursor)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPersonChangelogOkResponse._unmap(response)

    @cast_models
    def get_person_deals(
        self,
        id_: int,
        start: int = None,
        limit: int = None,
        status: GetPersonDealsStatus = None,
        sort: str = None,
    ) -> GetPersonDealsOkResponse:
        """Lists deals associated with a person.

        :param id_: The ID of the person
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param status: Only fetch deals with a specific status. If omitted, all not deleted deals are returned. If set to deleted, deals that have been deleted up to 30 days ago will be included., defaults to None
        :type status: GetPersonDealsStatus, optional
        :param sort: The field names and sorting mode separated by a comma (`field_name_1 ASC`, `field_name_2 DESC`). Only first-level field keys are supported (no nested keys)., defaults to None
        :type sort: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetPersonDealsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(GetPersonDealsStatus).is_optional().validate(status)
        Validator(str).is_optional().validate(sort)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/deals", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("status", status)
            .add_query("sort", sort)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPersonDealsOkResponse._unmap(response)

    @cast_models
    def get_person_files(
        self, id_: int, start: int = None, limit: int = None, sort: str = None
    ) -> GetPersonFilesOkResponse:
        """Lists files associated with a person.

        :param id_: The ID of the person
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
        :rtype: GetPersonFilesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(sort)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/files", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("sort", sort)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPersonFilesOkResponse._unmap(response)

    @cast_models
    def get_person_updates(
        self,
        id_: int,
        start: int = None,
        limit: int = None,
        all_changes: str = None,
        items: str = None,
    ) -> GetPersonUpdatesOkResponse:
        """Lists updates about a person.<br>If a company uses the [Campaigns product](https://pipedrive.readme.io/docs/campaigns-in-pipedrive-api), then this endpoint's response will also include updates for the `marketing_status` field.

        :param id_: The ID of the person
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param all_changes: Whether to show custom field updates or not. 1 = Include custom field changes. If omitted returns changes without custom field updates., defaults to None
        :type all_changes: str, optional
        :param items: A comma-separated string for filtering out item specific updates. (Possible values - call, activity, plannedActivity, change, note, deal, file, dealChange, personChange, organizationChange, follower, dealFollower, personFollower, organizationFollower, participant, comment, mailMessage, mailMessageWithAttachment, invoice, document, marketing_campaign_stat, marketing_status_change)., defaults to None
        :type items: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get the person updates
        :rtype: GetPersonUpdatesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(all_changes)
        Validator(str).is_optional().validate(items)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/flow", self.get_default_headers()
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

        return GetPersonUpdatesOkResponse._unmap(response)

    @cast_models
    def get_person_followers(self, id_: int) -> GetPersonFollowersOkResponse:
        """Lists the followers of a person.

        :param id_: The ID of the person
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetPersonFollowersOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/followers", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPersonFollowersOkResponse._unmap(response)

    @cast_models
    def add_person_follower(
        self, id_: int, request_body: AddPersonFollowerRequest = None
    ) -> AddPersonFollowerOkResponse:
        """Adds a follower to a person.

        :param request_body: The request body., defaults to None
        :type request_body: AddPersonFollowerRequest, optional
        :param id_: The ID of the person
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: AddPersonFollowerOkResponse
        """

        Validator(AddPersonFollowerRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/followers", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddPersonFollowerOkResponse._unmap(response)

    @cast_models
    def delete_person_follower(
        self, id_: int, follower_id: int
    ) -> DeletePersonFollowerOkResponse:
        """Deletes a follower from a person.

        :param id_: The ID of the person
        :type id_: int
        :param follower_id: The ID of the follower
        :type follower_id: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeletePersonFollowerOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).validate(follower_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/followers/{{follower_id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("follower_id", follower_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeletePersonFollowerOkResponse._unmap(response)

    @cast_models
    def get_person_mail_messages(
        self, id_: int, start: int = None, limit: int = None
    ) -> GetPersonMailMessagesOkResponse:
        """Lists mail messages associated with a person.

        :param id_: The ID of the person
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetPersonMailMessagesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/mailMessages",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPersonMailMessagesOkResponse._unmap(response)

    @cast_models
    def merge_persons(
        self, id_: int, request_body: MergePersonsRequest = None
    ) -> MergePersonsOkResponse:
        """Merges a person with another person. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/merging-two-persons" target="_blank" rel="noopener noreferrer">merging two persons</a>.

        :param request_body: The request body., defaults to None
        :type request_body: MergePersonsRequest, optional
        :param id_: The ID of the person
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: MergePersonsOkResponse
        """

        Validator(MergePersonsRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/merge", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return MergePersonsOkResponse._unmap(response)

    @cast_models
    def get_person_users(self, id_: int) -> GetPersonUsersOkResponse:
        """List users permitted to access a person.

        :param id_: The ID of the person
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetPersonUsersOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/permittedUsers",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPersonUsersOkResponse._unmap(response)

    @cast_models
    def add_person_picture(
        self, id_: int, request_body: dict = None
    ) -> AddPersonPictureOkResponse:
        """Adds a picture to a person. If a picture is already set, the old picture will be replaced. Added image (or the cropping parameters supplied with the request) should have an equal width and height and should be at least 128 pixels. GIF, JPG and PNG are accepted. All added images will be resized to 128 and 512 pixel wide squares.

        :param request_body: The request body., defaults to None
        :type request_body: dict, optional
        :param id_: The ID of the person
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: AddPersonPictureOkResponse
        """

        Validator(dict).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/picture", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
            .set_body(request_body, "multipart/form-data")
        )

        response = self.send_request(serialized_request)

        return AddPersonPictureOkResponse._unmap(response)

    @cast_models
    def delete_person_picture(self, id_: int) -> DeletePersonPictureOkResponse:
        """Deletes a person’s picture.

        :param id_: The ID of the person
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeletePersonPictureOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/picture", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeletePersonPictureOkResponse._unmap(response)

    @cast_models
    def get_person_products(
        self, id_: int, start: int = None, limit: int = None
    ) -> GetPersonProductsOkResponse:
        """Lists products associated with a person.

        :param id_: The ID of the person
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetPersonProductsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/persons/{{id}}/products", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPersonProductsOkResponse._unmap(response)
