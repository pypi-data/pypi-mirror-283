from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_activity_type_request import UpdateActivityTypeRequest
from ..models.update_activity_type_ok_response import UpdateActivityTypeOkResponse
from ..models.get_activity_types_ok_response import GetActivityTypesOkResponse
from ..models.delete_activity_types_ok_response import DeleteActivityTypesOkResponse
from ..models.delete_activity_type_ok_response import DeleteActivityTypeOkResponse
from ..models.add_activity_type_request import AddActivityTypeRequest
from ..models.add_activity_type_ok_response import AddActivityTypeOkResponse


class ActivityTypesService(BaseService):

    @cast_models
    def get_activity_types(self) -> GetActivityTypesOkResponse:
        """Returns all activity types.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of activity types
        :rtype: GetActivityTypesOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/activityTypes", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetActivityTypesOkResponse._unmap(response)

    @cast_models
    def add_activity_type(
        self, request_body: AddActivityTypeRequest = None
    ) -> AddActivityTypeOkResponse:
        """Adds a new activity type.

        :param request_body: The request body., defaults to None
        :type request_body: AddActivityTypeRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The activity type was successfully created
        :rtype: AddActivityTypeOkResponse
        """

        Validator(AddActivityTypeRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/activityTypes", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddActivityTypeOkResponse._unmap(response)

    @cast_models
    def delete_activity_types(self, ids: str) -> DeleteActivityTypesOkResponse:
        """Marks multiple activity types as deleted.

        :param ids: The comma-separated activity type IDs
        :type ids: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The activity types were successfully deleted
        :rtype: DeleteActivityTypesOkResponse
        """

        Validator(str).validate(ids)

        serialized_request = (
            Serializer(f"{self.base_url}/activityTypes", self.get_default_headers())
            .add_query("ids", ids)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteActivityTypesOkResponse._unmap(response)

    @cast_models
    def update_activity_type(
        self, id_: int, request_body: UpdateActivityTypeRequest = None
    ) -> UpdateActivityTypeOkResponse:
        """Updates an activity type.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateActivityTypeRequest, optional
        :param id_: The ID of the activity type
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The activity type was successfully updated
        :rtype: UpdateActivityTypeOkResponse
        """

        Validator(UpdateActivityTypeRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/activityTypes/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateActivityTypeOkResponse._unmap(response)

    @cast_models
    def delete_activity_type(self, id_: int) -> DeleteActivityTypeOkResponse:
        """Marks an activity type as deleted.

        :param id_: The ID of the activity type
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The activity type was successfully deleted
        :rtype: DeleteActivityTypeOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/activityTypes/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteActivityTypeOkResponse._unmap(response)
