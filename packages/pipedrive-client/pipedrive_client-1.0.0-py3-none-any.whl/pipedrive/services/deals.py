from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_deal_request import UpdateDealRequest
from ..models.update_deal_product_request import UpdateDealProductRequest
from ..models.update_deal_product_ok_response import UpdateDealProductOkResponse
from ..models.update_deal_ok_response import UpdateDealOkResponse
from ..models.search_deals_status import SearchDealsStatus
from ..models.search_deals_ok_response import SearchDealsOkResponse
from ..models.search_deals_include_fields import SearchDealsIncludeFields
from ..models.search_deals_fields import SearchDealsFields
from ..models.owned_by_you import OwnedByYou
from ..models.merge_deals_request import MergeDealsRequest
from ..models.merge_deals_ok_response import MergeDealsOkResponse
from ..models.include_product_data import IncludeProductData
from ..models.get_deals_timeline_ok_response import GetDealsTimelineOkResponse
from ..models.get_deals_timeline_interval import GetDealsTimelineInterval
from ..models.get_deals_summary_status import GetDealsSummaryStatus
from ..models.get_deals_summary_ok_response import GetDealsSummaryOkResponse
from ..models.get_deals_status import GetDealsStatus
from ..models.get_deals_ok_response import GetDealsOkResponse
from ..models.get_deals_collection_status import GetDealsCollectionStatus
from ..models.get_deals_collection_ok_response import GetDealsCollectionOkResponse
from ..models.get_deal_users_ok_response import GetDealUsersOkResponse
from ..models.get_deal_updates_ok_response import GetDealUpdatesOkResponse
from ..models.get_deal_products_ok_response import GetDealProductsOkResponse
from ..models.get_deal_persons_ok_response import GetDealPersonsOkResponse
from ..models.get_deal_participants_ok_response import GetDealParticipantsOkResponse
from ..models.get_deal_participants_changelog_ok_response import (
    GetDealParticipantsChangelogOkResponse,
)
from ..models.get_deal_ok_response import GetDealOkResponse
from ..models.get_deal_mail_messages_ok_response import GetDealMailMessagesOkResponse
from ..models.get_deal_followers_ok_response import GetDealFollowersOkResponse
from ..models.get_deal_files_ok_response import GetDealFilesOkResponse
from ..models.get_deal_changelog_ok_response import GetDealChangelogOkResponse
from ..models.get_deal_activities_ok_response import GetDealActivitiesOkResponse
from ..models.get_deal_activities_done import GetDealActivitiesDone
from ..models.exclude_deals import ExcludeDeals
from ..models.duplicate_deal_ok_response import DuplicateDealOkResponse
from ..models.delete_deals_ok_response import DeleteDealsOkResponse
from ..models.delete_deal_product_ok_response import DeleteDealProductOkResponse
from ..models.delete_deal_participant_ok_response import DeleteDealParticipantOkResponse
from ..models.delete_deal_ok_response import DeleteDealOkResponse
from ..models.delete_deal_follower_ok_response import DeleteDealFollowerOkResponse
from ..models.add_deal_request import AddDealRequest
from ..models.add_deal_product_request import AddDealProductRequest
from ..models.add_deal_product_ok_response import AddDealProductOkResponse
from ..models.add_deal_participant_request import AddDealParticipantRequest
from ..models.add_deal_participant_ok_response import AddDealParticipantOkResponse
from ..models.add_deal_follower_request import AddDealFollowerRequest
from ..models.add_deal_follower_ok_response import AddDealFollowerOkResponse
from ..models.add_deal_created_response import AddDealCreatedResponse


class DealsService(BaseService):

    @cast_models
    def get_deals(
        self,
        user_id: int = None,
        filter_id: int = None,
        stage_id: int = None,
        status: GetDealsStatus = None,
        start: int = None,
        limit: int = None,
        sort: str = None,
        owned_by_you: OwnedByYou = None,
    ) -> GetDealsOkResponse:
        """Returns all deals. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/getting-all-deals" target="_blank" rel="noopener noreferrer">getting all deals</a>.

        :param user_id: If supplied, only deals matching the given user will be returned. However, `filter_id` and `owned_by_you` takes precedence over `user_id` when supplied., defaults to None
        :type user_id: int, optional
        :param filter_id: The ID of the filter to use, defaults to None
        :type filter_id: int, optional
        :param stage_id: If supplied, only deals within the given stage will be returned, defaults to None
        :type stage_id: int, optional
        :param status: Only fetch deals with a specific status. If omitted, all not deleted deals are returned. If set to deleted, deals that have been deleted up to 30 days ago will be included., defaults to None
        :type status: GetDealsStatus, optional
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param sort: The field names and sorting mode separated by a comma (`field_name_1 ASC`, `field_name_2 DESC`). Only first-level field keys are supported (no nested keys)., defaults to None
        :type sort: str, optional
        :param owned_by_you: When supplied, only deals owned by you are returned. However, `filter_id` takes precedence over `owned_by_you` when both are supplied., defaults to None
        :type owned_by_you: OwnedByYou, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get all deals
        :rtype: GetDealsOkResponse
        """

        Validator(int).is_optional().validate(user_id)
        Validator(int).is_optional().validate(filter_id)
        Validator(int).is_optional().validate(stage_id)
        Validator(GetDealsStatus).is_optional().validate(status)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(sort)
        Validator(OwnedByYou).is_optional().validate(owned_by_you)

        serialized_request = (
            Serializer(f"{self.base_url}/deals", self.get_default_headers())
            .add_query("user_id", user_id)
            .add_query("filter_id", filter_id)
            .add_query("stage_id", stage_id)
            .add_query("status", status)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("sort", sort)
            .add_query("owned_by_you", owned_by_you)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealsOkResponse._unmap(response)

    @cast_models
    def add_deal(self, request_body: AddDealRequest = None) -> AddDealCreatedResponse:
        """Adds a new deal. All deals created through the Pipedrive API will have a `origin` set to `API`. Note that you can supply additional custom fields along with the request that are not described here. These custom fields are different for each Pipedrive account and can be recognized by long hashes as keys. To determine which custom fields exists, fetch the dealFields and look for `key` values. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/creating-a-deal" target="_blank" rel="noopener noreferrer">adding a deal</a>.

        :param request_body: The request body., defaults to None
        :type request_body: AddDealRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add a deal
        :rtype: AddDealCreatedResponse
        """

        Validator(AddDealRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/deals", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddDealCreatedResponse._unmap(response)

    @cast_models
    def delete_deals(self, ids: str) -> DeleteDealsOkResponse:
        """Marks multiple deals as deleted. After 30 days, the deals will be permanently deleted.

        :param ids: The comma-separated IDs that will be deleted
        :type ids: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete multiple deals in bulk
        :rtype: DeleteDealsOkResponse
        """

        Validator(str).validate(ids)

        serialized_request = (
            Serializer(f"{self.base_url}/deals", self.get_default_headers())
            .add_query("ids", ids)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteDealsOkResponse._unmap(response)

    @cast_models
    def get_deals_collection(
        self,
        cursor: str = None,
        limit: int = None,
        since: str = None,
        until: str = None,
        user_id: int = None,
        stage_id: int = None,
        status: GetDealsCollectionStatus = None,
    ) -> GetDealsCollectionOkResponse:
        """Returns all deals. This is a cursor-paginated endpoint that is currently in BETA. For more information, please refer to our documentation on <a href="https://pipedrive.readme.io/docs/core-api-concepts-pagination" target="_blank" rel="noopener noreferrer">pagination</a>. Please note that only global admins (those with global permissions) can access these endpoints. Users with regular permissions will receive a 403 response. Read more about global permissions <a href="https://support.pipedrive.com/en/article/global-user-management" target="_blank" rel="noopener noreferrer">here</a>.

        :param cursor: For pagination, the marker (an opaque string value) representing the first item on the next page, defaults to None
        :type cursor: str, optional
        :param limit: For pagination, the limit of entries to be returned. If not provided, 100 items will be returned. Please note that a maximum value of 500 is allowed., defaults to None
        :type limit: int, optional
        :param since: The time boundary that points to the start of the range of data. Datetime in ISO 8601 format. E.g. 2022-11-01 08:55:59. Operates on the `update_time` field., defaults to None
        :type since: str, optional
        :param until: The time boundary that points to the end of the range of data. Datetime in ISO 8601 format. E.g. 2022-11-01 08:55:59. Operates on the `update_time` field., defaults to None
        :type until: str, optional
        :param user_id: If supplied, only deals matching the given user will be returned, defaults to None
        :type user_id: int, optional
        :param stage_id: If supplied, only deals within the given stage will be returned, defaults to None
        :type stage_id: int, optional
        :param status: Only fetch deals with a specific status. If omitted, all not deleted deals are returned. If set to deleted, deals that have been deleted up to 30 days ago will be included., defaults to None
        :type status: GetDealsCollectionStatus, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get all deals
        :rtype: GetDealsCollectionOkResponse
        """

        Validator(str).is_optional().validate(cursor)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(since)
        Validator(str).is_optional().validate(until)
        Validator(int).is_optional().validate(user_id)
        Validator(int).is_optional().validate(stage_id)
        Validator(GetDealsCollectionStatus).is_optional().validate(status)

        serialized_request = (
            Serializer(f"{self.base_url}/deals/collection", self.get_default_headers())
            .add_query("cursor", cursor)
            .add_query("limit", limit)
            .add_query("since", since)
            .add_query("until", until)
            .add_query("user_id", user_id)
            .add_query("stage_id", stage_id)
            .add_query("status", status)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealsCollectionOkResponse._unmap(response)

    @cast_models
    def search_deals(
        self,
        term: str,
        fields: SearchDealsFields = None,
        exact_match: bool = None,
        person_id: int = None,
        organization_id: int = None,
        status: SearchDealsStatus = None,
        include_fields: SearchDealsIncludeFields = None,
        start: int = None,
        limit: int = None,
    ) -> SearchDealsOkResponse:
        """Searches all deals by title, notes and/or custom fields. This endpoint is a wrapper of <a href="https://developers.pipedrive.com/docs/api/v1/ItemSearch#searchItem">/v1/itemSearch</a> with a narrower OAuth scope. Found deals can be filtered by the person ID and the organization ID.

        :param term: The search term to look for. Minimum 2 characters (or 1 if using `exact_match`). Please note that the search term has to be URL encoded.
        :type term: str
        :param fields: A comma-separated string array. The fields to perform the search from. Defaults to all of them. Only the following custom field types are searchable: `address`, `varchar`, `text`, `varchar_auto`, `double`, `monetary` and `phone`. Read more about searching by custom fields <a href="https://support.pipedrive.com/en/article/search-finding-what-you-need#searching-by-custom-fields" target="_blank" rel="noopener noreferrer">here</a>., defaults to None
        :type fields: SearchDealsFields, optional
        :param exact_match: When enabled, only full exact matches against the given term are returned. It is <b>not</b> case sensitive., defaults to None
        :type exact_match: bool, optional
        :param person_id: Will filter deals by the provided person ID. The upper limit of found deals associated with the person is 2000., defaults to None
        :type person_id: int, optional
        :param organization_id: Will filter deals by the provided organization ID. The upper limit of found deals associated with the organization is 2000., defaults to None
        :type organization_id: int, optional
        :param status: Will filter deals by the provided specific status. open = Open, won = Won, lost = Lost. The upper limit of found deals associated with the status is 2000., defaults to None
        :type status: SearchDealsStatus, optional
        :param include_fields: Supports including optional fields in the results which are not provided by default, defaults to None
        :type include_fields: SearchDealsIncludeFields, optional
        :param start: Pagination start. Note that the pagination is based on main results and does not include related items when using `search_for_related_items` parameter., defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: SearchDealsOkResponse
        """

        Validator(str).validate(term)
        Validator(SearchDealsFields).is_optional().validate(fields)
        Validator(bool).is_optional().validate(exact_match)
        Validator(int).is_optional().validate(person_id)
        Validator(int).is_optional().validate(organization_id)
        Validator(SearchDealsStatus).is_optional().validate(status)
        Validator(SearchDealsIncludeFields).is_optional().validate(include_fields)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/deals/search", self.get_default_headers())
            .add_query("term", term)
            .add_query("fields", fields)
            .add_query("exact_match", exact_match)
            .add_query("person_id", person_id)
            .add_query("organization_id", organization_id)
            .add_query("status", status)
            .add_query("include_fields", include_fields)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return SearchDealsOkResponse._unmap(response)

    @cast_models
    def get_deals_summary(
        self,
        status: GetDealsSummaryStatus = None,
        filter_id: int = None,
        user_id: int = None,
        stage_id: int = None,
    ) -> GetDealsSummaryOkResponse:
        """Returns a summary of all the deals.

        :param status: Only fetch deals with a specific status. open = Open, won = Won, lost = Lost., defaults to None
        :type status: GetDealsSummaryStatus, optional
        :param filter_id: <code>user_id</code> will not be considered. Only deals matching the given filter will be returned., defaults to None
        :type filter_id: int, optional
        :param user_id: Only deals matching the given user will be returned. `user_id` will not be considered if you use `filter_id`., defaults to None
        :type user_id: int, optional
        :param stage_id: Only deals within the given stage will be returned, defaults to None
        :type stage_id: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get the summary of the deals
        :rtype: GetDealsSummaryOkResponse
        """

        Validator(GetDealsSummaryStatus).is_optional().validate(status)
        Validator(int).is_optional().validate(filter_id)
        Validator(int).is_optional().validate(user_id)
        Validator(int).is_optional().validate(stage_id)

        serialized_request = (
            Serializer(f"{self.base_url}/deals/summary", self.get_default_headers())
            .add_query("status", status)
            .add_query("filter_id", filter_id)
            .add_query("user_id", user_id)
            .add_query("stage_id", stage_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealsSummaryOkResponse._unmap(response)

    @cast_models
    def get_deals_timeline(
        self,
        start_date: str,
        interval: GetDealsTimelineInterval,
        amount: int,
        field_key: str,
        user_id: int = None,
        pipeline_id: int = None,
        filter_id: int = None,
        exclude_deals: ExcludeDeals = None,
        totals_convert_currency: str = None,
    ) -> GetDealsTimelineOkResponse:
        """Returns open and won deals, grouped by a defined interval of time set in a date-type dealField (`field_key`) — e.g. when month is the chosen interval, and 3 months are asked starting from January 1st, 2012, deals are returned grouped into 3 groups — January, February and March — based on the value of the given `field_key`.

        :param start_date: The date when the first interval starts. Format: YYYY-MM-DD.
        :type start_date: str
        :param interval: The type of the interval<table><tr><th>Value</th><th>Description</th></tr><tr><td>`day`</td><td>Day</td></tr><tr><td>`week`</td><td>A full week (7 days) starting from `start_date`</td></tr><tr><td>`month`</td><td>A full month (depending on the number of days in given month) starting from `start_date`</td></tr><tr><td>`quarter`</td><td>A full quarter (3 months) starting from `start_date`</td></tr></table>
        :type interval: GetDealsTimelineInterval
        :param amount: The number of given intervals, starting from `start_date`, to fetch. E.g. 3 (months).
        :type amount: int
        :param field_key: The date field key which deals will be retrieved from
        :type field_key: str
        :param user_id: If supplied, only deals matching the given user will be returned, defaults to None
        :type user_id: int, optional
        :param pipeline_id: If supplied, only deals matching the given pipeline will be returned, defaults to None
        :type pipeline_id: int, optional
        :param filter_id: If supplied, only deals matching the given filter will be returned, defaults to None
        :type filter_id: int, optional
        :param exclude_deals: Whether to exclude deals list (1) or not (0). Note that when deals are excluded, the timeline summary (counts and values) is still returned., defaults to None
        :type exclude_deals: ExcludeDeals, optional
        :param totals_convert_currency: The 3-letter currency code of any of the supported currencies. When supplied, `totals_converted` is returned per each interval which contains the currency-converted total amounts in the given currency. You may also set this parameter to `default_currency` in which case the user's default currency is used., defaults to None
        :type totals_convert_currency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get open and won deals, grouped by the defined interval of time
        :rtype: GetDealsTimelineOkResponse
        """

        Validator(str).validate(start_date)
        Validator(GetDealsTimelineInterval).validate(interval)
        Validator(int).validate(amount)
        Validator(str).validate(field_key)
        Validator(int).is_optional().validate(user_id)
        Validator(int).is_optional().validate(pipeline_id)
        Validator(int).is_optional().validate(filter_id)
        Validator(ExcludeDeals).is_optional().validate(exclude_deals)
        Validator(str).is_optional().validate(totals_convert_currency)

        serialized_request = (
            Serializer(f"{self.base_url}/deals/timeline", self.get_default_headers())
            .add_query("start_date", start_date)
            .add_query("interval", interval)
            .add_query("amount", amount)
            .add_query("field_key", field_key)
            .add_query("user_id", user_id)
            .add_query("pipeline_id", pipeline_id)
            .add_query("filter_id", filter_id)
            .add_query("exclude_deals", exclude_deals)
            .add_query("totals_convert_currency", totals_convert_currency)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealsTimelineOkResponse._unmap(response)

    @cast_models
    def get_deal(self, id_: int) -> GetDealOkResponse:
        """Returns the details of a specific deal. Note that this also returns some additional fields which are not present when asking for all deals – such as deal age and stay in pipeline stages. Also note that custom fields appear as long hashes in the resulting data. These hashes can be mapped against the `key` value of dealFields. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/getting-details-of-a-deal" target="_blank" rel="noopener noreferrer">getting details of a deal</a>.

        :param id_: The ID of the deal
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get a deal by its ID
        :rtype: GetDealOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/deals/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealOkResponse._unmap(response)

    @cast_models
    def update_deal(
        self, id_: int, request_body: UpdateDealRequest = None
    ) -> UpdateDealOkResponse:
        """Updates the properties of a deal. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/updating-a-deal" target="_blank" rel="noopener noreferrer">updating a deal</a>.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateDealRequest, optional
        :param id_: The ID of the deal
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add a deal
        :rtype: UpdateDealOkResponse
        """

        Validator(UpdateDealRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/deals/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateDealOkResponse._unmap(response)

    @cast_models
    def delete_deal(self, id_: int) -> DeleteDealOkResponse:
        """Marks a deal as deleted. After 30 days, the deal will be permanently deleted.

        :param id_: The ID of the deal
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete a deal
        :rtype: DeleteDealOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/deals/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteDealOkResponse._unmap(response)

    @cast_models
    def get_deal_activities(
        self,
        id_: int,
        start: int = None,
        limit: int = None,
        done: GetDealActivitiesDone = None,
        exclude: str = None,
    ) -> GetDealActivitiesOkResponse:
        """Lists activities associated with a deal.

        :param id_: The ID of the deal
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param done: Whether the activity is done or not. 0 = Not done, 1 = Done. If omitted, returns both Done and Not done activities., defaults to None
        :type done: GetDealActivitiesDone, optional
        :param exclude: A comma-separated string of activity IDs to exclude from result, defaults to None
        :type exclude: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetDealActivitiesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(GetDealActivitiesDone).is_optional().validate(done)
        Validator(str).is_optional().validate(exclude)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/activities", self.get_default_headers()
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

        return GetDealActivitiesOkResponse._unmap(response)

    @cast_models
    def get_deal_changelog(
        self, id_: int, cursor: str = None, limit: int = None
    ) -> GetDealChangelogOkResponse:
        """Lists updates about field values of a deal.

        :param id_: The ID of the deal
        :type id_: int
        :param cursor: For pagination, the marker (an opaque string value) representing the first item on the next page, defaults to None
        :type cursor: str, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get changelog of a deal
        :rtype: GetDealChangelogOkResponse
        """

        Validator(int).validate(id_)
        Validator(str).is_optional().validate(cursor)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/changelog", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("cursor", cursor)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealChangelogOkResponse._unmap(response)

    @cast_models
    def duplicate_deal(self, id_: int) -> DuplicateDealOkResponse:
        """Duplicates a deal.

        :param id_: The ID of the deal
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Duplicate a deal
        :rtype: DuplicateDealOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/duplicate", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)

        return DuplicateDealOkResponse._unmap(response)

    @cast_models
    def get_deal_files(
        self, id_: int, start: int = None, limit: int = None, sort: str = None
    ) -> GetDealFilesOkResponse:
        """Lists files associated with a deal.

        :param id_: The ID of the deal
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
        :rtype: GetDealFilesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(sort)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/files", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("sort", sort)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealFilesOkResponse._unmap(response)

    @cast_models
    def get_deal_updates(
        self,
        id_: int,
        start: int = None,
        limit: int = None,
        all_changes: str = None,
        items: str = None,
    ) -> GetDealUpdatesOkResponse:
        """Lists updates about a deal.

        :param id_: The ID of the deal
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
        :return: Get the deal updates
        :rtype: GetDealUpdatesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(all_changes)
        Validator(str).is_optional().validate(items)

        serialized_request = (
            Serializer(f"{self.base_url}/deals/{{id}}/flow", self.get_default_headers())
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("all_changes", all_changes)
            .add_query("items", items)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealUpdatesOkResponse._unmap(response)

    @cast_models
    def get_deal_participants_changelog(
        self, id_: int, limit: int = None, cursor: str = None
    ) -> GetDealParticipantsChangelogOkResponse:
        """List updates about participants of a deal. This is a cursor-paginated endpoint. For more information, please refer to our documentation on <a href="https://pipedrive.readme.io/docs/core-api-concepts-pagination" target="_blank" rel="noopener noreferrer">pagination</a>.

        :param id_: The ID of the deal
        :type id_: int
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param cursor: For pagination, the marker (an opaque string value) representing the first item on the next page, defaults to None
        :type cursor: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get participant changelogs for a given deal
        :rtype: GetDealParticipantsChangelogOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(cursor)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/participantsChangelog",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("limit", limit)
            .add_query("cursor", cursor)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealParticipantsChangelogOkResponse._unmap(response)

    @cast_models
    def get_deal_followers(self, id_: int) -> GetDealFollowersOkResponse:
        """Lists the followers of a deal.

        :param id_: The ID of the deal
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetDealFollowersOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/followers", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealFollowersOkResponse._unmap(response)

    @cast_models
    def add_deal_follower(
        self, id_: int, request_body: AddDealFollowerRequest = None
    ) -> AddDealFollowerOkResponse:
        """Adds a follower to a deal.

        :param request_body: The request body., defaults to None
        :type request_body: AddDealFollowerRequest, optional
        :param id_: The ID of the deal
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add a follower to a deal
        :rtype: AddDealFollowerOkResponse
        """

        Validator(AddDealFollowerRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/followers", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddDealFollowerOkResponse._unmap(response)

    @cast_models
    def delete_deal_follower(
        self, id_: int, follower_id: int
    ) -> DeleteDealFollowerOkResponse:
        """Deletes a follower from a deal.

        :param id_: The ID of the deal
        :type id_: int
        :param follower_id: The ID of the follower
        :type follower_id: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete a follower from a deal
        :rtype: DeleteDealFollowerOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).validate(follower_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/followers/{{follower_id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("follower_id", follower_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteDealFollowerOkResponse._unmap(response)

    @cast_models
    def get_deal_mail_messages(
        self, id_: int, start: int = None, limit: int = None
    ) -> GetDealMailMessagesOkResponse:
        """Lists mail messages associated with a deal.

        :param id_: The ID of the deal
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetDealMailMessagesOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/mailMessages", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealMailMessagesOkResponse._unmap(response)

    @cast_models
    def merge_deals(
        self, id_: int, request_body: MergeDealsRequest = None
    ) -> MergeDealsOkResponse:
        """Merges a deal with another deal. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/merging-two-deals" target="_blank" rel="noopener noreferrer">merging two deals</a>.

        :param request_body: The request body., defaults to None
        :type request_body: MergeDealsRequest, optional
        :param id_: The ID of the deal
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Merges a deal with another deal
        :rtype: MergeDealsOkResponse
        """

        Validator(MergeDealsRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/merge", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return MergeDealsOkResponse._unmap(response)

    @cast_models
    def get_deal_participants(
        self, id_: int, start: int = None, limit: int = None
    ) -> GetDealParticipantsOkResponse:
        """Lists the participants associated with a deal.<br>If a company uses the [Campaigns product](https://pipedrive.readme.io/docs/campaigns-in-pipedrive-api), then this endpoint will also return the `data.marketing_status` field.

        :param id_: The ID of the deal
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get all deal participants by the DealID
        :rtype: GetDealParticipantsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/participants", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealParticipantsOkResponse._unmap(response)

    @cast_models
    def add_deal_participant(
        self, id_: int, request_body: AddDealParticipantRequest = None
    ) -> AddDealParticipantOkResponse:
        """Adds a participant to a deal.

        :param request_body: The request body., defaults to None
        :type request_body: AddDealParticipantRequest, optional
        :param id_: The ID of the deal
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add new participant to the deal
        :rtype: AddDealParticipantOkResponse
        """

        Validator(AddDealParticipantRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/participants", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddDealParticipantOkResponse._unmap(response)

    @cast_models
    def delete_deal_participant(
        self, id_: int, deal_participant_id: int
    ) -> DeleteDealParticipantOkResponse:
        """Deletes a participant from a deal.

        :param id_: The ID of the deal
        :type id_: int
        :param deal_participant_id: The ID of the participant of the deal
        :type deal_participant_id: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete a participant from a deal
        :rtype: DeleteDealParticipantOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).validate(deal_participant_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/participants/{{deal_participant_id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("deal_participant_id", deal_participant_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteDealParticipantOkResponse._unmap(response)

    @cast_models
    def get_deal_users(self, id_: int) -> GetDealUsersOkResponse:
        """Lists the users permitted to access a deal.

        :param id_: The ID of the deal
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetDealUsersOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/permittedUsers",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealUsersOkResponse._unmap(response)

    @cast_models
    def get_deal_persons(
        self, id_: int, start: int = None, limit: int = None
    ) -> GetDealPersonsOkResponse:
        """Lists all persons associated with a deal, regardless of whether the person is the primary contact of the deal, or added as a participant.<br>If a company uses the [Campaigns product](https://pipedrive.readme.io/docs/campaigns-in-pipedrive-api), then this endpoint will also return the `data.marketing_status` field.

        :param id_: The ID of the deal
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetDealPersonsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/persons", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealPersonsOkResponse._unmap(response)

    @cast_models
    def get_deal_products(
        self,
        id_: int,
        start: int = None,
        limit: int = None,
        include_product_data: IncludeProductData = None,
    ) -> GetDealProductsOkResponse:
        """Lists products attached to a deal.

        :param id_: The ID of the deal
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param include_product_data: Whether to fetch product data along with each attached product (1) or not (0, default), defaults to None
        :type include_product_data: IncludeProductData, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetDealProductsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(IncludeProductData).is_optional().validate(include_product_data)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/products", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("include_product_data", include_product_data)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDealProductsOkResponse._unmap(response)

    @cast_models
    def add_deal_product(
        self, id_: int, request_body: AddDealProductRequest = None
    ) -> AddDealProductOkResponse:
        """Adds a product to a deal, creating a new item called a deal-product.

        :param request_body: The request body., defaults to None
        :type request_body: AddDealProductRequest, optional
        :param id_: The ID of the deal
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add a product to the deal
        :rtype: AddDealProductOkResponse
        """

        Validator(AddDealProductRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/products", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddDealProductOkResponse._unmap(response)

    @cast_models
    def update_deal_product(
        self,
        id_: int,
        product_attachment_id: int,
        request_body: UpdateDealProductRequest = None,
    ) -> UpdateDealProductOkResponse:
        """Updates the details of the product that has been attached to a deal.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateDealProductRequest, optional
        :param id_: The ID of the deal
        :type id_: int
        :param product_attachment_id: The ID of the deal-product (the ID of the product attached to the deal)
        :type product_attachment_id: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Update product attachment details
        :rtype: UpdateDealProductOkResponse
        """

        Validator(UpdateDealProductRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)
        Validator(int).validate(product_attachment_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/products/{{product_attachment_id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("product_attachment_id", product_attachment_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateDealProductOkResponse._unmap(response)

    @cast_models
    def delete_deal_product(
        self, id_: int, product_attachment_id: int
    ) -> DeleteDealProductOkResponse:
        """Deletes a product attachment from a deal, using the `product_attachment_id`.

        :param id_: The ID of the deal
        :type id_: int
        :param product_attachment_id: The product attachment ID
        :type product_attachment_id: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete an attached product from a deal
        :rtype: DeleteDealProductOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).validate(product_attachment_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/deals/{{id}}/products/{{product_attachment_id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("product_attachment_id", product_attachment_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteDealProductOkResponse._unmap(response)
