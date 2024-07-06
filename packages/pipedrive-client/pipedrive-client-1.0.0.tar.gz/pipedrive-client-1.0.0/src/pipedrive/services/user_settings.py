from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_user_settings_ok_response import GetUserSettingsOkResponse


class UserSettingsService(BaseService):

    @cast_models
    def get_user_settings(self) -> GetUserSettingsOkResponse:
        """Lists the settings of an authorized user. Example response contains a shortened list of settings.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The list of user settings
        :rtype: GetUserSettingsOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/userSettings", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetUserSettingsOkResponse._unmap(response)
