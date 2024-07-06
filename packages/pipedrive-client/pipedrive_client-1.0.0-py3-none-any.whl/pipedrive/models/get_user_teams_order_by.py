from enum import Enum


class GetUserTeamsOrderBy(Enum):
    """An enumeration representing different categories.

    :cvar ID: "id"
    :vartype ID: str
    :cvar NAME: "name"
    :vartype NAME: str
    :cvar MANAGER_ID: "manager_id"
    :vartype MANAGER_ID: str
    :cvar ACTIVE_FLAG: "active_flag"
    :vartype ACTIVE_FLAG: str
    """

    ID = "id"
    NAME = "name"
    MANAGER_ID = "manager_id"
    ACTIVE_FLAG = "active_flag"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, GetUserTeamsOrderBy._member_map_.values()))
