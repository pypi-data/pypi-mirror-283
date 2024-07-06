from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_mail_thread_details_request import UpdateMailThreadDetailsRequest
from ..models.update_mail_thread_details_ok_response import (
    UpdateMailThreadDetailsOkResponse,
)
from ..models.include_body import IncludeBody
from ..models.get_mail_threads_ok_response import GetMailThreadsOkResponse
from ..models.get_mail_thread_ok_response import GetMailThreadOkResponse
from ..models.get_mail_thread_messages_ok_response import (
    GetMailThreadMessagesOkResponse,
)
from ..models.get_mail_message_ok_response import GetMailMessageOkResponse
from ..models.folder import Folder
from ..models.delete_mail_thread_ok_response import DeleteMailThreadOkResponse


class MailboxService(BaseService):

    @cast_models
    def get_mail_message(
        self, id_: int, include_body: IncludeBody = None
    ) -> GetMailMessageOkResponse:
        """Returns data about a specific mail message.

        :param id_: The ID of the mail message to fetch
        :type id_: int
        :param include_body: Whether to include the full message body or not. `0` = Don't include, `1` = Include., defaults to None
        :type include_body: IncludeBody, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The mail messages that are being synced with Pipedrive
        :rtype: GetMailMessageOkResponse
        """

        Validator(int).validate(id_)
        Validator(IncludeBody).is_optional().validate(include_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/mailbox/mailMessages/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("include_body", include_body)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetMailMessageOkResponse._unmap(response)

    @cast_models
    def get_mail_threads(
        self, folder: Folder, start: int = None, limit: int = None
    ) -> GetMailThreadsOkResponse:
        """Returns mail threads in a specified folder ordered by the most recent message within.

        :param folder: The type of folder to fetch
        :type folder: Folder
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get mail threads
        :rtype: GetMailThreadsOkResponse
        """

        Validator(Folder).validate(folder)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/mailbox/mailThreads", self.get_default_headers()
            )
            .add_query("folder", folder)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetMailThreadsOkResponse._unmap(response)

    @cast_models
    def get_mail_thread(self, id_: int) -> GetMailThreadOkResponse:
        """Returns a specific mail thread.

        :param id_: The ID of the mail thread
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get mail threads
        :rtype: GetMailThreadOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/mailbox/mailThreads/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetMailThreadOkResponse._unmap(response)

    @cast_models
    def update_mail_thread_details(
        self, id_: int, request_body: UpdateMailThreadDetailsRequest = None
    ) -> UpdateMailThreadDetailsOkResponse:
        """Updates the properties of a mail thread.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateMailThreadDetailsRequest, optional
        :param id_: The ID of the mail thread
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Updates the properties of a mail thread
        :rtype: UpdateMailThreadDetailsOkResponse
        """

        Validator(UpdateMailThreadDetailsRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/mailbox/mailThreads/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body, "application/x-www-form-urlencoded")
        )

        response = self.send_request(serialized_request)

        return UpdateMailThreadDetailsOkResponse._unmap(response)

    @cast_models
    def delete_mail_thread(self, id_: int) -> DeleteMailThreadOkResponse:
        """Marks a mail thread as deleted.

        :param id_: The ID of the mail thread
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Marks mail thread as deleted
        :rtype: DeleteMailThreadOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/mailbox/mailThreads/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteMailThreadOkResponse._unmap(response)

    @cast_models
    def get_mail_thread_messages(self, id_: int) -> GetMailThreadMessagesOkResponse:
        """Returns all the mail messages inside a specified mail thread.

        :param id_: The ID of the mail thread
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get mail messages from thread
        :rtype: GetMailThreadMessagesOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/mailbox/mailThreads/{{id}}/mailMessages",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetMailThreadMessagesOkResponse._unmap(response)
