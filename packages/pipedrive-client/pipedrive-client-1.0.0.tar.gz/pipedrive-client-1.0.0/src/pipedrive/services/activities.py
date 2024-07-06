from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_activity_request import UpdateActivityRequest
from ..models.update_activity_ok_response import UpdateActivityOkResponse
from ..models.get_activity_ok_response import GetActivityOkResponse
from ..models.get_activities_ok_response import GetActivitiesOkResponse
from ..models.get_activities_done import GetActivitiesDone
from ..models.get_activities_collection_ok_response import (
    GetActivitiesCollectionOkResponse,
)
from ..models.delete_activity_ok_response import DeleteActivityOkResponse
from ..models.delete_activities_ok_response import DeleteActivitiesOkResponse
from ..models.add_activity_request import AddActivityRequest
from ..models.add_activity_created_response import AddActivityCreatedResponse


class ActivitiesService(BaseService):

    @cast_models
    def get_activities(
        self,
        user_id: int = None,
        filter_id: int = None,
        type_: str = None,
        limit: int = None,
        start: int = None,
        start_date: str = None,
        end_date: str = None,
        done: GetActivitiesDone = None,
    ) -> GetActivitiesOkResponse:
        """Returns all activities assigned to a particular user.

        :param user_id: The ID of the user whose activities will be fetched. If omitted, the user associated with the API token will be used. If 0, activities for all company users will be fetched based on the permission sets., defaults to None
        :type user_id: int, optional
        :param filter_id: The ID of the filter to use (will narrow down results if used together with `user_id` parameter), defaults to None
        :type filter_id: int, optional
        :param type_: The type of the activity, can be one type or multiple types separated by a comma. This is in correlation with the `key_string` parameter of ActivityTypes., defaults to None
        :type type_: str, optional
        :param limit: For pagination, the limit of entries to be returned. If not provided, 100 items will be returned., defaults to None
        :type limit: int, optional
        :param start: For pagination, the position that represents the first result for the page, defaults to None
        :type start: int, optional
        :param start_date: Use the activity due date where you wish to begin fetching activities from. Insert due date in YYYY-MM-DD format., defaults to None
        :type start_date: str, optional
        :param end_date: Use the activity due date where you wish to stop fetching activities from. Insert due date in YYYY-MM-DD format., defaults to None
        :type end_date: str, optional
        :param done: Whether the activity is done or not. 0 = Not done, 1 = Done. If omitted returns both done and not done activities., defaults to None
        :type done: GetActivitiesDone, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of activities
        :rtype: GetActivitiesOkResponse
        """

        Validator(int).is_optional().validate(user_id)
        Validator(int).is_optional().validate(filter_id)
        Validator(str).is_optional().validate(type_)
        Validator(int).is_optional().validate(limit)
        Validator(int).is_optional().validate(start)
        Validator(str).is_optional().validate(start_date)
        Validator(str).is_optional().validate(end_date)
        Validator(GetActivitiesDone).is_optional().validate(done)

        serialized_request = (
            Serializer(f"{self.base_url}/activities", self.get_default_headers())
            .add_query("user_id", user_id)
            .add_query("filter_id", filter_id)
            .add_query("type", type_)
            .add_query("limit", limit)
            .add_query("start", start)
            .add_query("start_date", start_date)
            .add_query("end_date", end_date)
            .add_query("done", done)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetActivitiesOkResponse._unmap(response)

    @cast_models
    def add_activity(
        self, request_body: AddActivityRequest = None
    ) -> AddActivityCreatedResponse:
        """Adds a new activity. Includes `more_activities_scheduled_in_context` property in response's `additional_data` which indicates whether there are more undone activities scheduled with the same deal, person or organization (depending on the supplied data). For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/adding-an-activity" target="_blank" rel="noopener noreferrer">adding an activity</a>.

        :param request_body: The request body., defaults to None
        :type request_body: AddActivityRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Created
        :rtype: AddActivityCreatedResponse
        """

        Validator(AddActivityRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/activities", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddActivityCreatedResponse._unmap(response)

    @cast_models
    def delete_activities(self, ids: str) -> DeleteActivitiesOkResponse:
        """Marks multiple activities as deleted. After 30 days, the activities will be permanently deleted.

        :param ids: The comma-separated IDs of activities that will be deleted
        :type ids: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The activities were successfully deleted
        :rtype: DeleteActivitiesOkResponse
        """

        Validator(str).validate(ids)

        serialized_request = (
            Serializer(f"{self.base_url}/activities", self.get_default_headers())
            .add_query("ids", ids)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteActivitiesOkResponse._unmap(response)

    @cast_models
    def get_activities_collection(
        self,
        cursor: str = None,
        limit: int = None,
        since: str = None,
        until: str = None,
        user_id: int = None,
        done: bool = None,
        type_: str = None,
    ) -> GetActivitiesCollectionOkResponse:
        """Returns all activities. This is a cursor-paginated endpoint that is currently in BETA. For more information, please refer to our documentation on <a href="https://pipedrive.readme.io/docs/core-api-concepts-pagination" target="_blank" rel="noopener noreferrer">pagination</a>. Please note that only global admins (those with global permissions) can access these endpoints. Users with regular permissions will receive a 403 response. Read more about global permissions <a href="https://support.pipedrive.com/en/article/global-user-management" target="_blank" rel="noopener noreferrer">here</a>.

        :param cursor: For pagination, the marker (an opaque string value) representing the first item on the next page, defaults to None
        :type cursor: str, optional
        :param limit: For pagination, the limit of entries to be returned. If not provided, 100 items will be returned. Please note that a maximum value of 500 is allowed., defaults to None
        :type limit: int, optional
        :param since: The time boundary that points to the start of the range of data. Datetime in ISO 8601 format. E.g. 2022-11-01 08:55:59. Operates on the `update_time` field., defaults to None
        :type since: str, optional
        :param until: The time boundary that points to the end of the range of data. Datetime in ISO 8601 format. E.g. 2022-11-01 08:55:59. Operates on the `update_time` field., defaults to None
        :type until: str, optional
        :param user_id: The ID of the user whose activities will be fetched. If omitted, all activities are returned., defaults to None
        :type user_id: int, optional
        :param done: Whether the activity is done or not. `false` = Not done, `true` = Done. If omitted, returns both done and not done activities., defaults to None
        :type done: bool, optional
        :param type_: The type of the activity, can be one type or multiple types separated by a comma. This is in correlation with the `key_string` parameter of ActivityTypes., defaults to None
        :type type_: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of activities
        :rtype: GetActivitiesCollectionOkResponse
        """

        Validator(str).is_optional().validate(cursor)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(since)
        Validator(str).is_optional().validate(until)
        Validator(int).is_optional().validate(user_id)
        Validator(bool).is_optional().validate(done)
        Validator(str).is_optional().validate(type_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/activities/collection", self.get_default_headers()
            )
            .add_query("cursor", cursor)
            .add_query("limit", limit)
            .add_query("since", since)
            .add_query("until", until)
            .add_query("user_id", user_id)
            .add_query("done", done)
            .add_query("type", type_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetActivitiesCollectionOkResponse._unmap(response)

    @cast_models
    def get_activity(self, id_: int) -> GetActivityOkResponse:
        """Returns the details of a specific activity.

        :param id_: The ID of the activity
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The request was successful
        :rtype: GetActivityOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/activities/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetActivityOkResponse._unmap(response)

    @cast_models
    def update_activity(
        self, id_: int, request_body: UpdateActivityRequest = None
    ) -> UpdateActivityOkResponse:
        """Updates an activity. Includes `more_activities_scheduled_in_context` property in response's `additional_data` which indicates whether there are more undone activities scheduled with the same deal, person or organization (depending on the supplied data).

        :param request_body: The request body., defaults to None
        :type request_body: UpdateActivityRequest, optional
        :param id_: The ID of the activity
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The request was successful
        :rtype: UpdateActivityOkResponse
        """

        Validator(UpdateActivityRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/activities/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateActivityOkResponse._unmap(response)

    @cast_models
    def delete_activity(self, id_: int) -> DeleteActivityOkResponse:
        """Marks an activity as deleted. After 30 days, the activity will be permanently deleted.

        :param id_: The ID of the activity
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The activity was successfully deleted
        :rtype: DeleteActivityOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/activities/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteActivityOkResponse._unmap(response)
