from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.save_user_provider_link_request import SaveUserProviderLinkRequest
from ..models.save_user_provider_link_ok_response import SaveUserProviderLinkOkResponse
from ..models.delete_user_provider_link_ok_response import (
    DeleteUserProviderLinkOkResponse,
)


class MeetingsService(BaseService):

    @cast_models
    def save_user_provider_link(
        self, request_body: SaveUserProviderLinkRequest = None
    ) -> SaveUserProviderLinkOkResponse:
        """A video calling provider must call this endpoint after a user has installed the video calling app so that the new user's information is sent.

        :param request_body: The request body., defaults to None
        :type request_body: SaveUserProviderLinkRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: User provider link was successfully created
        :rtype: SaveUserProviderLinkOkResponse
        """

        Validator(SaveUserProviderLinkRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/meetings/userProviderLinks",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return SaveUserProviderLinkOkResponse._unmap(response)

    @cast_models
    def delete_user_provider_link(self, id_: str) -> DeleteUserProviderLinkOkResponse:
        """A video calling provider must call this endpoint to remove the link between a user and the installed video calling app.

        :param id_: Unique identifier linking a user to the installed integration
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: User provider link successfully removed
        :rtype: DeleteUserProviderLinkOkResponse
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/meetings/userProviderLinks/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteUserProviderLinkOkResponse._unmap(response)
