from enum import Enum


class ArchivedStatus(Enum):
    """An enumeration representing different categories.

    :cvar ARCHIVED: "archived"
    :vartype ARCHIVED: str
    :cvar NOT_ARCHIVED: "not_archived"
    :vartype NOT_ARCHIVED: str
    :cvar ALL: "all"
    :vartype ALL: str
    """

    ARCHIVED = "archived"
    NOT_ARCHIVED = "not_archived"
    ALL = "all"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ArchivedStatus._member_map_.values()))
