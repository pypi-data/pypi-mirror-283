from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_user_connections_ok_response import GetUserConnectionsOkResponse


class UserConnectionsService(BaseService):

    @cast_models
    def get_user_connections(self) -> GetUserConnectionsOkResponse:
        """Returns data about all connections for the authorized user.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The data of user connections
        :rtype: GetUserConnectionsOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/userConnections", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetUserConnectionsOkResponse._unmap(response)
