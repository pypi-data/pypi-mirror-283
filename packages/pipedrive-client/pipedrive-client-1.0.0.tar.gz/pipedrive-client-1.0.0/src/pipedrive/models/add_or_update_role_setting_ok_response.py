from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class DealDefaultVisibility(Enum):
    """An enumeration representing different categories.

    :cvar _1: 1
    :vartype _1: str
    :cvar _3: 3
    :vartype _3: str
    :cvar _5: 5
    :vartype _5: str
    :cvar _7: 7
    :vartype _7: str
    """

    _1 = 1
    _3 = 3
    _5 = 5
    _7 = 7

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, DealDefaultVisibility._member_map_.values()))


@JsonMap({"id_": "id"})
class AddOrUpdateRoleSettingOkResponseData(BaseModel):
    """The response data

    :param id_: The ID of the role, defaults to None
    :type id_: int, optional
    :param deal_default_visibility: The setting, defaults to None
    :type deal_default_visibility: DealDefaultVisibility, optional
    """

    def __init__(
        self, id_: int = None, deal_default_visibility: DealDefaultVisibility = None
    ):
        if id_ is not None:
            self.id_ = id_
        if deal_default_visibility is not None:
            self.deal_default_visibility = self._enum_matching(
                deal_default_visibility,
                DealDefaultVisibility.list(),
                "deal_default_visibility",
            )


@JsonMap({})
class AddOrUpdateRoleSettingOkResponse(BaseModel):
    """AddOrUpdateRoleSettingOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The response data, defaults to None
    :type data: AddOrUpdateRoleSettingOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: AddOrUpdateRoleSettingOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddOrUpdateRoleSettingOkResponseData)
