from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class RefreshTokensRequestGrantType(Enum):
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
            map(lambda x: x.value, RefreshTokensRequestGrantType._member_map_.values())
        )


@JsonMap({})
class RefreshTokensRequest(BaseModel):
    """RefreshTokensRequest

    :param grant_type: Since you are to refresh your access_token, you must use the value "refresh_token", defaults to None
    :type grant_type: RefreshTokensRequestGrantType, optional
    :param refresh_token: The refresh token that you received after you exchanged the authorization code, defaults to None
    :type refresh_token: str, optional
    """

    def __init__(
        self,
        grant_type: RefreshTokensRequestGrantType = None,
        refresh_token: str = None,
    ):
        if grant_type is not None:
            self.grant_type = self._enum_matching(
                grant_type, RefreshTokensRequestGrantType.list(), "grant_type"
            )
        if refresh_token is not None:
            self.refresh_token = refresh_token
