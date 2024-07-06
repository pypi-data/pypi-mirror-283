from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_activity_fields_ok_response import GetActivityFieldsOkResponse


class ActivityFieldsService(BaseService):

    @cast_models
    def get_activity_fields(self) -> GetActivityFieldsOkResponse:
        """Returns all activity fields.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetActivityFieldsOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/activityFields", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetActivityFieldsOkResponse._unmap(response)
