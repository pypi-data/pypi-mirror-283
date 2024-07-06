from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class DataApp(Enum):
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
        return list(map(lambda x: x.value, DataApp._member_map_.values()))


class DataType3(Enum):
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
        return list(map(lambda x: x.value, DataType3._member_map_.values()))


@JsonMap({"id_": "id", "type_": "type"})
class GetPermissionSetsOkResponseData(BaseModel):
    """GetPermissionSetsOkResponseData

    :param id_: The ID of user permission set, defaults to None
    :type id_: str, optional
    :param name: The name of the permission set, defaults to None
    :type name: str, optional
    :param description: The description of the permission set, defaults to None
    :type description: str, optional
    :param app: The app that permission set belongs to, defaults to None
    :type app: DataApp, optional
    :param type_: The type of permission set, defaults to None
    :type type_: DataType3, optional
    :param assignment_count: The number of users assigned to this permission set, defaults to None
    :type assignment_count: int, optional
    """

    def __init__(
        self,
        id_: str = None,
        name: str = None,
        description: str = None,
        app: DataApp = None,
        type_: DataType3 = None,
        assignment_count: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if app is not None:
            self.app = self._enum_matching(app, DataApp.list(), "app")
        if type_ is not None:
            self.type_ = self._enum_matching(type_, DataType3.list(), "type_")
        if assignment_count is not None:
            self.assignment_count = assignment_count


@JsonMap({})
class GetPermissionSetsOkResponse(BaseModel):
    """GetPermissionSetsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of permission set, defaults to None
    :type data: List[GetPermissionSetsOkResponseData], optional
    """

    def __init__(
        self, success: bool = None, data: List[GetPermissionSetsOkResponseData] = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetPermissionSetsOkResponseData)
