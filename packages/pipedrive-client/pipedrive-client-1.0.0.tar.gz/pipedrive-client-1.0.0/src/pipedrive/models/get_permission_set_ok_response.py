from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class GetPermissionSetOkResponseApp(Enum):
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
        return list(
            map(lambda x: x.value, GetPermissionSetOkResponseApp._member_map_.values())
        )


class GetPermissionSetOkResponseType(Enum):
    """An enumeration representing different categories.

    :cvar ADMIN: "admin"
    :vartype ADMIN: str
    :cvar MANAGER: "manager"
    :vartype MANAGER: str
    :cvar REGULAR: "regular"
    :vartype REGULAR: str
    :cvar CUSTOM: "custom"
    :vartype CUSTOM: str
    """

    ADMIN = "admin"
    MANAGER = "manager"
    REGULAR = "regular"
    CUSTOM = "custom"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, GetPermissionSetOkResponseType._member_map_.values())
        )


@JsonMap({"id_": "id", "type_": "type"})
class GetPermissionSetOkResponse(BaseModel):
    """GetPermissionSetOkResponse

    :param id_: The ID of user permission set, defaults to None
    :type id_: str, optional
    :param name: The name of the permission set, defaults to None
    :type name: str, optional
    :param description: The description of the permission set, defaults to None
    :type description: str, optional
    :param app: The app that permission set belongs to, defaults to None
    :type app: GetPermissionSetOkResponseApp, optional
    :param type_: The type of permission set, defaults to None
    :type type_: GetPermissionSetOkResponseType, optional
    :param assignment_count: The number of users assigned to this permission set, defaults to None
    :type assignment_count: int, optional
    :param contents: A permission assigned to this permission set, defaults to None
    :type contents: List[str], optional
    """

    def __init__(
        self,
        id_: str = None,
        name: str = None,
        description: str = None,
        app: GetPermissionSetOkResponseApp = None,
        type_: GetPermissionSetOkResponseType = None,
        assignment_count: int = None,
        contents: List[str] = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if app is not None:
            self.app = self._enum_matching(
                app, GetPermissionSetOkResponseApp.list(), "app"
            )
        if type_ is not None:
            self.type_ = self._enum_matching(
                type_, GetPermissionSetOkResponseType.list(), "type_"
            )
        if assignment_count is not None:
            self.assignment_count = assignment_count
        if contents is not None:
            self.contents = contents
