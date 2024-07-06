from enum import Enum


class GetPermissionSetsApp(Enum):
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
        return list(map(lambda x: x.value, GetPermissionSetsApp._member_map_.values()))
