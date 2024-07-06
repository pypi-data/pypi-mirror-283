from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.refresh_tokens_request import RefreshTokensRequest
from ..models.refresh_tokens_ok_response import RefreshTokensOkResponse
from ..models.get_tokens_request import GetTokensRequest
from ..models.get_tokens_ok_response import GetTokensOkResponse


class OauthService(BaseService):

    @cast_models
    def authorize(self, client_id: str, redirect_uri: str, state: str = None) -> str:
        """Authorize a user by redirecting them to the Pipedrive OAuth authorization page and request their permissions to act on their behalf. This step is necessary to implement only when you allow app installation outside of the Marketplace.

        :param client_id: The client ID provided to you by the Pipedrive Marketplace when you register your app
        :type client_id: str
        :param redirect_uri: The callback URL you provided when you registered your app. Authorization code will be sent to that URL (if it matches with the value you entered in the registration form) if a user approves the app install. Or, if a customer declines, the corresponding error will also be sent to this URL.
        :type redirect_uri: str
        :param state: You may pass any random string as the state parameter and the same string will be returned to your app after a user authorizes access. It may be used to store the user's session ID from your app or distinguish different responses. Using state may increase security; see RFC-6749. The state parameter is not automatically available in Marketplace Manager. To enable it for your app, please write to us at marketplace.devs@pipedrive.com., defaults to None
        :type state: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Authorize user in the app.
        :rtype: str
        """

        Validator(str).validate(client_id)
        Validator(str).validate(redirect_uri)
        Validator(str).is_optional().validate(state)

        serialized_request = (
            Serializer(f"{self.base_url}/oauth/authorize", self.get_default_headers())
            .add_query("client_id", client_id)
            .add_query("redirect_uri", redirect_uri)
            .add_query("state", state)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def get_tokens(
        self, authorization: str, request_body: GetTokensRequest = None
    ) -> GetTokensOkResponse:
        """After the customer has confirmed the app installation, you will need to exchange the `authorization_code` to a pair of access and refresh tokens. Using an access token, you can access the user's data through the API.

        :param request_body: The request body., defaults to None
        :type request_body: GetTokensRequest, optional
        :param authorization: Base 64 encoded string containing the `client_id` and `client_secret` values. The header value should be `Basic <base64(client_id:client_secret)>`.
        :type authorization: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Returns user Oauth2 tokens.
        :rtype: GetTokensOkResponse
        """

        Validator(GetTokensRequest).is_optional().validate(request_body)
        Validator(str).validate(authorization)

        serialized_request = (
            Serializer(f"{self.base_url}/oauth/token", self.get_default_headers())
            .add_header("Authorization", authorization)
            .serialize()
            .set_method("POST")
            .set_body(request_body, "application/x-www-form-urlencoded")
        )

        response = self.send_request(serialized_request)

        return GetTokensOkResponse._unmap(response)

    @cast_models
    def refresh_tokens(
        self, authorization: str, request_body: RefreshTokensRequest = None
    ) -> RefreshTokensOkResponse:
        """The `access_token` has a lifetime. After a period of time, which was returned to you in `expires_in` JSON property, the `access_token` will be invalid, and you can no longer use it to get data from our API. To refresh the `access_token`, you must use the `refresh_token`.

        :param request_body: The request body., defaults to None
        :type request_body: RefreshTokensRequest, optional
        :param authorization: Base 64 encoded string containing the `client_id` and `client_secret` values. The header value should be `Basic <base64(client_id:client_secret)>`.
        :type authorization: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Returns user Oauth2 tokens.
        :rtype: RefreshTokensOkResponse
        """

        Validator(RefreshTokensRequest).is_optional().validate(request_body)
        Validator(str).validate(authorization)

        serialized_request = (
            Serializer(f"{self.base_url}/oauth/token/", self.get_default_headers())
            .add_header("Authorization", authorization)
            .serialize()
            .set_method("POST")
            .set_body(request_body, "application/x-www-form-urlencoded")
        )

        response = self.send_request(serialized_request)

        return RefreshTokensOkResponse._unmap(response)
