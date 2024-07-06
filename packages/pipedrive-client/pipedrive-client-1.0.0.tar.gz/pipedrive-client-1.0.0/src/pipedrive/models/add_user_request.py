from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class AccessApp3(Enum):
    """An enumeration representing different categories.

    :cvar SALES: "sales"
    :vartype SALES: str
    :cvar PROJECTS: "projects"
    :vartype PROJECTS: str
    :cvar CAMPAIGNS: "campaigns"
    :vartype CAMPAIGNS: str
    :cvar GLOBAL: "global"
    :vartype GLOBAL: str
    :cvar ACCOUNT_SETTINGS: "account_settings"
    :vartype ACCOUNT_SETTINGS: str
    """

    SALES = "sales"
    PROJECTS = "projects"
    CAMPAIGNS = "campaigns"
    GLOBAL = "global"
    ACCOUNT_SETTINGS = "account_settings"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, AccessApp3._member_map_.values()))


@JsonMap({})
class AddUserRequestAccess(BaseModel):
    """AddUserRequestAccess

    :param app: app
    :type app: AccessApp3
    :param admin: admin, defaults to None
    :type admin: bool, optional
    :param permission_set_id: permission_set_id, defaults to None
    :type permission_set_id: str, optional
    """

    def __init__(
        self, app: AccessApp3, admin: bool = None, permission_set_id: str = None
    ):
        self.app = self._enum_matching(app, AccessApp3.list(), "app")
        if admin is not None:
            self.admin = admin
        if permission_set_id is not None:
            self.permission_set_id = permission_set_id


@JsonMap({})
class AddUserRequest(BaseModel):
    """AddUserRequest

    :param email: The email of the user
    :type email: str
    :param access: The access given to the user. Each item in the array represents access to a specific app. Optionally may include either admin flag or permission set ID to specify which access to give within the app. If both are omitted, the default access for the corresponding app will be used. It requires structure as follows: `[{ app: 'sales', permission_set_id: '62cc4d7f-4038-4352-abf3-a8c1c822b631' }, { app: 'global', admin: true }, { app: 'account_settings' }]` , defaults to None
    :type access: List[AddUserRequestAccess], optional
    :param active_flag: Whether the user is active or not. `false` = Not activated, `true` = Activated, defaults to None
    :type active_flag: bool, optional
    """

    def __init__(
        self,
        email: str,
        access: List[AddUserRequestAccess] = None,
        active_flag: bool = None,
    ):
        self.email = email
        if access is not None:
            self.access = self._define_list(access, AddUserRequestAccess)
        if active_flag is not None:
            self.active_flag = active_flag
