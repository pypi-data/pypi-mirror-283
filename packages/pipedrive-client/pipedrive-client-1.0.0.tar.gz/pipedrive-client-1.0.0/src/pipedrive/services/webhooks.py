from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_webhooks_ok_response import GetWebhooksOkResponse
from ..models.delete_webhook_ok_response import DeleteWebhookOkResponse
from ..models.add_webhook_request import AddWebhookRequest
from ..models.add_webhook_created_response import AddWebhookCreatedResponse


class WebhooksService(BaseService):

    @cast_models
    def get_webhooks(self) -> GetWebhooksOkResponse:
        """Returns data about all the Webhooks of a company.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The list of webhooks objects from the logged in company and user
        :rtype: GetWebhooksOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/webhooks", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetWebhooksOkResponse._unmap(response)

    @cast_models
    def add_webhook(
        self, request_body: AddWebhookRequest = None
    ) -> AddWebhookCreatedResponse:
        """Creates a new Webhook and returns its details. Note that specifying an event which triggers the Webhook combines 2 parameters - `event_action` and `event_object`. E.g., use `*.*` for getting notifications about all events, `added.deal` for any newly added deals, `deleted.persons` for any deleted persons, etc. See <a href="https://pipedrive.readme.io/docs/guide-for-webhooks?ref=api_reference" target="_blank" rel="noopener noreferrer">the guide for Webhooks</a> for more details.

        :param request_body: The request body., defaults to None
        :type request_body: AddWebhookRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The created webhook object
        :rtype: AddWebhookCreatedResponse
        """

        Validator(AddWebhookRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/webhooks", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddWebhookCreatedResponse._unmap(response)

    @cast_models
    def delete_webhook(self, id_: int) -> DeleteWebhookOkResponse:
        """Deletes the specified Webhook.

        :param id_: The ID of the Webhook to delete
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The webhook deletion success response
        :rtype: DeleteWebhookOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/webhooks/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteWebhookOkResponse._unmap(response)
