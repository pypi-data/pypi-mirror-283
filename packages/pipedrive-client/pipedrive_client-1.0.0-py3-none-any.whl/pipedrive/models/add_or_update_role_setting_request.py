from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class SettingKey(Enum):
    """An enumeration representing different categories.

    :cvar DEAL_DEFAULT_VISIBILITY: "deal_default_visibility"
    :vartype DEAL_DEFAULT_VISIBILITY: str
    :cvar LEAD_DEFAULT_VISIBILITY: "lead_default_visibility"
    :vartype LEAD_DEFAULT_VISIBILITY: str
    :cvar ORG_DEFAULT_VISIBILITY: "org_default_visibility"
    :vartype ORG_DEFAULT_VISIBILITY: str
    :cvar PERSON_DEFAULT_VISIBILITY: "person_default_visibility"
    :vartype PERSON_DEFAULT_VISIBILITY: str
    :cvar PRODUCT_DEFAULT_VISIBILITY: "product_default_visibility"
    :vartype PRODUCT_DEFAULT_VISIBILITY: str
    """

    DEAL_DEFAULT_VISIBILITY = "deal_default_visibility"
    LEAD_DEFAULT_VISIBILITY = "lead_default_visibility"
    ORG_DEFAULT_VISIBILITY = "org_default_visibility"
    PERSON_DEFAULT_VISIBILITY = "person_default_visibility"
    PRODUCT_DEFAULT_VISIBILITY = "product_default_visibility"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SettingKey._member_map_.values()))


class AddOrUpdateRoleSettingRequestValue(Enum):
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
        return list(
            map(
                lambda x: x.value,
                AddOrUpdateRoleSettingRequestValue._member_map_.values(),
            )
        )


@JsonMap({})
class AddOrUpdateRoleSettingRequest(BaseModel):
    """AddOrUpdateRoleSettingRequest

    :param setting_key: setting_key
    :type setting_key: SettingKey
    :param value: Possible values for the `default_visibility` setting depending on the subscription plan:<br> <table class='role-setting'> <caption><b>Essential / Advanced plan</b></caption> <tr><th><b>Value</b></th><th><b>Description</b></th></tr> <tr><td>`1`</td><td>Owner & Followers</td></tr> <tr><td>`3`</td><td>Entire company</td></tr> </table> <br> <table class='role-setting'> <caption><b>Professional / Enterprise plan</b></caption> <tr><th><b>Value</b></th><th><b>Description</b></th></tr> <tr><td>`1`</td><td>Owner only</td></tr> <tr><td>`3`</td><td>Owner&#39;s visibility group</td></tr> <tr><td>`5`</td><td>Owner&#39;s visibility group and sub-groups</td></tr> <tr><td>`7`</td><td>Entire company</td></tr> </table> <br> Read more about visibility groups <a href='https://support.pipedrive.com/en/article/visibility-groups'>here</a>.
    :type value: AddOrUpdateRoleSettingRequestValue
    """

    def __init__(
        self, setting_key: SettingKey, value: AddOrUpdateRoleSettingRequestValue
    ):
        self.setting_key = self._enum_matching(
            setting_key, SettingKey.list(), "setting_key"
        )
        self.value = self._enum_matching(
            value, AddOrUpdateRoleSettingRequestValue.list(), "value"
        )
