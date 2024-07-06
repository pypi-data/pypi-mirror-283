from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_user_call_logs_ok_response import GetUserCallLogsOkResponse
from ..models.get_call_log_ok_response import GetCallLogOkResponse
from ..models.delete_call_log_ok_response import DeleteCallLogOkResponse
from ..models.add_call_log_request import AddCallLogRequest
from ..models.add_call_log_ok_response import AddCallLogOkResponse
from ..models.add_call_log_audio_file_request import AddCallLogAudioFileRequest
from ..models.add_call_log_audio_file_ok_response import AddCallLogAudioFileOkResponse


class CallLogsService(BaseService):

    @cast_models
    def get_user_call_logs(
        self, start: int = None, limit: int = None
    ) -> GetUserCallLogsOkResponse:
        """Returns all call logs assigned to a particular user.

        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: For pagination, the limit of entries to be returned. The upper limit is 50., defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of call logs.
        :rtype: GetUserCallLogsOkResponse
        """

        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/callLogs", self.get_default_headers())
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetUserCallLogsOkResponse._unmap(response)

    @cast_models
    def add_call_log(
        self, request_body: AddCallLogRequest = None
    ) -> AddCallLogOkResponse:
        """Adds a new call log.

        :param request_body: The request body., defaults to None
        :type request_body: AddCallLogRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The call log was successfully created.
        :rtype: AddCallLogOkResponse
        """

        Validator(AddCallLogRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/callLogs", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddCallLogOkResponse._unmap(response)

    @cast_models
    def get_call_log(self, id_: str) -> GetCallLogOkResponse:
        """Returns details of a specific call log.

        :param id_: The ID received when you create the call log
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The requested call log object.
        :rtype: GetCallLogOkResponse
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/callLogs/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetCallLogOkResponse._unmap(response)

    @cast_models
    def delete_call_log(self, id_: str) -> DeleteCallLogOkResponse:
        """Deletes a call log. If there is an audio recording attached to it, it will also be deleted. The related activity will not be removed by this request. If you want to remove the related activities, please use the endpoint which is specific for activities.

        :param id_: The ID received when you create the call log
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The call log was successfully deleted.
        :rtype: DeleteCallLogOkResponse
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/callLogs/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteCallLogOkResponse._unmap(response)

    @cast_models
    def add_call_log_audio_file(
        self, id_: str, request_body: dict = None
    ) -> AddCallLogAudioFileOkResponse:
        """Adds an audio recording to the call log. That audio can be played by those who have access to the call log object.

        :param request_body: The request body., defaults to None
        :type request_body: dict, optional
        :param id_: The ID received when you create the call log
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The audio recording was successfully added to the log.
        :rtype: AddCallLogAudioFileOkResponse
        """

        Validator(dict).is_optional().validate(request_body)
        Validator(str).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/callLogs/{{id}}/recordings",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
            .set_body(request_body, "multipart/form-data")
        )

        response = self.send_request(serialized_request)

        return AddCallLogAudioFileOkResponse._unmap(response)
