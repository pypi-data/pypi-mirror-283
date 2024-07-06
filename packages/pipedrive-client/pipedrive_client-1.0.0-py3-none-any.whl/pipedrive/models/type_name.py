from enum import Enum


class TypeName(Enum):
    """An enumeration representing different categories.

    :cvar DEALS_WON: "deals_won"
    :vartype DEALS_WON: str
    :cvar DEALS_PROGRESSED: "deals_progressed"
    :vartype DEALS_PROGRESSED: str
    :cvar ACTIVITIES_COMPLETED: "activities_completed"
    :vartype ACTIVITIES_COMPLETED: str
    :cvar ACTIVITIES_ADDED: "activities_added"
    :vartype ACTIVITIES_ADDED: str
    :cvar DEALS_STARTED: "deals_started"
    :vartype DEALS_STARTED: str
    """

    DEALS_WON = "deals_won"
    DEALS_PROGRESSED = "deals_progressed"
    ACTIVITIES_COMPLETED = "activities_completed"
    ACTIVITIES_ADDED = "activities_added"
    DEALS_STARTED = "deals_started"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, TypeName._member_map_.values()))
