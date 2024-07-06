from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class RefreshTokensOkResponse(BaseModel):
    """RefreshTokensOkResponse

    :param access_token: You need to use an `access_token` for accessing the user's data via API. You will need to [refresh the access token](https://pipedrive.readme.io/docs/marketplace-oauth-authorization#step-7-refreshing-the-tokens) if the `access_token` becomes invalid., defaults to None
    :type access_token: str, optional
    :param token_type: The format of the token. Always "Bearer"., defaults to None
    :type token_type: str, optional
    :param refresh_token: A refresh token is needed when you refresh the access token. refresh_token will expire if it isn't used in 60 days. Each time refresh_token is used, its expiry date is reset back to 60 days., defaults to None
    :type refresh_token: str, optional
    :param scope: List of scopes to which users have agreed to grant access within this `access_token`, defaults to None
    :type scope: str, optional
    :param expires_in: The maximum time in seconds until the `access_token` expires, defaults to None
    :type expires_in: int, optional
    :param api_domain: The base URL path, including the company_domain, where the requests can be sent to, defaults to None
    :type api_domain: str, optional
    """

    def __init__(
        self,
        access_token: str = None,
        token_type: str = None,
        refresh_token: str = None,
        scope: str = None,
        expires_in: int = None,
        api_domain: str = None,
    ):
        if access_token is not None:
            self.access_token = access_token
        if token_type is not None:
            self.token_type = token_type
        if refresh_token is not None:
            self.refresh_token = refresh_token
        if scope is not None:
            self.scope = scope
        if expires_in is not None:
            self.expires_in = expires_in
        if api_domain is not None:
            self.api_domain = api_domain
