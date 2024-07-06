from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_company_addons_ok_response import GetCompanyAddonsOkResponse


class BillingService(BaseService):

    @cast_models
    def get_company_addons(self) -> GetCompanyAddonsOkResponse:
        """Returns the add-ons for a single company.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetCompanyAddonsOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/billing/subscriptions/addons",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetCompanyAddonsOkResponse._unmap(response)
