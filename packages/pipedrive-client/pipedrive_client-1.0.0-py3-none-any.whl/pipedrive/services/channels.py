from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.receive_message_request import ReceiveMessageRequest
from ..models.receive_message_ok_response import ReceiveMessageOkResponse
from ..models.delete_conversation_ok_response import DeleteConversationOkResponse
from ..models.delete_channel_ok_response import DeleteChannelOkResponse
from ..models.add_channel_request import AddChannelRequest
from ..models.add_channel_ok_response import AddChannelOkResponse


class ChannelsService(BaseService):

    @cast_models
    def add_channel(
        self, request_body: AddChannelRequest = None
    ) -> AddChannelOkResponse:
        """Adds a new messaging channel, only admins are able to register new channels. It will use the getConversations endpoint to fetch conversations, participants and messages afterward. To use the endpoint, you need to have **Messengers integration** OAuth scope enabled and the Messaging manifest ready for the [Messaging app extension](https://pipedrive.readme.io/docs/messaging-app-extension).

        :param request_body: The request body., defaults to None
        :type request_body: AddChannelRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The channel registered
        :rtype: AddChannelOkResponse
        """

        Validator(AddChannelRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/channels", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddChannelOkResponse._unmap(response)

    @cast_models
    def delete_channel(self, id_: str) -> DeleteChannelOkResponse:
        """Deletes an existing messenger’s channel and all related entities (conversations and messages). To use the endpoint, you need to have **Messengers integration** OAuth scope enabled and the Messaging manifest ready for the [Messaging app extension](https://pipedrive.readme.io/docs/messaging-app-extension).

        :param id_: The ID of the channel provided by the integration
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The channel was deleted
        :rtype: DeleteChannelOkResponse
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/channels/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteChannelOkResponse._unmap(response)

    @cast_models
    def receive_message(
        self, request_body: ReceiveMessageRequest = None
    ) -> ReceiveMessageOkResponse:
        """Adds a message to a conversation. To use the endpoint, you need to have **Messengers integration** OAuth scope enabled and the Messaging manifest ready for the [Messaging app extension](https://pipedrive.readme.io/docs/messaging-app-extension).

        :param request_body: The request body., defaults to None
        :type request_body: ReceiveMessageRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The message was registered in the conversation
        :rtype: ReceiveMessageOkResponse
        """

        Validator(ReceiveMessageRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/channels/messages/receive", self.get_default_headers()
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return ReceiveMessageOkResponse._unmap(response)

    @cast_models
    def delete_conversation(
        self, channel_id: str, conversation_id: str
    ) -> DeleteConversationOkResponse:
        """Deletes an existing conversation. To use the endpoint, you need to have **Messengers integration** OAuth scope enabled and the Messaging manifest ready for the [Messaging app extension](https://pipedrive.readme.io/docs/messaging-app-extension).

        :param channel_id: The ID of the channel provided by the integration
        :type channel_id: str
        :param conversation_id: The ID of the conversation provided by the integration
        :type conversation_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The conversation was deleted
        :rtype: DeleteConversationOkResponse
        """

        Validator(str).validate(channel_id)
        Validator(str).validate(conversation_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/channels/{{channel-id}}/conversations/{{conversation-id}}",
                self.get_default_headers(),
            )
            .add_path("channel-id", channel_id)
            .add_path("conversation-id", conversation_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteConversationOkResponse._unmap(response)
