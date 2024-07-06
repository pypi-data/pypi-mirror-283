from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_lead_sources_ok_response import GetLeadSourcesOkResponse


class LeadSourcesService(BaseService):

    @cast_models
    def get_lead_sources(self) -> GetLeadSourcesOkResponse:
        """Returns all lead sources. Please note that the list of lead sources is fixed, it cannot be modified. All leads created through the Pipedrive API will have a lead source `API` assigned.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The successful response containing payload in the `data` field.
        :rtype: GetLeadSourcesOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/leadSources", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetLeadSourcesOkResponse._unmap(response)
