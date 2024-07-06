from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_subscription_installment_request import (
    UpdateSubscriptionInstallmentRequest,
)
from ..models.update_subscription_installment_ok_response import (
    UpdateSubscriptionInstallmentOkResponse,
)
from ..models.update_recurring_subscription_request import (
    UpdateRecurringSubscriptionRequest,
)
from ..models.update_recurring_subscription_ok_response import (
    UpdateRecurringSubscriptionOkResponse,
)
from ..models.get_subscription_payments_ok_response import (
    GetSubscriptionPaymentsOkResponse,
)
from ..models.get_subscription_ok_response import GetSubscriptionOkResponse
from ..models.find_subscription_by_deal_ok_response import (
    FindSubscriptionByDealOkResponse,
)
from ..models.delete_subscription_ok_response import DeleteSubscriptionOkResponse
from ..models.cancel_recurring_subscription_request import (
    CancelRecurringSubscriptionRequest,
)
from ..models.cancel_recurring_subscription_ok_response import (
    CancelRecurringSubscriptionOkResponse,
)
from ..models.add_subscription_installment_request import (
    AddSubscriptionInstallmentRequest,
)
from ..models.add_subscription_installment_ok_response import (
    AddSubscriptionInstallmentOkResponse,
)
from ..models.add_recurring_subscription_request import AddRecurringSubscriptionRequest
from ..models.add_recurring_subscription_ok_response import (
    AddRecurringSubscriptionOkResponse,
)


class SubscriptionsService(BaseService):

    @cast_models
    def get_subscription(self, id_: int) -> GetSubscriptionOkResponse:
        """Returns details of an installment or a recurring subscription.

        :param id_: The ID of the subscription
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetSubscriptionOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/subscriptions/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetSubscriptionOkResponse._unmap(response)

    @cast_models
    def delete_subscription(self, id_: int) -> DeleteSubscriptionOkResponse:
        """Marks an installment or a recurring subscription as deleted.

        :param id_: The ID of the subscription
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteSubscriptionOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/subscriptions/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteSubscriptionOkResponse._unmap(response)

    @cast_models
    def find_subscription_by_deal(
        self, deal_id: int
    ) -> FindSubscriptionByDealOkResponse:
        """Returns details of an installment or a recurring subscription by the deal ID.

        :param deal_id: The ID of the deal
        :type deal_id: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: FindSubscriptionByDealOkResponse
        """

        Validator(int).validate(deal_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/subscriptions/find/{{dealId}}",
                self.get_default_headers(),
            )
            .add_path("dealId", deal_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return FindSubscriptionByDealOkResponse._unmap(response)

    @cast_models
    def get_subscription_payments(self, id_: int) -> GetSubscriptionPaymentsOkResponse:
        """Returns all payments of an installment or recurring subscription.

        :param id_: The ID of the subscription
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetSubscriptionPaymentsOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/subscriptions/{{id}}/payments",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetSubscriptionPaymentsOkResponse._unmap(response)

    @cast_models
    def add_recurring_subscription(
        self, request_body: AddRecurringSubscriptionRequest = None
    ) -> AddRecurringSubscriptionOkResponse:
        """Adds a new recurring subscription.

        :param request_body: The request body., defaults to None
        :type request_body: AddRecurringSubscriptionRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: AddRecurringSubscriptionOkResponse
        """

        Validator(AddRecurringSubscriptionRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/subscriptions/recurring", self.get_default_headers()
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddRecurringSubscriptionOkResponse._unmap(response)

    @cast_models
    def add_subscription_installment(
        self, request_body: AddSubscriptionInstallmentRequest = None
    ) -> AddSubscriptionInstallmentOkResponse:
        """Adds a new installment subscription.

        :param request_body: The request body., defaults to None
        :type request_body: AddSubscriptionInstallmentRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: AddSubscriptionInstallmentOkResponse
        """

        Validator(AddSubscriptionInstallmentRequest).is_optional().validate(
            request_body
        )

        serialized_request = (
            Serializer(
                f"{self.base_url}/subscriptions/installment", self.get_default_headers()
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddSubscriptionInstallmentOkResponse._unmap(response)

    @cast_models
    def update_recurring_subscription(
        self, id_: int, request_body: UpdateRecurringSubscriptionRequest = None
    ) -> UpdateRecurringSubscriptionOkResponse:
        """Updates a recurring subscription.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateRecurringSubscriptionRequest, optional
        :param id_: The ID of the subscription
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateRecurringSubscriptionOkResponse
        """

        Validator(UpdateRecurringSubscriptionRequest).is_optional().validate(
            request_body
        )
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/subscriptions/recurring/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateRecurringSubscriptionOkResponse._unmap(response)

    @cast_models
    def update_subscription_installment(
        self, id_: int, request_body: UpdateSubscriptionInstallmentRequest = None
    ) -> UpdateSubscriptionInstallmentOkResponse:
        """Updates an installment subscription.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateSubscriptionInstallmentRequest, optional
        :param id_: The ID of the subscription
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateSubscriptionInstallmentOkResponse
        """

        Validator(UpdateSubscriptionInstallmentRequest).is_optional().validate(
            request_body
        )
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/subscriptions/installment/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateSubscriptionInstallmentOkResponse._unmap(response)

    @cast_models
    def cancel_recurring_subscription(
        self, id_: int, request_body: CancelRecurringSubscriptionRequest = None
    ) -> CancelRecurringSubscriptionOkResponse:
        """Cancels a recurring subscription.

        :param request_body: The request body., defaults to None
        :type request_body: CancelRecurringSubscriptionRequest, optional
        :param id_: The ID of the subscription
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: CancelRecurringSubscriptionOkResponse
        """

        Validator(CancelRecurringSubscriptionRequest).is_optional().validate(
            request_body
        )
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/subscriptions/recurring/{{id}}/cancel",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return CancelRecurringSubscriptionOkResponse._unmap(response)
