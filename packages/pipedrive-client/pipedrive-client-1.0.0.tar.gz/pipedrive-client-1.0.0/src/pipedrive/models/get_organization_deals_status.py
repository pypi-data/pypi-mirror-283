from enum import Enum


class GetOrganizationDealsStatus(Enum):
    """An enumeration representing different categories.

    :cvar OPEN: "open"
    :vartype OPEN: str
    :cvar WON: "won"
    :vartype WON: str
    :cvar LOST: "lost"
    :vartype LOST: str
    :cvar DELETED: "deleted"
    :vartype DELETED: str
    :cvar ALL_NOT_DELETED: "all_not_deleted"
    :vartype ALL_NOT_DELETED: str
    """

    OPEN = "open"
    WON = "won"
    LOST = "lost"
    DELETED = "deleted"
    ALL_NOT_DELETED = "all_not_deleted"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, GetOrganizationDealsStatus._member_map_.values())
        )
