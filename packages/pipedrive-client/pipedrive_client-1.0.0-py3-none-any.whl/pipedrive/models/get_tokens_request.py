from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class GetTokensRequestGrantType(Enum):
    """An enumeration representing different categories.

    :cvar AUTHORIZATION_CODE: "authorization_code"
    :vartype AUTHORIZATION_CODE: str
    :cvar REFRESH_TOKEN: "refresh_token"
    :vartype REFRESH_TOKEN: str
    """

    AUTHORIZATION_CODE = "authorization_code"
    REFRESH_TOKEN = "refresh_token"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, GetTokensRequestGrantType._member_map_.values())
        )


@JsonMap({})
class GetTokensRequest(BaseModel):
    """GetTokensRequest

    :param grant_type: Since you are trying to exchange an authorization code for a pair of tokens, you must use the value "authorization_code", defaults to None
    :type grant_type: GetTokensRequestGrantType, optional
    :param code: The authorization code that you received after the user confirmed app installation, defaults to None
    :type code: str, optional
    :param redirect_uri: The callback URL you provided when you registered your app, defaults to None
    :type redirect_uri: str, optional
    """

    def __init__(
        self,
        grant_type: GetTokensRequestGrantType = None,
        code: str = None,
        redirect_uri: str = None,
    ):
        if grant_type is not None:
            self.grant_type = self._enum_matching(
                grant_type, GetTokensRequestGrantType.list(), "grant_type"
            )
        if code is not None:
            self.code = code
        if redirect_uri is not None:
            self.redirect_uri = redirect_uri
