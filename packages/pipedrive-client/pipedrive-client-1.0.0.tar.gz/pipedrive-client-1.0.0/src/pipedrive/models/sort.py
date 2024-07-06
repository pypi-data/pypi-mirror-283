from enum import Enum


class Sort(Enum):
    """An enumeration representing different categories.

    :cvar ID: "id"
    :vartype ID: str
    :cvar TITLE: "title"
    :vartype TITLE: str
    :cvar OWNER_ID: "owner_id"
    :vartype OWNER_ID: str
    :cvar CREATOR_ID: "creator_id"
    :vartype CREATOR_ID: str
    :cvar WAS_SEEN: "was_seen"
    :vartype WAS_SEEN: str
    :cvar EXPECTED_CLOSE_DATE: "expected_close_date"
    :vartype EXPECTED_CLOSE_DATE: str
    :cvar NEXT_ACTIVITY_ID: "next_activity_id"
    :vartype NEXT_ACTIVITY_ID: str
    :cvar ADD_TIME: "add_time"
    :vartype ADD_TIME: str
    :cvar UPDATE_TIME: "update_time"
    :vartype UPDATE_TIME: str
    """

    ID = "id"
    TITLE = "title"
    OWNER_ID = "owner_id"
    CREATOR_ID = "creator_id"
    WAS_SEEN = "was_seen"
    EXPECTED_CLOSE_DATE = "expected_close_date"
    NEXT_ACTIVITY_ID = "next_activity_id"
    ADD_TIME = "add_time"
    UPDATE_TIME = "update_time"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Sort._member_map_.values()))
